from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import shutil
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


review_tool = load_module("wikidebia_editorial_review")
workspace_tool = sys.modules.get("wikidebia_editorial_workspace") or load_module("wikidebia_editorial_workspace")
common = sys.modules["wikidebia_corpus_build"]

from test_wikidebia_editorial_workspace import make_promoted_project  # noqa: E402


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def add_fourth_argument(corpus: Path) -> None:
    registry_path = corpus / "data/registre_debat.json"
    projection_path = corpus / "graph/graphe_argumentatif.json"
    provenance_path = corpus / "data/import_provenance.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    projection = json.loads(projection_path.read_text(encoding="utf-8"))
    provenance = json.loads(provenance_path.read_text(encoding="utf-8"))

    node = copy.deepcopy(registry["graph"]["nodes"][2])
    node["id"] = "A0004"
    node["fr"]["canonical_title"] = "Argument D"
    node["fr"]["displayed_title"] = "D soutient le débat"
    node["derived"] = {
        "is_main_argument_anywhere": True,
        "is_reused": False,
        "maximum_depth": 1,
        "minimum_depth": 1,
        "occurrence_count": 1,
        "primary_occurrence_id": "O00005",
    }
    node["pages"]["fr"]["file"]["path"] = "output/fr/arguments/A0004.wiki"
    node["pages"]["en"]["file"]["path"] = "output/en/arguments/A0004.wiki"
    registry["graph"]["nodes"].append(node)
    registry["graph"]["occurrences"].append({
        "id": "O00005",
        "node_id": "A0004",
        "parent_occurrence_id": None,
        "edge_id": None,
        "branch": "pro",
        "depth": 1,
        "order": 2,
        "occurrence_role": "primary",
        "render_children": False,
    })
    counts = registry["graph"]["derived_counts"]
    counts["distinct_nodes"] = 4
    counts["total_occurrences"] = 5
    counts["main_pro"] = 2
    counts["leaf_nodes"] = 2
    registry["graph"]["lifecycle"]["structural_sha256"] = common.structural_sha256(registry)

    projection["nodes"] = copy.deepcopy(registry["graph"]["nodes"])
    projection["occurrences"] = copy.deepcopy(registry["graph"]["occurrences"])
    projection["derived_counts"] = copy.deepcopy(counts)
    projection["lifecycle"] = copy.deepcopy(registry["graph"]["lifecycle"])

    source = corpus / "imports/fr/arguments/A0003.wiki"
    target = corpus / "imports/fr/arguments/A0004.wiki"
    shutil.copyfile(source, target)
    source_row = next(row for row in provenance["pages"] if row.get("page_id") == "A0003")
    new_row = copy.deepcopy(source_row)
    new_row["page_id"] = "A0004"
    new_row["canonical_title"] = "Argument D"
    new_row["source_graph_title"] = "Argument D"
    new_row["import_path"] = "imports/fr/arguments/A0004.wiki"
    new_row["sha256"] = sha256(target)
    provenance["pages"].append(new_row)

    common.write_json(registry_path, registry)
    common.write_json(projection_path, projection)
    common.write_json(provenance_path, provenance)


def make_workspace(tmp_path: Path) -> tuple[Path, Path, str]:
    project, corpus = make_promoted_project(tmp_path)
    add_fourth_argument(corpus)
    work_id = "EDIT-REVIEW-001"
    workspace_tool.create_workspace(project, "debat_test", work_id)
    validator_src = Path(__file__).resolve().parents[2] / "validator" / "src"
    shutil.copytree(validator_src, project / "validator" / "src")
    return project, project / ".state/editorial-workspaces/debat_test" / work_id, work_id


