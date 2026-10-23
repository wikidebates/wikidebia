from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

import wikidebia_continuity as continuity


def _signed(value: dict, field: str) -> dict:
    result = dict(value)
    body = dict(result)
    body.pop(field, None)
    result[field] = hashlib.sha256(
        json.dumps(body, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return result


def _write(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _fixture(project: Path, *, receipt_outside_work: bool = False) -> tuple[str, str, Path]:
    debate_id = "debat_test"
    work_id = "EDIT-20261023-001"
    _write(project / ".state/workflows" / debate_id / "workflow.json", {
        "debate_id": debate_id,
        "work_id": work_id,
    })

    checkpoint_plan = "1" * 64
    checkpoint_remote_receipt = "2" * 64
    content_receipt = _signed({
        "schema": "wikidebia-fr-publication-receipt-1.0",
        "debate_id": debate_id,
        "work_id": work_id,
        "status": "published",
        "plan_sha256": checkpoint_plan,
        "remote_receipt_sha256": checkpoint_remote_receipt,
    }, "receipt_sha256")
    _write(
        project / ".state/fr-publication" / debate_id / work_id / "content/publication-receipt.json",
        content_receipt,
    )

    page = {
        "page_id": "A0001",
        "page_type": "argument",
        "canonical_title": "Titre source",
        "content_sha256": "3" * 64,
        "revision_id": 10,
        "status": "published",
    }
    anchor = _signed({
        "schema": "wikidebia-published-state-1.0",
        "debate_id": debate_id,
        "language": "fr",
        "plan_sha256": checkpoint_plan,
        "receipt_sha256": checkpoint_remote_receipt,
        "source_manifest_sha256": "4" * 64,
        "corpus_version": "manifest-test",
        "pages": [page],
    }, "state_sha256")

    correction = _signed({
        "schema": "wikidebia-french-correction-receipt-1.0",
        "debate_id": debate_id,
        "work_id": work_id,
        "language": "fr",
        "plan_sha256": "5" * 64,
    }, "receipt_sha256")
    if receipt_outside_work:
        correction_path = project / ".state/other/correction-receipt.json"
    else:
        correction_path = (
            project / ".state/fr-publication" / debate_id / work_id / "content/correction-receipt.json"
        )
    _write(correction_path, correction)

    corrected_page = dict(page)
    corrected_page.update({
        "canonical_title": "Titre rétabli",
        "content_sha256": "6" * 64,
        "revision_id": 11,
    })
    corrected = dict(anchor)
    corrected.pop("state_sha256")
    corrected.update({
        "plan_sha256": correction["plan_sha256"],
        "receipt_path": correction_path.relative_to(project).as_posix(),
        "receipt_sha256": correction["receipt_sha256"],
        "pages": [corrected_page],
    })
    corrected = _signed(corrected, "state_sha256")

    state_root = project / ".state/published" / debate_id / "fr"
    _write(state_root / "20261023T120000Z.json", anchor)
    _write(state_root / "20261023T130000Z.json", corrected)
    _write(state_root / "latest.json", corrected)
    snapshot = project / "continuity" / debate_id / "latest"
    snapshot.mkdir(parents=True)
    (snapshot / "HANDOFF.md").write_text("# Reprise\n", encoding="utf-8")
    return debate_id, work_id, snapshot


def test_sync_copies_complete_signed_french_succession(tmp_path: Path):
    debate_id, work_id, snapshot = _fixture(tmp_path)

    result = continuity.sync_signed_french_history(tmp_path, debate_id)

    assert result["history_state_count"] == 2
    assert result["post_checkpoint_correction_count"] == 1
    assert (snapshot / "runtime/published/fr/20261023T120000Z.json").is_file()
    assert (snapshot / "runtime/published/fr/20261023T130000Z.json").is_file()
    assert (snapshot / "runtime/published/fr/latest.json").is_file()
    assert (snapshot / "runtime/fr-publication/content/publication-receipt.json").is_file()
    assert (snapshot / "runtime/fr-publication/content/correction-receipt.json").is_file()
    assert continuity.verify_committed_snapshot(snapshot) == {
        "status": "passed",
        "debate_id": debate_id,
        "work_id": work_id,
        "history_state_count": 2,
        "post_checkpoint_correction_count": 1,
        "current_state_sha256": result["current_state_sha256"],
    }


def test_check_refuses_incomplete_projection(tmp_path: Path):
    debate_id, _work_id, snapshot = _fixture(tmp_path)
    continuity.sync_signed_french_history(tmp_path, debate_id)
    (snapshot / "runtime/published/fr/20261023T120000Z.json").unlink()

    with pytest.raises(continuity.ContinuityError, match="incomplète"):
        continuity.sync_signed_french_history(tmp_path, debate_id, check_only=True)


def test_sync_refuses_correction_receipt_outside_work(tmp_path: Path):
    debate_id, _work_id, _snapshot = _fixture(tmp_path, receipt_outside_work=True)

    with pytest.raises(continuity.ContinuityError, match="extérieur au périmètre"):
        continuity.sync_signed_french_history(tmp_path, debate_id)


def test_every_committed_latest_snapshot_has_complete_signed_french_succession():
    project_root = Path(__file__).resolve().parents[2]
    snapshots = sorted((project_root / "continuity").glob("*/latest"))
    assert snapshots
    for snapshot in snapshots:
        continuity.verify_committed_snapshot(snapshot)
