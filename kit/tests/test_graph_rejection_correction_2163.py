from __future__ import annotations

import json
import shutil
import sys
import zipfile
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
TESTS = Path(__file__).resolve().parents[0]
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(TESTS))

import wikidebia_review_workflow as wf  # noqa: E402
import wikidebia_corpus_build as common  # noqa: E402
from test_wikidebia_corpus_review import make_project  # noqa: E402


def _rewrite_zip(source: Path, target: Path, edit) -> None:
    staging = target.parent / (target.stem + "-unzipped")
    shutil.rmtree(staging, ignore_errors=True)
    staging.mkdir(parents=True)
    with zipfile.ZipFile(source) as archive:
        archive.extractall(staging)
    edit(staging)
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(x for x in staging.rglob("*") if x.is_file()):
            archive.write(path, path.relative_to(staging).as_posix())
    shutil.rmtree(staging)


def _state(project: Path) -> dict:
    state = {
        "schema": wf.WORKFLOW_SCHEMA,
        "schema_version": "1.0",
        "debate_id": "debat_test",
        "debate_title": "Débat test ?",
        "short_code": "TEST",
        "phase": "graph_review",
        "status": "running",
        "work_id": None,
        "pending_review": None,
        "created_at": "2026-08-11T12:00:00+02:00",
        "updated_at": "2026-08-11T12:00:00+02:00",
    }
    wf._save_workflow(project, state)
    return state


def _complete_rejected_graph_review(staging: Path) -> None:
    placement_path = staging / f"editable/{common.PLACEMENT_REVIEW}"
    placement = json.loads(placement_path.read_text(encoding="utf-8"))
    for entry in placement["entries"]:
        entry["placement_status"] = "approved"
        entry["direct_fit"] = True
        entry["rationale"] = "Cette occurrence a été examinée contre sa cible logique immédiate; une correction globale reste toutefois nécessaire."
        if entry["declared_depth"] == 1:
            block = entry["main_argument_review"]
            block["direct_answer_to_debate"] = True
            block["autonomous_without_parent"] = True
            block["organizes_distinct_argument_family"] = True
            block["more_general_nonduplicate_parent_available"] = False
            block["principally_supports_or_attacks_specific_argument"] = False
            block["principally_example_or_specialization"] = False
        else:
            entry["subordinate_review"]["parent_is_best_immediate_target"] = True
            entry["subordinate_review"]["relation_to_parent_explicit"] = True
    common.write_json(placement_path, placement)

    envelope_path = staging / f"editable/{common.REVIEW_ENVELOPE}"
    envelope = json.loads(envelope_path.read_text(encoding="utf-8"))
    envelope["decision"] = "rejected"
    envelope["reviewer"] = "ChatGPT test"
    envelope["reviewed_at"] = "2026-08-11T18:00:00+02:00"
    envelope["attestations"] = {key: True for key in common.REQUIRED_ATTESTATIONS}
    envelope["blocking_issues"] = ["O00003 doit être une objection plutôt qu'une justification."]
    envelope["notes"] = "Le graphe doit être corrigé avant toute promotion."
    common.write_json(envelope_path, envelope)


def _complete_graph_correction(staging: Path, *, make_cycle: bool = False) -> None:
    path = staging / f"editable/{common.GRAPH_CORRECTION_REVIEW}"
    correction = json.loads(path.read_text(encoding="utf-8"))
    correction["status"] = "corrected"
    correction["reviewer"] = "ChatGPT correction"
    correction["reviewed_at"] = "2026-08-11T18:05:00+02:00"
    correction["notes"] = "Correction structurelle fondée sur les motifs de rejet de la revue précédente."
    if make_cycle:
        by_id = {row["occurrence_id"]: row for row in correction["placements"]}
        by_id["O00001"]["parent_occurrence_id"] = "O00003"
        by_id["O00001"]["relation"] = "justification"
        by_id["O00001"]["branch"] = None
    else:
        for row in correction["placements"]:
            if row["occurrence_id"] == "O00003":
                row["relation"] = "objection"
    common.write_json(path, correction)


