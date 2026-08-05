from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_versions_file_has_only_the_three_functional_versions():
    versions = json.loads((ROOT / "VERSIONS.json").read_text(encoding="utf-8"))
    assert versions == {"norm": "1.2.38", "validator": "0.4.40", "kit": "2.15.13"}


def test_versions_file_matches_validator_metadata():
    versions = json.loads((ROOT / "VERSIONS.json").read_text(encoding="utf-8"))
    compatibility = json.loads((ROOT / "COMPATIBILITY.json").read_text(encoding="utf-8"))
    assert compatibility["validator_version"] == versions["validator"]
    assert compatibility["implemented_normative_revision"] == versions["norm"]
    init_text = (ROOT / "src/wikidebia_validator/__init__.py").read_text(encoding="utf-8")
    assert re.search(r'^__version__\s*=\s*"' + re.escape(versions["validator"]) + r'"', init_text, re.M)


def test_compatibility_keeps_historical_corpus_revisions():
    compatibility = json.loads((ROOT / "COMPATIBILITY.json").read_text(encoding="utf-8"))
    supported = compatibility["compatible_normative_revisions"]
    assert "1.2.10" in supported
    assert "1.2.14" in supported
    assert supported[-1] == "1.2.38"


def test_schema_accepts_historical_and_current_norm_revisions():
    schema = json.loads((ROOT / "src/wikidebia_validator/schemas/debate_package.schema.json").read_text(encoding="utf-8"))
    text = json.dumps(schema)
    assert '"1.2.10"' in text
    assert '"1.2.16"' in text
    assert '"1.2.18"' in text
