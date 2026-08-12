from __future__ import annotations

import hashlib
import json
from pathlib import Path

from wikidebia_validator.editorial import validate_introduction_review_data
from wikidebia_validator.validator import validate_package
from wikidebia_validator.wikicode import parse_template
from .helpers import create_fr_package, dump


def _sha(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _attach_preservation_lock(root: Path) -> tuple[dict, dict[str, str]]:
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    debate_page = next(p for p in manifest["pages"] if p["language"] == "fr" and p["page_type"] == "debate")
    arg_pages = [p for p in manifest["pages"] if p["language"] == "fr" and p["page_type"] == "argument"]
    debate = parse_template((root / debate_page["file_path"]).read_text(encoding="utf-8"))
    intro = debate.one("introduction") or ""
    summaries: dict[str, str] = {}
    rows = []
    for page in arg_pages:
        tmpl = parse_template((root / page["file_path"]).read_text(encoding="utf-8"))
        summary = tmpl.one("résumé") or ""
        summaries[page["page_id"]] = summary
        rows.append({
            "id": page["page_id"],
            "page_origin": "preexisting",
            "summary_provenance": "historical_existing" if summary else "historical_absent",
            "source_sha256": _sha(summary),
            "preserved": True,
        })
    dump(root / "data/fr_content_lock.json", {
        "historical_text_preservation": {
            "policy": "preserve_preexisting_exact_v1",
            "debate": {
                "page_origin": "preexisting",
                "introduction_provenance": "historical_existing" if intro else "historical_absent",
                "source_sha256": _sha(intro),
                "preserved": True,
            },
            "arguments": rows,
        }
    })
    return debate_page, {"introduction": intro, **summaries}


def test_historical_text_lock_accepts_exact_rendered_values(tmp_path: Path):
    create_fr_package(tmp_path)
    _attach_preservation_lock(tmp_path)
    report = validate_package(tmp_path, scopes=["wikicode"])
    assert not any(f.code == "WDV-EDT-034" for f in report.findings)


def test_historical_text_lock_blocks_summary_rewrite(tmp_path: Path):
    create_fr_package(tmp_path)
    _attach_preservation_lock(tmp_path)
    manifest = json.loads((tmp_path / "manifest.json").read_text(encoding="utf-8"))
    page = next(p for p in manifest["pages"] if p["language"] == "fr" and p["page_id"] == "A0001")
    path = tmp_path / page["file_path"]
    text = path.read_text(encoding="utf-8")
    path.write_text(text.replace("La mesure X mutualiserait certains bénéfices et réduirait des coûts collectifs.", "Résumé réécrit qui ne doit pas passer."), encoding="utf-8")
    report = validate_package(tmp_path, scopes=["wikicode"])
    assert any(f.code == "WDV-EDT-034" and "Résumé historique" in f.message for f in report.findings)


def test_historical_text_lock_blocks_introduction_rewrite(tmp_path: Path):
    create_fr_package(tmp_path)
    debate_page, _ = _attach_preservation_lock(tmp_path)
    path = tmp_path / debate_page["file_path"]
    text = path.read_text(encoding="utf-8")
    path.write_text(text.replace("La mesure X est une mesure pilote.", "Une nouvelle introduction réécrite."), encoding="utf-8")
    report = validate_package(tmp_path, scopes=["wikicode"])
    assert any(f.code == "WDV-EDT-034" and "Introduction historique" in f.message for f in report.findings)


def test_historical_introduction_review_skips_creation_structure_requirements():
    intro = "{{Sous-partie|titre=Historique|contenu=Texte historique conservé.}}"
    review = {
        "entries": [{
            "language": "fr",
            "status": "historical_existing",
            "historical_content_preserved": True,
            "historical_source_sha256": _sha(intro),
            "note": "Introduction historique conservée exactement sans réécriture rétroactive.",
            "subsections": [{"title": "Historique"}],
        }]
    }
    issues = validate_introduction_review_data(review, {"fr": ["Historique"]})
    assert issues == []

def test_summary_style_schema_accepts_translated_historical_source():
    import json
    from pathlib import Path
    schema = json.loads((Path(__file__).resolve().parents[1] / "src/wikidebia_validator/schemas/summary_style_review.schema.json").read_text(encoding="utf-8"))
    variants = schema["properties"]["entries"]["items"]["properties"]["languages"]["patternProperties"]["^(fr|en)$"]["oneOf"]
    assert any(v.get("properties", {}).get("status", {}).get("const") == "translated_historical_source" for v in variants)

def test_summary_style_allows_english_translation_of_protected_historical_source():
    from wikidebia_validator.editorial import validate_summary_style_review_data
    review = {
        "entries": [{
            "id": "A0001",
            "languages": {
                "fr": {"status": "historical_existing", "historical_content_preserved": True, "note": "Résumé français historique conservé exactement."},
                "en": {"status": "translated_historical_source", "historical_source_preserved": True, "note": "English faithfully translates the protected historical French source."},
            },
        }]
    }
    issues = validate_summary_style_review_data(
        review,
        [{"id": "A0001"}],
        {"A0001": {"fr", "en"}},
        protected_historical={("A0001", "fr")},
        summaries={("A0001", "fr"): "A", ("A0001", "en"): "A"},
    )
    assert issues == []

