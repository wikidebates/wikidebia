from __future__ import annotations
import json
from pathlib import Path
from jsonschema import Draft202012Validator

SCHEMAS = Path(__file__).resolve().parents[1] / "src/wikidebia_validator/schemas"

def test_graph_correction_schema_accepts_pending_and_corrected_documents():
    root = json.loads((SCHEMAS / "graph_correction.schema.json").read_text(encoding="utf-8"))
    common = json.loads((SCHEMAS / "common.schema.json").read_text(encoding="utf-8"))
    registry = {root["$id"]: root, common["$id"]: common}
    from referencing import Registry, Resource
    reg = Registry().with_resources((key, Resource.from_contents(value)) for key, value in registry.items())
    validator = Draft202012Validator(root, registry=reg)
    doc = {
        "schema":"wikidebia-graph-correction-1.0", "schema_version":"1.0",
        "debate_id":"revenu_de_base", "source_build_sha256":"a"*64,
        "rejected_review_sha256":"b"*64, "status":"corrected",
        "reviewer":"ChatGPT", "reviewed_at":"2026-08-11T18:00:00+02:00", "notes":"Correction revue.",
        "placements":[{
            "occurrence_id":"O00001", "node_id":"A0001", "parent_occurrence_id":None,
            "relation":None, "branch":"pro", "order":1, "occurrence_role":"primary"
        }]
    }
    assert not list(validator.iter_errors(doc))

def test_schema_catalog_declares_graph_correction():
    catalog=json.loads((SCHEMAS/"schema_catalog.json").read_text(encoding="utf-8"))
    assert catalog["schema_count"] == len(catalog["schemas"])
    assert any(x["path"]=="graph_correction.schema.json" for x in catalog["schemas"])
