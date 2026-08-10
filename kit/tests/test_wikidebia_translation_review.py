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
convergence = load_module("wikidebia_semantic_convergence")
content = sys.modules.get("wikidebia_content_review") or load_module("wikidebia_content_review")
metadata = sys.modules.get("wikidebia_editorial_review") or load_module("wikidebia_editorial_review")
common = sys.modules["wikidebia_corpus_build"]


def fake_validator(*args, **kwargs):
    return {"validator_version": "0.4.29", "result": "passed", "summary": {"errors": 0, "warnings": 0}}


metadata._run_validator = fake_validator
content._run_validator = fake_validator
translation._run_validator = fake_validator

from test_wikidebia_content_review import make_metadata_applied, complete_content_review, source_row  # noqa: E402


def make_french_locked(tmp_path: Path) -> tuple[Path, Path, str]:
    project, workspace, work_id = make_metadata_applied(tmp_path)
    content.prepare_review(project, "debat_test", work_id)
    complete_content_review(workspace)
    sealed = content.finalize_review(project, "debat_test", work_id)
    content.apply_review(project, "debat_test", work_id, sealed["review_sha256"])
    return project, workspace, work_id


def complete_semantic_convergence(project: Path, work_id: str) -> None:
    first = convergence.record_pass(
        project, "debat_test", work_id,
        method="proposition-by-proposition semantic comparison",
        reviewer="Semantic reviewer A",
        note="The first independent pass compared propositions, modalities, logical relations and scope against the sealed French source.",
        new_certain_errors=0,
    )
    assert first["status"] == "in_progress"
    second = convergence.record_pass(
        project, "debat_test", work_id,
        method="risk-marker and boundary-focused reread",
        reviewer="Semantic reviewer B",
        note="The second independent pass rechecked risk markers, opening and closing propositions, exclusivities and concrete anchors.",
        new_certain_errors=0,
    )
    assert second["status"] == "converged"


def en_source(source_id: str, source_type: str, usages: list[dict[str, object]]) -> dict[str, object]:
    row = source_row(source_id, source_type, usages)
    row["language"] = "en"
    row["metadata"]["authors"] = [f"English Author {int(source_id[1:])}"]
    row["metadata"]["date"] = "3 August 2026"
    if source_type == "bibliography":
        row["metadata"]["work"] = f"English Reference Work {int(source_id[1:])}"
    elif source_type == "webliography":
        row["metadata"]["page"] = f"English documentary page {int(source_id[1:])}"
        row["metadata"]["site"] = f"English documentary site {int(source_id[1:])}"
    else:
        row["metadata"]["title"] = f"English documentary video {int(source_id[1:])}"
        row["metadata"]["site"] = f"English video platform {int(source_id[1:])}"
    row["verification"]["notes"] = ["English language, notice and attribution verified."]
    row["usage"] = usages
    row["deduplication_key"] = f"en-source-{int(source_id[1:])}"
    return row