def complete_review(workspace: Path) -> None:
    path = workspace / "reviews/fr/page_metadata_review.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    title_pairs = {
        "A0001": (
            "La démonstration A soutient explicitement la proposition du débat test",
            "La preuve A soutient la thèse",
        ),
        "A0002": (
            "La démonstration B contredit explicitement la proposition du débat test",
            "La preuve B contredit la thèse",
        ),
        "A0003": (
            "La démonstration C renforce précisément l'argument A du débat test",
            "La preuve C renforce l'argument A",
        ),
        "A0004": (
            "La démonstration D confirme distinctement la proposition du débat test",
            "La preuve D confirme la thèse",
        ),
    }
    keyword_sets = {
        "debate": ["raisonnement", "controverse", "preuve", "thèse", "réfutation"],
        "A0001": ["preuve", "raisonnement"],
        "A0002": ["réfutation", "désaccord"],
        "A0003": ["justification", "cohérence"],
        "A0004": ["confirmation", "argumentation"],
    }
    for item in data["items"]:
        entity_id = item["entity_id"]
        decision = item["review"]
        decision["status"] = "approved"
        decision["reviewer"] = "Relecteur Wikidéb'IA"
        decision["reviewed_at"] = "2026-08-03T20:00:00+02:00"
        decision["rubriques_decision"] = "keep"
        decision["rubriques_rationales"] = {
            rubric: "Cette rubrique décrit directement le domaine central du raisonnement."
            for rubric in item["source"]["rubriques"]
        }
        decision["keywords_decision"] = "change"
        decision["proposed_keywords"] = keyword_sets[entity_id]
        decision["keywords_rationales"] = {
            keyword: "Ce terme est central, nominal et utile à la navigation entre plusieurs débats."
            for keyword in keyword_sets[entity_id]
        }
        decision["keywords_ordered_by_relevance"] = True
        decision["keyword_order_rationale"] = "La liste commence par le concept le plus directement lié à la page, puis élargit progressivement le contexte."
        if entity_id == "debate":
            decision["canonical_title_decision"] = "not_applicable"
            decision["displayed_title_decision"] = "not_applicable"
        else:
            canonical, displayed = title_pairs[entity_id]
            decision["canonical_title_decision"] = "change"
            decision["proposed_canonical_title"] = canonical
            decision["canonical_title_rationale"] = "Le titre nomme explicitement le sujet et reste autonome hors de sa branche."
            decision["displayed_title_decision"] = "change"
            decision["proposed_displayed_title"] = displayed
            decision["displayed_title_rationale"] = "Le titre affiché conserve la proposition argumentative sous une forme réellement plus concise."
            decision["canonical_referents_explicit"] = True
            decision["displayed_title_complete_proposition"] = True
            decision["displayed_title_argument_intelligible"] = True
            decision["displayed_title_concision_reviewed"] = True
    common.write_json(path, data)

    usages: dict[str, list[dict[str, str]]] = {}
    argument_counts: dict[str, int] = {}
    for item in data["items"]:
        keywords = item["review"]["proposed_keywords"]
        for keyword in keywords:
            usages.setdefault(keyword, []).append({"entity_type": item["entity_type"], "entity_id": item["entity_id"]})
            if item["entity_type"] == "argument":
                argument_counts[keyword] = argument_counts.get(keyword, 0) + 1
    vocabulary = {
        "schema": "wikidebia-keyword-vocabulary-working-1.0",
        "debate_id": "debat_test",
        "work_id": "EDIT-REVIEW-001",
        "status": "draft",
        "entries": [
            {
                "fr": keyword,
                "en": None,
                "definition": f"Concept éditorial contrôlé correspondant au terme {keyword}.",
                "kind": "noun" if " " not in keyword else "noun_phrase",
                "capitalization_policy": "lowercase_common",
                "capitalization_rationale": "",
                "atomic_concept": True,
                "compositional_intersection": False,
                "multiword_exception": " " in keyword,
                **({"multiword_exception_rationale": f"Locution conventionnelle « {keyword} » dont le sens thématique est irréductible à ses constituants."} if " " in keyword else {}),
                "scope": "site_navigation",
                "cross_debate_reusable": True,
                "local_frequency_is_validity_criterion": False,
                "status": "approved_fr",
                "decision": "approved",
                "rationale": "Le terme peut regrouper des arguments appartenant à plusieurs débats distincts.",
                "usages": rows,
            }
            for keyword, rows in sorted(usages.items(), key=lambda pair: pair[0].casefold())
        ],
    }
    common.write_json(workspace / "data/keyword_vocabulary_working.json", vocabulary)


