from __future__ import annotations

import importlib.util
import json
import shutil
import sys
import zipfile
from pathlib import Path

import pytest

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


wf = load_module("wikidebia_review_workflow")
manage = load_module("wikidebia_manage")
common = sys.modules["wikidebia_corpus_build"]


def make_state(project: Path, base: Path, review_type: str = "graph_review") -> dict:
    state = {
        "schema": wf.WORKFLOW_SCHEMA,
        "schema_version": "1.0",
        "debate_id": "debat_test",
        "debate_title": "Débat test ?",
        "phase": review_type,
        "status": "running",
        "work_id": None,
        "pending_review": None,
        "created_at": "2026-08-11T12:00:00+02:00",
        "updated_at": "2026-08-11T12:00:00+02:00",
    }
    wf._save_workflow(project, state)
    return state


def make_base(project: Path) -> Path:
    base = project / ".state/corpus-builds/debat_test"
    (base / "reviews").mkdir(parents=True)
    (base / "data").mkdir(parents=True)
    (base / "private").mkdir(parents=True)
    common.write_json(base / "reviews/edit.json", {"debate_id": "debat_test", "value": "pending"})
    common.write_json(base / "data/context.json", {"debate_id": "debat_test", "locked": True})
    (base / "private/secret.txt").write_text("TOP-SECRET", encoding="utf-8")
    return base


def rewrite_zip(source: Path, target: Path, edit):
    temp = target.parent / "unzipped"
    shutil.rmtree(temp, ignore_errors=True)
    temp.mkdir(parents=True)
    with zipfile.ZipFile(source) as z:
        z.extractall(temp)
    edit(temp)
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for p in sorted(x for x in temp.rglob("*") if x.is_file()):
            z.write(p, p.relative_to(temp).as_posix())
    shutil.rmtree(temp)


def test_review_package_is_minimal_and_excludes_secrets(tmp_path: Path):
    project = tmp_path / "project"
    project.mkdir()
    base = make_base(project)
    state = make_state(project, base)
    pending = wf.create_review_package(
        project, state, review_type="graph_review", base=base,
        editable_paths=["reviews/edit.json"], context_paths=["data/context.json"], counts={"placements": 4},
    )
    archive = project / pending["package_path"]
    with zipfile.ZipFile(archive) as z:
        names = set(z.namelist())
        assert names == {
            "REVIEW_PACKAGE.json", "INSTRUCTIONS.md",
            "editable/reviews/edit.json", "context/data/context.json",
        }
        assert all("private" not in name and "secret" not in name for name in names)
        manifest = json.loads(z.read("REVIEW_PACKAGE.json"))
        assert manifest["schema"] == wf.PACKAGE_SCHEMA
        assert manifest["debate_id"] == "debat_test"
        assert manifest["editable_files"][0]["target_path"] == "reviews/edit.json"


def test_package_creation_is_idempotent_while_review_pending(tmp_path: Path):
    project = tmp_path / "project"
    project.mkdir()
    base = make_base(project)
    state = make_state(project, base)
    first = wf.create_review_package(project, state, review_type="graph_review", base=base, editable_paths=["reviews/edit.json"], context_paths=["data/context.json"])
    reloaded = wf._load_workflow(project, "debat_test")
    second = wf.create_review_package(project, reloaded, review_type="graph_review", base=base, editable_paths=["reviews/edit.json"], context_paths=["data/context.json"])
    assert first["package_id"] == second["package_id"]
    assert first["archive_sha256"] == second["archive_sha256"]


