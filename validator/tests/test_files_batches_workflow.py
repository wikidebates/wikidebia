from pathlib import Path
import json

from wikidebia_validator.validator import validate_package
from .helpers import create_fr_package, dump


def test_hash_mismatch_detected(tmp_path: Path):
    create_fr_package(tmp_path)
    p = tmp_path / "output/fr/arguments/A0001.wiki"
    p.write_text(p.read_text() + "<!-- modification -->\n", encoding="utf-8")
    report = validate_package(tmp_path, scopes=["files"])
    assert any(f.code == "WDV-FS-003" for f in report.findings)


def test_batch_overlap_and_gap_detected(tmp_path: Path):
    create_fr_package(tmp_path)
    mpath = tmp_path / "manifest.json"
    manifest = json.loads(mpath.read_text())
    extra = json.loads(json.dumps(manifest["batches"][0]))
    extra["id"] = "FR-A-002"
    extra["node_ids"] = ["A0001"]
    extra["root_node_ids"] = ["A0001"]
    manifest["batches"].append(extra)
    dump(mpath, manifest)
    report = validate_package(tmp_path, scopes=["batches"])
    assert any(f.code == "WDV-BAT-002" for f in report.findings)


def test_forbidden_transition_detected(tmp_path: Path):
    create_fr_package(tmp_path)
    report = validate_package(tmp_path, scopes=["workflow"], previous_status="initialized")
    assert any(f.code == "WDV-WF-002" for f in report.findings)
