#!/usr/bin/env python3
"""Lanceur local isolé du validateur Wikidéb'IA.

Le lanceur insère explicitement ``validator/src`` après l'initialisation de
Python, vérifie que les modules critiques proviennent bien de ce composant et
scelle leurs empreintes dans le rapport via des variables d'environnement.
"""
from pathlib import Path
import hashlib
import os
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = (ROOT / "src").resolve()
PACKAGE = (SRC / "wikidebia_validator").resolve()
sys.path.insert(0, str(SRC))

from wikidebia_validator import cli as _cli  # noqa: E402
from wikidebia_validator import editorial as _editorial  # noqa: E402


def _assert_component_module(module, label: str) -> Path:
    raw = getattr(module, "__file__", None)
    if not raw:
        raise SystemExit(f"Validateur runtime invalide : module {label} sans __file__")
    path = Path(raw).resolve()
    try:
        path.relative_to(PACKAGE)
    except ValueError as exc:
        raise SystemExit(
            f"Validateur runtime divergent : {label} chargé hors de validator/src"
        ) from exc
    return path


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


cli_path = _assert_component_module(_cli, "cli")
editorial_path = _assert_component_module(_editorial, "editorial")
os.environ["WIKIDEBIA_VALIDATOR_RUNTIME_MODE"] = "component_script_isolated_v1"
os.environ["WIKIDEBIA_VALIDATOR_RUNTIME_CLI_SHA256"] = _sha256(cli_path)
os.environ["WIKIDEBIA_VALIDATOR_RUNTIME_EDITORIAL_SHA256"] = _sha256(editorial_path)

raise SystemExit(_cli.main())
