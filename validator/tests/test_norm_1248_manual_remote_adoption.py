from pathlib import Path
from wikidebia_validator.schema_validation import SchemaStore


def valid_adoption():
    return {
        "version": "wikidebia-manual-remote-adoptions-1.0",
        "debate_id": "demo",
        "decision": "Le propriétaire autorise explicitement cette reprise distante.",
        "entries": [{
            "language": "fr",
            "page_id": "A1",
            "title": "Titre",
            "observed_revision_id": 42,
            "observed_sha256": "a" * 64,
            "allow_proposed_change": True,
            "reason": "Modification manuelle fournie et approuvée par le propriétaire.",
            "allowed_lifecycle_parameter_changes": [],
                "external_relations": [{"relation": "objection", "page": "External argument", "displayed_title": "External argument"}],
        }],
    }


def test_1248_schema_accepts_explicit_adoption():
    assert not SchemaStore().validate(valid_adoption(), "manual_remote_adoptions.schema.json")


def test_1248_schema_requires_revision_or_sha():
    data = valid_adoption()
    data["entries"][0].pop("observed_revision_id")
    data["entries"][0].pop("observed_sha256")
    assert SchemaStore().validate(data, "manual_remote_adoptions.schema.json")


def test_active_norm_is_1248():
    root = Path(__file__).parents[1] / "normative_reference" / "01_normes"
    assert sorted(p.name for p in root.glob("WIKIDEBIA_NORME_CONSOLIDEE_*.md")) == [
        "WIKIDEBIA_NORME_CONSOLIDEE_1.2.52.md"
    ]