def complete_translation_review(workspace: Path) -> None:
    path = workspace / "reviews/en/translation_review.json"
    review = json.loads(path.read_text(encoding="utf-8"))
    translations = {
        "argumentation": "argumentation", "cohérence": "coherence", "confirmation": "confirmation",
        "controverse": "controversy", "désaccord": "disagreement", "justification": "justification",
        "preuve": "evidence", "raisonnement": "reasoning", "réfutation": "refutation", "thèse": "thesis",
    }
    for row in review["vocabulary"]:
        row.update({
            "en": translations[row["fr"]],
            "definition_en": f"Controlled editorial concept corresponding to {translations[row['fr']]}",
            "capitalization_verified": True,
            "capitalization_rationale_en": "",
            "status": "approved", "idiomatic_equivalent": True, "same_concept": True,
            "reviewer": "English reviewer", "reviewed_at": "2026-08-03T21:30:00+02:00",
            "note": "The English term is idiomatic and preserves the French navigation concept.",
        })
    debate = review["debate"]
    fr_meta = debate["french"]["metadata"]
    debate.update({
        "status": "approved", "canonical_title": "Test debate", "topic": "Test debate",
        "complete_topic": "the proposition of the test debate",
        "sections": sorted([translation.SECTION_MAP[x] for x in fr_meta["rubriques"]], key=str.casefold),
        "keywords": [translations[x] for x in fr_meta["keywords"]],
        "introduction": "{{Subsection|title=Definition and scope|content=The test debate contrasts two clearly delimited answers and specifies what is actually at issue.}}{{Subsection|title=Stakes of the debate|content=The answer adopted changes how the phenomenon is explained and which standards are used to accept a conclusion. It may also shape collective decisions, institutional practices, and individual choices beyond the theoretical disagreement itself. Suspending judgment shifts attention toward the limits of the available evidence and toward the degree of confidence that can reasonably be placed in each position.}}",
        "subsections": [{"title": "Definition and scope", "purpose": "Define the proposition and the exact scope required to understand the disagreement.", "necessary_for_understanding": True, "technical_or_specialized": False, "relevance_to_debate_explained": True, "stakes_section": False, "concrete_stakes": []}, {"title": "Stakes of the debate", "purpose": "Explain the intellectual, institutional, and practical consequences of the possible answers.", "necessary_for_understanding": True, "technical_or_specialized": False, "relevance_to_debate_explained": True, "stakes_section": True, "concrete_stakes": ["Changes to explanatory frameworks and standards of rational belief", "Consequences for collective decisions and institutional practices"]}],
        "wikipedia_articles": ["Argumentation theory"],
        "documentation": {
            "pro-bibliography": ["S10001"], "con-bibliography": ["S10002"], "bibliography": [],
            "pro-webliography": ["S10003"], "con-webliography": ["S10004"], "webliography": [],
            "pro-videography": ["S10005"], "con-videography": ["S10006"], "videography": [],
        },
        "documentation_family_notes": {"bibliography": "Broad English-language works cover the debate.", "webliography": "Verified English-language web sources complement the books.", "videography": "Verified English-language videos cover each position."},
        "topic_label_rationale": "The nominal label identifies the controversy without restating it as a question.",
        "metadata_equivalent_to_french": True, "content_equivalent_to_french": True,
        "canonical_title_semantic_inventory_reviewed": True,
        "canonical_title_semantic_inventory_note": "Subject, predicate, scope and force of the canonical debate title were compared against the French source.",
        "topic_semantic_equivalence_reviewed": True,
        "complete_topic_semantic_equivalence_reviewed": True,
        "introduction_claim_inventory_reviewed": True,
        "introduction_claim_inventory_note": "All substantive claims, distinctions, historical framing and stakes in the French introduction were checked against the English introduction.",
        "subsection_structure_equivalence_reviewed": True,
        "sections_exactly_mapped": True, "keywords_exactly_mapped": True,
        "keywords_order_preserved_by_relevance": True,
        "introduction_functionally_equivalent": True, "wikipedia_articles_verified": True,
        "all_debate_sources_english": True, "reviewer": "English reviewer",
        "reviewed_at": "2026-08-03T21:40:00+02:00",
        "note": "The Debate metadata, introduction and documentation are ready for the bilingual lock.",
    })
    fr_dmeta = debate["french"]["metadata"]
    fr_dcontent = debate["french"]["content"]
    debate_pairs = {
        "canonical_title": (str(fr_dmeta.get("canonical_title") or ""), debate["canonical_title"]),
        "topic": (str(fr_dcontent.get("subject") or ""), debate["topic"]),
        "complete_topic": (str(fr_dcontent.get("complete_topic") or ""), debate["complete_topic"]),
        "introduction": (str(fr_dcontent.get("introduction") or ""), debate["introduction"]),
    }
    debate_risks = []
    debate_evidence = []
    for field_name, (source_text, target_text) in debate_pairs.items():
        for risk in translation._semantic_risk_signals(source_text, target_text):
            tagged = f"{field_name}:{risk}"
            debate_risks.append(tagged)
            debate_evidence.append({"risk": tagged, "source_excerpt": source_text, "target_excerpt": target_text, "note": "The source and target field were compared directly for this semantic-risk signal."})
    debate["debate_field_semantic_risk_reviewed"] = bool(debate_risks)
    debate["debate_field_semantic_risk_note"] = "All detected Debate field-level semantic risks were checked against the locked French source." if debate_risks else ""
    debate["debate_field_semantic_risk_evidence"] = debate_evidence
    for field in translation.INTRO_TRUE_FIELDS:
        debate[field] = True
    titles = {
        "A0001": ("Demonstration A explicitly supports the proposition of the test debate", "Evidence A supports the thesis"),
        "A0002": ("Demonstration B directly challenges the proposition of the test debate", "Evidence B challenges the thesis"),
        "A0003": ("Demonstration C specifically strengthens argument A in the test debate", "Evidence C strengthens argument A"),
        "A0004": ("Demonstration D distinctly confirms the proposition of the test debate", "Evidence D confirms the thesis"),
    }
    summaries = {
        "A0001": "The first line of evidence gives the test debate firmer ground by connecting an explicit premise to the conclusion assigned to node A0001. The mechanism remains accessible and does not pre-empt the objection directed at it.",
        "A0002": "The second line of evidence puts direct pressure on the test proposition by linking a clear premise to the conclusion assigned to node A0002. The mechanism remains accessible and leaves the opposing objection to its own page.",
        "A0003": "The third line of evidence strengthens the parent argument by connecting a precise premise to the conclusion assigned to node A0003. The mechanism remains accessible and does not smuggle its own rebuttal into the summary.",
        "A0004": "The fourth line of evidence gives the test proposition additional support by linking a distinct premise to the conclusion assigned to node A0004. The mechanism remains accessible and does not anticipate the objection against it.",
    }
    expressions = {
        "A0001": "The first line of evidence gives the test debate firmer ground",
        "A0002": "The second line of evidence puts direct pressure on the test proposition",
        "A0003": "The third line of evidence strengthens the parent argument",
        "A0004": "The fourth line of evidence gives the test proposition additional support",
    }
    for item in review["arguments"]:
        nid = item["id"]
        row = item["translation"]
        fr_meta = row["french"]["metadata"]
        row.update({
            "status": "approved", "canonical_title": titles[nid][0], "displayed_title": titles[nid][1],
            "sections": sorted([translation.SECTION_MAP[x] for x in fr_meta["rubriques"]], key=str.casefold),
            "keywords": [translations[x] for x in fr_meta["keywords"]], "summary": summaries[nid],
            "sources": {"bibliography": ["S10001"], "webliography": [], "videography": []},
            "argument_name_search_queries": [f'"{titles[nid][0]}" argument', f'{titles[nid][0]} conventional name literature'],
            "argument_name_search_scope_note": "English-language academic terminology and alternative phrasings were checked.",
            "argument_name_search_provenance": "actual_log",
            "argument_name_search_provenance_note": "The two query strings above were actually used during this test review.",
            "argument_name_outcome": "none", "argument_name": None, "argument_name_evidence": [],
            "argument_name_same_reasoning_confirmed": False,
            "argument_name_non_invented_label_confirmed": True,
            "argument_name_language_fit_confirmed": True,
            "argument_name_rationale": "No sufficiently established conventional name was found for this generated argument.",
            "argument_name_page_reasoning_scope_summary": "This page presents the exact reasoning expressed by its canonical title and summary.",
            "argument_name_literature_scope_summary": "",
            "argument_name_scope_relation": "",
            "argument_name_scope_identity_confirmed": False,
            "metadata_equivalent_to_french": True, "summary_equivalent_to_french": True,
            "canonical_title_semantic_inventory_reviewed": True,
            "canonical_title_semantic_inventory_note": "Subject, predicate, polarity, modality, attribution, quantifiers, force and logical relation of the canonical title were compared.",
            "canonical_title_equivalent_to_french": True,
            "canonical_title_subject_preserved": True, "canonical_title_predicate_preserved": True,
            "canonical_title_scope_preserved": True, "canonical_title_modality_preserved": True,
            "sections_exactly_mapped": True, "keywords_exactly_mapped": True,
        "keywords_order_preserved_by_relevance": True,
            "title_is_idiomatic": True,
            "displayed_title_source_form": "proposition", "displayed_title_target_form": "proposition",
            "displayed_title_source_form_reviewed": True, "displayed_title_no_formal_regression": True,
            "displayed_title_semantic_inventory_reviewed": True,
            "displayed_title_semantic_inventory_note": "Subject, predicate, polarity, modality, attribution, quantifiers, force, temporal scope, conditions and logical relation were compared.",
            "displayed_title_subject_preserved": True, "displayed_title_predicate_preserved": True,
            "displayed_title_scope_preserved": True, "displayed_title_modality_preserved": True,
            "displayed_title_translates_french_displayed_title": True,
            "displayed_title_identity_pattern_reviewed": True,
            "displayed_title_identity_pattern_note": "The English displayed title was compared directly with the French displayed title and not regenerated from the canonical title.",
            "displayed_title_is_complete_proposition": True,
            "displayed_title_concision_reviewed": True,
            "displayed_title_semantically_equivalent": True,
            "displayed_title_improves_readability_when_distinct": True,
            "summary_ratio_reviewed": True,
            "summary_subject_predicate_scope_modality_reviewed": True,
            "summary_opening_proposition_preserved": True,
            "summary_closing_proposition_preserved": True,
            "summary_conditions_exclusivities_preserved": True,
            "summary_decisive_premises_preserved": True,
            "summary_semantic_evidence_note": "Opening and closing propositions, conditions, exclusivities and decisive premises were compared directly with the French source.",
            "semantic_risk_reviewed": True,
            "semantic_risk_note": "Any semantic marker differences were explicitly reviewed against the French source and judged equivalent.",
            "forceful_expression": expressions[nid], "quantitative_claims_verified": False,
            "quantitative_claims_note": "No quantitative claim appears in this English summary.",
            "documentation_rationale": "The selected English source supports the central mechanism without imposing an artificial quota.",
            "reviewer": "English reviewer", "reviewed_at": "2026-08-03T21:45:00+02:00",
            "note": "The English title, summary, sections, keywords and documentation preserve the French node.",
        })
        fr_row = row["french"]
        fr_meta_row = fr_row["metadata"]
        fr_content_row = fr_row["content"]
        semantic_pairs = [
            (str(fr_meta_row.get("canonical_title") or ""), row["canonical_title"]),
            (str(fr_meta_row.get("displayed_title") or ""), row["displayed_title"]),
            (str(fr_content_row.get("summary") or ""), row["summary"]),
        ]
        risks = sorted({risk for source_text, target_text in semantic_pairs for risk in translation._semantic_risk_signals(source_text, target_text)})
        row["semantic_risk_reviewed"] = bool(risks)
        row["semantic_risk_note"] = "All semantic-risk signals in this test fixture were compared directly with the French source." if risks else ""
        row["semantic_risk_evidence"] = []
        for risk in risks:
            for source_text, target_text in semantic_pairs:
                if risk in translation._semantic_risk_signals(source_text, target_text):
                    row["semantic_risk_evidence"].append({"risk": risk, "source_excerpt": source_text, "target_excerpt": target_text, "note": "The source and target excerpts were checked directly for this semantic-risk signal."})
                    break
        translated_quotes = {
            "A0001": ("Freedom consists in wanting what one wants.", "25 June 2012"),
            "A0002": ("A sufficient cause is not necessarily a constraint.", "June 2012"),
            "A0003": ("The reasoning retains its force in this case.", "1971"),
            "A0004": ("The reasoning retains its force in this case.", "1971"),
        }
        for citation in row.get("citations") or []:
            translated_text, translated_date = translated_quotes[nid]
            citation.update({
                "status": "approved",
                "translated_citation": translated_text,
                "translated_date": translated_date,
                "citation_translated": True,
                "date_translated_or_language_neutral": True,
                "preserved_parameters_unchanged": True,
                "translation_warning_appended": True,
                "quote_completeness_reviewed": True,
                "quote_completeness_note": "The full French citation was compared from beginning to end with the English translation.",
                "quote_low_ratio_reviewed": True,
                "quote_low_ratio_note": "The English wording is concise but the full source meaning and all sentences were checked.",
                "reviewer": "English citation reviewer",
                "reviewed_at": "2026-08-03T21:46:00+02:00",
                "note": "Only the citation text and date were translated; all documentary parameters were preserved.",
            })
        for field in translation.SUMMARY_TRUE_FIELDS:
            row[field] = True
    for unit in review.get("review_units") or []:
        unit.update({
            "status": "approved", "reviewer": "Unit reviewer",
            "reviewed_at": "2026-08-03T21:59:00+02:00",
            "note": "This review unit was closed independently at the density recommended from the French source.",
        })
    review["global_review"] = {
        "reviewer": "English reviewer", "reviewed_at": "2026-08-03T22:00:00+02:00",
        "all_entities_translated": True, "all_equivalences_reviewed": True,
        "all_selected_sources_verified": True, "relations_and_occurrences_unchanged": True,
        "no_final_pages_generated": True, "remote_access_not_used": True,
        "blocking_issues": [], "note": "The English projection is complete, equivalent and ready to be locked without rendering pages.",
    }
    common.write_json(path, review)

    source_roles = {
        "S10001": "pro_reference", "S10002": "con_reference",
        "S10003": "pro_reference", "S10004": "con_reference",
        "S10005": "pro_reference", "S10006": "con_reference",
    }
    sources = []
    for sid, stype in (("S10001", "bibliography"), ("S10002", "bibliography"), ("S10003", "webliography"), ("S10004", "webliography"), ("S10005", "videography"), ("S10006", "videography")):
        usages = [{"page_id": "debat_test", "language": "en", "role": source_roles[sid], "language_fit": "native", "preferred_equivalent_source_id": None, "documentary_scope": "broad_synthesis", "selection_reason": "This verified English source documents the orientation assigned to it."}]
        if sid == "S10001":
            usages.extend({"page_id": nid, "language": "en", "role": "supports_summary", "argument_development_verified": True, "also_develops_objections": False, "objection_coverage_note": None, "language_fit": "native", "preferred_equivalent_source_id": None, "documentary_scope": "narrow_argument", "selection_reason": "This English source directly supports the mechanism stated in the argument summary."} for nid in titles)
        sources.append(en_source(sid, stype, usages))
    common.write_json(workspace / "data/sources_en_working.json", {"schema": translation.EN_SOURCES_WORKING_SCHEMA, "source_registry_version": "1.0", "debate_id": "debat_test", "work_id": review["work_id"], "status": "draft", "prepared_at": review["prepared_at"], "sources": sources})


