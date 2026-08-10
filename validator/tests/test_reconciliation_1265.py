from .current_policy_helpers import CURRENT_NORM_FILE, CURRENT_NORM, CURRENT_VALIDATOR, CURRENT_KIT, current_norm_path
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NORM = ROOT / "normative_reference" / "01_normes"

def test_active_interlanguage_and_quote_docs_match_current_contract():
    workflow = (NORM / "workflow_production_wikidebia.md").read_text(encoding="utf-8")
    profile = (NORM / "profils_rendu_wikidebia.md").read_text(encoding="utf-8")
    schema = (NORM / "schema_graphe_registre_wikidebia.md").read_text(encoding="utf-8")
    assert "Les pages françaises contiennent donc immédiatement leur lien" not in workflow
    assert "chaque page française contient exactement un lien interlangue dès sa première génération valide" not in profile
    assert "qu'aucune citation ou quote n'est produite" not in profile
    assert "chaque fichier français valide contient déjà son lien vers le titre anglais verrouillé" not in schema
    assert "translation_status.en=deferred" in workflow
    assert "`citations=` / `quotes=`" in profile

def test_current_norm_is_1265_and_1264_is_archived():
    assert (NORM / CURRENT_NORM_FILE).is_file()
    assert (NORM / "history" / "WIKIDEBIA_NORME_CONSOLIDEE_1.2.65.md").is_file()
    assert (NORM / "history" / "WIKIDEBIA_NORME_CONSOLIDEE_1.2.64.md").is_file()
