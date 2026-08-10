from pathlib import Path
import hashlib, json

ROOT = Path(__file__).resolve().parents[1]
NORM = ROOT / "normative_reference" / "01_normes"

EXPECTED_1265_SHA256 = "6239dba2c39612f6885a0bc6070cd803b67921267e2dd8735bd33e0f08cd3c22"


def test_previous_norm_1265_is_archived_bit_exact():
    p = NORM / "history" / "WIKIDEBIA_NORME_CONSOLIDEE_1.2.65.md"
    assert p.is_file()
    assert hashlib.sha256(p.read_bytes()).hexdigest() == EXPECTED_1265_SHA256


def test_norm_1266_requirements_are_unique_and_present():
    data = json.loads((NORM / "requirements_catalog_wikidebia.json").read_text(encoding="utf-8"))
    ids = [r["id"] for r in data["requirements"]]
    assert len(ids) == len(set(ids))
    for rid in [*(f"TRN-{n:03d}" for n in range(20, 28)), "EDT-066", "VAL-054"]:
        assert rid in ids
    assert data["active_package_revision"] == "1.2.68"
    assert data["normative_revision"] == "1.2.68"
    assert len(data["requirements"]) >= 494
    assert len(data["source_aliases"]) >= 101


def test_active_norm_1266_contains_convergence_contract():
    text=(NORM / "history" / "WIKIDEBIA_NORME_CONSOLIDEE_1.2.66.md").read_text(encoding="utf-8")
    assert "deux passes sémantiques indépendantes consécutives" in text
    assert "displayed-title" in text and "titre-affiché" in text
    assert "semantic_content_sha256" in text
