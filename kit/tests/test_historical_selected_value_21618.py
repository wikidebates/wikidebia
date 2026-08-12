from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import wikidebia_content_review as content
import wikidebia_french_checkpoint as checkpoint
import wikidebia_corpus_build as common
from test_wikidebia_content_review import (
    make_metadata_applied,
    _set_reviewed_historical_text,
    complete_content_review,
    _request_historical_change,
    _write_direct_owner_authorization,
)


HISTORICAL_INTRO = "".join([
    "{{Sous-partie|titre=Définition du vote électronique|contenu=Le vote électronique désigne ici l’usage d’un dispositif informatique pour exprimer, transmettre ou compter un suffrage.}}",
    "{{Sous-partie|titre=Expériences menées à l'échelle d'un pays|contenu=Plusieurs pays ont expérimenté des formes de vote électronique dans des contextes institutionnels différents.}}",
    "{{Sous-partie|titre=Expérimentations en France|contenu=La France a conduit différentes expérimentations, notamment pour certains électeurs et certains scrutins.}}",
    "{{Sous-partie|titre=Historique du débat en France|contenu=Le débat français oppose depuis plusieurs années les gains pratiques attendus aux exigences de sécurité et de contrôle démocratique.}}",
])

STAKES_CONTENT = (
    "Le choix d’un dispositif de vote électronique a des incidences concrètes sur la participation, l’organisation du scrutin et la confiance dans le résultat. "
    "Une panne, une indisponibilité ou une faille peut empêcher certains électeurs de voter, retarder les opérations ou rendre plus difficile la vérification d’un incident. "
    "À l’inverse, un accès à distance peut faciliter la participation de personnes éloignées, expatriées ou empêchées de se déplacer. "
    "La controverse porte donc aussi sur l’accessibilité effective du vote, la continuité du service électoral et la capacité des citoyens à avoir confiance dans le dépouillement."
)
FINAL_INTRO = HISTORICAL_INTRO + f"{{{{Sous-partie|titre=Enjeux du débat|contenu={STAKES_CONTENT}}}}}"


def _prepare_authorized_vote_intro(tmp_path: Path, *, write_authorization: bool = True, final_intro: str = FINAL_INTRO, declared_scope: dict | None = None):
    project, workspace, work_id = make_metadata_applied(tmp_path)
    _set_reviewed_historical_text(workspace, intro=HISTORICAL_INTRO)
    content.prepare_review(project, "debat_test", work_id)
    complete_content_review(workspace)
    review_path = workspace / "reviews/fr/content_review.json"
    data = json.loads(review_path.read_text(encoding="utf-8"))
    rev = data["debate"]["review"]
    rev["introduction_decision"] = "change"
    rev["proposed_introduction"] = final_intro
    rev["subsections"] = [
        {"title": "Définition du vote électronique"},
        {"title": "Expériences menées à l'échelle d'un pays"},
        {"title": "Expérimentations en France"},
        {"title": "Historique du débat en France"},
        {
            "title": "Enjeux du débat",
            "purpose": "Présenter les incidences concrètes nécessaires pour comprendre les conséquences du choix technique.",
            "necessary_for_understanding": True,
            "technical_or_specialized": False,
            "relevance_to_debate_explained": False,
            "stakes_section": True,
            "concrete_stakes": [
                "Accessibilité et continuité concrète du service électoral pour les différents électeurs.",
                "Confiance publique dans la vérifiabilité, l’exactitude et la légitimité du résultat final.",
            ],
        },
    ]
    rev["specialized_term_inventory"] = [{
        "subsection_title": "Enjeux du débat",
        "scan_complete": True,
        "scan_note": "La nouvelle sous-partie a été relue intégralement et ne contient aucune notion spécialisée nécessitant un traitement supplémentaire.",
        "terms": [],
    }]
    rev["terminal_period_sentence_exceptions"] = []
    _request_historical_change(
        rev,
        field_key="debate:debat_test:introduction",
        final_value=final_intro,
        change_type="structure",
        rationale="Ajout de la sous-partie Enjeux du débat explicitement demandé par le propriétaire.",
    )
    rev["historical_change_request"]["change_scope"] = declared_scope or content._subsection_change_scope(HISTORICAL_INTRO, FINAL_INTRO)
    common.write_json(review_path, data)
    auth = _write_direct_owner_authorization(workspace, data) if write_authorization else None
    return project, workspace, work_id, review_path, data, auth