def test_prepare_translation_is_read_only_for_french_copy(tmp_path: Path):
    project, workspace, work_id = make_french_locked(tmp_path)
    before = common.full_tree_sha256(workspace / "content-reviewed-copy")
    result = translation.prepare_review(project, "debat_test", work_id)
    assert result["status"] == "en_translation_review_ready"
    assert common.full_tree_sha256(workspace / "content-reviewed-copy") == before
    assert not (workspace / "translated-copy").exists()
    meta = json.loads((workspace / "workspace.json").read_text(encoding="utf-8"))
    assert meta["boundaries"]["english_translation_started"] is True
    assert meta["boundaries"]["final_pages_generated"] is False


def test_finalize_translation_seals_complete_bilingual_review(tmp_path: Path):
    project, workspace, work_id = make_french_locked(tmp_path)
    translation.prepare_review(project, "debat_test", work_id)
    complete_translation_review(workspace)
    before = common.full_tree_sha256(workspace / "content-reviewed-copy")
    result = translation.finalize_review(project, "debat_test", work_id)
    assert result["status"] == "en_translation_review_finalized"
    assert result["arguments"] == 4
    assert result["sources"] == 6
    assert common.full_tree_sha256(workspace / "content-reviewed-copy") == before
    sealed = json.loads((workspace / "reviews/en/translation_review.json").read_text(encoding="utf-8"))
    assert sealed["review_sha256"] == translation.translation_review_sha256(sealed)


