from pathlib import Path
from wikidebia_validator.editorial import keyword_form_issues

def test_singleton_keyword_remains_allowed_114():
    assert keyword_form_issues(["hypothèse nulle", "statistiques"]) == []

def test_active_norm_is_single_in_reference_tree():
    root=Path(__file__).parents[1]/"normative_reference"/"01_normes"
    active=sorted(p.name for p in root.glob("WIKIDEBIA_NORME_CONSOLIDEE_*.md"))
    assert active == ["WIKIDEBIA_NORME_CONSOLIDEE_1.2.24.md"]

def test_norm_contains_w11_non_overwrite_and_order():
    root=Path(__file__).parents[1]/"normative_reference"/"01_normes"
    text=(root/"WIKIDEBIA_NORME_CONSOLIDEE_1.2.24.md").read_text(encoding="utf-8")
    assert "ne jamais écraser une page existante par défaut" in text
    assert "première écriture distante un test sur l’unique page Débat française canonique" in text
    assert "ne créer aucune sous-page utilisateur" in text
    assert "titre + SHA-256" in text


def test_current_handoff_is_declared_by_manifest_not_stage_name():
    text=(Path(__file__).parents[1]/"src"/"wikidebia_validator"/"editorial.py").read_text(encoding="utf-8")
    assert "current_handoff_path" in text
    assert "is_historical_corrective_stage" not in text
