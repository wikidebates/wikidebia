from __future__ import annotations

import json
from pathlib import Path

from wikidebia_validator.validator import validate_package
from .helpers import create_graph_package, dump


def _legal_text_source(scope: str = "broad_synthesis") -> dict[str, object]:
    return {
        "id": "S10002",
        "type": "bibliography",
        "language": "fr",
        "document_kind": "legal_text",
        "equivalence_group": None,
        "metadata": {
            "authors": ["Conseil de l'Europe"], "article": None,
            "work": "Recommandation sur les normes applicables au vote électronique",
            "volume": None, "issue": None, "location": None,
            "publisher": "Conseil de l'Europe", "place": None, "date": "14 juin 2017",
            "link": "https://example.org/recommendation", "page": None, "site": None, "title": None,
        },
        "verification": {
            "status": "verified", "verified_at": "2026-08-18T20:00:00+02:00", "primary_source": True,
            "notes": ["Texte officiel vérifié."], "language_verified": True,
            "authorship_checked": True, "authorship_verified": True,
        },
        "usage": [{
            "page_id": "exemple", "language": "fr", "role": "neutral_reference",
            "language_fit": "native", "preferred_equivalent_source_id": None,
            "documentary_scope": scope,
            "selection_reason": "Texte officiel de portée générale fixant le cadre applicable à l'ensemble du débat.",
        }],
        "deduplication_key": "url:https://example.org/recommendation",
    }


def test_broad_legal_text_is_not_rejected_only_because_of_document_kind(tmp_path: Path):
    root = create_graph_package(tmp_path)
    dump(root / "data/sources.json", {"source_registry_version": "1.2", "debate_id": "exemple", "sources": [_legal_text_source()]})
    report = validate_package(root, scopes=["sources"])
    assert not any(f.code == "WDV-SRC-005" for f in report.findings), report.to_text()


def test_legal_text_still_fails_when_its_debate_scope_is_narrow(tmp_path: Path):
    root = create_graph_package(tmp_path)
    dump(root / "data/sources.json", {"source_registry_version": "1.2", "debate_id": "exemple", "sources": [_legal_text_source("narrow_argument")]})
    report = validate_package(root, scopes=["sources"])
    assert any(f.code == "WDV-SRC-005" for f in report.findings), report.to_text()