def test_finalize_rejects_missing_vocabulary_equivalence(tmp_path: Path):
    project, workspace, work_id = make_french_locked(tmp_path)
    translation.prepare_review(project, "debat_test", work_id)
    complete_translation_review(workspace)
    path = workspace / "reviews/en/translation_review.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["vocabulary"][0]["same_concept"] = False
    common.write_json(path, data)
    try:
        translation.finalize_review(project, "debat_test", work_id)
    except translation.TranslationReviewError as exc:
        assert "Équivalence lexicale" in str(exc)
    else:
        raise AssertionError("Équivalence lexicale incomplète acceptée")


def test_finalize_rejects_bad_summary_ratio(tmp_path: Path):
    project, workspace, work_id = make_french_locked(tmp_path)
    translation.prepare_review(project, "debat_test", work_id)
    complete_translation_review(workspace)
    path = workspace / "reviews/en/translation_review.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["arguments"][0]["translation"]["summary"] = "Evidence A supports the thesis with a premise."
    data["arguments"][0]["translation"]["forceful_expression"] = "Evidence A supports the thesis"
    common.write_json(path, data)
    try:
        translation.finalize_review(project, "debat_test", work_id)
    except translation.TranslationReviewError as exc:
        assert "Ratio anglais/français" in str(exc)
    else:
        raise AssertionError("Ratio bilingue invalide accepté")


