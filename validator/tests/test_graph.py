from pathlib import Path

from wikidebia_validator.validator import validate_package
from .helpers import create_graph_package, dump


def test_graph_package_valid(tmp_path: Path):
    create_graph_package(tmp_path)
    report = validate_package(tmp_path, scopes=["graph"])
    assert report.errors == 0, report.to_text()


def test_duplicate_title_and_cycle_detected(tmp_path: Path):
    create_graph_package(tmp_path)
    import json
    reg_path = tmp_path / "data/registre_debat.json"
    reg = json.loads(reg_path.read_text())
    reg["graph"]["nodes"][1]["fr"]["canonical_title"] = reg["graph"]["nodes"][0]["fr"]["canonical_title"]
    reg["graph"]["edges"] = [
        {"id": "E00001", "parent_node_id": "A0001", "child_node_id": "A0002", "relation": "justification", "order": 1, "status": "active"},
        {"id": "E00002", "parent_node_id": "A0002", "child_node_id": "A0001", "relation": "objection", "order": 1, "status": "active"},
    ]
    dump(reg_path, reg)
    report = validate_package(tmp_path, scopes=["graph"])
    codes = {f.code for f in report.findings if f.level == "ERROR"}
    assert "WDV-GRA-002" in codes
    assert "WDV-GRA-005" in codes


def test_bad_derived_counts_detected(tmp_path: Path):
    create_graph_package(tmp_path)
    import json
    reg_path = tmp_path / "data/registre_debat.json"
    reg = json.loads(reg_path.read_text())
    reg["graph"]["derived_counts"]["distinct_nodes"] = 99
    dump(reg_path, reg)
    report = validate_package(tmp_path, scopes=["graph"])
    assert any(f.code == "WDV-GRA-013" and f.level == "ERROR" for f in report.findings)
