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


def test_title_editorial_checks_are_deferred_until_french_metadata_lock(tmp_path: Path):
    create_graph_package(tmp_path)
    import json
    from wikidebia_validator.graph import structural_sha256

    reg_path = tmp_path / "data/registre_debat.json"
    graph_path = tmp_path / "graph/graphe_argumentatif.json"
    reg = json.loads(reg_path.read_text(encoding="utf-8"))
    reg["graph"]["nodes"][0]["fr"]["canonical_title"] = "Cette mesure produirait un bénéfice collectif."
    reg["graph"]["lifecycle"]["structural_sha256"] = structural_sha256(reg)
    dump(reg_path, reg)
    projection = json.loads(graph_path.read_text(encoding="utf-8"))
    projection["nodes"] = reg["graph"]["nodes"]
    projection["lifecycle"] = reg["graph"]["lifecycle"]
    dump(graph_path, projection)

    report = validate_package(tmp_path, scopes=["schema", "graph"])
    assert report.errors == 0, report.to_text()
    deferred = [f for f in report.findings if f.code in {"WDV-GRA-016", "WDV-EDT-016"}]
    assert deferred
    assert all(f.level == "WARNING" for f in deferred), report.to_text()

    dump(tmp_path / "data/fr_page_metadata_lock.json", {"schema": "test-lock"})
    report = validate_package(tmp_path, scopes=["schema", "graph"])
    enforced = [f for f in report.findings if f.code in {"WDV-GRA-016", "WDV-EDT-016"}]
    assert any(f.level == "ERROR" for f in enforced), report.to_text()
