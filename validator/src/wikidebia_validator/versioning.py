from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]


def _load_json(name: str) -> dict[str, Any]:
    data = json.loads((ROOT / name).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise RuntimeError(f"Objet JSON attendu dans {name}")
    return data


VERSIONS = _load_json("VERSIONS.json")
CAPABILITY_MANIFEST = _load_json("CAPABILITIES.json")
NORM_VERSION = str(VERSIONS["norm"])
VALIDATOR_VERSION = str(VERSIONS["validator"])
KIT_VERSION = str(VERSIONS["kit"])
REPORT_SCHEMA = "wikidebia-validator-report-1.0"
REPORT_SCHEMA_VERSION = "1.0"
