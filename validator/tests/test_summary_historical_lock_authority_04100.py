from __future__ import annotations

from pathlib import Path

from wikidebia_validator.editorial import (
    _historically_absent_summary_keys,
    _protected_historical_summary_keys,
    validate_summary_style_review_data,
)
from wikidebia_validator.package import PackageContext
from wikidebia_validator.report import Report
from .helpers import dump


def _ctx(root: Path) -> PackageContext:
    return PackageContext(root, Report("0.4.100", root.name, ["editorial"]))


def test_content_locks_are_authoritative_even_during_transient_translation_status(tmp_path: Path):
    dump(tmp_path / "manifest.json", {
        "translation_status": {"en": "in_review"},
        "pages": [
            {"page_id": "A0098", "page_type": "argument", "language": "fr"},
            {"page_id": "A0098", "page_type": "argument", "language": "en"},
        ],
        "editorial_controls": {},
    })
    dump(tmp_path / "data/fr_content_lock.json", {
        "arguments": [{
            "id": "A0098", "page_origin": "preexisting",
            "summary": "En 2017, 4 000 observations documentent le mécanisme.",
            "summary_provenance": "historical_authorized_change",
        }],
    })
    dump(tmp_path / "data/en_content_lock.json", {
        "arguments": [{
            "id": "A0098", "page_origin": "new", "source_page_origin": "preexisting",
            "summary": "In 2017, 4,000 observations document the mechanism.",
            "summary_provenance": "historical_authorized_change",
        }],
    })
    ctx = _ctx(tmp_path)
    protected = _protected_historical_summary_keys(ctx)
    assert ("A0098", "fr") in protected
    assert ("A0098", "en") in protected

    review = {"entries": [{
        "id": "A0098",
        "languages": {
            "fr": {
                "status": "historical_authorized_change",
                "owner_authorized_change": True,
                "historical_source_sha256": "0" * 64,
                "authorized_final_sha256": "1" * 64,
                "authorization": {"authorization_id": "AUTH"},
                "note": "Résumé historique modifié dans la portée autorisée par le propriétaire.",
            },
            "en": {
                "status": "translated_historical_source",
                "historical_source_preserved": True,
                "note": "English faithfully translates the protected historical French source without retroactive style rewriting.",
            },
        },
    }]}
    issues = validate_summary_style_review_data(
        review,
        [{"id": "A0098"}],
        {"A0098": {"fr", "en"}},
        quantitative_pages={("A0098", "fr"), ("A0098", "en")},
        summaries={
            ("A0098", "fr"): "En 2017, 4 000 observations documentent le mécanisme.",
            ("A0098", "en"): "In 2017, 4,000 observations document the mechanism.",
        },
        protected_historical=protected,
    )
    assert issues == []


def test_historical_absence_is_read_directly_from_both_content_locks(tmp_path: Path):
    dump(tmp_path / "manifest.json", {
        "translation_status": {"en": "in_review"},
        "pages": [
            {"page_id": "A0001", "page_type": "argument", "language": "fr"},
            {"page_id": "A0001", "page_type": "argument", "language": "en"},
        ],
        "editorial_controls": {},
    })
    dump(tmp_path / "data/fr_content_lock.json", {
        "arguments": [{"id": "A0001", "page_origin": "preexisting", "summary": None, "summary_provenance": "historical_absent"}],
    })
    dump(tmp_path / "data/en_content_lock.json", {
        "arguments": [{"id": "A0001", "source_page_origin": "preexisting", "summary": None, "summary_provenance": "historical_absent"}],
    })
    absent = _historically_absent_summary_keys(_ctx(tmp_path))
    assert {("A0001", "fr"), ("A0001", "en")} <= absent
