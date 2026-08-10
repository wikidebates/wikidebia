from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_validator_changelog_preserves_0471_0472_history():
    text = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    assert "## 0.4.71 — 10 août 2026 — familles de convergence normalisées" in text
    assert "## 0.4.72 — 10 août 2026 — renommage des paramètres MediaWiki" in text
    assert "## 0.4.73 — 10 août 2026 — alignement des métadonnées de première publication anglaise" in text


def test_validator_readme_does_not_reattribute_convergence_to_0472():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "Le correctif 0.4.71 formalise les familles de méthodes de convergence" in text
    assert "Le validateur 0.4.72 implémente le renommage des paramètres MediaWiki" in text
