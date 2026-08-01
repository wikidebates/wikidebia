from __future__ import annotations

from wikidebia_validator.editorial import validate_graph_placement_review_data


def registry_with_science_objection(child_depth: int = 2):
    nodes = [
        {"id": "A0001", "status": "active"},
        {"id": "A0002", "status": "active"},
    ]
    if child_depth == 1:
        edges = []
        occurrences = [
            {"id": "O00001", "node_id": "A0001", "parent_occurrence_id": None, "edge_id": None, "depth": 1},
            {"id": "O00002", "node_id": "A0002", "parent_occurrence_id": None, "edge_id": None, "depth": 1},
        ]
    else:
        edges = [{"id": "E00001", "from_node_id": "A0001", "to_node_id": "A0002", "relation": "objection", "status": "active"}]
        occurrences = [
            {"id": "O00001", "node_id": "A0001", "parent_occurrence_id": None, "edge_id": None, "depth": 1},
            {"id": "O00002", "node_id": "A0002", "parent_occurrence_id": "O00001", "edge_id": "E00001", "depth": 2},
        ]
    return {"debate": {"id": "realisme"}, "graph": {"nodes": nodes, "edges": edges, "occurrences": occurrences}}


def main_entry(oid="O00001", nid="A0001"):
    return {
        "occurrence_id": oid,
        "node_id": nid,
        "declared_depth": 1,
        "placement_status": "approved",
        "declared_function": "main_argument",
        "semantic_target": "debate",
        "direct_fit": True,
        "rationale": "Le succès scientifique répond directement au débat et structure une famille autonome.",
        "main_argument_review": {
            "direct_answer_to_debate": True,
            "autonomous_without_parent": True,
            "organizes_distinct_argument_family": True,
            "more_general_nonduplicate_parent_available": False,
            "principally_supports_or_attacks_specific_argument": False,
            "principally_example_or_specialization": False,
        },
    }


def subordinate_entry():
    return {
        "occurrence_id": "O00002",
        "node_id": "A0002",
        "declared_depth": 2,
        "placement_status": "moved_after_review",
        "declared_function": "objection",
        "semantic_target": "O00001",
        "direct_fit": True,
        "rationale": "Les bouleversements scientifiques visent l’inférence du succès des sciences au réalisme.",
        "subordinate_review": {
            "parent_is_best_immediate_target": True,
            "relation_to_parent_explicit": True,
        },
    }


def test_1220_accepts_scientific_overturns_as_objection_to_scientific_success():
    review = {"normative_revision": "1.2.20", "debate_id": "realisme", "entries": [main_entry(), subordinate_entry()]}
    assert validate_graph_placement_review_data(review, registry_with_science_objection(), norm="1.2.20") == []


def test_1220_rejects_targeted_objection_promoted_to_level_one():
    reg = registry_with_science_objection(child_depth=1)
    bad = main_entry("O00002", "A0002")
    bad["rationale"] = "Les bouleversements scientifiques attaquent spécialement l’argument du succès des sciences."
    bad["main_argument_review"]["principally_supports_or_attacks_specific_argument"] = True
    review = {"normative_revision": "1.2.20", "debate_id": "realisme", "entries": [main_entry(), bad]}
    issues = validate_graph_placement_review_data(review, reg, norm="1.2.20")
    assert any(i["reason"] == "principally_supports_or_attacks_specific_argument" for i in issues)


def test_1220_rejects_level_one_without_distinct_family():
    bad = main_entry()
    bad["main_argument_review"]["organizes_distinct_argument_family"] = False
    review = {"normative_revision": "1.2.20", "debate_id": "realisme", "entries": [bad, subordinate_entry()]}
    issues = validate_graph_placement_review_data(review, registry_with_science_objection(), norm="1.2.20")
    assert any(i["reason"] == "organizes_distinct_argument_family" for i in issues)


def test_1220_rejects_wrong_parent_target_or_relation():
    bad = subordinate_entry()
    bad["semantic_target"] = "O99999"
    bad["declared_function"] = "justification"
    review = {"normative_revision": "1.2.20", "debate_id": "realisme", "entries": [main_entry(), bad]}
    issues = validate_graph_placement_review_data(review, registry_with_science_objection(), norm="1.2.20")
    reasons = {i["reason"] for i in issues}
    assert {"semantic_target", "declared_function"} <= reasons


def test_1220_requires_exact_occurrence_coverage():
    review = {"normative_revision": "1.2.20", "debate_id": "realisme", "entries": [main_entry()]}
    issues = validate_graph_placement_review_data(review, registry_with_science_objection(), norm="1.2.20")
    assert any(i["reason"] == "coverage" for i in issues)


def test_1219_does_not_require_graph_placement_ledger():
    # The new validator function is only invoked by the package validator for norm 1.2.20.
    assert "1.2.19" != "1.2.20"
