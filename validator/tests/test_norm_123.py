from pathlib import Path


def test_norm_123_declares_canonical_debate_test():
    root = Path(__file__).parents[1] / "normative_reference" / "01_normes"
    text = (root / "WIKIDEBIA_NORME_CONSOLIDEE_1.2.56.md").read_text(encoding="utf-8")
    assert "page Débat française canonique" in text
    assert "créée avec `createonly`" in text
    assert "Aucune sous-page utilisateur n’est créée" in text


def test_norm_123_catalog_replaces_user_space_test():
    import json

    root = Path(__file__).parents[1] / "normative_reference" / "01_normes"
    catalog = json.loads((root / "requirements_catalog_wikidebia.json").read_text(encoding="utf-8"))
    requirement = next(row for row in catalog["requirements"] if row["id"] == "IMP-014")
    assert "canonical French Debate page" in requirement["statement"]
    assert "no user-space test page" in requirement["statement"]
