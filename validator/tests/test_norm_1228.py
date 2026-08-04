from __future__ import annotations

import json
from pathlib import Path

from wikidebia_validator import __version__

ROOT = Path(__file__).resolve().parents[1]

def test_validator_version_is_0430_for_norm_1228():
    assert __version__ == "0.4.30"

def test_active_normative_source_is_uniquely_1228():
    base = ROOT / "normative_reference/01_normes"
    active = sorted(base.glob("WIKIDEBIA_NORME_CONSOLIDEE_*.md"))
    assert [path.name for path in active] == ["WIKIDEBIA_NORME_CONSOLIDEE_1.2.28.md"]
    assert (base / "history/WIKIDEBIA_NORME_CONSOLIDEE_1.2.27.md").is_file()

def test_active_citation_documents_are_consistent():
    base = ROOT / "normative_reference/01_normes"
    structures = (base / "structures_mediawiki_wikidebia.md").read_text(encoding="utf-8")
    assert "|quotes={{Citation" in structures
    assert "|quotes={{Quote" not in structures
    assert "|avertissements-citation=" in structures
    assert "|auteurs=" in structures and "|ouvrage=" in structures
    profiles = (base / "profils_rendu_wikidebia.md").read_text(encoding="utf-8")
    assert "Les citations textuelles ne sont jamais générées" not in profiles
    assert "Quotes are never generated" not in profiles
    cahier = (base / "cahier_des_charges_consolide_wikidebia.md").read_text(encoding="utf-8")
    assert "MW-009 — SUPERSEDED" in cahier
    catalog = json.loads((base / "requirements_catalog_wikidebia.json").read_text(encoding="utf-8"))
    mw009 = next(row for row in catalog["requirements"] if row["id"] == "MW-009")
    assert mw009["disposition"] == "superseded"

def test_package_schema_accepts_norm_1228():
    schema = json.loads((ROOT / "src/wikidebia_validator/schemas/debate_package.schema.json").read_text(encoding="utf-8"))
    assert "1.2.28" in json.dumps(schema, ensure_ascii=False)
