#!/usr/bin/env python3
"""Finalize a rendered workspace as an installable, locally sealed corpus.

The command consumes ``rendered-copy/`` only after the bilingual renderer has
validated it.  It creates an immutable ``release-copy/`` and a deterministic
ZIP under ``.state/corpus-releases/``.  The package is marked ``release_ready``
for local use, while remote writes remain explicitly unauthorized.  No wiki
connection, comparison, plan construction or publication is performed.
"""

from __future__ import annotations

import argparse
import copy
import datetime as dt
import hashlib
import json
import os
import shutil
import tempfile
import zipfile
from pathlib import Path
from typing import Any, Mapping, Sequence

from wikidebia_corpus_build import (
    NORM_VERSION,
    VALIDATOR_VERSION,
    CorpusBuildError,
    assert_control_directory,
    assert_no_symlinks,
    exclusive_lock,
    full_tree_sha256,
    load_json,
    now_iso,
    relative_to_project,
    sha256_file,
    structural_sha256,
    validate_debate_id,
    write_json,
)
from wikidebia_editorial_review import EditorialReviewError, _assert_source_unchanged, _run_validator
from wikidebia_editorial_workspace import WorkspaceError, fsync_directory, validate_work_id, workspace_receipt_hash
from wikidebia_render import RenderError, _load_workspace

KIT_VERSION = "2.15.43"
RELEASE_MANIFEST_SCHEMA = "1.0"
RELEASE_RECEIPT_SCHEMA = "wikidebia-local-release-receipt-1.0"
REMOTE_INPUT_SCHEMA = "wikidebia-remote-comparison-input-1.0"


class ReleaseError(WorkspaceError):
    pass


