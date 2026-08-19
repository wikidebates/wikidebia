from __future__ import annotations

from wikidebia_validator.editorial import validate_summary_style_review_data


def test_historical_summaries_do_not_require_creation_style_attestations():
    nodes = [{"id": "A0005"}, {"id": "A0098"}]
    page_languages = {"A0005": {"fr", "en"}, "A0098": {"fr", "en"}}
    protected = {
        ("A0005", "fr"), ("A0005", "en"),
        ("A0098", "fr"), ("A0098", "en"),
    }
    # Deliberately stale legacy rows: no opening, tone, force or quantitative
    # attestations. The authoritative content locks (represented by
    # protected_historical) make those creation-style fields inapplicable.
    review = {
        "entries": [
            {"id": "A0005", "languages": {"fr": {"status": "approved"}, "en": {"status": "approved"}}},
            {"id": "A0098", "languages": {"fr": {"status": "approved"}, "en": {"status": "approved"}}},
        ]
    }
    issues = validate_summary_style_review_data(
        review,
        nodes,
        page_languages,
        quantitative_pages={("A0098", "fr"), ("A0098", "en")},
        summaries={
            ("A0005", "fr"): "Résumé historique.",
            ("A0005", "en"): "Historical summary.",
            ("A0098", "fr"): "En 2017, 4 000 observations documentent le mécanisme.",
            ("A0098", "en"): "In 2017, 4,000 observations document the mechanism.",
        },
        protected_historical=protected,
    )
    assert issues == []


def test_style_ledger_may_omit_nodes_whose_summaries_are_all_historical():
    issues = validate_summary_style_review_data(
        {"entries": []},
        [{"id": "A0005"}],
        {"A0005": {"fr", "en"}},
        summaries={("A0005", "fr"): "Résumé historique.", ("A0005", "en"): "Historical summary."},
        protected_historical={("A0005", "fr"), ("A0005", "en")},
    )
    assert issues == []


def test_new_summary_still_requires_all_creation_style_attestations():
    review = {"entries": [{"id": "A0100", "languages": {"fr": {"status": "approved"}}}]}
    issues = validate_summary_style_review_data(
        review,
        [{"id": "A0100"}],
        {"A0100": {"fr"}},
        quantitative_pages={("A0100", "fr")},
        summaries={("A0100", "fr"): "En 2026, 42 cas montrent le mécanisme de manière concrète."},
        protected_historical=set(),
    )
    reasons = {issue.get("reason") for issue in issues}
    assert "general_public_style" in reasons
    assert "opening_develops_title" in reasons
    assert "conviction_visible" in reasons or "forceful_expression" in reasons
    assert "quantitative_claims_verified" in reasons
