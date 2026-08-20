#!/usr/bin/env python3
"""Work-scoped bilingual baseline evidence for final publication.

This module deliberately contains no MediaWiki access.  It verifies that a sealed
``release_ready`` corpus belongs to the current editorial Work, that the final
French checkpoint was actually published and signed, and that English has not
been published by that Work before the final-publication boundary.  The evidence
can be consumed read-only by ``update --archive`` or sealed under ``.state`` by
the high-level workflow.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any, Mapping

from wikidebia_corpus_build import full_tree_sha256, load_json, now_iso, sha256_file, write_json
from wikidebia_editorial_workspace import workspace_receipt_hash
import hashlib

BASELINE_SCHEMA = "wikidebia-final-publication-baseline-1.0"
WORKFLOW_SCHEMA = "wikidebia-editorial-orchestration-1.0"


class WorkflowBaselineError(RuntimeError):
    pass


def sha_object(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def _canonical(value: Mapping[str, Any], excluded: str) -> str:
    body = dict(value)
    body.pop(excluded, None)
    return sha_object(body)


def _verify_sha_object(value: dict[str, Any], field: str, label: str) -> str:
    body = dict(value)
    claimed = body.pop(field, None)
    if not claimed or claimed != sha_object(body):
        raise WorkflowBaselineError(f"Empreinte {label} invalide")
    return str(claimed)


def _relative(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def _release_identity(corpus_root: Path) -> tuple[str, str, dict[str, Any]]:
    report_path = corpus_root / "reports/release_report.json"
    release_manifest_path = corpus_root / "release/release_manifest.json"
    if not report_path.is_file() or not release_manifest_path.is_file():
        raise WorkflowBaselineError("Le corpus ne porte pas les preuves release_ready attendues")
    report = load_json(report_path, "rapport de release")
    if report.get("result") != "passed":
        raise WorkflowBaselineError("Le rapport de release n'est pas positif")
    return sha256_file(report_path), sha256_file(release_manifest_path), report


def _load_signed_published_state(project_root: Path, debate_id: str, language: str) -> tuple[Path, dict[str, Any]] | None:
    path = project_root / ".state/published" / debate_id / language / "latest.json"
    if not path.is_file():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    _verify_sha_object(data, "state_sha256", f"de l'état publié {language}")
    if data.get("debate_id") != debate_id or data.get("language") != language:
        raise WorkflowBaselineError(f"État publié {language} rattaché à un autre débat")
    return path, data


def resolve_workflow_release_baseline(
    project_root: Path,
    debate_id: str,
    corpus_root: Path,
    *,
    expected_work_id: str | None = None,
) -> dict[str, Any] | None:
    """Return verified Work-scoped baseline evidence, or ``None`` if not applicable.

    ``None`` means that ``corpus_root`` is not recognisably a workflow release and
    callers may continue with their legacy evidence mechanisms.  Once a release
    report identifies a Work, however, inconsistencies are blocking rather than
    silently falling back to weaker evidence.
    """
    project_root = project_root.resolve()
    corpus_root = corpus_root.resolve()
    report_path = corpus_root / "reports/release_report.json"
    if not report_path.is_file():
        return None

    report_sha, release_manifest_sha, report = _release_identity(corpus_root)
    if str(report.get("debate_id") or "") != debate_id:
        raise WorkflowBaselineError("Le rapport de release vise un autre débat")
    work_id = str(report.get("work_id") or "").strip()
    if not work_id:
        raise WorkflowBaselineError("work_id absent du rapport de release")
    if expected_work_id and work_id != expected_work_id:
        raise WorkflowBaselineError("Le release_ready ne correspond pas au Work attendu")

    workflow_path = project_root / ".state/workflows" / debate_id / "workflow.json"
    if not workflow_path.is_file():
        raise WorkflowBaselineError("Workflow local absent pour le release_ready identifié")
    workflow = load_json(workflow_path, "workflow")
    if workflow.get("schema") != WORKFLOW_SCHEMA or workflow.get("debate_id") != debate_id:
        raise WorkflowBaselineError("Workflow local invalide ou rattaché à un autre débat")
    if str(workflow.get("work_id") or "") != work_id:
        raise WorkflowBaselineError("Le workflow local appartient à un autre Work")
    if str(workflow.get("status") or "") not in {
        "release_ready", "final_publication", "blocked_final_publication", "published"
    }:
        raise WorkflowBaselineError("Le Work n'est pas arrivé à la frontière de publication finale")
    if str(workflow.get("phase") or "") not in {
        "release_ready", "final_publication", "final_publication_resume", "published"
    }:
        raise WorkflowBaselineError("La phase du Work n'autorise pas une baseline finale")

    workspace = project_root / ".state/editorial-workspaces" / debate_id / work_id
    meta_path = workspace / "workspace.json"
    release_copy = workspace / "release-copy"
    if not meta_path.is_file() or not release_copy.is_dir():
        raise WorkflowBaselineError("Workspace ou release-copy du Work absent")
    meta = load_json(meta_path, "workspace")
    if meta.get("workspace_sha256") != workspace_receipt_hash(meta):
        raise WorkflowBaselineError("Empreinte du workspace invalide")
    if str(meta.get("debate_id") or "") != debate_id or str(meta.get("work_id") or "") != work_id:
        raise WorkflowBaselineError("Workspace rattaché à un autre débat ou Work")
    release_tree_sha = full_tree_sha256(release_copy)
    expected_tree = str((meta.get("release_copy") or {}).get("tree_sha256") or "")
    if not expected_tree or release_tree_sha != expected_tree:
        raise WorkflowBaselineError("Le release-copy du Work a changé depuis son scellement")
    # A staged extraction of the exact release archive has the same signed release
    # identity files even though its absolute path differs.
    canonical_report_sha, canonical_release_manifest_sha, canonical_report = _release_identity(release_copy)
    if str(canonical_report.get("work_id") or "") != work_id:
        raise WorkflowBaselineError("Le release-copy canonique appartient à un autre Work")
    if report_sha != canonical_report_sha or release_manifest_sha != canonical_release_manifest_sha:
        raise WorkflowBaselineError("Le corpus fourni ne correspond pas au release-copy du Work")

    release_receipt_path = project_root / ".state/corpus-releases" / debate_id / work_id / "release-receipt.json"
    if not release_receipt_path.is_file():
        raise WorkflowBaselineError("Reçu de release du Work absent")
    release_receipt = load_json(release_receipt_path, "reçu de release")
    _verify_sha_object(release_receipt, "receipt_sha256", "du reçu de release")
    if release_receipt.get("debate_id") != debate_id or release_receipt.get("work_id") != work_id:
        raise WorkflowBaselineError("Reçu de release rattaché à un autre Work")
    if str(release_receipt.get("release_copy_tree_sha256") or "") != release_tree_sha:
        raise WorkflowBaselineError("Le reçu de release ne correspond pas au release-copy")
    if release_receipt.get("publication_started") is not False:
        # A resumed final publication is handled by its own sealed baseline below;
        # old release receipts remain immutable and therefore must keep the original
        # pre-publication flag.
        raise WorkflowBaselineError("Le reçu de release ne porte pas la barrière prépublication attendue")

    content_receipt_path = project_root / ".state/fr-publication" / debate_id / work_id / "content/publication-receipt.json"
    if not content_receipt_path.is_file():
        # compatibility with the single-checkpoint 2.16.13 path
        legacy = project_root / ".state/fr-publication" / debate_id / work_id / "publication-receipt.json"
        if legacy.is_file():
            content_receipt_path = legacy
        else:
            raise WorkflowBaselineError("Reçu du dernier checkpoint français absent")
    content_receipt = load_json(content_receipt_path, "reçu du checkpoint français final")
    _verify_sha_object(content_receipt, "receipt_sha256", "du checkpoint français final")
    if content_receipt.get("debate_id") != debate_id or content_receipt.get("work_id") != work_id:
        raise WorkflowBaselineError("Checkpoint français final rattaché à un autre Work")
    if str(content_receipt.get("status") or "") not in {"published", "verified_no_changes"}:
        raise WorkflowBaselineError("Le checkpoint français final n'est pas attesté publié")

    workflow_content = workflow.get("french_content_publication") or workflow.get("french_publication")
    if not isinstance(workflow_content, dict):
        raise WorkflowBaselineError("Le workflow ne référence pas son checkpoint français final")
    if str(workflow_content.get("receipt_sha256") or "") != str(content_receipt.get("receipt_sha256") or ""):
        raise WorkflowBaselineError("Le workflow et le reçu du checkpoint français final divergent")

    fr_state_entry = _load_signed_published_state(project_root, debate_id, "fr")
    if fr_state_entry is None:
        raise WorkflowBaselineError("État publié français signé absent après le checkpoint final")
    fr_state_path, fr_state = fr_state_entry
    if str(fr_state.get("plan_sha256") or "") != str(content_receipt.get("plan_sha256") or ""):
        raise WorkflowBaselineError("L'état français courant ne correspond pas au dernier checkpoint du Work")

    installed_manifest_path = project_root / "corpus" / debate_id / "manifest.json"
    if not installed_manifest_path.is_file():
        raise WorkflowBaselineError("Corpus installé préalable absent pour attester le mode anglais deferred")
    installed_manifest = load_json(installed_manifest_path, "manifest du corpus installé")
    if installed_manifest.get("debate_id") != debate_id:
        raise WorkflowBaselineError("Corpus installé préalable rattaché à un autre débat")
    if str(((installed_manifest.get("translation_status") or {}).get("en") or "")) != "deferred":
        raise WorkflowBaselineError(
            "Le Work ne dispose pas de la preuve préalable translation_status.en=deferred requise"
        )
    if any(str(row.get("language") or "") == "en" for row in (installed_manifest.get("pages") or [])):
        raise WorkflowBaselineError("Le corpus deferred préalable contient pourtant des pages anglaises")

    en_state_entry = _load_signed_published_state(project_root, debate_id, "en")
    if en_state_entry is not None:
        # This evidence is deliberately a *pre-publication* empty-English baseline.
        # After any signed English state exists, callers must use that state rather
        # than reconstructing an empty baseline from the old deferred corpus.
        raise WorkflowBaselineError(
            "Un état anglais signé existe déjà : la baseline EN vide de ce Work n'est plus applicable"
        )

    evidence = {
        "schema": BASELINE_SCHEMA,
        "schema_version": "1.0",
        "debate_id": debate_id,
        "work_id": work_id,
        "attested_at": now_iso(),
        "release": {
            "release_copy_tree_sha256": release_tree_sha,
            "release_report_sha256": report_sha,
            "release_manifest_sha256": release_manifest_sha,
            "release_receipt_path": _relative(release_receipt_path, project_root),
            "release_receipt_sha256": str(release_receipt.get("receipt_sha256") or ""),
        },
        "fr": {
            "mode": "published_checkpoint_state",
            "checkpoint_receipt_path": _relative(content_receipt_path, project_root),
            "checkpoint_receipt_sha256": str(content_receipt.get("receipt_sha256") or ""),
            "published_state_path": _relative(fr_state_path, project_root),
            "published_state_sha256": str(fr_state.get("state_sha256") or ""),
            "plan_sha256": str(fr_state.get("plan_sha256") or ""),
        },
        "en": {
            "mode": "never_published_by_this_work",
            "empty_baseline": True,
            "proof_basis": [
                "workflow_reached_release_ready_without_an_english_publication_phase",
                "pre_final_installed_manifest_explicitly_declares_translation_status_en_deferred",
                "release_receipt_publication_started_false",
            ],
            "installed_manifest_path": _relative(installed_manifest_path, project_root),
            "installed_manifest_sha256": sha256_file(installed_manifest_path),
            "signed_english_state_absent": en_state_entry is None,
            "remote_absence_not_assumed": True,
            "remote_title_collisions_must_be_checked_before_any_write": True,
        },
        "semantic_convergence": {
            "pass_count": release_receipt.get("semantic_convergence_passes"),
            "semantic_content_sha256": release_receipt.get("semantic_content_sha256"),
            "review_sha256": release_receipt.get("semantic_convergence_review_sha256"),
            "reused_without_rerun": True,
        },
    }
    evidence["baseline_sha256"] = _canonical(evidence, "baseline_sha256")
    return evidence


def _repair_stale_workflow_content_receipt_reference(
    project_root: Path,
    debate_id: str,
    work_id: str,
) -> bool:
    """Repair only a stale workflow receipt hash for the already-published FR content checkpoint.

    This compatibility repair is deliberately narrower than adopting a new checkpoint.
    It is allowed only before any final-publication authorization exists, when the
    workflow and the current checkpoint receipt identify the same Work, stage, status
    and *same signed publication plan*, and when ``.state/published/fr/latest.json``
    independently attests that plan.  Any plan divergence remains blocking.
    """
    project_root = project_root.resolve()
    workflow_path = project_root / ".state/workflows" / debate_id / "workflow.json"
    receipt_path = project_root / ".state/fr-publication" / debate_id / work_id / "content/publication-receipt.json"
    if not receipt_path.is_file():
        legacy = project_root / ".state/fr-publication" / debate_id / work_id / "publication-receipt.json"
        receipt_path = legacy if legacy.is_file() else receipt_path
    if not workflow_path.is_file() or not receipt_path.is_file():
        return False

    workflow = load_json(workflow_path, "workflow")
    current = load_json(receipt_path, "reçu du checkpoint français final")
    _verify_sha_object(current, "receipt_sha256", "du checkpoint français final")
    workflow_content = workflow.get("french_content_publication") or workflow.get("french_publication")
    if not isinstance(workflow_content, dict):
        return False
    old_sha = str(workflow_content.get("receipt_sha256") or "")
    new_sha = str(current.get("receipt_sha256") or "")
    if not new_sha or old_sha == new_sha:
        return False
    legacy_unbound_receipt = not old_sha

    # Never mutate the workflow once final publication has crossed its first-write
    # authorization boundary, or once any English published state exists.
    final_dir = project_root / ".state/final-publication" / debate_id / work_id
    if (final_dir / "authorization.json").exists() or (final_dir / "publication-receipt.json").exists():
        raise WorkflowBaselineError(
            "La référence du checkpoint français diverge après le début de la publication finale"
        )
    if (project_root / ".state/published" / debate_id / "en/latest.json").exists():
        raise WorkflowBaselineError(
            "La référence du checkpoint français diverge alors qu'un état anglais signé existe déjà"
        )

    if current.get("debate_id") != debate_id or current.get("work_id") != work_id:
        raise WorkflowBaselineError("Checkpoint français final rattaché à un autre Work")
    if str(current.get("stage") or "content") != "content":
        raise WorkflowBaselineError("Le reçu français courant n'est pas le checkpoint de contenu")
    if str(current.get("status") or "") not in {"published", "verified_no_changes"}:
        raise WorkflowBaselineError("Le checkpoint français courant n'est pas attesté publié")

    # The stale workflow entry itself must still describe the same final checkpoint
    # identity.  Receipt timestamps/hashes may drift after a local transaction
    # restoration, but the publication plan may not.
    if workflow_content.get("debate_id") not in {None, debate_id}:
        raise WorkflowBaselineError("Le workflow référence un checkpoint français d'un autre débat")
    if workflow_content.get("work_id") not in {None, work_id}:
        raise WorkflowBaselineError("Le workflow référence un checkpoint français d'un autre Work")
    if str(workflow_content.get("stage") or "content") != "content":
        raise WorkflowBaselineError("Le workflow ne référence pas le checkpoint français de contenu")
    workflow_status = str(workflow_content.get("status") or "")
    old_plan = str(workflow_content.get("plan_sha256") or "")
    legacy_unbound_status = False
    if workflow_status not in {"published", "verified_no_changes", "no_changes"}:
        # Some pre-two-checkpoint workflow states reached final_publication with an
        # orchestration-local status label (or no checkpoint status at all) and
        # without ever binding receipt_sha256/plan_sha256 into workflow.json.  At
        # this late boundary that local label is redundant: the current signed
        # checkpoint receipt plus the independently signed FR published state are
        # authoritative.  Never reinterpret an already-bound workflow, a workflow
        # that has not reached final publication, or one with a pending review.
        legacy_unbound_status = bool(
            legacy_unbound_receipt
            and not old_plan
            and str(workflow.get("phase") or "") == "final_publication"
            and not workflow.get("pending_review")
        )
        if not legacy_unbound_status:
            raise WorkflowBaselineError("Le workflow ne référence pas un checkpoint français final publié")
    new_plan = str(current.get("plan_sha256") or "")
    if not new_plan:
        raise WorkflowBaselineError("Le reçu français courant ne référence aucun plan signé")
    if old_plan and old_plan != new_plan:
        raise WorkflowBaselineError(
            "Le workflow et le reçu du checkpoint français final divergent sur le plan signé"
        )
    # A legacy workflow may have recorded only that the content checkpoint
    # completed, without copying either receipt_sha256 or plan_sha256.  That
    # historical omission is repairable only when the workflow is truly
    # unbound to a receipt hash; a stale *bound* hash without a plan cannot be
    # adopted because its publication plan cannot be proven equivalent.
    if not old_plan and not legacy_unbound_receipt:
        raise WorkflowBaselineError(
            "Le workflow référence un ancien reçu français sans plan signé vérifiable"
        )

    fr_state_entry = _load_signed_published_state(project_root, debate_id, "fr")
    if fr_state_entry is None:
        raise WorkflowBaselineError("État publié français signé absent pendant la réconciliation du checkpoint")
    _fr_state_path, fr_state = fr_state_entry
    if str(fr_state.get("plan_sha256") or "") != new_plan:
        raise WorkflowBaselineError(
            "L'état français signé ne correspond pas au plan du checkpoint courant"
        )

    repaired = copy.deepcopy(current)
    workflow["french_content_publication"] = repaired
    workflow["french_publication"] = copy.deepcopy(repaired)  # legacy alias
    migrations = workflow.setdefault("compatibility_migrations", [])
    if not isinstance(migrations, list):
        raise WorkflowBaselineError("Registre de migrations du workflow mal formé")
    migrations.append({
        "kind": (
            "legacy_unbound_fr_content_receipt_reference_adopted"
            if legacy_unbound_receipt
            else "stale_fr_content_receipt_reference_reconciled"
        ),
        "reconciled_at": now_iso(),
        "work_id": work_id,
        "old_receipt_sha256": old_sha or None,
        "old_plan_sha256": old_plan or None,
        "old_status": workflow_status or None,
        "legacy_status_reconciled": legacy_unbound_status,
        "new_receipt_sha256": new_sha,
        "plan_sha256": new_plan,
        "proof": "current_checkpoint_receipt_plus_signed_fr_published_state",
    })
    workflow["updated_at"] = now_iso()
    write_json(workflow_path, workflow)
    return True


def seal_workflow_release_baseline(
    project_root: Path,
    debate_id: str,
    work_id: str,
    corpus_root: Path,
) -> dict[str, Any]:
    _repair_stale_workflow_content_receipt_reference(project_root, debate_id, work_id)
    evidence = resolve_workflow_release_baseline(
        project_root, debate_id, corpus_root, expected_work_id=work_id
    )
    if evidence is None:
        raise WorkflowBaselineError("Le corpus n'est pas un release_ready de workflow reconnu")
    target = project_root / ".state/final-publication" / debate_id / work_id / "baseline.json"
    if target.is_file():
        existing = load_json(target, "baseline finale")
        _verify_sha_object(existing, "baseline_sha256", "de la baseline finale")
        # attested_at may differ across a fresh recomputation; compare immutable
        # identity/evidence fields instead of forcing a new receipt.
        for key in ("schema", "debate_id", "work_id", "release", "fr", "en", "semantic_convergence"):
            if existing.get(key) != evidence.get(key):
                raise WorkflowBaselineError("La baseline finale existante diverge de l'état courant")
        return existing
    target.parent.mkdir(parents=True, exist_ok=True)
    write_json(target, evidence)
    return evidence