def test_finalize_review_seals_complete_decisions_without_mutating_copies(tmp_path: Path):
    project, workspace, work_id = make_workspace(tmp_path)
    complete_review(workspace)
    source_hash = common.full_tree_sha256(project / "corpus/debat_test")
    working_hash = common.full_tree_sha256(workspace / "working-copy")
    result = review_tool.finalize_review(project, "debat_test", work_id)
    assert result["status"] == "fr_review_finalized"
    assert len(result["review_sha256"]) == 64
    assert common.full_tree_sha256(project / "corpus/debat_test") == source_hash
    assert common.full_tree_sha256(workspace / "working-copy") == working_hash
    sealed = json.loads((workspace / "reviews/fr/page_metadata_review.json").read_text(encoding="utf-8"))
    assert sealed["status"] == "approved"
    assert sealed["review_sha256"] == review_tool.review_sha256(sealed)
    assert len(sealed["finalized_vocabulary"]) >= 8


def test_finalize_rejects_incomplete_page_review(tmp_path: Path):
    project, workspace, work_id = make_workspace(tmp_path)
    complete_review(workspace)
    data = json.loads((workspace / "reviews/fr/page_metadata_review.json").read_text(encoding="utf-8"))
    data["items"][1]["review"]["displayed_title_complete_proposition"] = False
    common.write_json(workspace / "reviews/fr/page_metadata_review.json", data)
    try:
        review_tool.finalize_review(project, "debat_test", work_id)
    except review_tool.EditorialReviewError as exc:
        assert "displayed_title_complete_proposition" in str(exc)
    else:
        raise AssertionError("Revue incomplète acceptée")


def test_finalize_rejects_title_collision(tmp_path: Path):
    project, workspace, work_id = make_workspace(tmp_path)
    complete_review(workspace)
    data = json.loads((workspace / "reviews/fr/page_metadata_review.json").read_text(encoding="utf-8"))
    data["items"][2]["review"]["proposed_canonical_title"] = data["items"][1]["review"]["proposed_canonical_title"]
    common.write_json(workspace / "reviews/fr/page_metadata_review.json", data)
    try:
        review_tool.finalize_review(project, "debat_test", work_id)
    except review_tool.EditorialReviewError as exc:
        assert "Collision" in str(exc)
    else:
        raise AssertionError("Collision de titres acceptée")


def test_finalize_rejects_dominant_exact_keyword_set(tmp_path: Path):
    project, workspace, work_id = make_workspace(tmp_path)
    complete_review(workspace)
    data = json.loads((workspace / "reviews/fr/page_metadata_review.json").read_text(encoding="utf-8"))
    common_set = ["preuve", "raisonnement"]
    for item in data["items"]:
        if item["entity_type"] == "argument":
            item["review"]["proposed_keywords"] = common_set
            item["review"]["keywords_rationales"] = {k: "Ce terme reste central et réutilisable dans plusieurs débats distincts." for k in common_set}
            item["review"]["keywords_ordered_by_relevance"] = True
            item["review"]["keyword_order_rationale"] = "Les concepts sont classés du plus directement pertinent au moins direct pour cette page."
    common.write_json(workspace / "reviews/fr/page_metadata_review.json", data)
    # Align vocabulary so the corpus-level dominance check is the actual blocker.
    usages = []
    for item in data["items"]:
        if item["entity_type"] == "argument":
            usages.append({"entity_type": "argument", "entity_id": item["entity_id"]})
    vocab = json.loads((workspace / "data/keyword_vocabulary_working.json").read_text(encoding="utf-8"))
    # No need to make vocabulary valid: dominance is checked before vocabulary.
    try:
        review_tool.finalize_review(project, "debat_test", work_id)
    except review_tool.EditorialReviewError as exc:
        assert "domine" in str(exc)
    else:
        raise AssertionError("Jeu de mots-clés dominant accepté")


