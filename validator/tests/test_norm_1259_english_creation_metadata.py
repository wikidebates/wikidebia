from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_norm_1259_records_english_creation_metadata_rules():
    text = (ROOT / "normative_reference/01_normes/WIKIDEBIA_NORME_CONSOLIDEE_1.2.64.md").read_text(encoding="utf-8")
    assert "ne transporte jamais `|initialisation=`/`|initialization=`" in text
    assert "jour civil de la publication distante" in text
    assert "Europe/Paris" in text

def test_new_english_argument_still_forbids_initialization():
    from wikidebia_validator import wikicode
    assert "initialization" in wikicode.TOP[("en", "argument")]["forbidden_generated"]
    assert wikicode.TOP[("en", "argument")]["order"][:3] == ["initialization", "established-name", "name"]
