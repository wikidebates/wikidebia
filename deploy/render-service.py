"""Écrire les chemins littéraux dans une unité systemd, sans shell intermédiaire."""
import sys


def quote(value: str, *, exec_argument: bool = False) -> str:
    if any(ord(char) < 32 or ord(char) == 127 for char in value):
        raise ValueError("Les caractères de contrôle ne sont pas autorisés.")
    value = value.replace("\\", "\\\\").replace('"', '\\"').replace("%", "%%")
    if exec_argument:
        value = value.replace("$", "$$")
    return '"' + value + '"'


def render(repo: str, branch: str) -> str:
    if not repo.startswith("/"):
        raise ValueError("Un chemin absolu est requis.")
    repo_argument = quote(repo, exec_argument=True)
    # WorkingDirectory reçoit un chemin brut, contrairement aux mots d'ExecStart.
    # Le suffixe /. conserve aussi un éventuel espace final dans le nom du dossier.
    working_directory = repo.replace("%", "%%") + "/."
    return f"""[Unit]
Description=Mise à jour validée de Wikidéb’IA depuis GitHub

[Service]
Type=oneshot
UMask=0077
WorkingDirectory={working_directory}
ExecStart=/bin/bash "%h/.local/libexec/wikidebia/update.sh" {repo_argument} {quote(branch, exec_argument=True)}
TimeoutStartSec=30min
"""


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage : render-service.py DOSSIER BRANCHE")
    try:
        print(render(sys.argv[1], sys.argv[2]), end="")
    except ValueError as error:
        sys.exit(str(error))