def test_rejected_graph_review_opens_correction_package_and_never_promotes(tmp_path: Path) -> None:
    project, build = make_project(tmp_path)
    state = _state(project)
    pending = wf._prepare_graph_package(project, state)
    source = project / pending["package_path"]
    returned = tmp_path / "rejected-review.zip"
    _rewrite_zip(source, returned, _complete_rejected_graph_review)

    result = wf.import_review(project, "debat_test", returned)

    assert result["phase"] == "graph_correction"
    assert result["pending_review"]["review_type"] == "graph_correction"
    assert not (project / "corpus/debat_test").exists()
    assert (project / ".state/corpus-builds/debat_test").is_dir()
    assert json.loads((build / "manifest.json").read_text(encoding="utf-8"))["global_status"] == "graph_draft"
    assert result["graph_rejections"][-1]["blocking_issues"] == ["O00003 doit être une objection plutôt qu'une justification."]

    correction_zip = project / result["pending_review"]["package_path"]
    with zipfile.ZipFile(correction_zip) as archive:
        names = set(archive.namelist())
        assert f"editable/{common.GRAPH_CORRECTION_REVIEW}" in names
        assert f"context/{common.REVIEW_ENVELOPE}" in names
        assert "context/reports/graph_build_review_report.json" in names


def test_valid_graph_correction_is_applied_then_new_review_package_is_prepared(tmp_path: Path, monkeypatch) -> None:
    project, build = make_project(tmp_path)
    state = _state(project)
    pending = wf._prepare_graph_package(project, state)
    rejected = tmp_path / "rejected-review.zip"
    _rewrite_zip(project / pending["package_path"], rejected, _complete_rejected_graph_review)
    after_rejection = wf.import_review(project, "debat_test", rejected)

    correction_return = tmp_path / "corrected-graph.zip"
    _rewrite_zip(project / after_rejection["pending_review"]["package_path"], correction_return, _complete_graph_correction)
    monkeypatch.setattr(wf, "run_initial_validator", lambda project_root, package: {"status": "passed"})
    resumed = wf.import_review(project, "debat_test", correction_return)

    assert resumed["phase"] == "graph_review"
    assert resumed["pending_review"]["review_type"] == "graph_review"
    assert not (project / "corpus/debat_test").exists()
    registry = json.loads((build / "data/registre_debat.json").read_text(encoding="utf-8"))
    occ = next(x for x in registry["graph"]["occurrences"] if x["id"] == "O00003")
    edge = next(x for x in registry["graph"]["edges"] if x["id"] == occ["edge_id"])
    assert edge["relation"] == "objection"
    correction = json.loads((build / common.GRAPH_CORRECTION_REVIEW).read_text(encoding="utf-8"))
    assert correction["status"] == "applied"
    new_review = json.loads((build / common.REVIEW_ENVELOPE).read_text(encoding="utf-8"))
    assert new_review["decision"] == "pending"
    assert new_review["source_build_sha256"] == common.build_payload_sha256(build)


def test_invalid_graph_correction_rolls_back_and_remains_pending(tmp_path: Path) -> None:
    project, build = make_project(tmp_path)
    state = _state(project)
    pending = wf._prepare_graph_package(project, state)
    rejected = tmp_path / "rejected-review.zip"
    _rewrite_zip(project / pending["package_path"], rejected, _complete_rejected_graph_review)
    after_rejection = wf.import_review(project, "debat_test", rejected)

    correction_return = tmp_path / "bad-correction.zip"
    _rewrite_zip(project / after_rejection["pending_review"]["package_path"], correction_return, lambda root: _complete_graph_correction(root, make_cycle=True))
    before = (build / "data/registre_debat.json").read_bytes()
    with pytest.raises(Exception, match="Cycle|racine|Parent|occurrence"):
        wf.import_review(project, "debat_test", correction_return)
    assert (build / "data/registre_debat.json").read_bytes() == before
    current = wf._load_workflow(project, "debat_test")
    assert current["phase"] == "graph_correction"
    assert current["pending_review"]["review_type"] == "graph_correction"
    assert not (project / "corpus/debat_test").exists()


