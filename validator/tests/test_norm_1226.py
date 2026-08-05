from __future__ import annotations

import json
from pathlib import Path

from wikidebia_validator import __version__


def test_validator_version_is_0428_for_norm_1226():
    assert __version__ == "0.4.38"


def test_package_schema_accepts_norm_1226():
    schema_path = Path(__file__).resolve().parents[1] / "src" / "wikidebia_validator" / "schemas" / "debate_package.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    assert "1.2.26" in json.dumps(schema, ensure_ascii=False)


def test_active_normative_source_is_uniquely_1226():
    base = Path(__file__).resolve().parents[1] / "normative_reference" / "01_normes"
    active = sorted(base.glob("WIKIDEBIA_NORME_CONSOLIDEE_*.md"))
    assert [path.name for path in active] == ["WIKIDEBIA_NORME_CONSOLIDEE_1.2.36.md"]
