#!/usr/bin/env bash
# Installe le minuteur utilisateur après un premier déploiement réussi.
set -euo pipefail
umask 077
[[ $# -ge 1 && $# -le 2 ]] || { echo 'Usage : bash install-timer.sh DOSSIER [BRANCHE]' >&2; exit 1; }
[[ $(id -u) != 0 ]] || { echo 'Utiliser le compte propriétaire du checkout, pas root.' >&2; exit 1; }
repo=$(cd -- "$1" && pwd -P)
branch=${2:-main}
script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
# Préparer l'unité avant toute modification du checkout ou du minuteur.
unit=$(python3 "$script_dir/render-service.py" "$repo" "$branch")
systemctl --user show-environment >/dev/null
bash "$script_dir/update.sh" "$repo" "$branch"
mkdir -p "$HOME/.local/libexec/wikidebia" "$HOME/.config/systemd/user"
# Copie stable : une mise à jour du dépôt ne remplace pas le déployeur actif.
install -m 700 "$script_dir/update.sh" "$HOME/.local/libexec/wikidebia/update.sh"
printf '%s\n' "$unit" > "$HOME/.config/systemd/user/wikidebia-deploy.service"
cat > "$HOME/.config/systemd/user/wikidebia-deploy.timer" <<'EOF'
[Unit]
Description=Vérifier les mises à jour Wikidéb’IA toutes les cinq minutes

[Timer]
OnBootSec=2min
OnUnitInactiveSec=5min
Persistent=true

[Install]
WantedBy=timers.target
EOF
systemctl --user daemon-reload
systemctl --user enable --now wikidebia-deploy.timer
systemctl --user list-timers wikidebia-deploy.timer --no-pager