def test_import_refuses_modified_context_and_wrong_corpus(tmp_path: Path):
    project = tmp_path / "project"
    project.mkdir()
    base = make_base(project)
    state = make_state(project, base)
    pending = wf.create_review_package(project, state, review_type="graph_review", base=base, editable_paths=["reviews/edit.json"], context_paths=["data/context.json"])
    original = project / pending["package_path"]

    bad_context = tmp_path / "bad-context.zip"
    def change_context(root: Path):
        (root / "context/data/context.json").write_text('{}\n', encoding="utf-8")
    rewrite_zip(original, bad_context, change_context)
    with pytest.raises(wf.WorkflowError, match="contexte"):
        wf.import_review(project, "debat_test", bad_context)

    wrong = tmp_path / "wrong.zip"
    def change_manifest(root: Path):
        path = root / "REVIEW_PACKAGE.json"
        data = json.loads(path.read_text())
        data["debate_id"] = "autre_debat"
        data["manifest_sha256"] = wf._package_manifest_hash(data)
        common.write_json(path, data)
    rewrite_zip(original, wrong, change_manifest)
    with pytest.raises(wf.WorkflowError, match="autre corpus|provenance"):
        wf.import_review(project, "debat_test", wrong)


def test_valid_import_installs_only_editable_and_resumes(tmp_path: Path, monkeypatch):
    project = tmp_path / "project"
    project.mkdir()
    base = make_base(project)
    state = make_state(project, base)
    pending = wf.create_review_package(project, state, review_type="graph_review", base=base, editable_paths=["reviews/edit.json"], context_paths=["data/context.json"])
    original = project / pending["package_path"]
    returned = tmp_path / "returned.zip"
    def complete(root: Path):
        common.write_json(root / "editable/reviews/edit.json", {"debate_id": "debat_test", "value": "approved"})
    rewrite_zip(original, returned, complete)

    monkeypatch.setattr(wf, "finalize_graph_review", lambda project_root, base_path, debate_id: {"status": "approved", "review_sha256": "a" * 64})
    monkeypatch.setattr(wf, "_mechanical_advance", lambda project_root, s: s)
    result = wf.import_review(project, "debat_test", returned)
    assert common.load_json(base / "reviews/edit.json", "edit")["value"] == "approved"
    assert common.load_json(base / "data/context.json", "context")["locked"] is True
    assert result["phase"] == "promote_and_workspace"
    assert result["pending_review"] is None


def test_failed_import_restores_complete_control_directory(tmp_path: Path, monkeypatch):
    project = tmp_path / "project"
    project.mkdir()
    base = make_base(project)
    state = make_state(project, base)
    pending = wf.create_review_package(project, state, review_type="graph_review", base=base, editable_paths=["reviews/edit.json"], context_paths=["data/context.json"])
    original = project / pending["package_path"]
    returned = tmp_path / "returned.zip"
    rewrite_zip(original, returned, lambda root: common.write_json(root / "editable/reviews/edit.json", {"debate_id": "debat_test", "value": "bad"}))

    def failing_finalize(project_root, base_path, debate_id):
        (base_path / "reports").mkdir(exist_ok=True)
        (base_path / "reports/partial.txt").write_text("partial", encoding="utf-8")
        raise RuntimeError("validation failed")
    monkeypatch.setattr(wf, "finalize_graph_review", failing_finalize)
    with pytest.raises(RuntimeError, match="validation failed"):
        wf.import_review(project, "debat_test", returned)
    assert common.load_json(base / "reviews/edit.json", "edit")["value"] == "pending"
    assert not (base / "reports/partial.txt").exists()
    assert wf._load_workflow(project, "debat_test")["pending_review"]["package_id"] == pending["package_id"]


def test_manage_keeps_advanced_commands_and_adds_high_level_commands():
    parser = manage.build_parser()
    choices = parser._subparsers._group_actions[0].choices
    for command in (
        "corpus-init-from-snapshot", "corpus-review-graph", "corpus-promote",
        "corpus-workspace-review", "corpus-workspace-content-review",
        "corpus-workspace-translation", "corpus-workspace-semantic-convergence",
        "workflow", "review-import", "workflow-status",
    ):
        assert command in choices