def test_apply_creates_reviewed_copy_and_preserves_provenance(tmp_path: Path):
    project, workspace, work_id = make_workspace(tmp_path)
    complete_review(workspace)
    finalized = review_tool.finalize_review(project, "debat_test", work_id)
    source_hash = common.full_tree_sha256(project / "corpus/debat_test")
    working_hash = common.full_tree_sha256(workspace / "working-copy")
    imports_hash = common.full_tree_sha256(workspace / "working-copy/imports")
    result = review_tool.apply_review(project, "debat_test", work_id, finalized["review_sha256"])
    reviewed = workspace / "reviewed-copy"
    assert result["status"] == "fr_metadata_applied"
    assert reviewed.is_dir()
    assert common.full_tree_sha256(project / "corpus/debat_test") == source_hash
    assert common.full_tree_sha256(workspace / "working-copy") == working_hash
    assert common.full_tree_sha256(reviewed / "imports") == imports_hash
    assert not (reviewed / "output").exists()
    registry = json.loads((reviewed / "data/registre_debat.json").read_text(encoding="utf-8"))
    assert registry["graph"]["nodes"][0]["fr"]["title_status"] == "validated"
    assert registry["graph"]["nodes"][0]["fr"]["canonical_title"].startswith("La démonstration A")
    lock = json.loads((reviewed / "data/fr_page_metadata_lock.json").read_text(encoding="utf-8"))
    assert lock["status"] == "locked_for_generation"
    changes = json.loads((reviewed / "changes/changeset.json").read_text(encoding="utf-8"))
    assert changes["source_imports_mutated"] is False
    translation = json.loads((workspace / "reviews/en/translation_readiness.json").read_text(encoding="utf-8"))
    assert translation["status"] == "ready_for_translation"
    assert {row["translation_status"] for row in translation["items"]} == {"ready_for_translation"}


def test_apply_requires_exact_review_sha256(tmp_path: Path):
    project, workspace, work_id = make_workspace(tmp_path)
    complete_review(workspace)
    review_tool.finalize_review(project, "debat_test", work_id)
    try:
        review_tool.apply_review(project, "debat_test", work_id, "0" * 64)
    except review_tool.EditorialReviewError as exc:
        assert "empreinte confirmée" in str(exc)
    else:
        raise AssertionError("Mauvaise empreinte acceptée")
    assert not (workspace / "reviewed-copy").exists()


def test_apply_rejects_working_copy_changed_after_finalize(tmp_path: Path):
    project, workspace, work_id = make_workspace(tmp_path)
    complete_review(workspace)
    finalized = review_tool.finalize_review(project, "debat_test", work_id)
    (workspace / "working-copy/scope.json").write_text("{}\n", encoding="utf-8")
    try:
        review_tool.apply_review(project, "debat_test", work_id, finalized["review_sha256"])
    except review_tool.EditorialReviewError as exc:
        assert "working-copy" in str(exc)
    else:
        raise AssertionError("Copie de travail altérée acceptée")


def test_apply_is_idempotent_after_success(tmp_path: Path):
    project, workspace, work_id = make_workspace(tmp_path)
    complete_review(workspace)
    finalized = review_tool.finalize_review(project, "debat_test", work_id)
    first = review_tool.apply_review(project, "debat_test", work_id, finalized["review_sha256"])
    second = review_tool.apply_review(project, "debat_test", work_id, finalized["review_sha256"])
    assert second["idempotent"] is True
    assert second["reviewed_copy_tree_sha256"] == first["reviewed_copy_tree_sha256"]


