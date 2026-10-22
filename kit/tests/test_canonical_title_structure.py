import copy
import json

import pytest

import wikidebia_translation_review as translation
import wikidebia_editorial_review as editorial
from wikidebia_title_structure import canonical_title_structure_issues
from test_wikidebia_publish import FakeAdapter, module as publication, write_fixture
from test_wikidebia_remote_update import FakeAdapter as UpdateAdapter, argument, make_fixture, module as update


BAD_TITLES = [
    "Alcohol and tobacco are not inherently dangerous; only excessive use is",
    "The addictive potential of cannabis is neither inherently low nor high; it depends on the level of use",
    "Drug dependence is not independent of the person and their environment. Drugs are a way of coping with life, not the cause of dependence",
    "The law is not only enforced; enforcement has intensified since 2001",
    "La dépendance dépend de la personne. La drogue aide à s'adapter",
]


@pytest.mark.parametrize("title", BAD_TITLES)
def test_compound_canonical_titles_fail_before_translation_is_approved(title):
    with pytest.raises(translation.TranslationReviewError, match="semicolon_joined_statements|multiple_sentences"):
        translation._validate_title(title, "canonical title")


@pytest.mark.parametrize("title", [
    "The addictive potential of cannabis varies with the level of use",
    "Drug dependence depends on the person and their environment",
    "Enforcement of France's drug laws has intensified since 2001",
    "Alcohol and tobacco are dangerous only when used excessively",
    "U.S. drug policies influence other countries",
    "Dr. Smith disputes J. Dupont's interpretation",
    "The price exceeds 1.5 euros",
    "Should cannabis be legalised?",
])
def test_one_sentence_titles_and_abbreviations_are_accepted(title):
    assert canonical_title_structure_issues(title) == []


def test_converged_approved_review_is_still_reported_and_never_rewritten():
    review = {
        "status": "approved", "semantic_convergence_status": "passed",
        "final_values": {"arguments": [
            {"id": f"A{i}", "canonical_title": title, "displayed_title": "Historical label"}
            for i, title in enumerate(BAD_TITLES[:4])
        ]},
    }
    before = copy.deepcopy(review)
    findings = translation.collect_english_title_format_findings(review)
    assert len(findings) == 4
    assert all(row["field"] == "canonical_title" for row in findings)
    assert review == before


def test_historical_displayed_label_is_not_forced_into_creation_form():
    review = {"final_values": {"arguments": [{
        "id": "A1", "canonical_title": "Drug dependence depends on the person",
        "displayed_title": "Historical label; contextual explanation",
    }]}}
    assert translation.collect_english_title_format_findings(review) == []


@pytest.mark.parametrize("validate", [editorial._validate_item, editorial._validate_title_item])
def test_an_approved_keep_decision_cannot_hide_a_bad_french_page_name(validate):
    item = {
        "entity_type": "argument", "entity_id": "A1",
        "source": {
            "page_origin": "preexisting", "canonical_title": BAD_TITLES[-1],
            "displayed_title": "Ancien libellé nominal", "rubriques": [], "keywords": [],
        },
        "review": {
            "status": "approved", "reviewer": "Test reviewer", "reviewed_at": "2026-10-22T00:00:00Z",
            "canonical_title_decision": "keep", "displayed_title_decision": "keep",
            "rubriques_decision": "keep", "keywords_decision": "keep",
        },
    }
    with pytest.raises(editorial.EditorialReviewError, match="Titre canonique à revoir"):
        validate(item)


def test_publication_refuses_an_archive_with_an_old_approved_compound_title(tmp_path):
    config, path, _, _ = write_fixture(tmp_path, "full_page")
    corpus = tmp_path / "corpus/demo"
    manifest_path = corpus / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    for row in manifest["pages"]:
        if row["language"] == "en" and row["page_id"] == "A1":
            row["canonical_title"] = BAD_TITLES[1]
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    adapter = FakeAdapter()
    publisher = publication.GenericPublisher(config, adapter, path)
    with pytest.raises(publication.PublicationError, match="Titre canonique à revoir"):
        publisher.build_plan()
    assert not adapter.pages


def test_update_reports_the_bad_creation_without_writing(tmp_path):
    config, path = make_fixture(tmp_path, old_pages=[], new_pages=[("fr", "A1", BAD_TITLES[-1], argument("Historical text"))])
    adapter = UpdateAdapter()
    plan = update.RemoteUpdatePlanner(config, adapter, path).build_plan()
    assert plan["counts"]["blocked"] == 1
    assert plan["counts"]["create"] == 0
    assert plan["operations"]["blocked"][0]["title_structure_issues"] == ["multiple_sentences"]
    assert not adapter.pages


def test_old_signed_plan_does_not_bypass_the_creation_guard(tmp_path, monkeypatch):
    config, path = make_fixture(tmp_path, old_pages=[], new_pages=[("fr", "A1", BAD_TITLES[-1], argument("Historical text"))])
    adapter = UpdateAdapter()
    original = update.canonical_title_structure_issues
    monkeypatch.setattr(update, "canonical_title_structure_issues", lambda title: [])
    plan = update.RemoteUpdatePlanner(config, adapter, path).build_plan()
    assert plan["counts"]["create"] == 1
    monkeypatch.setattr(update, "canonical_title_structure_issues", original)
    with pytest.raises(update.PlanConflict, match="Titre canonique à revoir"):
        update.PlanExecutor(config, adapter, path).execute(plan, plan["plan_sha256"])
    assert not adapter.pages