def test_finalize_rejects_non_english_debate_source(tmp_path: Path):
    project, workspace, work_id = make_french_locked(tmp_path)
    translation.prepare_review(project, "debat_test", work_id)
    complete_translation_review(workspace)
    path = workspace / "data/sources_en_working.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["sources"][0]["language"] = "fr"
    common.write_json(path, data)
    try:
        translation.finalize_review(project, "debat_test", work_id)
    except translation.TranslationReviewError as exc:
        assert "doit être en" in str(exc)
    else:
        raise AssertionError("Source française acceptée dans la projection anglaise")


def test_apply_translation_creates_distinct_bilingual_copy(tmp_path: Path):
    project, workspace, work_id = make_french_locked(tmp_path)
    translation.prepare_review(project, "debat_test", work_id)
    complete_translation_review(workspace)
    sealed = translation.finalize_review(project, "debat_test", work_id)
    corpus_hash = common.full_tree_sha256(project / "corpus/debat_test")
    content_hash = common.full_tree_sha256(workspace / "content-reviewed-copy")
    fr_meta = (workspace / "content-reviewed-copy/data/fr_page_metadata_lock.json").read_bytes()
    fr_content = (workspace / "content-reviewed-copy/data/fr_content_lock.json").read_bytes()
    complete_semantic_convergence(project, work_id)
    result = translation.apply_review(project, "debat_test", work_id, sealed["review_sha256"])
    target = workspace / "translated-copy"
    assert result["status"] == "en_translation_applied"
    assert target.is_dir()
    assert common.full_tree_sha256(project / "corpus/debat_test") == corpus_hash
    assert common.full_tree_sha256(workspace / "content-reviewed-copy") == content_hash
    assert (target / "data/fr_page_metadata_lock.json").read_bytes() == fr_meta
    assert (target / "data/fr_content_lock.json").read_bytes() == fr_content
    assert (target / "data/en_page_metadata_lock.json").is_file()
    assert (target / "data/en_content_lock.json").is_file()
    assert (target / "data/en_translation_lock.json").is_file()
    assert (target / "data/keyword_vocabulary_bilingual.json").is_file()
    assert not (target / "output").exists()
    registry = json.loads((target / "data/registre_debat.json").read_text(encoding="utf-8"))
    assert registry["debate"]["pages"]["en"]["canonical_title"] == "Test debate"
    assert all(node["en"]["title_status"] == "validated" for node in registry["graph"]["nodes"] if node["status"] == "active")
    name_review = json.loads((target / "reviews/argument_name_discovery_review.json").read_text(encoding="utf-8"))
    assert name_review["normative_revision"] == translation.NORM_VERSION
    assert name_review["version"] == "wikidebia-argument-name-discovery-review-1.2"
    assert all(row.get("search_provenance") in {"actual_log", "fresh_recheck"} for row in name_review["entries"] if row.get("language") == "en")
    manifest = json.loads((target / "manifest.json").read_text(encoding="utf-8"))
    assert "argument_name_discovery_revision" not in manifest["editorial_controls"]
    assert manifest["editorial_controls"]["argument_name_discovery_path"] == "reviews/argument_name_discovery_review.json"



def test_finalize_translation_preserves_citation_metadata_and_appends_warning(tmp_path: Path):
    project, workspace, work_id = make_french_locked(tmp_path)
    translation.prepare_review(project, "debat_test", work_id)
    complete_translation_review(workspace)
    sealed = translation.finalize_review(project, "debat_test", work_id)
    complete_semantic_convergence(project, work_id)
    translation.apply_review(project, "debat_test", work_id, sealed["review_sha256"])
    lock = json.loads((workspace / "translated-copy/data/en_content_lock.json").read_text(encoding="utf-8"))
    by_id = {row["id"]: row for row in lock["arguments"]}
    a = by_id["A0001"]["citations"][0]
    source_preserved = {row["name"]: row["value"] for row in a["source"]["preserved_parameters"]}
    output = {row["name"]: row["value"] for row in a["parameters"]}
    assert source_preserved["auteurs"] == "Harry G. Frankfurt"
    assert output["authors"] == "Harry G. Frankfurt"
    assert output["work"] == "The Importance of What We Care About"
    assert output["article"] == "Freedom of the Will and the Concept of a Person"
    assert output["quote"] == "Freedom consists in wanting what one wants."
    assert output["date"] == "25 June 2012"
    assert output["warnings"] == "Texte abrégé, AI-translated quote"
    assert a["output_template"] == "Quote"
    assert a["quote_completeness_reviewed"] is True
    assert a["source_word_count"] > 0 and a["translated_word_count"] > 0
    assert isinstance(a["lexical_ratio"], float)
    assert all(row["name"] not in {"citation", "auteurs", "ouvrage", "numéro", "localisation", "édition", "lieu", "lien", "avertissements-citation"} for row in a["parameters"])
    b = by_id["A0002"]["citations"][0]
    output_b = {row["name"]: row["value"] for row in b["parameters"]}
    assert output_b["warnings"] == "AI-translated quote"
    assert by_id["A0004"]["citations"][0]["date"] == "1971"


