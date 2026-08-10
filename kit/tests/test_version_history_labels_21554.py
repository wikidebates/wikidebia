from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_kit_changelog_preserves_21552_21553_history():
    text = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    assert "## 2.15.52 — 10 août 2026 — durcissement final des preuves" in text
    assert "## 2.15.53 — 10 août 2026 — renommage des paramètres MediaWiki" in text
    assert "## 2.15.54 — 10 août 2026 — alignement des métadonnées de première publication anglaise" in text


def test_kit_readme_keeps_historical_version_attribution():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "La version 2.15.52 durcit la preuve d’indépendance" in text
    assert "La version 2.15.53 émet les paramètres MediaWiki" in text
    assert "La version 2.15.54 corrige l’alignement du validateur" in text


def test_manifest_declares_historical_version_attribution_gate():
    import json
    data = json.loads((ROOT / "KIT_MANIFEST.json").read_text(encoding="utf-8"))
    assert "historical_version_attribution_regression" in data["regression_gates"]
