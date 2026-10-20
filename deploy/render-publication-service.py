"""Render the separately enabled French publication service."""
from pathlib import Path
import runpy
import sys

quote = runpy.run_path(str(Path(__file__).with_name("render-service.py")))["quote"]


def render(repo: str) -> str:
    if not repo.startswith("/"):
        raise ValueError("Un chemin absolu est requis")
    executable = quote(repo + "/wikidebia", exec_argument=True)
    return f"""[Unit]
Description=Publier les demandes françaises explicitement envoyées depuis Codex

[Service]
Type=oneshot
UMask=0077
WorkingDirectory={repo.replace('%', '%%')}/.
ExecStart=/bin/bash {executable} fr-publication-relay --execute
TimeoutStartSec=30min
"""


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage : render-publication-service.py DOSSIER")
    try:
        print(render(sys.argv[1]), end="")
    except ValueError as error:
        sys.exit(str(error))
