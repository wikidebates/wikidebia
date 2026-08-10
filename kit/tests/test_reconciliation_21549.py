from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent

def test_active_norms_translation_guide_uses_current_established_name_contract():
    guide = (PROJECT / "norms" / "docs" / "GUIDE_TRADUCTION_METADONNEES_FR_EN.md").read_text(encoding="utf-8")
    compatibility = json.loads((PROJECT / "norms" / "COMPATIBILITY.json").read_text(encoding="utf-8"))
    assert "le sous-titre `name=`" not in guide
    assert "nouvelle recherche de `nom=` / `name=`" not in guide
    assert "`established-name=` commence par une majuscule" in guide
    assert "`nom-consacré=` / `established-name=`" in guide
    assert not any("nouvelles revues de name=" in note for note in compatibility["notes"])
