from __future__ import annotations

import json
from pathlib import Path

from wikidebia_validator import __version__

ROOT = Path(__file__).resolve().parents[1]

def test_validator_version_is_current_for_norm_1230():
    assert __version__ == "0.4.54"

def test_active_normative_source_is_uniquely_1230():
    base = ROOT / "normative_reference/01_normes"
    active = sorted(base.glob("WIKIDEBIA_NORME_CONSOLIDEE_*.md"))
    assert [path.name for path in active] == ["WIKIDEBIA_NORME_CONSOLIDEE_1.2.51.md"]
    assert (base / "history/WIKIDEBIA_NORME_CONSOLIDEE_1.2.29.md").is_file()

def test_active_citation_documents_use_quote_in_english():
    base = ROOT / "normative_reference/01_normes"
    structures = (base / "structures_mediawiki_wikidebia.md").read_text(encoding="utf-8")
    assert "|citations={{Citation" in structures
    assert "|quotes={{Quote" in structures
    assert "|quotes={{Citation" not in structures
    quote_block = structures.split("|quotes={{Quote", 1)[1].split("}}", 1)[0]
    assert "|quote=" in quote_block
    assert "|authors=" in quote_block and "|work=" in quote_block
    assert "|warnings=" in quote_block
    assert "|citation=" not in quote_block
    assert "|auteurs=" not in quote_block and "|ouvrage=" not in quote_block
    profiles = (base / "profils_rendu_wikidebia.md").read_text(encoding="utf-8")
    assert "using the `Quote` model" in profiles
    cahier = (base / "cahier_des_charges_consolide_wikidebia.md").read_text(encoding="utf-8")
    assert "MW-009 — SUPERSEDED" in cahier
    catalog = json.loads((base / "requirements_catalog_wikidebia.json").read_text(encoding="utf-8"))
    assert catalog["active_package_revision"] == "1.2.51"
    rnd3 = next(row for row in catalog["requirements"] if row["id"] == "RND-003")
    assert "Quote model" in rnd3["statement"]
    assert "parameter names use the declared English contract" in rnd3["statement"]

def test_package_schema_accepts_norm_1230():
    schema = json.loads((ROOT / "src/wikidebia_validator/schemas/debate_package.schema.json").read_text(encoding="utf-8"))
    assert "1.2.32" in json.dumps(schema, ensure_ascii=False)
