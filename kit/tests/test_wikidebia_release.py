from __future__ import annotations

import importlib.util
import json
import sys
import zipfile
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


release = load_module("wikidebia_release")
render = sys.modules.get("wikidebia_render") or load_module("wikidebia_render")
common = sys.modules["wikidebia_corpus_build"]
from test_wikidebia_render import make_translated  # noqa: E402


def writing_validator(project_root, package_root, *, scopes, json_output, text_output):
    report = {
        "validator_version": "0.4.29",
        "result": "passed",
        "summary": {"errors": 0, "warnings": 0},
        "scopes": list(scopes),
    }
    json_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    text_output.write_text("Validation réussie.\n", encoding="utf-8")
    return report


render._run_validator = writing_validator
release._run_validator = writing_validator


def make_rendered(tmp_path: Path):
    project, workspace, work_id, translation_sha = make_translated(tmp_path)
    render_result = render.render_workspace(project, "debat_test", work_id, translation_sha)
    return project, workspace, work_id, render_result["rendered_copy_tree_sha256"]


def test_release_creates_installable_archive_and_exact_manifest(tmp_path: Path):
    project, workspace, work_id, render_sha = make_rendered(tmp_path)
    rendered_before = common.full_tree_sha256(workspace / "rendered-copy")
    result = release.release_workspace(project, "debat_test", work_id, render_sha)
    target = workspace / "release-copy"
    archive = project / result["archive"]
    assert result["status"] == "release_ready"
    assert result["remote_access"] is False
    assert result["publication_started"] is False
    assert common.full_tree_sha256(workspace / "rendered-copy") == rendered_before
    assert target.is_dir() and archive.is_file()

    manifest = json.loads((target / "manifest.json").read_text(encoding="utf-8"))
    release_manifest = json.loads((target / "release/release_manifest.json").read_text(encoding="utf-8"))
    remote_input = json.loads((target / "release/remote_comparison_input.json").read_text(encoding="utf-8"))
    assert manifest["global_status"] == "release_ready"
    assert manifest["publication_gate"]["remote_write_authorized"] is False
    assert remote_input["page_count"] == len(manifest["pages"])
    assert remote_input["remote_access_performed"] is False
    assert remote_input["plan_created"] is False

    excluded = {"release/release_manifest.json"}
    actual = {
        path.relative_to(target).as_posix()
        for path in target.rglob("*") if path.is_file() and path.relative_to(target).as_posix() not in excluded
    }
    declared = {row["path"] for row in release_manifest["files"]}
    assert declared == actual
    assert "release/release_manifest.json" not in declared

    extracted = tmp_path / "unzipped"
    with zipfile.ZipFile(archive) as bundle:
        bundle.extractall(extracted)
    assert common.full_tree_sha256(extracted) == common.full_tree_sha256(target)
    assert (extracted / "manifest.json").is_file()


def test_release_requires_exact_render_hash(tmp_path: Path):
    project, workspace, work_id, _ = make_rendered(tmp_path)
    try:
        release.release_workspace(project, "debat_test", work_id, "0" * 64)
    except release.ReleaseError as exc:
        assert "empreinte confirmée" in str(exc)
    else:
        raise AssertionError("Une empreinte de rendu erronée a été acceptée")
    assert not (workspace / "release-copy").exists()


def test_release_is_idempotent_and_receipt_is_bound_to_archive(tmp_path: Path):
    project, workspace, work_id, render_sha = make_rendered(tmp_path)
    first = release.release_workspace(project, "debat_test", work_id, render_sha)
    second = release.release_workspace(project, "debat_test", work_id, render_sha)
    assert second["idempotent"] is True
    assert second["archive_sha256"] == first["archive_sha256"]
    receipt_path = project / ".state/corpus-releases/debat_test" / work_id / "release-receipt.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    archive = receipt_path.parent / receipt["archive_name"]
    assert common.sha256_file(archive) == receipt["archive_sha256"]
    assert release._canonical_sha(receipt, "receipt_sha256") == receipt["receipt_sha256"]


def test_release_refuses_partial_existing_state(tmp_path: Path):
    project, workspace, work_id, render_sha = make_rendered(tmp_path)
    (workspace / "release-copy").mkdir()
    try:
        release.release_workspace(project, "debat_test", work_id, render_sha)
    except release.ReleaseError as exc:
        assert "partiel" in str(exc) or "occupé" in str(exc)
    else:
        raise AssertionError("Un état partiel a été accepté")