def test_semantic_response_requires_real_method_family():
    response = wf._semantic_response_template("semantic_convergence_1")
    assert response["new_certain_errors"] is None
    assert response["method_family"] == ""
    assert wf.ALLOWED_METHOD_FAMILIES == {
        "proposition_by_proposition", "risk_marker_review", "reverse_source_target",
        "field_boundary_review", "independent_bilingual_reread",
    }


def test_end_to_end_graph_handoff_resumes_to_metadata_handoff(tmp_path: Path, monkeypatch):
    from test_wikidebia_corpus_init import make_extraction

    project = tmp_path / "project"
    project.mkdir()
    source = make_extraction(tmp_path / "source")
    monkeypatch.setattr(wf, "run_initial_validator", lambda project_root, package: {"status": "passed"})

    def fake_graph_validator(project_root, package, json_output, text_output, **kwargs):
        common.write_json(json_output, {"result": "passed", "summary": {"errors": 0, "warnings": 0}})
        text_output.parent.mkdir(parents=True, exist_ok=True)
        text_output.write_text("passed\n", encoding="utf-8")
        return {"result": "passed", "summary": {"errors": 0, "warnings": 0}}
    monkeypatch.setitem(wf.finalize_graph_review.__globals__, "run_validator", fake_graph_validator)

    def fake_promote(project_root: Path, debate_id: str, confirm_review_sha256: str):
        build = project_root / ".state/corpus-builds" / debate_id
        target = project_root / "corpus" / debate_id
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(build), str(target))
        return {"status": "promoted", "review_sha256": confirm_review_sha256}

    monkeypatch.setattr(wf, "promote_graph", fake_promote)

    state = wf.start_workflow(project, "Débat test ?", debate_id="debat_test", short_code="TEST", snapshot=source)
    assert state["pending_review"]["review_type"] == "graph_review"
    graph_zip = project / state["pending_review"]["package_path"]
    returned = tmp_path / "graph-reviewed.zip"

    def complete_graph(root: Path):
        placement_path = root / f"editable/{common.PLACEMENT_REVIEW}"
        placement = json.loads(placement_path.read_text(encoding="utf-8"))
        for entry in placement["entries"]:
            entry["placement_status"] = "approved"
            entry["direct_fit"] = True
            entry["rationale"] = "Cette occurrence vise directement la meilleure cible logique et conserve exactement sa fonction argumentative."
            if entry["declared_depth"] == 1:
                block = entry["main_argument_review"]
                block.update({
                    "direct_answer_to_debate": True,
                    "autonomous_without_parent": True,
                    "organizes_distinct_argument_family": True,
                    "more_general_nonduplicate_parent_available": False,
                    "principally_supports_or_attacks_specific_argument": False,
                    "principally_example_or_specialization": False,
                })
            else:
                entry["subordinate_review"].update({
                    "parent_is_best_immediate_target": True,
                    "relation_to_parent_explicit": True,
                })
        common.write_json(placement_path, placement)
        envelope_path = root / f"editable/{common.REVIEW_ENVELOPE}"
        envelope = json.loads(envelope_path.read_text(encoding="utf-8"))
        envelope["decision"] = "approved"
        envelope["reviewer"] = "ChatGPT review"
        envelope["reviewed_at"] = "2026-08-11T14:00:00+02:00"
        envelope["attestations"] = {key: True for key in common.REQUIRED_ATTESTATIONS}
        envelope["blocking_issues"] = []
        envelope["notes"] = "Revue complète des placements et de la cohérence argumentative du graphe."
        common.write_json(envelope_path, envelope)

    rewrite_zip(graph_zip, returned, complete_graph)
    resumed = wf.import_review(project, "debat_test", returned)
    assert resumed["work_id"]
    assert resumed["pending_review"]["review_type"] == "fr_metadata_review"
    metadata_zip = project / resumed["pending_review"]["package_path"]
    assert metadata_zip.is_file()
    with zipfile.ZipFile(metadata_zip) as z:
        assert "editable/reviews/fr/page_metadata_review.json" in z.namelist()
        assert "editable/data/keyword_vocabulary_working.json" in z.namelist()
        assert not any(name.startswith("context/private/") for name in z.namelist())


