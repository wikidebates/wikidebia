#!/usr/bin/env python3
"""High-level orchestration for editorial workflows with ChatGPT review handoffs.

The low-level commands remain authoritative primitives. This module only chains
mechanical transitions, creates minimal review packages, validates their return,
and stops at genuine editorial decision points.
"""
from __future__ import annotations

import argparse
import copy
import datetime as dt
import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import uuid
import zipfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Iterable, Mapping, Sequence

from wikidebia_release_info import KIT_VERSION, NORM_VERSION, VALIDATOR_VERSION
from wikidebia_corpus_build import (
    REVIEW_ENVELOPE,
    PLACEMENT_REVIEW,
    GRAPH_CORRECTION_REVIEW,
    build_payload_sha256,
    full_tree_sha256,
    load_json,
    now_iso,
    resolve_build,
    review_sha256 as graph_review_sha256,
    validate_debate_id,
    write_json,
)
from wikidebia_corpus_init import (
    build_corpus, canonical_debate_id, derive_short_code, validate_short_code,
    run_validator as run_initial_validator,
)
from wikidebia_corpus_review import make_review_template, finalize_review as finalize_graph_review
from wikidebia_graph_correction import make_correction_template as make_graph_correction_template, apply_correction as apply_graph_correction
from wikidebia_graph_actions import execute_review_actions as execute_graph_review_actions
from wikidebia_corpus_promote import promote as promote_graph
from wikidebia_editorial_workspace import create_workspace, validate_work_id, workspace_receipt_hash, next_work_id
from wikidebia_editorial_review import (
    finalize_review as finalize_metadata_review,
    apply_review as apply_metadata_review,
    review_sha256 as metadata_review_sha256,
)
from wikidebia_content_review import (
    prepare_review as prepare_content_review,
    finalize_review as finalize_content_review,
    apply_review as apply_content_review,
    content_review_sha256,
)
from wikidebia_translation_review import (
    prepare_review as prepare_translation_review,
    finalize_review as finalize_translation_review,
    apply_review as apply_translation_review,
    translation_review_sha256,
)
from wikidebia_semantic_convergence import record_pass as record_semantic_pass
from wikidebia_render import render_workspace
from wikidebia_release import release_workspace

PACKAGE_SCHEMA = "wikidebia-chatgpt-review-package-1.0"
WORKFLOW_SCHEMA = "wikidebia-editorial-orchestration-1.0"
SEMANTIC_RESPONSE_SCHEMA = "wikidebia-semantic-review-response-1.0"
DIAGNOSTIC_SCHEMA = "wikidebia-workflow-diagnostic-package-1.0"
ALLOWED_METHOD_FAMILIES = {
    "proposition_by_proposition",
    "risk_marker_review",
    "reverse_source_target",
    "field_boundary_review",
    "independent_bilingual_reread",
}


@dataclass(frozen=True)
class ReviewTypeSpec:
    key: str
    label: str
    user_message: str


REVIEW_TYPES: dict[str, ReviewTypeSpec] = {
    "graph_review": ReviewTypeSpec("graph_review", "Revue du graphe et des placements", "Revue du graphe préparée."),
    "graph_correction": ReviewTypeSpec("graph_correction", "Correction du graphe après rejet", "Correction du graphe préparée."),
    "fr_metadata_review": ReviewTypeSpec("fr_metadata_review", "Revue des titres, rubriques et mots-clés français", "Revue des titres, rubriques et mots-clés préparée."),
    "fr_content_review": ReviewTypeSpec("fr_content_review", "Revue du contenu et de la documentation française", "Revue du contenu français préparée."),
    "en_translation_review": ReviewTypeSpec("en_translation_review", "Traduction et revue documentaire anglaises", "Revue de traduction anglaise préparée."),
    "en_translation_correction": ReviewTypeSpec("en_translation_correction", "Correction de traduction après convergence sémantique", "Correction de traduction anglaise préparée."),
    "semantic_convergence_1": ReviewTypeSpec("semantic_convergence_1", "Première passe de convergence sémantique", "Première passe de convergence sémantique préparée."),
    "semantic_convergence_2": ReviewTypeSpec("semantic_convergence_2", "Deuxième passe indépendante de convergence sémantique", "Deuxième passe de convergence sémantique préparée."),
}


class WorkflowError(RuntimeError):
    pass


def _canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _safe_zip_name(name: str) -> bool:
    pure = PurePosixPath(name)
    return not pure.is_absolute() and ".." not in pure.parts and not (len(name) >= 2 and name[1] == ":")


def _assert_regular_file(path: Path, label: str) -> None:
    if not path.is_file() or path.is_symlink():
        raise WorkflowError(f"{label} absent ou non régulier : {path}")


def _workflow_root(project_root: Path, debate_id: str) -> Path:
    return project_root / ".state" / "workflows" / debate_id


def _workflow_path(project_root: Path, debate_id: str) -> Path:
    return _workflow_root(project_root, debate_id) / "workflow.json"


def _load_workflow(project_root: Path, debate_id: str) -> dict[str, Any]:
    path = _workflow_path(project_root, debate_id)
    if not path.is_file():
        raise WorkflowError(f"Workflow introuvable pour {debate_id}")
    data = load_json(path, "workflow")
    if data.get("schema") != WORKFLOW_SCHEMA or data.get("debate_id") != debate_id:
        raise WorkflowError("Identité ou schéma du workflow invalide")
    return data


def _save_workflow(project_root: Path, state: Mapping[str, Any]) -> None:
    path = _workflow_path(project_root, str(state["debate_id"]))
    path.parent.mkdir(parents=True, exist_ok=True)
    write_json(path, dict(state))


