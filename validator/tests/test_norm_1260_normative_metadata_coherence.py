from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
NORM = ROOT / "normative_reference" / "01_normes"

def test_matrix_declares_active_revision_1260():
    text = (NORM / "MATRICE_TRACEABILITE_DESIDERATA.md").read_text(encoding="utf-8")
    assert "- **Révision :** 1.2.64" in text

def test_requirements_catalog_precedence_points_to_active_norm_1260():
    data = json.loads((NORM / "requirements_catalog_wikidebia.json").read_text(encoding="utf-8"))
    assert data["active_package_revision"] == "1.2.64"
    assert data["normative_revision"] == "1.2.64"
    assert "WIKIDEBIA_NORME_CONSOLIDEE_1.2.64.md" in data["precedence"]
    assert "WIKIDEBIA_NORME_CONSOLIDEE_1.2.58.md" not in data["precedence"]

def test_active_and_archived_consolidated_norms_are_coherent():
    active = sorted(p.name for p in NORM.glob("WIKIDEBIA_NORME_CONSOLIDEE_*.md"))
    assert active == ["WIKIDEBIA_NORME_CONSOLIDEE_1.2.64.md"]
    assert (NORM / "history" / "WIKIDEBIA_NORME_CONSOLIDEE_1.2.59.md").is_file()
    text = (NORM / active[0]).read_text(encoding="utf-8")
    assert "**Date d’effet :** 10 août 2026" in text