def _canonical_sha(value: Mapping[str, Any], excluded: str) -> str:
    body = dict(value)
    body.pop(excluded, None)
    payload = json.dumps(body, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _release_state_parent(project_root: Path, debate_id: str) -> Path:
    state = assert_control_directory(project_root / ".state", project_root, create=True)
    releases = assert_control_directory(state / "corpus-releases", project_root, create=True)
    return assert_control_directory(releases / validate_debate_id(debate_id), project_root, create=True)


def _assert_rendered_copy(workspace: Path, meta: Mapping[str, Any], confirmed: str) -> Path:
    if meta.get("status") not in {"bilingual_rendered", "release_ready"}:
        raise ReleaseError(f"Statut incompatible avec la libération locale : {meta.get('status')}")
    path = workspace / "rendered-copy"
    if not path.is_dir() or path.is_symlink():
        raise ReleaseError("rendered-copy absent ou non sûr")
    assert_no_symlinks(path)
    expected = str((meta.get("rendered_copy") or {}).get("tree_sha256") or "")
    actual = full_tree_sha256(path)
    if not expected or actual != expected:
        raise ReleaseError("rendered-copy a changé depuis le rendu")
    if confirmed != expected:
        raise ReleaseError("L’empreinte confirmée ne correspond pas à rendered-copy")
    render_lock = load_json(path / "data/bilingual_render_lock.json", "verrou de rendu")
    if render_lock.get("status") != "rendered_and_validated":
        raise ReleaseError("Le verrou de rendu n’atteste pas un rendu validé")
    manifest = load_json(path / "manifest.json", "manifest du rendu")
    if manifest.get("global_status") != "bilingual_validated":
        raise ReleaseError("Le rendu source n’est pas bilingual_validated")
    final_report = load_json(path / "reports/final_validation.json", "validation finale du rendu")
    if final_report.get("result") not in {"passed", "passed_with_warnings"}:
        raise ReleaseError("La validation finale du rendu n’est pas réussie")
    return path


def _next_validation_id(manifest: Mapping[str, Any], timestamp: str) -> str:
    used = {str(row.get("id")) for row in manifest.get("validations") or []}
    prefix = f"V{timestamp[:10].replace('-', '')}-"
    index = 1
    while f"{prefix}{index:03d}" in used:
        index += 1
    return f"{prefix}{index:03d}"


def _remote_input(target: Path, manifest: Mapping[str, Any], timestamp: str) -> dict[str, Any]:
    pages = []
    for page in manifest.get("pages") or []:
        pages.append({
            "page_id": page.get("page_id"),
            "language": page.get("language"),
            "page_type": page.get("page_type"),
            "canonical_title": page.get("canonical_title"),
            "file_path": page.get("file_path"),
            "content_sha256": page.get("sha256"),
            "local_status": "candidate",
        })
    pages.sort(key=lambda row: (str(row["language"]), str(row["page_type"]), str(row["page_id"])))
    value = {
        "schema": REMOTE_INPUT_SCHEMA,
        "schema_version": "1.0",
        "debate_id": manifest.get("debate_id"),
        "created_at": timestamp,
        "source_global_status": "release_ready",
        "page_count": len(pages),
        "pages": pages,
        "published_state_required": True,
        "remote_inventory_required": True,
        "remote_access_performed": False,
        "plan_created": False,
        "publication_started": False,
    }
    write_json(target / "release/remote_comparison_input.json", value)
    return value


def _inventory(root: Path, excluded: set[str]) -> list[dict[str, Any]]:
    rows = []
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        rel = path.relative_to(root).as_posix()
        if rel in excluded:
            continue
        rows.append({"path": rel, "size_bytes": path.stat().st_size, "sha256": sha256_file(path)})
    return rows


def _verify_inventory(root: Path, release_manifest: Mapping[str, Any], excluded: set[str]) -> None:
    declared = {str(row["path"]): row for row in release_manifest.get("files") or []}
    actual_paths = {
        path.relative_to(root).as_posix()
        for path in root.rglob("*") if path.is_file() and path.relative_to(root).as_posix() not in excluded
    }
    if set(declared) != actual_paths:
        raise ReleaseError("L’inventaire de libération n’est pas exhaustif")
    for rel, row in declared.items():
        path = root / rel
        if path.stat().st_size != row.get("size_bytes") or sha256_file(path) != row.get("sha256"):
            raise ReleaseError(f"Inventaire divergent pour {rel}")


def _zip_timestamp(timestamp: str) -> tuple[int, int, int, int, int, int]:
    value = dt.datetime.fromisoformat(timestamp)
    year = min(max(value.year, 1980), 2107)
    return (year, value.month, value.day, value.hour, value.minute, value.second - value.second % 2)


def _write_deterministic_zip(source: Path, archive: Path, timestamp: str) -> None:
    stamp = _zip_timestamp(timestamp)
    archive.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
        for path in sorted(item for item in source.rglob("*") if item.is_file()):
            rel = path.relative_to(source).as_posix()
            info = zipfile.ZipInfo(rel, date_time=stamp)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            info.create_system = 3
            bundle.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def _build_release_copy(project_root: Path, source: Path, target: Path, *, debate_id: str, work_id: str) -> dict[str, Any]:
    shutil.copytree(source, target)
    assert_no_symlinks(target)
    timestamp = now_iso()
    manifest_path = target / "manifest.json"
    manifest = load_json(manifest_path, "manifest de rendu")
    registry = load_json(target / "data/registre_debat.json", "registre maître")
    structural = structural_sha256(registry)
    gate = {
        "local_release_status": "release_ready",
        "remote_write_authorized": False,
        "remote_template_compatibility": "not_checked",
        "blocking_reason": "Le préflight distant, la comparaison avec l’état publié et le test canonique n’ont pas encore été exécutés.",
        "checked_at": timestamp,
    }
    manifest["global_status"] = "release_ready"
    manifest["updated_at"] = timestamp
    manifest["normative_versions"].update({"consolidated_norm": NORM_VERSION, "validator": VALIDATOR_VERSION})
    manifest["publication_gate"] = copy.deepcopy(gate)
    manifest["release"] = {
        "release_manifest_path": "release/release_manifest.json",
        "release_zip_path": None,
        "released_at": None,
        "archived_at": None,
        "release_receipt_path": None,
    }
    manifest.setdefault("validations", []).append({
        "id": _next_validation_id(manifest, timestamp),
        "scope": "interlanguage",
        "language": None,
        "validator_version": VALIDATOR_VERSION,
        "executed_at": timestamp,
        "input_sha256": structural,
        "result": "passed",
        "blocking_errors": 0,
        "warnings": 0,
        "report_path": "reports/release_validation.json",
    })
    release_work_id = f"{work_id}-RELEASE"
    if not any(row.get("work_id") == release_work_id for row in manifest.get("works") or []):
        manifest.setdefault("works", []).append({
            "work_id": release_work_id,
            "work_type": "corrective_prepublication",
            "conversation_name": "Scellement local du corpus installable",
            "status": "completed",
            "input_handoff": None,
            "output_handoff": None,
            "started_at": timestamp,
            "completed_at": timestamp,
        })
    write_json(manifest_path, manifest)
    write_json(target / "logs/publication/not_started.json", {
        "schema": "wikidebia-publication-log-1.0",
        "debate_id": debate_id,
        "created_at": timestamp,
        "status": "not_started",
        "remote_access": False,
        "remote_write_authorized": False,
        "reason": gate["blocking_reason"],
    })
    remote_input = _remote_input(target, manifest, timestamp)
    write_json(target / "reports/release_validation.json", {"status": "pending"})
    internal_validation = _run_validator(
        project_root, target, scopes=("all",),
        json_output=target / "reports/release_validation.json",
        text_output=target / "reports/release_validation.txt",
    )
    if internal_validation.get("result") not in {"passed", "passed_with_warnings"}:
        raise ReleaseError("La validation locale du corpus release_ready a échoué")
    write_json(target / "reports/release_report.json", {
        "schema": "wikidebia-local-release-report-1.0",
        "debate_id": debate_id,
        "work_id": work_id,
        "created_at": timestamp,
        "result": "passed",
        "page_count": len(manifest.get("pages") or []),
        "remote_comparison_input": "release/remote_comparison_input.json",
        "remote_access": False,
        "publication_started": False,
    })
    release_rel = "release/release_manifest.json"
    excluded = {release_rel}
    files = _inventory(target, excluded)
    validation_reports = sorted({
        str(row.get("report_path")) for row in manifest.get("validations") or []
        if isinstance(row.get("report_path"), str) and (target / str(row.get("report_path"))).is_file()
    } | {"reports/release_report.json"})
    release_manifest = {
        "release_manifest_version": RELEASE_MANIFEST_SCHEMA,
        "debate_id": debate_id,
        "created_at": timestamp,
        "normative_versions": copy.deepcopy(manifest.get("normative_versions")),
        "global_status": "release_ready",
        "structural_sha256": structural,
        "files": files,
        "validation_reports": validation_reports,
        "publication_logs": ["logs/publication/not_started.json"],
        "finalized_at": timestamp,
        "self_excluded": True,
        "publication_gate": copy.deepcopy(gate),
        "counts": {
            "files": len(files),
            "pages": len(manifest.get("pages") or []),
            "french_pages": sum(1 for row in manifest.get("pages") or [] if row.get("language") == "fr"),
            "english_pages": sum(1 for row in manifest.get("pages") or [] if row.get("language") == "en"),
            "remote_candidates": remote_input["page_count"],
        },
    }
    write_json(target / release_rel, release_manifest)
    _verify_inventory(target, release_manifest, excluded)
    return {
        "timestamp": timestamp,
        "release_manifest": release_manifest,
        "release_manifest_sha256": sha256_file(target / release_rel),
        "internal_validation": internal_validation,
    }


def release_workspace(project_root: Path, debate_id: str, work_id: str, confirm_render_sha256: str) -> dict[str, Any]:
    workspace, meta = _load_workspace(project_root, debate_id, work_id)
    _assert_source_unchanged(project_root, debate_id, meta)
    source = _assert_rendered_copy(workspace, meta, confirm_render_sha256)
    target = workspace / "release-copy"
    release_parent = _release_state_parent(project_root, debate_id)
    artifact_target = release_parent / work_id
    if target.is_dir() or artifact_target.is_dir():
        if meta.get("status") != "release_ready" or not target.is_dir() or not artifact_target.is_dir():
            raise ReleaseError("État partiel ou incohérent d’une libération précédente")
        expected_tree = str((meta.get("release_copy") or {}).get("tree_sha256") or "")
        expected_archive = str((meta.get("local_release") or {}).get("archive_sha256") or "")
        archive = artifact_target / f"{debate_id}.zip"
        if full_tree_sha256(target) != expected_tree or not archive.is_file() or sha256_file(archive) != expected_archive:
            raise ReleaseError("La libération existante a été altérée")
        return {
            "status": "release_ready", "debate_id": debate_id, "work_id": work_id,
            "release_copy_tree_sha256": expected_tree,
            "archive": relative_to_project(archive, project_root),
            "archive_sha256": expected_archive,
            "idempotent": True,
        }
    if target.exists() or target.is_symlink() or artifact_target.exists() or artifact_target.is_symlink():
        raise ReleaseError("Chemin de libération déjà occupé")

    temp_copy = Path(tempfile.mkdtemp(prefix=".release-copy.tmp-", dir=workspace))
    temp_artifact = Path(tempfile.mkdtemp(prefix=f".{work_id}.tmp-", dir=release_parent))
    installed_artifact = False
    try:
        shutil.rmtree(temp_copy)
        built = _build_release_copy(project_root, source, temp_copy, debate_id=debate_id, work_id=work_id)
        tree_hash = full_tree_sha256(temp_copy)
        external_json = temp_artifact / "postrelease-validation.json"
        external_txt = temp_artifact / "postrelease-validation.txt"
        final_validation = _run_validator(
            project_root, temp_copy, scopes=("all",), json_output=external_json, text_output=external_txt,
        )
        if final_validation.get("result") not in {"passed", "passed_with_warnings"}:
            raise ReleaseError("La validation externe du paquet final a échoué")
        archive = temp_artifact / f"{debate_id}.zip"
        _write_deterministic_zip(temp_copy, archive, built["timestamp"])
        archive_sha = sha256_file(archive)
        receipt = {
            "schema": RELEASE_RECEIPT_SCHEMA,
            "schema_version": "1.0",
            "debate_id": debate_id,
            "work_id": work_id,
            "created_at": built["timestamp"],
            "normative_revision": NORM_VERSION,
            "validator_version": VALIDATOR_VERSION,
            "kit_version": KIT_VERSION,
            "status": "release_ready",
            "release_copy_tree_sha256": tree_hash,
            "release_manifest_sha256": built["release_manifest_sha256"],
            "archive_name": archive.name,
            "archive_sha256": archive_sha,
            "archive_size_bytes": archive.stat().st_size,
            "postrelease_validation_result": final_validation.get("result"),
            "postrelease_validation_sha256": sha256_file(external_json),
            "remote_access": False,
            "publication_started": False,
        }
        receipt["receipt_sha256"] = _canonical_sha(receipt, "receipt_sha256")
        write_json(temp_artifact / "release-receipt.json", receipt)
        os.replace(temp_artifact, artifact_target)
        installed_artifact = True
        fsync_directory(release_parent)
        os.replace(temp_copy, target)
        fsync_directory(workspace)
    except Exception:
        shutil.rmtree(temp_copy, ignore_errors=True)
        shutil.rmtree(temp_artifact, ignore_errors=True)
        if installed_artifact:
            shutil.rmtree(artifact_target, ignore_errors=True)
        raise

    meta = copy.deepcopy(meta)
    meta.update({
        "normative_revision": NORM_VERSION,
        "validator_version": VALIDATOR_VERSION,
        "kit_version": KIT_VERSION,
        "status": "release_ready",
    })
    meta.setdefault("artifacts", {})["release_copy"] = "release-copy"
    meta["release_copy"] = {
        "path": "release-copy",
        "tree_sha256": tree_hash,
        "status": "release_ready",
        "rendered_copy_sha256": confirm_render_sha256,
        "released_at": built["timestamp"],
    }
    final_archive = artifact_target / f"{debate_id}.zip"
    meta["local_release"] = {
        "path": relative_to_project(artifact_target, project_root),
        "archive": relative_to_project(final_archive, project_root),
        "archive_sha256": archive_sha,
        "receipt": relative_to_project(artifact_target / "release-receipt.json", project_root),
        "remote_comparison_prepared": True,
    }
    meta.setdefault("boundaries", {}).update({
        "final_pages_generated": True,
        "corpus_release_packaged": True,
        "remote_comparison_prepared": True,
        "remote_access": False,
        "publication_started": False,
    })
    meta["workspace_sha256"] = None
    meta["workspace_sha256"] = workspace_receipt_hash(meta)
    write_json(workspace / "workspace.json", meta)
    return {
        "status": "release_ready",
        "debate_id": debate_id,
        "work_id": work_id,
        "release_copy": relative_to_project(target, project_root),
        "release_copy_tree_sha256": tree_hash,
        "archive": relative_to_project(final_archive, project_root),
        "archive_sha256": archive_sha,
        "release_manifest_sha256": built["release_manifest_sha256"],
        "remote_comparison_prepared": True,
        "remote_access": False,
        "publication_started": False,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Sceller un rendu bilingue en corpus local installable.")
    parser.add_argument("debate_id")
    parser.add_argument("--work-id", required=True)
    parser.add_argument("--confirm-render-sha256", required=True)
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--machine-readable", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    project_root = args.project_root.expanduser().resolve()
    debate_id = validate_debate_id(args.debate_id)
    work_id = validate_work_id(args.work_id)
    with exclusive_lock(project_root, "editorial_local_release"):
        result = release_workspace(project_root, debate_id, work_id, str(args.confirm_render_sha256))
    print(json.dumps(result, ensure_ascii=False, sort_keys=True) if args.machine_readable else json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ReleaseError, RenderError, EditorialReviewError, WorkspaceError, CorpusBuildError) as exc:
        print(f"WIKIDEBIA BLOQUÉ : {exc}", file=__import__("sys").stderr)
        raise SystemExit(2)
