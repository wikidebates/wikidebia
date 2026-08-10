from __future__ import annotations

from wikidebia_validator.schema_validation import SchemaStore


def _entry(**overrides):
    row = {
        "language": "en",
        "page_id": "A0001",
        "title": "A conventional argument title",
        "page_origin": "new",
        "search_reviewed": True,
        "search_queries": ["conventional argument title philosophy", "alternative argument label literature"],
        "search_scope_note": "Academic English terminology for the exact reasoning was checked.",
        "search_provenance": "actual_log",
        "search_provenance_note": "These exact query strings were actually used during the review.",
        "outcome": "none",
        "name": None,
        "evidence": [],
        "same_reasoning_confirmed": False,
        "non_invented_label_confirmed": True,
        "language_fit_confirmed": True,
        "rationale": "No sufficiently established conventional name was found for this exact reasoning.",
    }
    row.update(overrides)
    return row


def test_argument_name_discovery_11_requires_real_search_provenance():
    store = SchemaStore()
    data = {
        "version": "wikidebia-argument-name-discovery-review-1.1",
        "normative_revision": "1.2.59",
        "debate_id": "example",
        "entries": [_entry()],
    }
    assert not store.validate(data, "argument_name_discovery_review.schema.json")

    bad = {**data, "entries": [_entry(search_provenance="historical_reconstruction")]}
    assert store.validate(bad, "argument_name_discovery_review.schema.json")


def test_argument_name_discovery_10_remains_readable_without_provenance_fields():
    store = SchemaStore()
    old = _entry()
    old.pop("search_provenance")
    old.pop("search_provenance_note")
    data = {
        "version": "wikidebia-argument-name-discovery-review-1.0",
        "normative_revision": "1.2.55",
        "debate_id": "example",
        "entries": [old],
    }
    assert not store.validate(data, "argument_name_discovery_review.schema.json")
