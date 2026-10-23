#!/usr/bin/env python3
"""Project signed publication history into a portable continuity snapshot."""
from __future__ import annotations

import hashlib
import json
import re
import shutil
from pathlib import Path
from typing import Any, Mapping


class ContinuityError(RuntimeError):
    pass


HISTORY_NAME = re.compile(r"^\d{8}T\d{6}Z\.json$")


def _sha_object(value: Mapping[str, Any], field: str) -> str:
    body = dict(value)
    body.pop(field, None)
    return hashlib.sha256(
        json.dumps(body, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _load_signed(path: Path, field: str, label: str) -> dict[str, Any]:
    if not path.is_file() or path.is_symlink():
        raise ContinuityError(f"{label} absent ou non régulier : {path}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ContinuityError(f"{label} illisible : {path}") from exc
    if not isinstance(value, dict) or value.get(field) != _sha_object(value, field):
        raise ContinuityError(f"Empreinte invalide pour {label} : {path}")
    return value


def _inside(path: Path, parent: Path, label: str) -> Path:
    resolved = path.resolve()
    try:
        return resolved.relative_to(parent.resolve())
    except ValueError as exc:
        raise ContinuityError(f"{label} extérieur au périmètre autorisé : {path}") from exc


def _same_file(source: Path, target: Path) -> bool:
    return target.is_file() and not target.is_symlink() and source.read_bytes() == target.read_bytes()


def _copy_exact(source: Path, target: Path) -> None:
    if source.is_symlink() or not source.is_file():
        raise ContinuityError(f"Source de continuité non régulière : {source}")
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)


def _refresh_sha256sums(snapshot_root: Path) -> None:
    rows: list[str] = []
    for path in sorted(item for item in snapshot_root.rglob("*") if item.is_file() and item.name != "SHA256SUMS"):
        if path.is_symlink():
            raise ContinuityError(f"Lien symbolique interdit dans la continuité : {path}")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        rows.append(f"{digest}  ./{path.relative_to(snapshot_root).as_posix()}")
    (snapshot_root / "SHA256SUMS").write_text("\n".join(rows) + "\n", encoding="utf-8", newline="\n")


def _verify_sha256sums(snapshot_root: Path) -> None:
    manifest = snapshot_root / "SHA256SUMS"
    if not manifest.is_file() or manifest.is_symlink():
        raise ContinuityError("SHA256SUMS absent de la projection de continuité")
    expected: dict[str, str] = {}
    for line in manifest.read_text(encoding="utf-8").splitlines():
        digest, separator, relative = line.partition("  ./")
        if not separator or not re.fullmatch(r"[0-9a-f]{64}", digest) or not relative:
            raise ContinuityError("Ligne SHA256SUMS invalide")
        if relative in expected:
            raise ContinuityError(f"Entrée SHA256SUMS dupliquée : {relative}")
        expected[relative] = digest
    if any(path.is_symlink() for path in snapshot_root.rglob("*")):
        raise ContinuityError("Lien symbolique interdit dans la continuité")
    actual_paths = sorted(
        path.relative_to(snapshot_root).as_posix()
        for path in snapshot_root.rglob("*")
        if path.is_file() and path.name != "SHA256SUMS"
    )
    if actual_paths != sorted(expected):
        raise ContinuityError("SHA256SUMS ne couvre pas exactement la projection de continuité")
    for relative, digest in expected.items():
        path = snapshot_root / relative
        if path.is_symlink() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise ContinuityError(f"Empreinte de continuité divergente : {relative}")


def _page_map(state: Mapping[str, Any], label: str) -> dict[tuple[str, str], Mapping[str, Any]]:
    pages = state.get("pages")
    if not isinstance(pages, list):
        raise ContinuityError(f"Liste de pages invalide dans {label}")
    result: dict[tuple[str, str], Mapping[str, Any]] = {}
    for row in pages:
        if not isinstance(row, dict):
            raise ContinuityError(f"Page invalide dans {label}")
        key = (str(row.get("page_type") or ""), str(row.get("page_id") or ""))
        if not all(key) or key in result:
            raise ContinuityError(f"Identifiant de page absent ou dupliqué dans {label}")
        result[key] = row
    return result


def _validate_transition(
    anchor: Mapping[str, Any],
    previous: Mapping[str, Any],
    current: Mapping[str, Any],
    label: str,
) -> None:
    if current.get("source_manifest_sha256") != anchor.get("source_manifest_sha256"):
        raise ContinuityError("Une correction change le manifeste source du checkpoint")
    if current.get("corpus_version") != anchor.get("corpus_version"):
        raise ContinuityError("Une correction change la version de corpus du checkpoint")
    previous_pages = _page_map(previous, "l'état précédent")
    pages = _page_map(current, label)
    if set(pages) != set(previous_pages):
        raise ContinuityError("Une correction change l'ensemble des pages du checkpoint")
    for key, before in previous_pages.items():
        after = pages[key]
        before_revision = int(before.get("revision_id") or 0)
        after_revision = int(after.get("revision_id") or 0)
        if before_revision <= 0 or after_revision < before_revision:
            raise ContinuityError("Une correction fait régresser une révision publiée")
        if after_revision == before_revision and after != before:
            raise ContinuityError("Une correction change une page sans nouvelle révision")


def verify_committed_snapshot(snapshot_root: Path, debate_id: str | None = None) -> dict[str, Any]:
    """Verify that a committed snapshot carries a self-contained FR succession."""
    snapshot_root = snapshot_root.resolve()
    if not snapshot_root.is_dir():
        raise ContinuityError("Racine de continuité absente")
    _verify_sha256sums(snapshot_root)
    debate_id = debate_id or snapshot_root.parent.name

    content_receipt = _load_signed(
        snapshot_root / "runtime/fr-publication/content/publication-receipt.json",
        "receipt_sha256",
        "reçu du checkpoint de contenu",
    )
    work_id = str(content_receipt.get("work_id") or "")
    if content_receipt.get("debate_id") != debate_id or not work_id:
        raise ContinuityError("Reçu du checkpoint rattaché à un autre débat ou sans Work")

    state_root = snapshot_root / "runtime/published/fr"
    latest = _load_signed(state_root / "latest.json", "state_sha256", "état français courant")
    if latest.get("debate_id") != debate_id or latest.get("language") != "fr":
        raise ContinuityError("État français courant rattaché à un autre débat ou langue")
    history: list[tuple[Path, dict[str, Any]]] = []
    for path in sorted(state_root.glob("*.json")):
        if HISTORY_NAME.fullmatch(path.name):
            history.append((path, _load_signed(path, "state_sha256", f"état historique {path.name}")))
    if not history:
        raise ContinuityError("Aucun état historique français signé dans la continuité")
    for path, state in history:
        if state.get("debate_id") != debate_id or state.get("language") != "fr":
            raise ContinuityError(f"État historique hors débat : {path.name}")
    if history[-1][1] != latest:
        raise ContinuityError("L'état courant n'est pas le dernier état historique signé")

    checkpoint_plan = str(content_receipt.get("plan_sha256") or "")
    checkpoint_receipt = str(content_receipt.get("remote_receipt_sha256") or "")
    anchor_index = next((
        index for index, (_path, state) in enumerate(history)
        if str(state.get("plan_sha256") or "") == checkpoint_plan
        and (not checkpoint_receipt or str(state.get("receipt_sha256") or "") == checkpoint_receipt)
    ), None)
    if anchor_index is None:
        raise ContinuityError("État historique du checkpoint de contenu introuvable")

    anchor = history[anchor_index][1]
    previous = anchor
    correction_count = 0
    receipt_prefix = Path(".state/fr-publication") / debate_id / work_id
    for path, state in history[anchor_index + 1:]:
        _validate_transition(anchor, previous, state, f"l'état corrigé {path.name}")
        receipt_value = str(state.get("receipt_path") or "").strip()
        receipt_path = Path(receipt_value)
        if not receipt_value or receipt_path.is_absolute():
            raise ContinuityError("Chemin de reçu de correction non portable")
        try:
            receipt_relative = receipt_path.relative_to(receipt_prefix)
        except ValueError as exc:
            raise ContinuityError("Reçu de correction extérieur au Work courant") from exc
        receipt = _load_signed(
            snapshot_root / "runtime/fr-publication" / receipt_relative,
            "receipt_sha256",
            "reçu de correction",
        )
        if receipt.get("debate_id") != debate_id or receipt.get("work_id") != work_id:
            raise ContinuityError("Reçu de correction rattaché à un autre débat ou Work")
        if receipt.get("language") not in {None, "fr"}:
            raise ContinuityError("Reçu de correction rattaché à une autre langue")
        if receipt.get("plan_sha256") != state.get("plan_sha256") or receipt.get("receipt_sha256") != state.get("receipt_sha256"):
            raise ContinuityError("Reçu de correction divergent de l'état publié")
        correction_count += 1
        previous = state

    return {
        "status": "passed",
        "debate_id": debate_id,
        "work_id": work_id,
        "history_state_count": len(history),
        "post_checkpoint_correction_count": correction_count,
        "current_state_sha256": latest.get("state_sha256"),
    }


def sync_signed_french_history(
    project_root: Path,
    debate_id: str,
    *,
    work_id: str | None = None,
    snapshot_root: Path | None = None,
    check_only: bool = False,
) -> dict[str, Any]:
    """Copy and verify all signed FR states required to resume final publication."""
    project_root = project_root.resolve()
    workflow_path = project_root / ".state/workflows" / debate_id / "workflow.json"
    if not workflow_path.is_file():
        raise ContinuityError("Workflow local absent")
    try:
        workflow = json.loads(workflow_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ContinuityError("Workflow local illisible") from exc
    current_work = str(workflow.get("work_id") or "")
    if not current_work or (work_id and work_id != current_work):
        raise ContinuityError("Work demandé différent du workflow courant")
    work_id = current_work

    default_snapshot = project_root / "continuity" / debate_id / "latest"
    snapshot_root = (snapshot_root or default_snapshot)
    snapshot_root = snapshot_root.resolve() if snapshot_root.is_absolute() else (project_root / snapshot_root).resolve()
    _inside(snapshot_root, project_root / "continuity", "Projection de continuité")
    if not snapshot_root.is_dir():
        raise ContinuityError("Racine de continuité absente")

    work_root = project_root / ".state/fr-publication" / debate_id / work_id
    content_receipt_path = work_root / "content/publication-receipt.json"
    content_receipt = _load_signed(content_receipt_path, "receipt_sha256", "reçu du checkpoint de contenu")
    if content_receipt.get("debate_id") != debate_id or content_receipt.get("work_id") != work_id:
        raise ContinuityError("Reçu du checkpoint rattaché à un autre débat ou Work")

    state_root = project_root / ".state/published" / debate_id / "fr"
    latest_path = state_root / "latest.json"
    latest = _load_signed(latest_path, "state_sha256", "état français courant")
    if latest.get("debate_id") != debate_id or latest.get("language") != "fr":
        raise ContinuityError("État français courant rattaché à un autre débat ou langue")

    history: list[tuple[Path, dict[str, Any]]] = []
    for path in sorted(state_root.glob("*.json")):
        if not HISTORY_NAME.fullmatch(path.name):
            continue
        state = _load_signed(path, "state_sha256", f"état historique {path.name}")
        if state.get("debate_id") != debate_id or state.get("language") != "fr":
            raise ContinuityError(f"État historique hors débat : {path.name}")
        history.append((path, state))
    if not history:
        raise ContinuityError("Aucun état historique français signé")

    anchor_plan = str(content_receipt.get("plan_sha256") or "")
    anchor_receipt = str(content_receipt.get("remote_receipt_sha256") or "")
    anchor_index = next((
        index for index, (_path, state) in enumerate(history)
        if str(state.get("plan_sha256") or "") == anchor_plan
        and (not anchor_receipt or str(state.get("receipt_sha256") or "") == anchor_receipt)
    ), None)
    current_index = next((
        index for index, (_path, state) in enumerate(history)
        if state.get("state_sha256") == latest.get("state_sha256")
    ), None)
    if anchor_index is None:
        raise ContinuityError("État historique du checkpoint de contenu introuvable")
    if current_index is None or current_index < anchor_index or current_index != len(history) - 1:
        raise ContinuityError("L'état courant n'est pas le dernier état historique signé")

    required: list[tuple[Path, Path]] = []
    target_state_root = snapshot_root / "runtime/published/fr"
    for source, _state in history[:current_index + 1]:
        required.append((source, target_state_root / source.name))
    required.append((latest_path, target_state_root / "latest.json"))
    required.append((content_receipt_path, snapshot_root / "runtime/fr-publication/content/publication-receipt.json"))

    anchor = history[anchor_index][1]
    previous = anchor
    correction_count = 0
    for path, state in history[anchor_index + 1:current_index + 1]:
        _validate_transition(anchor, previous, state, f"l'état corrigé {path.name}")
        receipt_value = str(state.get("receipt_path") or "")
        receipt_source = (project_root / receipt_value).resolve() if receipt_value else Path()
        receipt_relative = _inside(receipt_source, work_root, "Reçu de correction")
        receipt = _load_signed(receipt_source, "receipt_sha256", "reçu de correction")
        if receipt.get("debate_id") != debate_id or receipt.get("work_id") != work_id:
            raise ContinuityError("Reçu de correction rattaché à un autre débat ou Work")
        if receipt.get("language") not in {None, "fr"}:
            raise ContinuityError("Reçu de correction rattaché à une autre langue")
        if receipt.get("plan_sha256") != state.get("plan_sha256") or receipt.get("receipt_sha256") != state.get("receipt_sha256"):
            raise ContinuityError("Reçu de correction divergent de l'état publié")
        required.append((receipt_source, snapshot_root / "runtime/fr-publication" / receipt_relative))
        correction_count += 1
        previous = state

    if check_only:
        missing = [str(target.relative_to(snapshot_root)) for source, target in required if not _same_file(source, target)]
        if missing:
            raise ContinuityError("Projection de continuité incomplète : " + ", ".join(missing))
        _verify_sha256sums(snapshot_root)
    else:
        for source, target in required:
            _copy_exact(source, target)
        _refresh_sha256sums(snapshot_root)
        for source, target in required:
            if not _same_file(source, target):
                raise ContinuityError(f"Copie de continuité divergente : {target}")
        _verify_sha256sums(snapshot_root)

    return {
        "status": "passed",
        "mode": "check" if check_only else "sync",
        "debate_id": debate_id,
        "work_id": work_id,
        "snapshot_root": snapshot_root.relative_to(project_root).as_posix(),
        "history_state_count": current_index + 1,
        "post_checkpoint_correction_count": correction_count,
        "current_state_sha256": latest.get("state_sha256"),
    }