def _rename_keyword_in_review_and_vocabulary(workspace: Path, old: str, new: str) -> None:
    review_path = workspace / "reviews/fr/page_metadata_review.json"
    review = json.loads(review_path.read_text(encoding="utf-8"))
    for item in review["items"]:
        values = item["review"]["proposed_keywords"]
        item["review"]["proposed_keywords"] = [new if value == old else value for value in values]
        rationales = item["review"]["keywords_rationales"]
        if old in rationales:
            rationales[new] = rationales.pop(old)
    common.write_json(review_path, review)
    vocabulary_path = workspace / "data/keyword_vocabulary_working.json"
    vocabulary = json.loads(vocabulary_path.read_text(encoding="utf-8"))
    for entry in vocabulary["entries"]:
        if entry["fr"] == old:
            entry["fr"] = new
    common.write_json(vocabulary_path, vocabulary)


def test_finalize_rejects_uppercase_common_keyword(tmp_path: Path):
    project, workspace, work_id = make_workspace(tmp_path)
    complete_review(workspace)
    _rename_keyword_in_review_and_vocabulary(workspace, "argumentation", "Argumentation")
    vocabulary_path = workspace / "data/keyword_vocabulary_working.json"
    vocabulary = json.loads(vocabulary_path.read_text(encoding="utf-8"))
    entry = next(row for row in vocabulary["entries"] if row["fr"] == "Argumentation")
    entry["kind"] = "noun"
    entry["capitalization_policy"] = "lowercase_common"
    common.write_json(vocabulary_path, vocabulary)
    try:
        review_tool.finalize_review(project, "debat_test", work_id)
    except review_tool.EditorialReviewError as exc:
        assert "Capitalisation non canonique" in str(exc)
    else:
        raise AssertionError("Majuscule décorative acceptée pour un nom commun")


def test_finalize_accepts_justified_proper_name_keyword(tmp_path: Path):
    project, workspace, work_id = make_workspace(tmp_path)
    complete_review(workspace)
    _rename_keyword_in_review_and_vocabulary(workspace, "argumentation", "Dieu")
    vocabulary_path = workspace / "data/keyword_vocabulary_working.json"
    vocabulary = json.loads(vocabulary_path.read_text(encoding="utf-8"))
    entry = next(row for row in vocabulary["entries"] if row["fr"] == "Dieu")
    entry["kind"] = "proper_name"
    entry["capitalization_policy"] = "canonical_proper_name"
    entry["capitalization_rationale"] = "Nom propre canonique de la divinité désignée dans ce thème."
    common.write_json(vocabulary_path, vocabulary)
    result = review_tool.finalize_review(project, "debat_test", work_id)
    assert result["status"] == "fr_review_finalized"


def test_finalize_rejects_case_only_keyword_duplicates(tmp_path: Path):
    project, workspace, work_id = make_workspace(tmp_path)
    complete_review(workspace)
    _rename_keyword_in_review_and_vocabulary(workspace, "argumentation", "Preuve")
    vocabulary_path = workspace / "data/keyword_vocabulary_working.json"
    vocabulary = json.loads(vocabulary_path.read_text(encoding="utf-8"))
    entry = next(row for row in vocabulary["entries"] if row["fr"] == "Preuve")
    entry["kind"] = "proper_name"
    entry["capitalization_policy"] = "canonical_proper_name"
    entry["capitalization_rationale"] = "Graphie volontairement fautive pour tester le doublon de casse."
    common.write_json(vocabulary_path, vocabulary)
    try:
        review_tool.finalize_review(project, "debat_test", work_id)
    except review_tool.EditorialReviewError as exc:
        assert "différant seulement par la casse" in str(exc)
    else:
        raise AssertionError("Doublon preuve/Preuve accepté")