def test_second_rejection_reopens_correction_without_promotion(tmp_path: Path, monkeypatch) -> None:
    project, _build = make_project(tmp_path)
    state = _state(project)
    first_pending = wf._prepare_graph_package(project, state)

    first_rejected = tmp_path / "first-rejected.zip"
    _rewrite_zip(project / first_pending["package_path"], first_rejected, _complete_rejected_graph_review)
    after_first_rejection = wf.import_review(project, "debat_test", first_rejected)
    assert after_first_rejection["phase"] == "graph_correction"

    correction_return = tmp_path / "first-correction.zip"
    _rewrite_zip(
        project / after_first_rejection["pending_review"]["package_path"],
        correction_return,
        _complete_graph_correction,
    )
    monkeypatch.setattr(wf, "run_initial_validator", lambda project_root, package: {"status": "passed"})
    after_correction = wf.import_review(project, "debat_test", correction_return)
    assert after_correction["phase"] == "graph_review"

    second_rejected = tmp_path / "second-rejected.zip"
    _rewrite_zip(
        project / after_correction["pending_review"]["package_path"],
        second_rejected,
        _complete_rejected_graph_review,
    )
    after_second_rejection = wf.import_review(project, "debat_test", second_rejected)

    assert after_second_rejection["phase"] == "graph_correction"
    assert after_second_rejection["pending_review"]["review_type"] == "graph_correction"
    assert len(after_second_rejection["graph_rejections"]) == 2
    assert not (project / "corpus/debat_test").exists()


def test_pending_rejected_package_from_2162_remains_importable_after_upgrade(tmp_path: Path) -> None:
    project, _build = make_project(tmp_path)
    state = _state(project)
    pending = wf._prepare_graph_package(project, state)
    returned = tmp_path / "rejected-from-2162.zip"
    captured: dict[str, str] = {}

    def edit_as_2162(staging: Path) -> None:
        _complete_rejected_graph_review(staging)
        manifest_path = staging / "REVIEW_PACKAGE.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["normative_revision"] = "1.2.75"
        manifest["validator_version"] = "0.4.78"
        manifest["kit_version"] = "2.16.2"
        manifest["manifest_sha256"] = wf._package_manifest_hash(manifest)
        captured["manifest_sha256"] = manifest["manifest_sha256"]
        common.write_json(manifest_path, manifest)

    _rewrite_zip(project / pending["package_path"], returned, edit_as_2162)
    legacy_state = wf._load_workflow(project, "debat_test")
    legacy_state["normative_revision"] = "1.2.75"
    legacy_state["validator_version"] = "0.4.78"
    legacy_state["kit_version"] = "2.16.2"
    legacy_state["pending_review"]["manifest_sha256"] = captured["manifest_sha256"]
    wf._save_workflow(project, legacy_state)

    resumed = wf.import_review(project, "debat_test", returned)
    assert resumed["phase"] == "graph_correction"
    assert resumed["pending_review"]["review_type"] == "graph_correction"
    assert not (project / "corpus/debat_test").exists()


def test_rejected_review_with_execute_graph_actions_uses_direct_action_bridge(tmp_path: Path, monkeypatch) -> None:
    project, _build = make_project(tmp_path)
    state = _state(project)
    pending = wf._prepare_graph_package(project, state)
    returned = tmp_path / "rejected-direct-actions.zip"
    _rewrite_zip(project / pending["package_path"], returned, _complete_rejected_graph_review)

    called = {"value": False}
    def fake_actions(project_root, base, debate_id, **kwargs):
        called["value"] = True
        return {"status": "graph_actions_applied", "removed_nodes": ["A9999"], "remaining_occurrences": 3}
    monkeypatch.setattr(wf, "execute_graph_review_actions", fake_actions)
    monkeypatch.setattr(wf, "run_initial_validator", lambda project_root, package: {"status": "passed"})
    resumed = wf.import_review(project, "debat_test", returned, execute_graph_actions=True)
    assert called["value"] is True
    assert resumed["phase"] == "graph_review"
    assert resumed["pending_review"]["review_type"] == "graph_review"
    assert resumed["graph_action_executions"][-1]["status"] == "graph_actions_applied"
