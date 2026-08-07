from __future__ import annotations

from typing import Any, Mapping


def complete_individual_entry(entry: Mapping[str, Any], node: Mapping[str, Any], *, english_deferred: bool = False) -> dict[str, Any]:
    """Fill an individual-review row with the cumulative current attestations.

    Tests can still override any field afterwards to exercise one specific control.
    """
    out = dict(entry)
    fr = dict(node.get("fr") or {})
    en = dict(node.get("en") or {})
    out.setdefault("title_decision", "retained_after_review")
    out.setdefault("canonical_referents_explicit_fr", True)
    out.setdefault("displayed_referents_explicit_fr", True)
    out.setdefault("displayed_title_complete_proposition_fr", True)
    out.setdefault("displayed_title_argument_intelligible_fr", True)
    out.setdefault("displayed_title_concision_reviewed_fr", True)
    out.setdefault("new_displayed_title_fr", fr.get("displayed_title"))
    out.setdefault("new_rubriques", list(fr.get("rubriques") or []))
    out.setdefault("new_keywords_fr", list(fr.get("keywords") or []))
    out.setdefault("keywords_ordered_by_relevance_fr", True)
    out.setdefault("keyword_order_rationale_fr", "Ordre relu du concept le plus directement pertinent au moins direct.")
    if not english_deferred:
        out.setdefault("canonical_referents_explicit_en", True)
        out.setdefault("displayed_referents_explicit_en", True)
        out.setdefault("displayed_title_complete_proposition_en", True)
        out.setdefault("displayed_title_argument_intelligible_en", True)
        out.setdefault("displayed_title_concision_reviewed_en", True)
        out.setdefault("new_displayed_title_en", en.get("displayed_title"))
        out.setdefault("new_sections_en", list(en.get("sections") or []))
        out.setdefault("new_keywords_en", list(en.get("keywords") or []))
        out.setdefault("keywords_ordered_by_relevance_en", True)
        out.setdefault("keyword_order_rationale_en", "Reviewed from the most directly relevant concept to the least direct one.")
    out.setdefault("rubric_decision", "retained_after_review")
    selected = list(fr.get("rubriques") or [])
    out.setdefault("rubric_rationales", {rubric: f"Justification éditoriale spécifique et suffisamment développée pour {rubric}." for rubric in selected})
    out.setdefault("title_reason", "Le titre a été relu individuellement et cette formulation demeure la plus claire et la plus fidèle au raisonnement.")
    for lang, data in (("fr", fr), ("en", en)):
        if lang == "en" and english_deferred:
            continue
        canonical = str(data.get("canonical_title") or "").strip().casefold()
        displayed = str(data.get("displayed_title") or "").strip().casefold()
        if canonical and canonical != displayed:
            out.setdefault(f"displayed_title_semantic_equivalence_reviewed_{lang}", True)
            out.setdefault(f"displayed_title_readability_improvement_reviewed_{lang}", True)
    return out


def current_summary_text() -> str:
    return "Le mécanisme central relie directement la cause alléguée à la conclusion défendue. Cette formulation reste claire pour le lecteur général."


def complete_summary_decision(decision: Mapping[str, Any] | None = None, *, summary: str | None = None) -> tuple[dict[str, Any], str]:
    text = summary or current_summary_text()
    out = dict(decision or {})
    for key in (
        "thesis_first",
        "general_public_style",
        "sentence_rhythm_reviewed",
        "technical_terms_reviewed",
        "opening_develops_title",
        "example_or_data_reviewed",
        "assertive_tone_reviewed",
        "no_artificial_example_or_number",
        "no_polemical_overstatement",
        "conviction_visible",
        "wikipedia_hover_links_reviewed",
        "specialized_terms_linked_or_explained",
        "originality_reviewed",
    ):
        out.setdefault(key, True)
    out.setdefault("status", "revised")
    out.setdefault("forceful_expression", "relie directement la cause alléguée")
    out.setdefault("mechanism_statement", "Le mécanisme central relie directement la cause alléguée à la conclusion défendue.")
    out.setdefault("note", "Résumé relu individuellement selon l’ensemble de la politique éditoriale courante.")
    return out, text
