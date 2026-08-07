from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_versions_file_has_only_the_three_functional_versions():
    versions = json.loads((ROOT / "VERSIONS.json").read_text(encoding="utf-8"))
    assert versions == {"norm": "1.2.49", "validator": "0.4.52", "kit": "2.15.26"}


def test_versions_file_matches_kit_metadata_and_script():
    versions = json.loads((ROOT / "VERSIONS.json").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "KIT_MANIFEST.json").read_text(encoding="utf-8"))
    assert manifest["version"] == versions["kit"]
    assert manifest["validator_version"] == versions["validator"]
    assert manifest["normative_revision"] == versions["norm"]
    script = (ROOT / "scripts/wikidebia_publish.py").read_text(encoding="utf-8")
    assert re.search(r'^KIT_VERSION\s*=\s*"' + re.escape(versions["kit"]) + r'"', script, re.M)
    assert re.search(r'^REQUIRED_VALIDATOR_VERSION\s*=\s*"' + re.escape(versions["validator"]) + r'"', script, re.M)


def test_graph_extractor_versions_match_kit():
    versions = json.loads((ROOT / "VERSIONS.json").read_text(encoding="utf-8"))
    script = (ROOT / "scripts/wikidebia_graph_extract.py").read_text(encoding="utf-8")
    assert re.search(r'^KIT_VERSION\s*=\s*"' + re.escape(versions["kit"]) + r'"', script, re.M)
    assert re.search(r'^GRAPH_EXTRACT_VERSION\s*=\s*"1\.0\.2"', script, re.M)


def test_editorial_workspace_versions_match_kit():
    versions = json.loads((ROOT / "VERSIONS.json").read_text(encoding="utf-8"))
    script = (ROOT / "scripts/wikidebia_editorial_workspace.py").read_text(encoding="utf-8")
    assert re.search(r'^KIT_VERSION\s*=\s*"' + re.escape(versions["kit"]) + r'"', script, re.M)
    assert re.search(r'^NORM_VERSION\s*=\s*"' + re.escape(versions["norm"]) + r'"', (ROOT / "scripts/wikidebia_corpus_build.py").read_text(encoding="utf-8"), re.M)


def test_editorial_review_versions_match_kit():
    versions = json.loads((ROOT / "VERSIONS.json").read_text(encoding="utf-8"))
    script = (ROOT / "scripts/wikidebia_editorial_review.py").read_text(encoding="utf-8")
    assert re.search(r'^KIT_VERSION\s*=\s*"' + re.escape(versions["kit"]) + r'"', script, re.M)