def test_vote_electronique_authorized_4_to_5_subsections_uses_selected_final_everywhere(tmp_path: Path):
    project, workspace, work_id, review_path, _data, auth = _prepare_authorized_vote_intro(tmp_path)
    finalized = content.finalize_review(project, "debat_test", work_id)
    sealed = json.loads(review_path.read_text(encoding="utf-8"))
    debate = sealed["final_values"]["debate"]
    assert debate["introduction"] == FINAL_INTRO
    assert [row["title"] for row in debate["subsections"]] == [
        "Définition du vote électronique",
        "Expériences menées à l'échelle d'un pays",
        "Expérimentations en France",
        "Historique du débat en France",
        "Enjeux du débat",
    ]
    assert debate["historical_text_decision"] == "authorized_change"
    assert debate["historical_introduction_sha256"] == content._historical_text_sha256(HISTORICAL_INTRO)
    assert debate["historical_final_introduction_sha256"] == content._historical_text_sha256(FINAL_INTRO)
    assert debate["historical_change_scope"]["mode"] == "subsections"
    assert debate["historical_change_scope"]["added"] == [{"title": "Enjeux du débat", "occurrence": 1}]

    content.apply_review(project, "debat_test", work_id, finalized["review_sha256"])
    lock = json.loads((workspace / "content-reviewed-copy/data/fr_content_lock.json").read_text(encoding="utf-8"))
    decision = lock["historical_text_decisions"]["debate"]
    assert decision["decision"] == "authorized_change"
    assert decision["historical_sha256"] == content._historical_text_sha256(HISTORICAL_INTRO)
    assert decision["final_sha256"] == content._historical_text_sha256(FINAL_INTRO)
    assert decision["authorization"]["authorization_id"] == auth["authorization_id"]
    assert decision["change_scope"]["added"] == [{"title": "Enjeux du débat", "occurrence": 1}]

    changes = json.loads((workspace / "content-reviewed-copy/changes/fr_content_changeset.json").read_text(encoding="utf-8"))
    intro_ops = [op for op in changes["operations"] if op.get("entity_type") == "debate" and op.get("field") == "introduction"]
    assert len(intro_ops) == 1
    assert intro_ops[0]["before"] == HISTORICAL_INTRO
    assert intro_ops[0]["after"] == FINAL_INTRO

    cp = checkpoint.build_checkpoint(project, "debat_test", work_id, stage="content")
    rendered = (cp / "output/fr/debate/debate.wiki").read_text(encoding="utf-8")
    assert rendered.count("{{Sous-partie") == 5
    for title in (
        "Définition du vote électronique",
        "Expériences menées à l'échelle d'un pays",
        "Expérimentations en France",
        "Historique du débat en France",
        "Enjeux du débat",
    ):
        assert f"|titre={title}" in rendered
    cp_receipt = json.loads((project / ".state/fr-publication/debat_test" / work_id / "content/checkpoint.json").read_text(encoding="utf-8"))
    assert cp_receipt["stage"] == "content"


def test_vote_electronique_same_4_to_5_delta_without_owner_authorization_is_blocked(tmp_path: Path):
    project, _workspace, work_id, _review_path, _data, _auth = _prepare_authorized_vote_intro(tmp_path, write_authorization=False)
    with pytest.raises(content.ContentReviewError, match="autorisation propriétaire"):
        content.finalize_review(project, "debat_test", work_id)


def test_structured_scope_blocks_parasitic_change_to_unchanged_historical_subsection(tmp_path: Path):
    clean_scope = content._subsection_change_scope(HISTORICAL_INTRO, FINAL_INTRO)
    malicious = HISTORICAL_INTRO.replace(
        "Plusieurs pays ont expérimenté des formes de vote électronique",
        "Plusieurs pays ont largement expérimenté des formes de vote électronique",
        1,
    ) + f"{{{{Sous-partie|titre=Enjeux du débat|contenu={STAKES_CONTENT}}}}}"
    project, _workspace, work_id = make_metadata_applied(tmp_path)
    _set_reviewed_historical_text(_workspace, intro=HISTORICAL_INTRO)
    content.prepare_review(project, "debat_test", work_id)
    complete_content_review(_workspace)
    path = _workspace / "reviews/fr/content_review.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    rev = data["debate"]["review"]
    rev["introduction_decision"] = "change"
    rev["proposed_introduction"] = malicious
    _request_historical_change(
        rev,
        field_key="debate:debat_test:introduction",
        final_value=malicious,
        change_type="structure",
        rationale="Le propriétaire a demandé uniquement l’ajout de la sous-partie Enjeux du débat.",
    )
    rev["historical_change_request"]["change_scope"] = clean_scope
    common.write_json(path, data)
    with pytest.raises(content.ContentReviewError, match="dépasse la portée structurée"):
        content.collect_historical_change_requests(data)