def test_resume_after_interruption_adopts_existing_graph_draft_but_revalidates(tmp_path: Path, monkeypatch):
    from test_wikidebia_corpus_init import make_extraction
    project = tmp_path / "project"
    project.mkdir()
    source = make_extraction(project / "source")
    build = project / ".state/corpus-builds/debat_test"
    wf.build_corpus(source, build, debate_id="debat_test", short_code="TEST", scope_summary=None, overwrite=False)
    state = {
        "schema": wf.WORKFLOW_SCHEMA, "schema_version": "1.0", "debate_id": "debat_test",
        "debate_title": "Débat test ?", "short_code": "TEST", "phase": "initialize_graph",
        "status": "running", "work_id": None, "pending_review": None,
        "snapshot_path": "source", "force_refresh": False,
        "created_at": "2026-08-11T12:00:00+02:00", "updated_at": "2026-08-11T12:00:00+02:00",
    }
    wf._save_workflow(project, state)
    calls = []
    monkeypatch.setattr(wf, "run_initial_validator", lambda root, package: calls.append(package) or {"status": "passed"})
    resumed = wf.start_workflow(project, "Débat test ?", debate_id="debat_test")
    assert len(calls) == 1
    assert resumed["pending_review"]["review_type"] == "graph_review"


def test_import_refuses_local_edit_outside_handoff(tmp_path: Path):
    project = tmp_path / "project"
    project.mkdir()
    base = make_base(project)
    state = make_state(project, base)
    pending = wf.create_review_package(project, state, review_type="graph_review", base=base, editable_paths=["reviews/edit.json"], context_paths=["data/context.json"])
    common.write_json(base / "reviews/edit.json", {"debate_id": "debat_test", "value": "modified-locally"})
    with pytest.raises(wf.WorkflowError, match="hors réimport"):
        wf.import_review(project, "debat_test", project / pending["package_path"])


def make_full_workspace(project: Path, debate_id: str = "debat_test", work_id: str = "EDIT-20260811-001") -> Path:
    workspace = project / ".state/editorial-workspaces" / debate_id / work_id
    common.write_json(workspace / "workspace.json", {
        "schema": "wikidebia-editorial-workspace-1.0", "schema_version": "1.0",
        "debate_id": debate_id, "work_id": work_id, "status": "audit_ready",
        "workspace_sha256": "0" * 64,
    })
    files = {
        "reviews/fr/page_metadata_review.json": {"items": [{"id": "A0001"}]},
        "data/keyword_vocabulary_working.json": {"entries": []},
        "audits/editorial_inventory.json": {"items": []},
        "tasks/editorial_tasks.json": {"tasks": []},
        "working-copy/scope.json": {"debate_id": debate_id},
        "working-copy/data/registre_debat.json": {"debate_id": debate_id},
        "working-copy/graph/graphe_argumentatif.json": {"debate_id": debate_id},
        "reviews/fr/content_review.json": {"arguments": [{"id": "A0001"}]},
        "data/sources_working.json": {"sources": []},
        "audits/fr_content_inventory.json": {"arguments": []},
        "reviewed-copy/data/fr_page_metadata_lock.json": {"status": "locked"},
        "reviewed-copy/data/registre_debat.json": {"debate_id": debate_id},
        "reviewed-copy/data/sources.json": {"sources": []},
        "reviewed-copy/scope.json": {"debate_id": debate_id},
        "reviews/en/translation_review.json": {"status": "draft", "arguments": [{"id": "A0001"}], "review_units": [{"id": "U1"}]},
        "data/sources_en_working.json": {"sources": []},
        "audits/en_translation_inventory.json": {"arguments": []},
        "content-reviewed-copy/data/fr_page_metadata_lock.json": {"status": "locked"},
        "content-reviewed-copy/data/fr_content_lock.json": {"status": "locked"},
        "content-reviewed-copy/data/registre_debat.json": {"debate_id": debate_id},
        "content-reviewed-copy/data/sources.json": {"sources": []},
        "content-reviewed-copy/data/keyword_vocabulary.json": {"entries": []},
        "reviews/en/translation_readiness.json": {"status": "ready_for_translation"},
    }
    for rel, payload in files.items():
        common.write_json(workspace / rel, payload)
    for rel in (
        "audits/editorial_inventory.md", "audits/fr_content_inventory.md", "audits/en_translation_inventory.md",
    ):
        path = workspace / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("inventory\n", encoding="utf-8")
    return workspace