def _relative(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def _relative_or_external(path: Path, root: Path) -> str:
    try:
        return _relative(path, root)
    except ValueError:
        return f"external:{path.name}"


def _workspace_path(project_root: Path, debate_id: str, work_id: str) -> Path:
    return project_root / ".state" / "editorial-workspaces" / debate_id / work_id


def _current_workspace_meta(project_root: Path, state: Mapping[str, Any]) -> tuple[Path, dict[str, Any]]:
    work_id = str(state.get("work_id") or "")
    if not work_id:
        raise WorkflowError("Le workflow n'a pas encore de work_id")
    workspace = _workspace_path(project_root, str(state["debate_id"]), work_id)
    meta = load_json(workspace / "workspace.json", "workspace")
    return workspace, meta


def _copy_context_files(base: Path, explicit: Iterable[str], globs: Iterable[str]) -> list[Path]:
    found: dict[str, Path] = {}
    for rel in explicit:
        p = base / rel
        if not p.is_file() or p.is_symlink():
            raise WorkflowError(f"Fichier de contexte requis absent : {rel}")
        found[p.relative_to(base).as_posix()] = p
    for pattern in globs:
        for p in base.glob(pattern):
            if p.is_file() and not p.is_symlink():
                found[p.relative_to(base).as_posix()] = p
    return [found[key] for key in sorted(found)]


def _instructions(review_type: str, debate_id: str, work_id: str | None, editable: Sequence[str]) -> str:
    spec = REVIEW_TYPES.get(review_type)
    lines = [
        f"# {spec.label if spec else review_type}",
        "",
        f"Débat : `{debate_id}`",
    ]
    if work_id:
        lines.append(f"Work : `{work_id}`")
    lines += [
        "",
        "Ce paquet a été préparé par Wikidéb’IA pour une intervention éditoriale externe.",
        "Ne modifiez que les fichiers placés sous `editable/`. Les fichiers sous `context/` sont des sources en lecture seule.",
        "Ne renommez, n'ajoutez et ne supprimez aucun fichier du ZIP.",
        "Le fichier `REVIEW_PACKAGE.json` ne doit jamais être modifié.",
    ]
    if review_type == "graph_review":
        lines += [
            "",
            "Si la revue exige une modification structurelle, renseignez pour l'occurrence concernée l'objet `correction`.",
            "Actions prises en charge : `remove`, `merge_redirect`, `move` et `relation_change`.",
            "Pour `merge_redirect`, indiquez `target_node_id` : la page doublon deviendra `#REDIRECTION [[Titre de destination]]` et son lien sera retiré de la page mère.",
            "Pour `remove`, indiquez `page_disposition=delete` : le lien sera retiré de la page mère avant suppression de la page.",
            "Les résumés MediaWiki doivent être individualisés. Pour un doublon, le résumé de la page mère doit contenir le titre de destination sous la forme `[[Titre de destination]]`.",
            "Une revue rejetée comportant ces décisions pourra être appliquée par `./wikidebia review-import <debate_id> <zip> --execute-graph-actions`.",
            "Après application, Wikidéb’IA reconstruira le graphe et préparera une nouvelle revue complète avant toute promotion.",
        ]
    if review_type == "graph_correction":
        lines += [
            "",
            "Cette phase corrige le graphe après une revue rejetée. Elle ne constitue pas une approbation du graphe.",
            "Modifiez uniquement les placements nécessaires à partir des motifs de rejet présents dans le contexte.",
            "Renseignez le statut `corrected`, le relecteur, la date de revue et les notes dans le fichier de correction.",
            "Après réimport, Wikidéb’IA reconstruira et validera mécaniquement le graphe puis préparera une nouvelle revue complète.",
        ]
    lines += [
        "",
        "## Fichiers à compléter",
        "",
    ]
    lines.extend(f"- `{path}`" for path in editable)
    lines += [
        "",
        "Après la revue, rendez un ZIP conservant exactement la même structure. L'utilisateur lancera `./wikidebia review-import <debate_id> <zip>`.",
        "",
    ]
    return "\n".join(lines)


def _package_manifest_hash(manifest: Mapping[str, Any]) -> str:
    body = copy.deepcopy(dict(manifest))
    body.pop("manifest_sha256", None)
    return _sha256_bytes(_canonical_json(body))


def _write_deterministic_zip(staging: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for p in sorted((x for x in staging.rglob("*") if x.is_file()), key=lambda x: x.relative_to(staging).as_posix()):
            rel = p.relative_to(staging).as_posix()
            info = zipfile.ZipInfo(rel, date_time=(2026, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, p.read_bytes())


def create_review_package(
    project_root: Path,
    state: dict[str, Any],
    *,
    review_type: str,
    base: Path,
    editable_paths: Sequence[str],
    context_paths: Sequence[str],
    context_globs: Sequence[str] = (),
    counts: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    if review_type not in REVIEW_TYPES:
        raise WorkflowError(f"Type de revue non enregistré : {review_type}")
    debate_id = str(state["debate_id"])
    work_id = state.get("work_id")
    pending = state.get("pending_review")
    if isinstance(pending, dict) and pending.get("review_type") == review_type:
        existing = project_root / str(pending.get("package_path") or "")
        if existing.is_file() and _sha256_file(existing) == pending.get("archive_sha256"):
            return dict(pending)
        raise WorkflowError("Le paquet de revue en attente a disparu ou a été altéré")

    editable_abs: list[Path] = []
    for rel in editable_paths:
        p = base / rel
        _assert_regular_file(p, f"Fichier éditable {rel}")
        editable_abs.append(p)
    context_abs = _copy_context_files(base, context_paths, context_globs)
    editable_set = {p.resolve() for p in editable_abs}
    context_abs = [p for p in context_abs if p.resolve() not in editable_set]

    package_id = str(uuid.uuid4())
    outgoing = project_root / "outgoing"
    filename = f"{debate_id}_{review_type}.zip"
    target = outgoing / filename
    staging = Path(tempfile.mkdtemp(prefix=f".{debate_id}-{review_type}-", dir=str(outgoing) if outgoing.is_dir() else None))
    try:
        if staging.parent != outgoing and not outgoing.exists():
            outgoing.mkdir(parents=True, exist_ok=True)
            shutil.rmtree(staging)
            staging = Path(tempfile.mkdtemp(prefix=f".{debate_id}-{review_type}-", dir=outgoing))
        editable_entries = []
        context_entries = []
        for source in editable_abs:
            target_rel = source.relative_to(base).as_posix()
            package_rel = f"editable/{target_rel}"
            dest = staging / package_rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, dest)
            editable_entries.append({
                "package_path": package_rel,
                "target_path": target_rel,
                "sha256_at_prepare": _sha256_file(source),
            })
        for source in context_abs:
            target_rel = source.relative_to(base).as_posix()
            package_rel = f"context/{target_rel}"
            dest = staging / package_rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, dest)
            context_entries.append({
                "package_path": package_rel,
                "target_path": target_rel,
                "sha256": _sha256_file(source),
            })
        source_anchor = full_tree_sha256(base) if base.is_dir() else None
        manifest = {
            "schema": PACKAGE_SCHEMA,
            "schema_version": "1.0",
            "package_id": package_id,
            "review_type": review_type,
            "debate_id": debate_id,
            "work_id": work_id,
            "normative_revision": NORM_VERSION,
            "validator_version": VALIDATOR_VERSION,
            "kit_version": KIT_VERSION,
            "prepared_at": now_iso(),
            "source_anchor_sha256": source_anchor,
            "editable_files": editable_entries,
            "context_files": context_entries,
            "counts": dict(counts or {}),
            "manifest_sha256": None,
        }
        instructions = _instructions(review_type, debate_id, str(work_id) if work_id else None, [x["package_path"] for x in editable_entries])
        manifest["instructions_sha256"] = _sha256_bytes(instructions.encode("utf-8"))
        manifest["manifest_sha256"] = _package_manifest_hash(manifest)
        write_json(staging / "REVIEW_PACKAGE.json", manifest)
        (staging / "INSTRUCTIONS.md").write_text(instructions, encoding="utf-8", newline="\n")
        _write_deterministic_zip(staging, target)
    finally:
        shutil.rmtree(staging, ignore_errors=True)

    pending_record = {
        "package_id": package_id,
        "review_type": review_type,
        "package_path": _relative(target, project_root),
        "archive_sha256": _sha256_file(target),
        "manifest_sha256": manifest["manifest_sha256"],
        "base_path": _relative(base, project_root),
        "work_id": work_id,
        "created_at": manifest["prepared_at"],
        "counts": dict(counts or {}),
    }
    state["status"] = "awaiting_review"
    state["pending_review"] = pending_record
    state["updated_at"] = now_iso()
    _save_workflow(project_root, state)
    return pending_record


def _read_returned_package(archive: Path) -> tuple[dict[str, Any], dict[str, bytes]]:
    if not archive.is_file():
        raise WorkflowError(f"ZIP de revue introuvable : {archive}")
    files: dict[str, bytes] = {}
    try:
        with zipfile.ZipFile(archive) as bundle:
            seen: set[str] = set()
            for info in bundle.infolist():
                name = PurePosixPath(info.filename).as_posix()
                if not _safe_zip_name(name) or name in seen:
                    raise WorkflowError(f"Entrée ZIP dangereuse ou dupliquée : {info.filename}")
                seen.add(name)
                mode = (info.external_attr >> 16) & 0o170000
                if mode == stat.S_IFLNK:
                    raise WorkflowError(f"Lien symbolique interdit dans le ZIP : {name}")
                if info.is_dir():
                    continue
                files[name] = bundle.read(info)
    except zipfile.BadZipFile as exc:
        raise WorkflowError("Archive de revue invalide") from exc
    if "REVIEW_PACKAGE.json" not in files or "INSTRUCTIONS.md" not in files:
        raise WorkflowError("Le ZIP ne contient pas le manifeste de revue attendu")
    try:
        manifest = json.loads(files["REVIEW_PACKAGE.json"].decode("utf-8"))
    except Exception as exc:
        raise WorkflowError("REVIEW_PACKAGE.json est illisible") from exc
    if not isinstance(manifest, dict) or manifest.get("schema") != PACKAGE_SCHEMA or manifest.get("schema_version") != "1.0":
        raise WorkflowError("Schéma de paquet de revue non pris en charge")
    if manifest.get("manifest_sha256") != _package_manifest_hash(manifest):
        raise WorkflowError("REVIEW_PACKAGE.json a été modifié ou corrompu")
    if _sha256_bytes(files["INSTRUCTIONS.md"]) != manifest.get("instructions_sha256"):
        raise WorkflowError("INSTRUCTIONS.md a été modifié; seuls les fichiers sous editable/ peuvent changer")
    allowed = {"REVIEW_PACKAGE.json", "INSTRUCTIONS.md"}
    allowed.update(str(x.get("package_path")) for x in manifest.get("editable_files") or [])
    allowed.update(str(x.get("package_path")) for x in manifest.get("context_files") or [])
    extras = set(files) - allowed
    missing = allowed - set(files)
    if extras:
        raise WorkflowError(f"Fichiers non autorisés dans le ZIP : {sorted(extras)[:5]}")
    if missing:
        raise WorkflowError(f"Fichiers manquants dans le ZIP : {sorted(missing)[:5]}")
    for row in manifest.get("context_files") or []:
        name = str(row.get("package_path"))
        if _sha256_bytes(files[name]) != row.get("sha256"):
            raise WorkflowError(f"Un fichier de contexte en lecture seule a été modifié : {name}")
    return manifest, files


def _atomic_restore_dir(target: Path, backup: Path) -> None:
    failed = target.with_name(target.name + ".failed-import")
    shutil.rmtree(failed, ignore_errors=True)
    if target.exists():
        os.replace(target, failed)
    os.replace(backup, target)
    shutil.rmtree(failed, ignore_errors=True)


def _install_editable_files(base: Path, manifest: Mapping[str, Any], files: Mapping[str, bytes]) -> None:
    for row in manifest.get("editable_files") or []:
        target_rel = str(row.get("target_path") or "")
        package_rel = str(row.get("package_path") or "")
        if not target_rel or not _safe_zip_name(target_rel):
            raise WorkflowError(f"Chemin éditable invalide : {target_rel}")
        target = (base / target_rel).resolve()
        try:
            target.relative_to(base.resolve())
        except ValueError as exc:
            raise WorkflowError(f"Chemin éditable hors base : {target_rel}") from exc
        target.parent.mkdir(parents=True, exist_ok=True)
        temp = target.with_name(target.name + ".importing")
        temp.write_bytes(files[package_rel])
        os.replace(temp, target)




def _validation_errors(validation: Mapping[str, Any]) -> list[dict[str, Any]]:
    report_path = validation.get("report_json")
    if not report_path:
        return []
    path = Path(str(report_path))
    if not path.is_file():
        return []
    try:
        report = load_json(path, "rapport de validation initiale")
    except Exception:
        return []
    return [
        dict(item) for item in (report.get("findings") or report.get("issues") or [])
        if str(item.get("level") or item.get("severity") or "").upper() == "ERROR"
    ]


def _create_initial_validation_diagnostic(
    project_root: Path, state: dict[str, Any], build_dir: Path, validation: Mapping[str, Any]
) -> dict[str, Any]:
    debate_id = str(state["debate_id"])
    outgoing = project_root / "outgoing"
    outgoing.mkdir(parents=True, exist_ok=True)
    target = outgoing / f"{debate_id}_initial_validation_diagnostic.zip"
    explicit = [
        "manifest.json",
        "scope.json",
        "data/registre_debat.json",
        "graph/graphe_argumentatif.json",
        "graph/graphe_argumentatif.md",
        "reports/import_report.md",
        "reports/initial_validation.json",
        "reports/initial_validation.txt",
        "reports/initial_validation_execution.json",
    ]
    files = _copy_context_files(build_dir, [rel for rel in explicit if (build_dir / rel).is_file()], ["imports/fr/**/*.wiki", "imports/fr/**/*.json"])
    entries = []
    staging = Path(tempfile.mkdtemp(prefix=f".{debate_id}-initial-validation-", dir=outgoing))
    try:
        for source in files:
            rel = source.relative_to(build_dir).as_posix()
            dest = staging / "context" / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, dest)
            entries.append({
                "path": f"context/{rel}",
                "sha256": _sha256_file(source),
                "size_bytes": source.stat().st_size,
            })
        errors = _validation_errors(validation)
        manifest = {
            "schema": DIAGNOSTIC_SCHEMA,
            "schema_version": "1.0",
            "debate_id": debate_id,
            "debate_title": state.get("debate_title"),
            "phase": "initial_validation",
            "normative_revision": NORM_VERSION,
            "validator_version": VALIDATOR_VERSION,
            "kit_version": KIT_VERSION,
            "created_at": now_iso(),
            "build_tree_sha256": full_tree_sha256(build_dir),
            "error_count": len(errors),
            "errors": errors,
            "files": sorted(entries, key=lambda row: row["path"]),
        }
        write_json(staging / "DIAGNOSTIC_PACKAGE.json", manifest)
        _write_deterministic_zip(staging, target)
    finally:
        shutil.rmtree(staging, ignore_errors=True)
    return {
        "diagnostic_path": _relative(target, project_root),
        "diagnostic_sha256": _sha256_file(target),
        "errors": _validation_errors(validation),
    }


def _record_initial_validation_block(
    project_root: Path, state: dict[str, Any], build_dir: Path, validation: Mapping[str, Any]
) -> None:
    diagnostic = _create_initial_validation_diagnostic(project_root, state, build_dir, validation)
    state["phase"] = "initial_validation_blocked"
    state["status"] = "blocked_technical"
    state["last_block"] = {
        "kind": "initial_validation",
        "created_at": now_iso(),
        **diagnostic,
    }
    state["updated_at"] = now_iso()
    _save_workflow(project_root, state)

def _semantic_response_template(review_type: str) -> dict[str, Any]:
    pass_no = 1 if review_type.endswith("_1") else 2
    return {
        "schema": SEMANTIC_RESPONSE_SCHEMA,
        "schema_version": "1.0",
        "pass_number": pass_no,
        "method_family": "",
        "method": "",
        "reviewer": "",
        "note": "",
        "new_certain_errors": None,
        "findings": [],
    }


def _prepare_semantic_package(project_root: Path, state: dict[str, Any], pass_number: int) -> dict[str, Any]:
    workspace, meta = _current_workspace_meta(project_root, state)
    response_rel = "reviews/en/semantic_review_response.json"
    write_json(workspace / response_rel, _semantic_response_template(f"semantic_convergence_{pass_number}"))
    context = [
        "reviews/en/translation_review.json",
        "audits/en_translation_inventory.json",
        "data/sources_en_working.json",
        "content-reviewed-copy/data/fr_page_metadata_lock.json",
        "content-reviewed-copy/data/fr_content_lock.json",
        "content-reviewed-copy/data/sources.json",
        "content-reviewed-copy/data/registre_debat.json",
    ]
    if pass_number == 2:
        context.append("reviews/en/semantic_convergence_review.json")
    return create_review_package(
        project_root, state,
        review_type=f"semantic_convergence_{pass_number}",
        base=workspace,
        editable_paths=[response_rel],
        context_paths=context,
        counts={"pass_number": pass_number},
    )


def _prepare_graph_package(project_root: Path, state: dict[str, Any]) -> dict[str, Any]:
    build = resolve_build(project_root, str(state["debate_id"]))
    overwrite = bool(state.pop("overwrite_graph_review", False))
    result = make_review_template(build, str(state["debate_id"]), overwrite=overwrite)
    return create_review_package(
        project_root, state,
        review_type="graph_review", base=build,
        editable_paths=[REVIEW_ENVELOPE, PLACEMENT_REVIEW],
        context_paths=["manifest.json", "scope.json", "data/registre_debat.json", "graph/graphe_argumentatif.json", "graph/graphe_argumentatif.md", "reports/import_report.md"],
        context_globs=["imports/fr/**/*.wiki", "imports/fr/**/*.json"],
        counts={"placements": result.get("occurrences")},
    )


def _prepare_graph_correction_package(project_root: Path, state: dict[str, Any]) -> dict[str, Any]:
    build = resolve_build(project_root, str(state["debate_id"]))
    result = make_graph_correction_template(build, str(state["debate_id"]))
    return create_review_package(
        project_root, state,
        review_type="graph_correction", base=build,
        editable_paths=[GRAPH_CORRECTION_REVIEW],
        context_paths=[REVIEW_ENVELOPE, PLACEMENT_REVIEW, "reports/graph_build_review_report.json", "manifest.json", "scope.json", "data/registre_debat.json", "graph/graphe_argumentatif.json", "graph/graphe_argumentatif.md", "reports/import_report.md"],
        context_globs=["imports/fr/**/*.wiki", "imports/fr/**/*.json"],
        counts={"placements": result.get("occurrences")},
    )


def _prepare_metadata_package(project_root: Path, state: dict[str, Any]) -> dict[str, Any]:
    workspace, meta = _current_workspace_meta(project_root, state)
    review = load_json(workspace / "reviews/fr/page_metadata_review.json", "revue française")
    return create_review_package(
        project_root, state,
        review_type="fr_metadata_review", base=workspace,
        editable_paths=["reviews/fr/page_metadata_review.json", "data/keyword_vocabulary_working.json"],
        context_paths=["audits/editorial_inventory.json", "audits/editorial_inventory.md", "tasks/editorial_tasks.json", "working-copy/scope.json", "working-copy/data/registre_debat.json", "working-copy/graph/graphe_argumentatif.json"],
        context_globs=["working-copy/imports/fr/**/*.wiki", "working-copy/imports/fr/**/*.json"],
        counts={"pages": len(review.get("items") or [])},
    )


def _prepare_content_package(project_root: Path, state: dict[str, Any]) -> dict[str, Any]:
    workspace, _ = _current_workspace_meta(project_root, state)
    result = prepare_content_review(project_root, str(state["debate_id"]), str(state["work_id"]), overwrite=False)
    review = load_json(workspace / "reviews/fr/content_review.json", "revue contenu")
    return create_review_package(
        project_root, state,
        review_type="fr_content_review", base=workspace,
        editable_paths=["reviews/fr/content_review.json", "data/sources_working.json"],
        context_paths=["audits/fr_content_inventory.json", "audits/fr_content_inventory.md", "reviewed-copy/data/fr_page_metadata_lock.json", "reviewed-copy/data/registre_debat.json", "reviewed-copy/data/sources.json", "reviewed-copy/scope.json"],
        context_globs=["reviewed-copy/imports/fr/**/*.wiki", "reviewed-copy/imports/fr/**/*.json"],
        counts={"arguments": len(review.get("arguments") or [])},
    )


def _prepare_translation_package(project_root: Path, state: dict[str, Any], *, correction: bool = False) -> dict[str, Any]:
    workspace, meta = _current_workspace_meta(project_root, state)
    if not correction:
        prepare_translation_review(project_root, str(state["debate_id"]), str(state["work_id"]), overwrite=False)
    review = load_json(workspace / "reviews/en/translation_review.json", "revue anglaise")
    context = [
        "audits/en_translation_inventory.json", "audits/en_translation_inventory.md",
        "content-reviewed-copy/data/fr_page_metadata_lock.json", "content-reviewed-copy/data/fr_content_lock.json",
        "content-reviewed-copy/data/registre_debat.json", "content-reviewed-copy/data/sources.json",
        "content-reviewed-copy/data/keyword_vocabulary.json",
        "reviews/en/translation_readiness.json",
    ]
    if correction:
        context.append("reviews/en/semantic_convergence_findings.json")
    return create_review_package(
        project_root, state,
        review_type="en_translation_correction" if correction else "en_translation_review",
        base=workspace,
        editable_paths=["reviews/en/translation_review.json", "data/sources_en_working.json"],
        context_paths=context,
        context_globs=["content-reviewed-copy/imports/fr/**/*.wiki", "content-reviewed-copy/imports/fr/**/*.json"],
        counts={"arguments": len(review.get("arguments") or []), "review_units": len(review.get("review_units") or [])},
    )


def _reopen_translation_after_findings(project_root: Path, state: dict[str, Any], findings: Mapping[str, Any]) -> None:
    workspace, meta = _current_workspace_meta(project_root, state)
    review_path = workspace / "reviews/en/translation_review.json"
    review = load_json(review_path, "revue anglaise")
    for key in ("review_sha256", "finalized_at", "semantic_content_sha256", "summary", "final_values", "semantic_review"):
        review.pop(key, None)
    review["status"] = "draft"
    write_json(review_path, review)
    write_json(workspace / "reviews/en/semantic_convergence_findings.json", dict(findings))
    convergence = workspace / "reviews/en/semantic_convergence_review.json"
    if convergence.exists():
        convergence.unlink()
    meta = copy.deepcopy(meta)
    meta["status"] = "en_translation_review_ready"
    meta["english_translation_review"] = {
        "status": "prepared",
        "prepared_at": now_iso(),
        "prepared_content_reviewed_copy_sha256": review.get("prepared_content_reviewed_copy_sha256"),
        "reopened_after_semantic_findings": True,
    }
    meta["workspace_sha256"] = None
    meta["workspace_sha256"] = workspace_receipt_hash(meta)
    write_json(workspace / "workspace.json", meta)


def _mechanical_advance(project_root: Path, state: dict[str, Any]) -> dict[str, Any]:
    """Advance until a ChatGPT review or release-ready terminal state is reached."""
    debate_id = str(state["debate_id"])
    while True:
        phase = str(state.get("phase") or "graph_review")
        if state.get("pending_review"):
            return state
        if phase == "initialize_graph":
            _initialize_graph_stage(project_root, state)
            continue
        if phase == "initial_validation_blocked":
            return state
        if phase == "graph_review":
            _prepare_graph_package(project_root, state)
            return state
        if phase == "graph_correction":
            _prepare_graph_correction_package(project_root, state)
            return state
        if phase == "promote_and_workspace":
            build = project_root / ".state" / "corpus-builds" / debate_id
            corpus = project_root / "corpus" / debate_id
            if build.is_dir() and corpus.exists():
                raise WorkflowError("Le build et le corpus promu existent simultanément; une décision humaine est requise")
            source = build if build.is_dir() else corpus
            if not source.is_dir():
                raise WorkflowError("Ni build validé ni corpus promu disponible pour reprendre le workflow")
            review = load_json(source / REVIEW_ENVELOPE, "revue graphe")
            review_sha = str(review.get("review_sha256") or "")
            if not review_sha or review_sha != graph_review_sha256(review):
                raise WorkflowError("La revue du graphe finalisée n'a pas d'empreinte valide")
            if build.is_dir():
                promote_graph(project_root, debate_id, review_sha)
                corpus = project_root / "corpus" / debate_id
            if not corpus.is_dir():
                raise WorkflowError("La promotion du corpus n'a pas produit le corpus actif attendu")

            editorial_root = project_root / ".state" / "editorial-workspaces" / debate_id
            work_id = state.get("work_id")
            if not work_id:
                editorial_root.mkdir(parents=True, exist_ok=True)
                work_id = next_work_id(editorial_root)
                state["work_id"] = work_id
                state["updated_at"] = now_iso()
                _save_workflow(project_root, state)
            workspace = editorial_root / str(work_id)
            if workspace.is_dir():
                meta = load_json(workspace / "workspace.json", "workspace")
                if meta.get("debate_id") != debate_id or meta.get("work_id") != work_id:
                    raise WorkflowError("Le workspace de reprise ne correspond pas au workflow")
            else:
                create_workspace(project_root, debate_id, str(work_id))
            state["phase"] = "fr_metadata_review"
            state["updated_at"] = now_iso()
            _save_workflow(project_root, state)
            continue
        if phase == "fr_metadata_review":
            _prepare_metadata_package(project_root, state)
            return state
        if phase == "fr_content_review":
            _prepare_content_package(project_root, state)
            return state
        if phase == "en_translation_review":
            _prepare_translation_package(project_root, state)
            return state
        if phase == "semantic_convergence_1":
            _prepare_semantic_package(project_root, state, 1)
            return state
        if phase == "semantic_convergence_2":
            _prepare_semantic_package(project_root, state, 2)
            return state
        if phase == "en_translation_correction":
            _prepare_translation_package(project_root, state, correction=True)
            return state
        if phase == "apply_render_release":
            workspace, meta = _current_workspace_meta(project_root, state)
            review = load_json(workspace / "reviews/en/translation_review.json", "revue anglaise")
            review_sha = str(review.get("review_sha256") or "")
            apply_translation_review(project_root, debate_id, str(state["work_id"]), review_sha)
            render = render_workspace(project_root, debate_id, str(state["work_id"]), review_sha)
            release = release_workspace(project_root, debate_id, str(state["work_id"]), str(render["rendered_copy_tree_sha256"]))
            state["phase"] = "release_ready"
            state["status"] = "release_ready"
            state["release"] = release
            state["updated_at"] = now_iso()
            _save_workflow(project_root, state)
            return state
        if phase == "release_ready":
            return state
        raise WorkflowError(f"Phase d'orchestration inconnue : {phase}")


def _run_graph_extract(project_root: Path, title: str, *, force_refresh: bool = False) -> Path:
    from wikidebia_graph_extract import slugify
    slug = slugify(title)
    output = project_root / ".state" / "graph-extract" / slug
    if not force_refresh and (output / "snapshot" / "snapshot_manifest.json").is_file():
        return output
    script = project_root / "kit" / "scripts" / "wikidebia_graph_extract.py"
    if not script.is_file():
        raise WorkflowError("Extracteur de graphe absent")
    python = project_root / ".venv" / "bin" / "python"
    if not python.is_file():
        python = Path(sys.executable)
    command = [
        str(python), str(script), "--debate", title, "--family", "wikidebates", "--lang", "fr",
        "--pywikibot-dir", str(project_root / "private" / "pywikibot"),
        "--family-file", str(project_root / "kit" / "families" / "wikidebates_family.py"),
        "--output-dir", str(output), "--slug", slug, "--machine-readable",
    ]
    if force_refresh:
        command.append("--force-refresh")
    completed = subprocess.run(command, cwd=project_root, text=True, capture_output=True, check=False)
    if completed.returncode != 0:
        raise WorkflowError("graph-extract a échoué : " + (completed.stderr or completed.stdout)[-2000:])
    if not (output / "snapshot" / "snapshot_manifest.json").is_file():
        raise WorkflowError("graph-extract n'a pas produit le snapshot attendu")
    return output



def _stage_snapshot_input(project_root: Path, debate_id: str, snapshot: Path | None) -> str | None:
    if snapshot is None:
        return None
    source = snapshot.expanduser().resolve()
    if not source.exists() or source.is_symlink():
        raise WorkflowError(f"Snapshot invalide : {snapshot}")
    work_root = _workflow_root(project_root, debate_id)
    work_root.mkdir(parents=True, exist_ok=True)
    if source.is_dir():
        target = work_root / "snapshot-input"
        if not target.exists():
            shutil.copytree(source, target, symlinks=False)
        return _relative(target, project_root)
    target = work_root / "snapshot-input.zip"
    if not target.exists():
        shutil.copy2(source, target)
    return _relative(target, project_root)


def _initialize_graph_stage(project_root: Path, state: dict[str, Any]) -> None:
    debate_id = str(state["debate_id"])
    build_dir = project_root / ".state" / "corpus-builds" / debate_id
    if build_dir.is_dir():
        manifest = load_json(build_dir / "manifest.json", "manifest build")
        if manifest.get("debate_id") != debate_id or manifest.get("global_status") not in {"graph_draft", "graph_validated"}:
            raise WorkflowError("Un build existant incompatible empêche la reprise automatique")
        if manifest.get("global_status") == "graph_draft":
            validation = run_initial_validator(project_root, build_dir)
            if validation.get("status") == "failed":
                _record_initial_validation_block(project_root, state, build_dir, validation)
                return
            state["phase"] = "graph_review"
            state["status"] = "running"
            state.pop("last_block", None)
        else:
            state["phase"] = "promote_and_workspace"
        state["updated_at"] = now_iso()
        _save_workflow(project_root, state)
        return
    staged = state.get("snapshot_path")
    if staged:
        source = project_root / str(staged)
    else:
        source = _run_graph_extract(project_root, str(state["debate_title"]), force_refresh=bool(state.get("force_refresh")))
        state["snapshot_path"] = _relative(source, project_root)
        state["updated_at"] = now_iso()
        _save_workflow(project_root, state)
    result = build_corpus(
        source, build_dir, debate_id=debate_id, short_code=state.get("short_code"),
        scope_summary=None, overwrite=False,
    )
    state["short_code"] = result.get("short_code")
    validation = run_initial_validator(project_root, build_dir)
    if validation.get("status") == "failed":
        _record_initial_validation_block(project_root, state, build_dir, validation)
        return
    state["phase"] = "graph_review"
    state["status"] = "running"
    state.pop("last_block", None)
    state["updated_at"] = now_iso()
    _save_workflow(project_root, state)


def start_workflow(
    project_root: Path,
    debate_title: str,
    *, debate_id: str | None = None,
    short_code: str | None = None,
    snapshot: Path | None = None,
    force_refresh: bool = False,
) -> dict[str, Any]:
    selected_id = validate_debate_id(debate_id or canonical_debate_id(debate_title))
    try:
        requested_short_code = validate_short_code(short_code) if short_code else None
        automatic_short_code = derive_short_code(selected_id)
    except Exception as exc:
        raise WorkflowError(str(exc)) from exc
    state_path = _workflow_path(project_root, selected_id)
    if state_path.is_file():
        state = _load_workflow(project_root, selected_id)
        if state.get("debate_title") != debate_title:
            raise WorkflowError("Le debate_id demandé appartient déjà à un autre titre")
        existing_short_code = str(state.get("short_code") or "").strip()
        try:
            existing_valid = validate_short_code(existing_short_code) if existing_short_code else None
        except Exception:
            existing_valid = None
        if requested_short_code:
            if existing_valid and existing_valid != requested_short_code:
                raise WorkflowError(
                    f"Le workflow utilise déjà le short_code {existing_valid}; "
                    f"le code demandé {requested_short_code} est différent"
                )
            if existing_valid != requested_short_code:
                state["short_code"] = requested_short_code
                state["updated_at"] = now_iso()
                _save_workflow(project_root, state)
        elif not existing_valid:
            state["short_code"] = automatic_short_code
            state["updated_at"] = now_iso()
            _save_workflow(project_root, state)
        if state.get("phase") == "initial_validation_blocked":
            state["phase"] = "initialize_graph"
            state["status"] = "running"
            state["updated_at"] = now_iso()
            _save_workflow(project_root, state)
        return _mechanical_advance(project_root, state)

    state = {
        "schema": WORKFLOW_SCHEMA,
        "schema_version": "1.0",
        "normative_revision": NORM_VERSION,
        "validator_version": VALIDATOR_VERSION,
        "kit_version": KIT_VERSION,
        "debate_id": selected_id,
        "debate_title": debate_title,
        "short_code": requested_short_code or automatic_short_code,
        "phase": "initialize_graph",
        "status": "running",
        "work_id": None,
        "pending_review": None,
        "snapshot_path": None,
        "force_refresh": bool(force_refresh),
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }
    _save_workflow(project_root, state)
    state["snapshot_path"] = _stage_snapshot_input(project_root, selected_id, snapshot)
    state["updated_at"] = now_iso()
    _save_workflow(project_root, state)
    return _mechanical_advance(project_root, state)


def _validate_pending_identity(state: Mapping[str, Any], manifest: Mapping[str, Any]) -> None:
    pending = state.get("pending_review") or {}
    if manifest.get("debate_id") != state.get("debate_id"):
        raise WorkflowError("Le ZIP appartient à un autre corpus")
    if manifest.get("work_id") != state.get("work_id"):
        raise WorkflowError("Le ZIP appartient à un autre Work")
    if manifest.get("package_id") != pending.get("package_id"):
        raise WorkflowError("Le ZIP ne correspond pas au paquet de revue actuellement attendu")
    if manifest.get("review_type") != pending.get("review_type"):
        raise WorkflowError("Type de revue inattendu")
    if manifest.get("manifest_sha256") != pending.get("manifest_sha256"):
        raise WorkflowError("La provenance locale du paquet ne correspond pas")


def import_review(project_root: Path, debate_id: str, archive: Path, *, execute_graph_actions: bool = False) -> dict[str, Any]:
    debate_id = validate_debate_id(debate_id)
    state = _load_workflow(project_root, debate_id)
    pending = state.get("pending_review")
    if not isinstance(pending, dict):
        raise WorkflowError("Aucune revue ChatGPT n'est actuellement attendue")
    manifest, files = _read_returned_package(archive)
    _validate_pending_identity(state, manifest)
    base = project_root / str(pending["base_path"])
    if not base.is_dir():
        raise WorkflowError("La base locale de la revue n'existe plus")

    # Context is validated against both the returned package and current local files.
    for row in manifest.get("context_files") or []:
        local = base / str(row.get("target_path"))
        _assert_regular_file(local, "Contexte local")
        if _sha256_file(local) != row.get("sha256"):
            raise WorkflowError(f"Le contexte local a changé depuis la préparation : {row.get('target_path')}")
    for row in manifest.get("editable_files") or []:
        local = base / str(row.get("target_path"))
        _assert_regular_file(local, "Fichier éditable local")
        if _sha256_file(local) != row.get("sha256_at_prepare"):
            raise WorkflowError(f"Un fichier éditable local a changé hors réimport : {row.get('target_path')}")

    backup = base.with_name(base.name + f".review-import-backup-{uuid.uuid4().hex[:8]}")
    if backup.exists():
        shutil.rmtree(backup)
    shutil.copytree(base, backup, symlinks=False)
    try:
        _install_editable_files(base, manifest, files)
        review_type = str(manifest["review_type"])
        if execute_graph_actions and review_type != "graph_review":
            raise WorkflowError("--execute-graph-actions est réservé aux paquets de revue du graphe")
        if review_type == "graph_review":
            result = finalize_graph_review(project_root, base, debate_id)
            if result.get("status") == "approved":
                state["phase"] = "promote_and_workspace"
            elif result.get("status") == "rejected":
                state.setdefault("graph_rejections", []).append({
                    "review_sha256": result.get("review_sha256"),
                    "blocking_issues": copy.deepcopy(result.get("blocking_issues") or []),
                    "recorded_at": now_iso(),
                })
                if execute_graph_actions:
                    action_result = execute_graph_review_actions(
                        project_root, base, debate_id,
                        preflight_validator=lambda preview: run_initial_validator(project_root, preview),
                    )
                    validation = run_initial_validator(project_root, base)
                    if validation.get("status") == "failed":
                        raise WorkflowError("Les décisions structurelles appliquées produisent un graphe local invalide")
                    state.setdefault("graph_action_executions", []).append(copy.deepcopy(action_result))
                    state["phase"] = "graph_review"
                    state["overwrite_graph_review"] = True
                else:
                    state["phase"] = "graph_correction"
            else:
                raise WorkflowError(f"Statut final de revue du graphe inattendu : {result.get('status')!r}")
        elif review_type == "graph_correction":
            result = apply_graph_correction(project_root, base, debate_id)
            validation = run_initial_validator(project_root, base)
            if validation.get("status") == "failed":
                raise WorkflowError("La correction du graphe reste structurellement invalide; elle n'a pas été acceptée")
            state["phase"] = "graph_review"
            state["overwrite_graph_review"] = True
        elif review_type == "fr_metadata_review":
            result = finalize_metadata_review(project_root, debate_id, str(state["work_id"]))
            apply_metadata_review(project_root, debate_id, str(state["work_id"]), str(result["review_sha256"]))
            state["phase"] = "fr_content_review"
        elif review_type == "fr_content_review":
            result = finalize_content_review(project_root, debate_id, str(state["work_id"]))
            apply_content_review(project_root, debate_id, str(state["work_id"]), str(result["review_sha256"]))
            state["phase"] = "en_translation_review"
        elif review_type in {"en_translation_review", "en_translation_correction"}:
            result = finalize_translation_review(project_root, debate_id, str(state["work_id"]))
            state["phase"] = "semantic_convergence_1"
        elif review_type in {"semantic_convergence_1", "semantic_convergence_2"}:
            response = load_json(base / "reviews/en/semantic_review_response.json", "réponse de convergence")
            if response.get("schema") != SEMANTIC_RESPONSE_SCHEMA:
                raise WorkflowError("Réponse de convergence sémantique invalide")
            family = str(response.get("method_family") or "")
            if family not in ALLOWED_METHOD_FAMILIES:
                raise WorkflowError("Famille de méthode de convergence invalide")
            if not str(response.get("method") or "").strip() or not str(response.get("reviewer") or "").strip():
                raise WorkflowError("Méthode et relecteur sont obligatoires pour la convergence")
            try:
                errors = int(response.get("new_certain_errors"))
            except Exception as exc:
                raise WorkflowError("new_certain_errors doit être un entier") from exc
            if errors < 0:
                raise WorkflowError("new_certain_errors ne peut pas être négatif")
            result = record_semantic_pass(
                project_root, debate_id, str(state["work_id"]), method_family=family,
                method=str(response["method"]), reviewer=str(response["reviewer"]),
                note=str(response.get("note") or ""), new_certain_errors=errors,
            )
            findings = response.get("findings") or []
            if errors > 0:
                _reopen_translation_after_findings(project_root, state, {
                    "schema": "wikidebia-semantic-convergence-findings-1.0",
                    "debate_id": debate_id,
                    "work_id": state.get("work_id"),
                    "recorded_at": now_iso(),
                    "source_review_type": review_type,
                    "new_certain_errors": errors,
                    "findings": findings,
                })
                state["phase"] = "en_translation_correction"
            elif review_type == "semantic_convergence_1":
                state["phase"] = "semantic_convergence_2"
            else:
                if result.get("status") != "converged":
                    raise WorkflowError("Deux passes propres et indépendantes sont requises avant l'application")
                state["phase"] = "apply_render_release"
        else:
            raise WorkflowError(f"Type de revue non pris en charge : {review_type}")
    except Exception:
        _atomic_restore_dir(base, backup)
        raise
    else:
        shutil.rmtree(backup, ignore_errors=True)

    state["pending_review"] = None
    state["status"] = "running"
    state["updated_at"] = now_iso()
    _save_workflow(project_root, state)
    return _mechanical_advance(project_root, state)


def status_summary(project_root: Path, debate_id: str) -> dict[str, Any]:
    state = _load_workflow(project_root, validate_debate_id(debate_id))
    return state


def _print_user_result(state: Mapping[str, Any]) -> None:
    pending = state.get("pending_review")
    if isinstance(pending, dict):
        spec = REVIEW_TYPES.get(str(pending.get("review_type")))
        print(spec.user_message if spec else "Revue éditoriale préparée.")
        counts = pending.get("counts") or {}
        if counts.get("placements") is not None:
            print(f"{counts['placements']} placements doivent être analysés par ChatGPT.")
        elif counts.get("arguments") is not None:
            print(f"{counts['arguments']} arguments sont inclus dans cette revue.")
        print("\nEnvoyez ce fichier à ChatGPT :")
        print(pending.get("package_path"))
        print("\nAprès correction, réimportez le ZIP rendu avec :")
        print(f"./wikidebia review-import {state.get('debate_id')} <fichier_corrige.zip>")
        return
    if state.get("status") == "blocked_technical":
        block = state.get("last_block") or {}
        print("Le workflow s’est arrêté sur une incohérence technique avant la prochaine revue éditoriale.")
        errors = block.get("errors") or []
        if errors:
            print("\nErreurs détectées :")
            for item in errors[:8]:
                code = item.get("code") or "ERREUR"
                message = item.get("message") or "Erreur sans libellé"
                print(f"- {code} — {message}")
            if len(errors) > 8:
                print(f"- … {len(errors) - 8} autre(s) erreur(s)")
        print("\nEnvoyez ce fichier à ChatGPT pour diagnostic :")
        print(block.get("diagnostic_path"))
        print("\nAprès mise à jour/correction du kit ou du corpus, relancez simplement la même commande workflow.")
        return
    if state.get("status") == "release_ready":
        release = state.get("release") or {}
        print("Workflow éditorial terminé : corpus bilingue release_ready.")
        print(f"Archive : {release.get('archive')}")
        return
    print(json.dumps(dict(state), ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Orchestration Wikidéb’IA jusqu'aux seuls points de revue éditoriale.")
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--machine-readable", action="store_true")
    sub = parser.add_subparsers(dest="command", required=True)
    start = sub.add_parser("workflow")
    start.add_argument("debate_title")
    start.add_argument("--debate-id")
    start.add_argument("--short-code")
    start.add_argument("--snapshot", type=Path)
    start.add_argument("--force-refresh", action="store_true")
    imp = sub.add_parser("review-import")
    imp.add_argument("debate_id")
    imp.add_argument("archive", type=Path)
    imp.add_argument("--execute-graph-actions", action="store_true", help="Appliquer et publier immédiatement les décisions structurelles explicites de la revue du graphe")
    status = sub.add_parser("workflow-status")
    status.add_argument("debate_id")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = args.project_root.expanduser().resolve()
    try:
        if args.command == "workflow":
            snapshot = args.snapshot
            if snapshot is not None and not snapshot.is_absolute():
                snapshot = (root / snapshot).resolve()
            state = start_workflow(root, args.debate_title, debate_id=args.debate_id, short_code=args.short_code, snapshot=snapshot, force_refresh=args.force_refresh)
        elif args.command == "review-import":
            archive = args.archive if args.archive.is_absolute() else (root / args.archive)
            state = import_review(root, args.debate_id, archive.resolve(), execute_graph_actions=args.execute_graph_actions)
        else:
            state = status_summary(root, args.debate_id)
    except Exception as exc:
        if args.machine_readable:
            print(json.dumps({"status": "blocked", "error": str(exc)}, ensure_ascii=False, sort_keys=True))
        else:
            print(f"WIKIDEBIA BLOQUÉ : {exc}", file=sys.stderr)
        return 2
    if args.machine_readable:
        print(json.dumps(state, ensure_ascii=False, sort_keys=True))
    else:
        _print_user_result(state)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