def test_finalize_translation_rejects_wrong_citation_date(tmp_path: Path):
    project, workspace, work_id = make_french_locked(tmp_path)
    translation.prepare_review(project, "debat_test", work_id)
    complete_translation_review(workspace)
    path = workspace / "reviews/en/translation_review.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["arguments"][0]["translation"]["citations"][0]["translated_date"] = "26 June 2012"
    common.write_json(path, data)
    try:
        translation.finalize_review(project, "debat_test", work_id)
    except translation.TranslationReviewError as exc:
        assert "même date" in str(exc)
    else:
        raise AssertionError("Date de citation divergente acceptée")


def test_finalize_translation_rejects_mutated_citation_source_parameters(tmp_path: Path):
    project, workspace, work_id = make_french_locked(tmp_path)
    translation.prepare_review(project, "debat_test", work_id)
    complete_translation_review(workspace)
    path = workspace / "reviews/en/translation_review.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["arguments"][0]["translation"]["citations"][0]["source"]["preserved_parameters"][0]["value"] = "Auteur modifié"
    common.write_json(path, data)
    try:
        translation.finalize_review(project, "debat_test", work_id)
    except translation.TranslationReviewError as exc:
        assert "paramètres source" in str(exc)
    else:
        raise AssertionError("Altération des paramètres documentaires acceptée")

def test_apply_requires_exact_translation_hash(tmp_path: Path):
    project, workspace, work_id = make_french_locked(tmp_path)
    translation.prepare_review(project, "debat_test", work_id)
    complete_translation_review(workspace)
    translation.finalize_review(project, "debat_test", work_id)
    complete_semantic_convergence(project, work_id)
    try:
        translation.apply_review(project, "debat_test", work_id, "0" * 64)
    except translation.TranslationReviewError as exc:
        assert "empreinte confirmée" in str(exc)
    else:
        raise AssertionError("Mauvaise empreinte anglaise acceptée")
    assert not (workspace / "translated-copy").exists()


def test_finalize_rejects_french_copy_changed_after_prepare(tmp_path: Path):
    project, workspace, work_id = make_french_locked(tmp_path)
    translation.prepare_review(project, "debat_test", work_id)
    complete_translation_review(workspace)
    (workspace / "content-reviewed-copy/scope.json").write_text("{}\n", encoding="utf-8")
    try:
        translation.finalize_review(project, "debat_test", work_id)
    except translation.TranslationReviewError as exc:
        assert "content-reviewed-copy" in str(exc)
    else:
        raise AssertionError("Base française altérée acceptée")


def test_finalize_translation_rejects_french_template_in_english_introduction(tmp_path: Path):
    project, workspace, work_id = make_french_locked(tmp_path)
    translation.prepare_review(project, "debat_test", work_id)
    complete_translation_review(workspace)
    path = workspace / "reviews/en/translation_review.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["debate"]["introduction"] = "{{Sous-partie|titre=Definition|contenu=This English paragraph explains the debate in sufficient detail for a general reader.}}"
    common.write_json(path, data)
    try:
        translation.finalize_review(project, "debat_test", work_id)
    except translation.TranslationReviewError as exc:
        assert "Modèle français interdit" in str(exc)
    else:
        raise AssertionError("Un modèle français a été accepté dans l’introduction anglaise")


def test_finalize_translation_rejects_french_parameter_in_english_summary(tmp_path: Path):
    project, workspace, work_id = make_french_locked(tmp_path)
    translation.prepare_review(project, "debat_test", work_id)
    complete_translation_review(workspace)
    path = workspace / "reviews/en/translation_review.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    summary = data["arguments"][0]["translation"]["summary"]
    data["arguments"][0]["translation"]["summary"] = summary + " {{Wikipedia link|article=Free will|texte-affiché=free will}}"
    common.write_json(path, data)
    try:
        translation.finalize_review(project, "debat_test", work_id)
    except translation.TranslationReviewError as exc:
        assert "Paramètre français interdit" in str(exc)
    else:
        raise AssertionError("Un paramètre français a été accepté dans le summary anglais")


def test_vocabulary_accepts_justified_english_proper_name_and_rejects_common_capital():
    french = [{
        "fr": "Dieu", "kind": "proper_name",
        "capitalization_policy": "canonical_proper_name",
    }]
    rows = [{
        "fr": "Dieu", "en": "God", "definition_en": "The proper name used for the deity.",
        "kind": "proper_name", "capitalization_policy": "canonical_proper_name",
        "capitalization_verified": True,
        "capitalization_rationale_en": "Canonical English proper name for the deity.",
        "status": "approved", "idiomatic_equivalent": True, "same_concept": True,
        "reviewer": "English reviewer", "reviewed_at": "2026-08-04T14:00:00+02:00",
        "note": "The term preserves the same concept and canonical spelling.",
    }]
    result, mapping = translation._validate_vocabulary(rows, french)
    assert mapping == {"Dieu": "God"}
    bad_french = [{"fr": "revenu", "kind": "noun", "capitalization_policy": "lowercase_common"}]
    bad_rows = [dict(rows[0], fr="revenu", en="Income", kind="noun", capitalization_policy="lowercase_common", capitalization_rationale_en="")]
    try:
        translation._validate_vocabulary(bad_rows, bad_french)
    except translation.TranslationReviewError as exc:
        assert "Capitalisation anglaise non canonique" in str(exc)
    else:
        raise AssertionError("Capitalized English common noun accepted")


