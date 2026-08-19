from __future__ import annotations

import json
from pathlib import Path

from wikidebia_validator import editorial, wikicode
from wikidebia_validator.package import PackageContext
from wikidebia_validator.report import Report


def _write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def test_wikicode_cannot_poison_editorial_historical_summary_cache(tmp_path: Path):
    manifest = {
        "debate_id": "vote_test",
        "pages": [
            {"page_id": "A0001", "page_type": "argument", "language": "fr"},
            {"page_id": "A0001", "page_type": "argument", "language": "en"},
        ],
        "editorial_controls": {},
    }
    _write_json(tmp_path / "manifest.json", manifest)
    _write_json(tmp_path / "data/fr_content_lock.json", {
        "arguments": [{
            "id": "A0001",
            "page_origin": "preexisting",
            "summary": "Résumé historique autorisé.",
            "summary_provenance": "historical_authorized_change",
        }]
    })
    _write_json(tmp_path / "data/en_content_lock.json", {
        "arguments": [{
            "id": "A0001",
            "page_origin": "new",
            "source_page_origin": "preexisting",
            "summary": "Authorized historical summary.",
            "summary_provenance": "historical_authorized_change",
        }]
    })
    ctx = PackageContext(tmp_path, Report("0.4.103", str(tmp_path), ["wikicode", "editorial"]))

    # Validation order is wikicode before editorial. Both wrappers must now
    # resolve through one shared authoritative cache.
    from_wikicode = wikicode._protected_historical_summary_keys(ctx)
    from_editorial = editorial._protected_historical_summary_keys(ctx)
    expected = {("A0001", "fr"), ("A0001", "en")}
    assert expected <= from_wikicode
    assert from_wikicode == from_editorial

    review = {
        "entries": [{
            "id": "A0001",
            "languages": {
                "fr": {"status": "historical_authorized_change"},
                "en": {"status": "historical_authorized_change"},
            },
        }]
    }
    issues = editorial.validate_summary_style_review_data(
        review,
        [{"id": "A0001"}],
        {"A0001": {"fr", "en"}},
        protected_historical=from_editorial,
    )
    assert issues == []