def returned_semantic_zip(source: Path, target: Path, *, family: str, method: str, errors: int, findings=None):
    def edit(root: Path):
        path = root / "editable/reviews/en/semantic_review_response.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data.update({
            "method_family": family,
            "method": method,
            "reviewer": "Relecteur indépendant",
            "note": "Relecture indépendante complète de la traduction.",
            "new_certain_errors": errors,
            "findings": list(findings or []),
        })
        common.write_json(path, data)
    rewrite_zip(source, target, edit)


def test_full_orchestration_reaches_release_ready_through_all_editorial_stops(tmp_path: Path, monkeypatch):
    project = tmp_path / "project"
    project.mkdir()
    work_id = "EDIT-20260811-001"
    workspace = make_full_workspace(project, work_id=work_id)
    state = {
        "schema": wf.WORKFLOW_SCHEMA, "schema_version": "1.0",
        "normative_revision": wf.NORM_VERSION, "validator_version": wf.VALIDATOR_VERSION, "kit_version": wf.KIT_VERSION,
        "debate_id": "debat_test", "debate_title": "Débat test ?", "short_code": "TEST",
        "phase": "fr_metadata_review", "status": "running", "work_id": work_id,
        "pending_review": None, "snapshot_path": None, "force_refresh": False,
        "created_at": "2026-08-11T12:00:00+02:00", "updated_at": "2026-08-11T12:00:00+02:00",
    }
    wf._save_workflow(project, state)

    monkeypatch.setattr(wf, "prepare_content_review", lambda *a, **k: {"status": "prepared"})
    monkeypatch.setattr(wf, "prepare_translation_review", lambda *a, **k: {"status": "prepared"})
    monkeypatch.setattr(wf, "finalize_metadata_review", lambda *a, **k: {"review_sha256": "1" * 64})
    monkeypatch.setattr(wf, "apply_metadata_review", lambda *a, **k: {"status": "applied"})
    monkeypatch.setattr(wf, "finalize_content_review", lambda *a, **k: {"review_sha256": "2" * 64})
    monkeypatch.setattr(wf, "apply_content_review", lambda *a, **k: {"status": "applied"})

    def finalize_translation(*args, **kwargs):
        review = common.load_json(workspace / "reviews/en/translation_review.json", "translation")
        review["status"] = "approved"
        review["review_sha256"] = "3" * 64
        review["semantic_content_sha256"] = "4" * 64
        common.write_json(workspace / "reviews/en/translation_review.json", review)
        return {"review_sha256": "3" * 64}
    monkeypatch.setattr(wf, "finalize_translation_review", finalize_translation)

    pass_calls = []
    def semantic_pass(*args, **kwargs):
        pass_calls.append(kwargs["method_family"])
        pass_no = len(pass_calls)
        status = "converged" if pass_no == 2 else "in_progress"
        common.write_json(workspace / "reviews/en/semantic_convergence_review.json", {
            "schema": "wikidebia-semantic-convergence-review-1.1", "schema_version": "1.1",
            "status": status, "passes": [{"pass_id": f"P{pass_no:03d}"}], "receipt_sha256": "5" * 64,
        })
        return {"status": status, "receipt_sha256": "5" * 64}
    monkeypatch.setattr(wf, "record_semantic_pass", semantic_pass)
    calls = []
    monkeypatch.setattr(wf, "apply_translation_review", lambda *a, **k: calls.append("apply") or {"status": "applied"})
    monkeypatch.setattr(wf, "render_workspace", lambda *a, **k: calls.append("render") or {"rendered_copy_tree_sha256": "6" * 64})
    monkeypatch.setattr(wf, "release_workspace", lambda *a, **k: calls.append("release") or {"archive": "outgoing/debat_test_release.zip", "status": "release_ready"})

    # Metadata stop.
    state = wf._mechanical_advance(project, state)
    assert state["pending_review"]["review_type"] == "fr_metadata_review"
    metadata_zip = project / state["pending_review"]["package_path"]
    state = wf.import_review(project, "debat_test", metadata_zip)
    assert state["pending_review"]["review_type"] == "fr_content_review"

    # French content stop.
    content_zip = project / state["pending_review"]["package_path"]
    state = wf.import_review(project, "debat_test", content_zip)
    assert state["pending_review"]["review_type"] == "en_translation_review"

    # English translation stop.
    translation_zip = project / state["pending_review"]["package_path"]
    state = wf.import_review(project, "debat_test", translation_zip)
    assert state["pending_review"]["review_type"] == "semantic_convergence_1"

    # First independent semantic pass.
    sem1 = project / state["pending_review"]["package_path"]
    sem1_return = tmp_path / "semantic-pass-1.zip"
    returned_semantic_zip(sem1, sem1_return, family="proposition_by_proposition", method="Comparaison proposition par proposition", errors=0)
    state = wf.import_review(project, "debat_test", sem1_return)
    assert state["pending_review"]["review_type"] == "semantic_convergence_2"

    # Second distinct semantic pass triggers all remaining mechanics.
    sem2 = project / state["pending_review"]["package_path"]
    sem2_return = tmp_path / "semantic-pass-2.zip"
    returned_semantic_zip(sem2, sem2_return, family="risk_marker_review", method="Relecture des marqueurs de risque", errors=0)
    state = wf.import_review(project, "debat_test", sem2_return)
    assert state["status"] == "release_ready"
    assert state["phase"] == "release_ready"
    assert pass_calls == ["proposition_by_proposition", "risk_marker_review"]
    assert calls == ["apply", "render", "release"]
    assert state["release"]["archive"] == "outgoing/debat_test_release.zip"