def test_finalize_translation_rejects_missing_stakes_subsection(tmp_path: Path):
    project, workspace, work_id = make_french_locked(tmp_path)
    translation.prepare_review(project, "debat_test", work_id)
    complete_translation_review(workspace)
    review_path = workspace / "reviews/en/translation_review.json"
    review = json.loads(review_path.read_text(encoding="utf-8"))
    debate = review["debate"]
    debate["introduction"] = "{{Subsection|title=Definition and scope|content=This introduction defines the scope but deliberately omits the mandatory subsection devoted to the consequences of the debate.}}"
    debate["subsections"] = [debate["subsections"][0]]
    common.write_json(review_path, review)
    try:
        translation.finalize_review(project, "debat_test", work_id)
    except translation.TranslationReviewError as exc:
        assert "Stakes of the debate" in str(exc)
    else:
        raise AssertionError("A missing Stakes of the debate subsection should have been rejected")


def test_english_argument_established_name_parameters_are_preserved_import_parameters():
    assert 'established-name' in translation.EN_PAGE_LIFECYCLE_PARAMETERS['argument']
    assert 'name' in translation.EN_PAGE_LIFECYCLE_PARAMETERS['argument']


def test_validate_argument_preserves_historical_absent_summary(monkeypatch):
    row = {
        "status": "approved", "page_origin": "new", "preserved_parameters": {},
        "french": {"metadata": {"rubriques": ["Philosophie"], "keywords": ["cause", "existence"]}, "content": {"summary": None, "citations": []}},
        "canonical_title": "A complete argument is valid", "displayed_title": "A complete argument is valid",
        "sections": ["Philosophy"], "keywords": ["cause", "existence"], "summary": "",
        "citations": [], "sources": {"bibliography": [], "webliography": [], "videography": []},
        "argument_name_search_queries": ["complete argument name", "complete argument terminology"],
        "argument_name_search_scope_note": "Academic English terminology was reviewed.",
        "argument_name_search_provenance": "fresh_recheck",
        "argument_name_search_provenance_note": "The test models an actual fresh terminology recheck with the two recorded queries.",
        "argument_name_outcome": "none", "argument_name": None, "argument_name_evidence": [],
        "argument_name_same_reasoning_confirmed": False, "argument_name_non_invented_label_confirmed": True,
        "argument_name_language_fit_confirmed": True, "argument_name_rationale": "No conventional name is sufficiently established.",
        "argument_name_page_reasoning_scope_summary": "This page presents the exact reasoning expressed by its canonical title and summary.",
        "argument_name_literature_scope_summary": "", "argument_name_scope_relation": "",
        "argument_name_scope_identity_confirmed": False,
        "metadata_equivalent_to_french": True, "summary_equivalent_to_french": True,
        "canonical_title_semantic_inventory_reviewed": True,
        "canonical_title_semantic_inventory_note": "The canonical title subject, predicate, polarity, modality and logical scope were compared with the French source.",
        "canonical_title_equivalent_to_french": True,
        "canonical_title_subject_preserved": True, "canonical_title_predicate_preserved": True,
        "canonical_title_scope_preserved": True, "canonical_title_modality_preserved": True,
        "sections_exactly_mapped": True, "keywords_exactly_mapped": True, "keywords_order_preserved_by_relevance": True,
        "title_is_idiomatic": True,
        "displayed_title_source_form": "proposition", "displayed_title_target_form": "proposition",
        "displayed_title_source_form_reviewed": True, "displayed_title_no_formal_regression": True,
        "displayed_title_semantic_inventory_reviewed": True,
        "displayed_title_semantic_inventory_note": "The test explicitly reviews subject, predicate, polarity, modality, attribution and logical scope.",
        "displayed_title_subject_preserved": True, "displayed_title_predicate_preserved": True,
        "displayed_title_scope_preserved": True, "displayed_title_modality_preserved": True,
        "displayed_title_translates_french_displayed_title": True,
        "displayed_title_identity_pattern_reviewed": True,
        "displayed_title_identity_pattern_note": "The displayed-title is directly tied to the French displayed-title in this historical-absence test.",
        "displayed_title_is_complete_proposition": True,
        "displayed_title_concision_reviewed": True, "displayed_title_semantically_equivalent": True,
        "displayed_title_improves_readability_when_distinct": True, "summary_ratio_reviewed": False,
        "forceful_expression": "", "quantitative_claims_verified": False, "quantitative_claims_note": "",
        "documentation_rationale": "No English documentary source is selected for this test page.",
        "reviewer": "Reviewer", "reviewed_at": "2026-08-07T22:00:00+02:00",
        "note": "French source summary is historically absent and must remain absent in English.",
    }
    result = translation._validate_argument({"id": "A9999", "translation": row}, {"cause": "cause", "existence": "existence"}, {})
    assert result["summary"] is None
    assert result["summary_length_ratio"] is None
    assert result["forceful_expression"] is None


