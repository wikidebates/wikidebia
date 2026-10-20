#!/usr/bin/env bash
# Activation explicite, indépendante du déploiement du programme.
set -euo pipefail
umask 077
[[ $# == 1 ]] || { echo 'Usage : bash install-publication-relay.sh DOSSIER' >&2; exit 1; }
[[ $(id -u) != 0 ]] || { echo 'Utiliser webmaster, pas root.' >&2; exit 1; }
repo=$(cd -- "$1" && pwd -P)
script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
[[ -f "$repo/private/pywikibot/user-config.py" ]] || { echo 'Configuration Pywikibot absente.' >&2; exit 1; }
[[ $(git -C "$repo" symbolic-ref --short HEAD) == main ]] || { echo 'Le checkout doit être sur main.' >&2; exit 1; }
[[ -z $(git -C "$repo" status --porcelain --untracked-files=all) ]] || { echo 'Conserver les modifications locales avant activation.' >&2; exit 1; }
unit=$(python3 "$script_dir/render-publication-service.py" "$repo")
systemctl --user show-environment >/dev/null
# Lecture et préflight uniquement avant d'activer le service qui écrit.
(cd -- "$repo" && bash ./wikidebia fr-publication-relay)
mkdir -p "$HOME/.config/systemd/user"
printf '%s\n' "$unit" > "$HOME/.config/systemd/user/wikidebia-publish-fr.service"
cat > "$HOME/.config/systemd/user/wikidebia-publish-fr.timer" <<'EOF'
[Unit]
Description=Lire les demandes explicites de publication française chaque minute

[Timer]
OnBootSec=2min
OnUnitInactiveSec=1min

[Install]
WantedBy=timers.target
EOF
systemctl --user daemon-reload
systemctl --user enable --now wikidebia-publish-fr.timer
systemctl --user start wikidebia-publish-fr.service
systemctl --user list-timers wikidebia-publish-fr.timer --no-pager