def _refresh_content_reviewed_tree_receipt(workspace: Path) -> None:
    meta_path = workspace / "workspace.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    meta["content_reviewed_copy"]["tree_sha256"] = common.full_tree_sha256(workspace / "content-reviewed-copy")
    meta["workspace_sha256"] = None
    meta["workspace_sha256"] = checkpoint.workspace_receipt_hash(meta)
    common.write_json(meta_path, meta)


def test_stale_content_checkpoint_without_executable_plan_is_rebuilt_and_graph_is_untouched(tmp_path: Path):
    project, workspace, work_id, review_path, _data, _auth = _prepare_authorized_vote_intro(tmp_path)
    finalized = content.finalize_review(project, "debat_test", work_id)
    content.apply_review(project, "debat_test", work_id, finalized["review_sha256"])

    graph_stage = project / ".state/fr-publication/debat_test" / work_id / "graph"
    (graph_stage / "checkpoint-corpus").mkdir(parents=True, exist_ok=True)
    (graph_stage / "checkpoint-corpus/marker.txt").write_text("published graph", encoding="utf-8")
    common.write_json(graph_stage / "checkpoint.json", {"stage": "graph", "source_tree_sha256": "g"})
    common.write_json(graph_stage / "publication-receipt.json", {"stage": "graph", "status": "published"})
    graph_before = {p.relative_to(graph_stage).as_posix(): p.read_bytes() for p in graph_stage.rglob("*") if p.is_file()}

    first = checkpoint.build_checkpoint(project, "debat_test", work_id, stage="content")
    first_receipt = json.loads((first.parent / "checkpoint.json").read_text(encoding="utf-8"))
    common.write_json(first.parent / "remote-update-config.json", {"attempt": "v6-preflight"})
    assert not (first.parent / "update-plan.json").exists()

    marker = workspace / "content-reviewed-copy/reports/retry-v7.txt"
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text("corrected documentary review", encoding="utf-8")
    _refresh_content_reviewed_tree_receipt(workspace)

    second = checkpoint.build_checkpoint(project, "debat_test", work_id, stage="content")
    second_receipt = json.loads((second.parent / "checkpoint.json").read_text(encoding="utf-8"))
    assert second_receipt["source_tree_sha256"] != first_receipt["source_tree_sha256"]
    assert not (second.parent / "remote-update-config.json").exists()
    graph_after = {p.relative_to(graph_stage).as_posix(): p.read_bytes() for p in graph_stage.rglob("*") if p.is_file()}
    assert graph_after == graph_before


def test_stale_content_checkpoint_with_execution_capable_plan_is_never_auto_cleaned(tmp_path: Path):
    project, workspace, work_id, _review_path, _data, _auth = _prepare_authorized_vote_intro(tmp_path)
    finalized = content.finalize_review(project, "debat_test", work_id)
    content.apply_review(project, "debat_test", work_id, finalized["review_sha256"])
    cp = checkpoint.build_checkpoint(project, "debat_test", work_id, stage="content")
    stage = cp.parent
    old_receipt = (stage / "checkpoint.json").read_bytes()
    common.write_json(stage / "update-plan.json", {"plan_sha256": "p" * 64, "operations": {"update": [{"page_id": "A0001"}]}})

    marker = workspace / "content-reviewed-copy/reports/retry-after-remote-risk.txt"
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text("new source", encoding="utf-8")
    _refresh_content_reviewed_tree_receipt(workspace)

    with pytest.raises(checkpoint.FrenchCheckpointError, match="autre état verrouillé"):
        checkpoint.build_checkpoint(project, "debat_test", work_id, stage="content")
    assert (stage / "checkpoint.json").read_bytes() == old_receipt
    assert (stage / "update-plan.json").is_file()


def test_stale_content_checkpoint_with_publication_receipt_is_never_auto_cleaned(tmp_path: Path):
    project, workspace, work_id, _review_path, _data, _auth = _prepare_authorized_vote_intro(tmp_path)
    finalized = content.finalize_review(project, "debat_test", work_id)
    content.apply_review(project, "debat_test", work_id, finalized["review_sha256"])
    cp = checkpoint.build_checkpoint(project, "debat_test", work_id, stage="content")
    stage = cp.parent
    common.write_json(stage / "publication-receipt.json", {"stage": "content", "status": "published"})

    marker = workspace / "content-reviewed-copy/reports/retry-after-published.txt"
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text("new source", encoding="utf-8")
    _refresh_content_reviewed_tree_receipt(workspace)

    with pytest.raises(checkpoint.FrenchCheckpointError, match="autre état verrouillé"):
        checkpoint.build_checkpoint(project, "debat_test", work_id, stage="content")
    assert (stage / "publication-receipt.json").is_file()