def test_validate_argument_requires_canonical_semantic_review():
    item = {
        "id": "A9998",
        "translation": {
            "status": "approved", "page_origin": "new", "preserved_parameters": {},
            "french": {"metadata": {"rubriques": ["Philosophie"], "keywords": ["cause", "existence"]}, "content": {"summary": None, "citations": []}},
            "canonical_title": "A complete translated claim is valid", "displayed_title": "A complete translated claim is valid",
            "sections": ["Philosophy"], "keywords": ["cause", "existence"], "summary": "",
            "citations": [], "sources": {"bibliography": [], "webliography": [], "videography": []},
            "argument_name_search_queries": ["query one", "query two"],
            "argument_name_search_scope_note": "English academic naming was checked across multiple phrasings.",
            "argument_name_search_provenance": "fresh_recheck",
            "argument_name_search_provenance_note": "These two queries were actually used in the fresh recheck.",
            "argument_name_outcome": "none", "argument_name": None, "argument_name_evidence": [],
            "argument_name_same_reasoning_confirmed": False, "argument_name_non_invented_label_confirmed": True,
            "argument_name_language_fit_confirmed": True, "argument_name_rationale": "No conventional name was found.",
            "metadata_equivalent_to_french": True, "summary_equivalent_to_french": True,
            "canonical_title_semantic_inventory_reviewed": False,
            "canonical_title_semantic_inventory_note": "", "canonical_title_equivalent_to_french": False,
            "sections_exactly_mapped": True, "keywords_exactly_mapped": True, "keywords_order_preserved_by_relevance": True,
            "title_is_idiomatic": True, "displayed_title_source_form": "proposition", "displayed_title_target_form": "proposition",
            "displayed_title_source_form_reviewed": True, "displayed_title_no_formal_regression": True,
            "displayed_title_semantic_inventory_reviewed": True,
            "displayed_title_semantic_inventory_note": "Subject, predicate, polarity, modality and scope were reviewed.",
            "displayed_title_translates_french_displayed_title": True,
            "displayed_title_identity_pattern_reviewed": True,
            "displayed_title_identity_pattern_note": "The displayed-title is directly tied to its French source for this negative canonical-title test.",
            "displayed_title_is_complete_proposition": True, "displayed_title_concision_reviewed": True,
            "displayed_title_semantically_equivalent": True, "displayed_title_improves_readability_when_distinct": True,
            "summary_ratio_reviewed": False, "forceful_expression": "", "quantitative_claims_verified": False, "quantitative_claims_note": "",
            "documentation_rationale": "No source is selected in this unit test.", "reviewer": "Reviewer",
            "reviewed_at": "2026-08-09T19:30:00+02:00", "note": "The row is intentionally missing canonical semantic approval."
        }
    }
    import pytest
    with pytest.raises(translation.TranslationReviewError, match="titre canonique"):
        translation._validate_argument(item, {"cause": "cause", "existence": "existence"}, {})


def test_validate_debate_requires_claim_inventory():
    row = translation._blank_debate({"rubriques": [], "keywords": []}, {"subject": "Test", "complete_topic": "test", "introduction": "source"})
    row.update({"status": "approved", "canonical_title": "A complete test debate", "topic": "Test debate", "complete_topic": "the complete test debate",
                "canonical_title_semantic_inventory_reviewed": True,
                "canonical_title_semantic_inventory_note": "The canonical title was compared semantically with its source.",
                "topic_semantic_equivalence_reviewed": True, "complete_topic_semantic_equivalence_reviewed": True,
                "introduction_claim_inventory_reviewed": False, "subsection_structure_equivalence_reviewed": True})
    import pytest
    with pytest.raises(translation.TranslationReviewError, match="introduction_claim_inventory_reviewed"):
        translation._validate_debate(row, {}, {}, "debate_test")


def test_finalize_translation_requires_second_completeness_review_for_low_quote_ratio(tmp_path: Path):
    project, workspace, work_id = make_french_locked(tmp_path)
    translation.prepare_review(project, "debat_test", work_id)
    complete_translation_review(workspace)
    path = workspace / "reviews/en/translation_review.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    citation = data["arguments"][0]["translation"]["citations"][0]
    citation["translated_citation"] = "Short translation."
    citation["quote_low_ratio_reviewed"] = False
    citation["quote_low_ratio_note"] = ""
    common.write_json(path, data)
    try:
        translation.finalize_review(project, "debat_test", work_id)
    except translation.TranslationReviewError as exc:
        assert "seconde revue explicite" in str(exc)
    else:
        raise AssertionError("Une Quote très courte sans seconde revue de complétude a été acceptée")


def test_translation_risk_profile_shrinks_dense_review_units():
    dense = translation._translation_risk_profile(
        {"preserved_parameters": {"name": "Argument cosmologique"}},
        {
            "summary": ("Si tous les faits doivent être expliqués, alors cette conclusion peut être nécessaire; " * 30),
            "citations": [{"citation": "mot " * 140}, {"citation": "mot " * 150}, {"citation": "court"}],
            "sources": {"bibliography": ["S1", "S2", "S3"], "webliography": ["S4"], "videography": []},
        },
    )
    assert dense["level"] in {"high", "very_high"}
    assert dense["recommended_unit_size"] <= 6


def test_translation_risk_profile_keeps_simple_page_at_default_ten():
    simple = translation._translation_risk_profile({}, {"summary": "Une prémisse simple conduit à une conclusion simple.", "citations": [], "sources": {}})
    assert simple["level"] == "low"
    assert simple["recommended_unit_size"] == 10

# Historical test-name alias retained for non-regression traceability.
def test_english_argument_name_is_a_preserved_import_parameter():
    assert 'name' in translation.EN_PAGE_LIFECYCLE_PARAMETERS['argument']
