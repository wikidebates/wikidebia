from .current_policy_helpers import CURRENT_NORM_FILE, CURRENT_NORM, CURRENT_VALIDATOR, CURRENT_KIT, current_norm_path
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NORM = ROOT / "normative_reference" / "01_normes"

def test_active_contract_uses_current_publication_terminology():
    data = json.loads((NORM / "requirements_catalog_wikidebia.json").read_text(encoding="utf-8"))
    by_id = {row["id"]: row for row in data["requirements"]}
    assert "nom-consacré/established-name" in by_id["MW-008"]["statement"]
    assert "nom-consacré/established-name" in by_id["EDT-062"]["statement"]
    assert "established-name=" in by_id["EDT-065"]["statement"]
    assert "AI-translated quote" in by_id["RND-004"]["statement"]
    assert "AI-translated quote" in by_id["RND-006"]["statement"]
    active = (NORM / CURRENT_NORM_FILE).read_text(encoding="utf-8")
    assert "|warnings=AI-translated quote" in active
    assert "### `established-name=` : recherche propre à la langue anglaise" in active
    assert "Addendum 1.2.61" not in active
    hist = (NORM / "history" / "translation_branch" / "WIKIDEBIA_NORME_CONSOLIDEE_1.2.61__translation_branch.md").read_text(encoding="utf-8")
    assert "Révision 1.2.61 — cohérence inter-composants et archivage normatif" in hist
    assert "Addendum 1.2.61 — cohérence inter-composants et archivage normatif" in hist

def test_validator_code_matches_current_quote_warning_and_established_name():
    source = (ROOT / "src" / "wikidebia_validator" / "wikicode.py").read_text(encoding="utf-8")
    assert "AI-translated quote" in source
    assert "established-name" in source