def test_semantic_error_reopens_translation_and_restarts_two_pass_cycle(tmp_path: Path, monkeypatch):
    project = tmp_path / "project"
    project.mkdir()
    work_id = "EDIT-20260811-001"
    workspace = make_full_workspace(project, work_id=work_id)
    review = common.load_json(workspace / "reviews/en/translation_review.json", "translation")
    review.update({"status": "approved", "review_sha256": "3" * 64, "semantic_content_sha256": "4" * 64, "finalized_at": "2026-08-11"})
    common.write_json(workspace / "reviews/en/translation_review.json", review)
    state = {
        "schema": wf.WORKFLOW_SCHEMA, "schema_version": "1.0",
        "normative_revision": wf.NORM_VERSION, "validator_version": wf.VALIDATOR_VERSION, "kit_version": wf.KIT_VERSION,
        "debate_id": "debat_test", "debate_title": "Débat test ?", "short_code": "TEST",
        "phase": "semantic_convergence_1", "status": "running", "work_id": work_id,
        "pending_review": None, "snapshot_path": None, "force_refresh": False,
        "created_at": "2026-08-11T12:00:00+02:00", "updated_at": "2026-08-11T12:00:00+02:00",
    }
    wf._save_workflow(project, state)
    monkeypatch.setattr(wf, "record_semantic_pass", lambda *a, **k: {"status": "requires_revision"})
    monkeypatch.setattr(wf, "prepare_translation_review", lambda *a, **k: {"status": "prepared"})

    state = wf._mechanical_advance(project, state)
    first = project / state["pending_review"]["package_path"]
    returned = tmp_path / "semantic-with-error.zip"
    returned_semantic_zip(first, returned, family="field_boundary_review", method="Relecture des frontières de champs", errors=1, findings=[{"field": "summary", "issue": "Perte de modalité"}])
    state = wf.import_review(project, "debat_test", returned)
    assert state["pending_review"]["review_type"] == "en_translation_correction"
    correction_zip = project / state["pending_review"]["package_path"]
    with zipfile.ZipFile(correction_zip) as z:
        assert "context/reviews/en/semantic_convergence_findings.json" in z.namelist()
        findings = json.loads(z.read("context/reviews/en/semantic_convergence_findings.json"))
        assert findings["new_certain_errors"] == 1
    reopened = common.load_json(workspace / "reviews/en/translation_review.json", "translation")
    assert reopened["status"] == "draft"
    assert "review_sha256" not in reopened
    assert not (workspace / "reviews/en/semantic_convergence_review.json").exists()

    def finalize_translation(*args, **kwargs):
        fixed = common.load_json(workspace / "reviews/en/translation_review.json", "translation")
        fixed.update({"status": "approved", "review_sha256": "7" * 64, "semantic_content_sha256": "8" * 64})
        common.write_json(workspace / "reviews/en/translation_review.json", fixed)
        return {"review_sha256": "7" * 64}
    monkeypatch.setattr(wf, "finalize_translation_review", finalize_translation)
    state = wf.import_review(project, "debat_test", correction_zip)
    assert state["pending_review"]["review_type"] == "semantic_convergence_1"


