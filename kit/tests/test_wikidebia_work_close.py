from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import wikidebia_corpus_build as corpus
import wikidebia_editorial_workspace as workspace_mod
import wikidebia_remote_execute as execution
import wikidebia_work_close as closure
from test_wikidebia_remote_execute import make_approved_fixture


def passing_validator(project_root, package_root, *, scopes, json_output, text_output):
    report = {
        "validator_version": closure.VALIDATOR_VERSION,
        "result": "passed",
        "summary": {"errors": 0, "warnings": 0},
        "scopes": list(scopes),
    }
    json_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    text_output.write_text("Validation réussie.\n", encoding="utf-8")
    return report


closure._run_validator = passing_validator


def make_executed(tmp_path: Path, *, no_changes: bool = False):
    project, debate_id, work_id, comparison_id, approved, adapter, _ = make_approved_fixture(tmp_path, no_changes=no_changes)
    active = project / "corpus" / debate_id
    active.mkdir(parents=True)
    (active / "old.json").write_text('{"status":"graph_validated"}\n', encoding="utf-8")
    source_sha = corpus.full_tree_sha256(active)
    workspace = project / ".state/editorial-workspaces" / debate_id / work_id
    meta_path = workspace / "workspace.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    meta["source"] = {"path": f"corpus/{debate_id}", "tree_sha256": source_sha, "global_status": "graph_validated"}
    meta["workspace_sha256"] = workspace_mod.workspace_receipt_hash(meta)
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    prepared = execution.prepare_execution(project, debate_id, work_id, comparison_id, approved["acceptance_sha256"], adapter=adapter)
    if prepared["status"] == "no_changes_in_scope":
        preflight_path = project / ".state/remote-executions" / debate_id / work_id / comparison_id / "execution-preflight.json"
        value = json.loads(preflight_path.read_text(encoding="utf-8"))
        value["status"] = "ready"
        value["preflight_sha256"] = execution._canonical(value, "preflight_sha256")
        preflight_path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        receipt_path = preflight_path.parent / "preflight-receipt.json"
        pre_receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        pre_receipt["status"] = "ready"
        pre_receipt["preflight_sha256"] = value["preflight_sha256"]
        pre_receipt["receipt_sha256"] = execution._canonical(pre_receipt, "receipt_sha256")
        receipt_path.write_text(json.dumps(pre_receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        prepared["preflight_sha256"] = value["preflight_sha256"]
    receipt = execution.execute_accepted_plan(project, debate_id, work_id, comparison_id, prepared["preflight_sha256"], adapter=adapter)
    return project, debate_id, work_id, comparison_id, receipt, source_sha


def test_close_promotes_published_corpus_and_archives_chain(tmp_path: Path):
    project, debate_id, work_id, comparison_id, execution_receipt, old_sha = make_executed(tmp_path)
    release = project / ".state/editorial-workspaces" / debate_id / work_id / "release-copy"
    release_sha = corpus.full_tree_sha256(release)
    result = closure.close_work(project, debate_id, work_id, comparison_id, execution_receipt["receipt_sha256"])
    active = project / "corpus" / debate_id
    assert result["status"] == "work_closed"
    assert result["atomic_exchange"] is True
    assert corpus.full_tree_sha256(active) == release_sha == result["active_corpus_tree_sha256"]
    backup = project / result["previous_corpus_archive"]
    assert backup.is_dir() and corpus.full_tree_sha256(backup) == old_sha
    evidence = project / result["evidence_archive"]
    assert evidence.is_file() and corpus.sha256_file(evidence) == result["evidence_archive_sha256"]
    assert (project / ".state/completed-works" / debate_id / "latest.json").is_file()
    workspace = json.loads((project / ".state/editorial-workspaces" / debate_id / work_id / "workspace.json").read_text(encoding="utf-8"))
    assert workspace["status"] == "work_closed"


def test_close_is_idempotent(tmp_path: Path):
    project, debate_id, work_id, comparison_id, execution_receipt, _ = make_executed(tmp_path)
    first = closure.close_work(project, debate_id, work_id, comparison_id, execution_receipt["receipt_sha256"])
    second = closure.close_work(project, debate_id, work_id, comparison_id, execution_receipt["receipt_sha256"])
    assert second["idempotent"] is True
    assert second["receipt_sha256"] == first["receipt_sha256"]


def test_close_refuses_wrong_execution_hash_without_partial_directory(tmp_path: Path):
    project, debate_id, work_id, comparison_id, _, _ = make_executed(tmp_path)
    try:
        closure.close_work(project, debate_id, work_id, comparison_id, "0" * 64)
    except closure.WorkClosureError as exc:
        assert "empreinte confirmée" in str(exc)
    else:
        raise AssertionError("Une mauvaise empreinte d’exécution a été acceptée")
    assert not (project / ".state/work-closures" / debate_id / work_id / comparison_id).exists()


def test_close_refuses_pending_delete(tmp_path: Path):
    project, debate_id, work_id, comparison_id, execution_receipt, _ = make_executed(tmp_path)
    state_path = project / ".state/published" / debate_id / "fr/latest.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["pages"][0]["status"] = "pending_delete"
    unsigned = dict(state)
    unsigned.pop("state_sha256", None)
    state["state_sha256"] = closure.sha_object(unsigned)
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    try:
        closure.close_work(project, debate_id, work_id, comparison_id, execution_receipt["receipt_sha256"])
    except closure.WorkClosureError as exc:
        assert "suppression" in str(exc) and "différée" in str(exc)
    else:
        raise AssertionError("Un état pending_delete a été clôturé")


def test_no_changes_execution_can_close(tmp_path: Path):
    project, debate_id, work_id, comparison_id, execution_receipt, _ = make_executed(tmp_path, no_changes=True)
    result = closure.close_work(project, debate_id, work_id, comparison_id, execution_receipt["receipt_sha256"])
    assert result["execution_status"] == "no_changes"
    assert result["work_completed"] is True


def test_manage_exposes_workspace_close_command():
    import wikidebia_manage as manage
    args = manage.build_parser().parse_args([
        "corpus-workspace-close", "debat_test",
        "--work-id", "EDIT-CLOSE-001",
        "--comparison-id", "REMOTE-20260804-001",
        "--confirm-execution-sha256", "a" * 64,
    ])
    assert args.command == "corpus-workspace-close"
    assert args.confirm_execution_sha256 == "a" * 64
