from pathlib import Path
import json

from wikidebia_validator.recalc import recalculate
from wikidebia_validator.validator import validate_package
from .helpers import create_graph_package, dump


def test_recalc_graph_repairs_derived_data(tmp_path: Path):
    create_graph_package(tmp_path)
    reg_path = tmp_path / "data/registre_debat.json"
    reg = json.loads(reg_path.read_text())
    reg["graph"]["derived_counts"]["distinct_nodes"] = 999
    reg["graph"]["nodes"][0].pop("derived")
    dump(reg_path, reg)
    changed, report = recalculate(tmp_path, graph=True, aggregates=False, hashes=False, write=True)
    assert report.errors == 0
    assert "data/registre_debat.json" in changed
    validated = validate_package(tmp_path, scopes=["graph"])
    assert validated.errors == 0, validated.to_text()


def test_recalc_requires_write(tmp_path: Path):
    create_graph_package(tmp_path)
    changed, report = recalculate(tmp_path, graph=True, aggregates=False, hashes=False, write=False)
    assert not changed
    assert report.errors == 1