def test_resume_after_promotion_interruption_reuses_promoted_corpus_and_preallocated_work_id(tmp_path: Path, monkeypatch):
    project = tmp_path / "project"
    project.mkdir()
    corpus = project / "corpus/debat_test"
    common.write_json(corpus / wf.REVIEW_ENVELOPE, {"review_sha256": "a" * 64})
    state = {
        "schema": wf.WORKFLOW_SCHEMA, "schema_version": "1.0",
        "normative_revision": wf.NORM_VERSION, "validator_version": wf.VALIDATOR_VERSION, "kit_version": wf.KIT_VERSION,
        "debate_id": "debat_test", "debate_title": "Débat test ?", "short_code": "TEST",
        "phase": "promote_and_workspace", "status": "running", "work_id": None,
        "pending_review": None, "snapshot_path": None, "force_refresh": False,
        "created_at": "2026-08-11T12:00:00+02:00", "updated_at": "2026-08-11T12:00:00+02:00",
    }
    wf._save_workflow(project, state)
    monkeypatch.setattr(wf, "graph_review_sha256", lambda review: "a" * 64)
    created = []
    def create_ws(root, debate_id, work_id):
        created.append(work_id)
        common.write_json(root / ".state/editorial-workspaces" / debate_id / work_id / "workspace.json", {"debate_id": debate_id, "work_id": work_id})
        return {"work_id": work_id}
    monkeypatch.setattr(wf, "create_workspace", create_ws)
    monkeypatch.setattr(wf, "_prepare_metadata_package", lambda root, s: s)
    result = wf._mechanical_advance(project, state)
    assert created and created[0].startswith("EDIT-")
    persisted = wf._load_workflow(project, "debat_test")
    assert persisted["work_id"] == created[0]
    assert result["phase"] == "fr_metadata_review"


def test_outgoing_is_private_for_git_and_root_template():
    assert manage.forbidden_git_path("outgoing/revenu_de_base_graph_review.zip")
    assert "/outgoing/" in manage.REQUIRED_GITIGNORE_RULES
    template = (Path(__file__).resolve().parents[1] / "root_template/.gitignore").read_text(encoding="utf-8")
    assert "/outgoing/" in {line.strip() for line in template.splitlines()}


def test_review_registry_covers_every_orchestrated_external_stop():
    assert set(wf.REVIEW_TYPES) == {
        "graph_review", "fr_metadata_review", "fr_content_review", "en_translation_review",
        "en_translation_correction", "semantic_convergence_1", "semantic_convergence_2",
    }
