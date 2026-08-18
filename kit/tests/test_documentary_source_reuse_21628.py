from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))


def load_module(name: str):
    path = SCRIPTS / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


translation = load_module("wikidebia_translation_review")
doc_resources = sys.modules.get("wikidebia_documentary_resources") or load_module("wikidebia_documentary_resources")


def _metadata(page: str) -> dict[str, object]:
    return {
        "authors": ["Matt Blaze", "Jake Braun", "Harri Hursti", "David Jefferson", "Margaret MacAlpine", "Jeff Moss"],
        "article": None,
        "work": None,
        "volume": None,
        "issue": None,
        "location": None,
        "publisher": None,
        "place": None,
        "date": "2018",
        "link": "https://defcon.org/images/defcon-26/DEF%20CON%2026%20voting%20village%20report.pdf",
        "page": page,
        "site": "DEF CON",
        "title": None,
    }


def test_existing_english_resource_is_reused_when_translation_selects_same_url():
    existing = {
        "id": "S00013",
        "type": "webliography",
        "document_kind": "synthesis_report",
        "language": "en",
        "metadata": _metadata("DEFCON 26 Voting Village - Report on Cyber Vulnerabilities in U.S. Election Equipment, Databases, and Infrastructure"),
        "verification": {"status": "verified", "verified_at": "2026-08-12T17:20:00+02:00", "primary_source": True, "notes": ["Historical verification."], "language_verified": True, "authorship_checked": True, "authorship_verified": True},
        "usage": [{"page_id": "A0098", "language": "fr", "role": "supports_summary", "selection_reason": "Historical cross-language use.", "argument_development_verified": True, "also_develops_objections": False, "language_fit": "original_no_equivalent", "preferred_equivalent_source_id": None}],
        "deduplication_key": "url:https://defcon.org/images/defcon-26/DEF%20CON%2026%20voting%20village%20report.pdf",
        "equivalence_group": None,
    }
    translated = {
        "id": "S10003",
        "type": "webliography",
        "document_kind": "synthesis_report",
        "language": "en",
        "metadata": _metadata("DEF CON 26 Voting Village - Report on Cyber Vulnerabilities in U.S. Election Equipment, Databases, and Infrastructure"),
        "verification": {"status": "verified", "verified_at": "2026-08-13T16:45:00+02:00", "primary_source": True, "notes": ["Translation review verification."], "language_verified": True, "authorship_checked": True, "authorship_verified": True},
        "usage": [{"page_id": "A0098", "language": "en", "role": "supports_summary", "selection_reason": "Primary English technical report for the translated summary.", "argument_development_verified": True, "also_develops_objections": False, "documentary_scope": "narrow_argument"}],
        "deduplication_key": "url:https://defcon.org/images/defcon-26/DEF%20CON%2026%20voting%20village%20report.pdf",
    }

    merged, remap = translation._merge_translated_sources_with_existing([existing], [translated])

    assert remap == {"S10003": "S00013"}
    assert len(merged) == 1
    assert merged[0]["id"] == "S00013"
    assert merged[0]["metadata"]["page"].startswith("DEFCON 26")  # historical canonical notice is preserved
    assert {(u["language"], u["page_id"], u["role"]) for u in merged[0]["usage"]} == {
        ("fr", "A0098", "supports_summary"),
        ("en", "A0098", "supports_summary"),
    }

    final = {
        "debate": {"documentation": {"webliography": ["S10003"]}},
        "arguments": [{"id": "A0098", "sources": {"bibliography": [], "webliography": ["S10003"], "videography": []}}],
    }
    effective = translation._remap_final_source_ids(final, remap)
    assert effective["debate"]["documentation"]["webliography"] == ["S00013"]
    assert effective["arguments"][0]["sources"]["webliography"] == ["S00013"]

    registry = doc_resources.build_resource_registry({"debate_id": "vote", "sources": merged}, "0" * 64)
    assert len(registry["resources"]) == 1
    assert registry["resources"][0]["conflicts"] == []


def test_source_reuse_refuses_documentary_family_change():
    existing = {
        "id": "S00013", "type": "webliography", "document_kind": "synthesis_report", "language": "en",
        "metadata": _metadata("Historical label"), "verification": {}, "usage": [],
        "deduplication_key": "url:https://defcon.org/images/defcon-26/DEF%20CON%2026%20voting%20village%20report.pdf",
    }
    translated = dict(existing)
    translated["id"] = "S10003"
    translated["type"] = "bibliography"
    try:
        translation._merge_translated_sources_with_existing([existing], [translated])
    except translation.TranslationReviewError as exc:
        assert "autre type documentaire" in str(exc)
    else:
        raise AssertionError("A same-resource documentary-family conflict must not be normalized silently")
