#!/usr/bin/env bash
# À exécuter sous le compte propriétaire du checkout Debian.
set -euo pipefail
umask 077
export GIT_TERMINAL_PROMPT=0 PIP_NO_INPUT=1

fail() { printf 'Déploiement arrêté : %s\n' "$*" >&2; exit 1; }
[[ $# -ge 1 && $# -le 2 ]] || fail "usage : bash update.sh DOSSIER [BRANCHE]"
repo=$(cd -- "$1" && pwd -P)
branch=${2:-main}
python=${DEPLOY_PYTHON:-python3}
[[ $(id -u) != 0 ]] || fail "utiliser le compte propriétaire du checkout, pas root"
git check-ref-format "refs/heads/$branch" >/dev/null
[[ $(git -C "$repo" rev-parse --show-toplevel) == "$repo" ]] || fail "le dossier doit être la racine Git"
[[ -x "$repo/wikidebia" ]] || fail "commande wikidebia absente"

lock=$(git -C "$repo" rev-parse --path-format=absolute --git-path wikidebia-deploy.lock)
exec 9>"$lock"
flock -n 9 || { printf 'Un déploiement est déjà en cours.\n'; exit 0; }

check_checkout() {
  [[ $(git -C "$repo" symbolic-ref --quiet --short HEAD) == "$branch" ]] || fail "le checkout doit être sur $branch"
  [[ -z $(git -C "$repo" status --porcelain --untracked-files=all) ]] || fail "modifications locales : les conserver ou les valider avant de déployer"
}
check_checkout
[[ -f "$repo/private/pywikibot/user-config.py" ]] || fail "installation initiale requise : private/pywikibot/user-config.py absent"
git -C "$repo" fetch --no-tags origin "refs/heads/$branch"
target=$(git -C "$repo" rev-parse --verify 'FETCH_HEAD^{commit}')
before=$(git -C "$repo" rev-parse HEAD)
git -C "$repo" merge-base --is-ancestor "$before" "$target" || fail "historique divergent : aucun reset automatique"
# Ne jamais remplacer les chemins réservés aux données locales par du code suivi.
# ls-tree -r énumère les fichiers/liens, pas les répertoires ordinaires :
# protéger aussi les parents (ex. config) et les racines (ex. corpus).
reserved_paths=(
  private corpus archives updates incoming outgoing logs plans .state .venv
  configs apicache config/wikidebia.local.json .gitconfig-wikidebia
  user-config.py user-password.cfg throttle.ctrl
)
while IFS= read -r -d '' tracked; do
  for reserved in "${reserved_paths[@]}"; do
    if [[ "$tracked" == "$reserved" || "$tracked" == "$reserved/"* || "$reserved" == "$tracked/"* ]]; then
      fail "le commit distant suit un chemin réservé aux données locales : $tracked"
    fi
  done
done < <(git -C "$repo" ls-tree -rz --name-only "$target")
marker="$repo/.state/deployed-commit"
if [[ "$before" == "$target" && -f "$marker" && $(cat "$marker") == "$target" ]]; then
  printf 'Déjà déployé : %s\n' "$target"
  exit 0
fi

# Les tests ne voient ni les corpus ni les secrets du serveur.
candidate=$(mktemp -d)
trap 'rm -rf -- "$candidate"' EXIT
git -C "$repo" archive "$target" | tar -x -C "$candidate"
"$python" -m venv "$candidate/.venv"
test_python="$candidate/.venv/bin/python"
"$test_python" -m pip install --disable-pip-version-check -r "$candidate/requirements-runtime.txt" -r "$candidate/validator/requirements-dev.txt"
"$test_python" -m pip check
# Réutiliser exactement les versions validées lors de l'installation réelle.
"$test_python" -m pip freeze > "$candidate/validated-requirements.txt"
(
  cd "$candidate"
  PYTHONPATH=validator/src "$test_python" -m pytest -q validator/tests
  "$test_python" -m pytest -q kit/tests
  "$test_python" validator/scripts/self_audit.py
)

# Vérifier de nouveau : personne ne doit modifier le checkout pendant les tests.
check_checkout
[[ $(git -C "$repo" rev-parse HEAD) == "$before" ]] || fail "HEAD a changé pendant la validation"
git -C "$repo" merge --ff-only "$target"
if [[ ! -x "$repo/.venv/bin/python" ]]; then
  "$python" -m venv "$repo/.venv"
fi
"$repo/.venv/bin/python" -m pip install --disable-pip-version-check --constraint "$candidate/validated-requirements.txt" -r "$repo/requirements-runtime.txt"
"$repo/.venv/bin/python" -m pip check
"$repo/wikidebia" doctor
mkdir -p -- "$repo/.state"
printf '%s\n' "$target" > "$marker"
printf 'Déploiement validé : %s\n' "$target"
