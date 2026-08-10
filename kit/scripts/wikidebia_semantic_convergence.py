#!/usr/bin/env python3
"""Record and verify two-pass semantic convergence for a sealed EN translation.

The convergence receipt is deliberately separate from translation_review.json so
recording an audit pass never mutates the semantic artifact being audited.
"""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any, Mapping

from wikidebia_corpus_build import canonical_json, load_json, now_iso, sha256_bytes, write_json
from wikidebia_editorial_workspace import workspace_receipt_hash
from wikidebia_translation_review import (
    KIT_VERSION,
    NORM_VERSION,
    TRANSLATION_REVIEW_SCHEMA,
    SEMANTIC_CONVERGENCE_SCHEMA,
    SEMANTIC_CONVERGENCE_SUPPORTED,
    SEMANTIC_CONVERGENCE_METHOD_FAMILIES,
    TranslationReviewError,
    _load_workspace,
    semantic_content_sha256,
    translation_review_sha256,
)

RECEIPT_REL = Path("reviews/en/semantic_convergence_review.json")


def convergence_receipt_sha256(receipt: Mapping[str, Any]) -> str:
    data = copy.deepcopy(dict(receipt))
    data.pop("receipt_sha256", None)
    return sha256_bytes(canonical_json(data))


def _assert_review(review: Mapping[str, Any]) -> tuple[str, str]:
    if review.get("schema") != TRANSLATION_REVIEW_SCHEMA or review.get("schema_version") != "1.1":
        raise TranslationReviewError("La convergence sémantique exige une revue de traduction 1.1")
    if review.get("status") != "approved":
        raise TranslationReviewError("La convergence exige une revue de traduction finalisée")
    review_sha = str(review.get("review_sha256") or "")
    if not review_sha or review_sha != translation_review_sha256(review):
        raise TranslationReviewError("Empreinte de revue de traduction invalide")
    semantic_sha = semantic_content_sha256(review)
    if review.get("semantic_content_sha256") != semantic_sha:
        raise TranslationReviewError("Empreinte du contenu sémantique de la revue invalide")
    return review_sha, semantic_sha


def verify_receipt(receipt: Mapping[str, Any], review: Mapping[str, Any], *, require_converged: bool = True) -> None:
    review_sha, semantic_sha = _assert_review(review)
    schema_pair = (str(receipt.get("schema") or ""), str(receipt.get("schema_version") or ""))
    if schema_pair not in SEMANTIC_CONVERGENCE_SUPPORTED:
        raise TranslationReviewError("Schéma du reçu de convergence invalide")
    if receipt.get("translation_review_sha256") != review_sha or receipt.get("semantic_content_sha256") != semantic_sha:
        raise TranslationReviewError("Le reçu de convergence ne correspond plus à la revue scellée")
    if receipt.get("receipt_sha256") != convergence_receipt_sha256(receipt):
        raise TranslationReviewError("Empreinte du reçu de convergence invalide")
    passes = receipt.get("passes") or []
    if not isinstance(passes, list):
        raise TranslationReviewError("Liste de passes de convergence invalide")
    for row in passes:
        if not isinstance(row, dict) or row.get("translation_review_sha256") != review_sha or row.get("semantic_content_sha256") != semantic_sha:
            raise TranslationReviewError("Une passe de convergence ne vise pas l'artefact scellé courant")
    if require_converged:
        if receipt.get("status") != "converged" or len(passes) < 2:
            raise TranslationReviewError("Deux passes sémantiques convergentes sont requises avant application")
        p1, p2 = passes[-2], passes[-1]
        if p1.get("new_certain_errors") != 0 or p2.get("new_certain_errors") != 0:
            raise TranslationReviewError("Les deux dernières passes doivent constater zéro nouvelle erreur certaine")
        if str(p1.get("method") or "").strip().casefold() == str(p2.get("method") or "").strip().casefold():
            raise TranslationReviewError("Les deux passes finales doivent employer des méthodes distinctes")
        if schema_pair[1] == "1.1":
            families = [str(row.get("method_family") or "").strip() for row in (p1, p2)]
            if any(family not in SEMANTIC_CONVERGENCE_METHOD_FAMILIES for family in families):
                raise TranslationReviewError("Les passes 1.1 doivent déclarer une famille de méthode normalisée")
            if families[0] == families[1]:
                raise TranslationReviewError("Les deux passes finales doivent appartenir à des familles de méthodes distinctes")


def record_pass(
    project_root: Path, debate_id: str, work_id: str, *, method_family: str, method: str, reviewer: str,
    note: str, new_certain_errors: int = 0,
) -> dict[str, Any]:
    workspace, meta = _load_workspace(project_root, debate_id, work_id)
    if meta.get("status") not in {"en_translation_review_finalized", "en_translation_applied"}:
        raise TranslationReviewError(f"Statut incompatible avec la convergence sémantique : {meta.get('status')}")
    review = load_json(workspace / "reviews/en/translation_review.json", "revue anglaise")
    review_sha, semantic_sha = _assert_review(review)
    method_family = str(method_family or "").strip()
    method = str(method or "").strip()
    reviewer = str(reviewer or "").strip()
    note = str(note or "").strip()
    if method_family not in SEMANTIC_CONVERGENCE_METHOD_FAMILIES:
        raise TranslationReviewError("Famille de méthode de convergence inconnue")
    if len(method) < 8 or len(reviewer) < 3 or len(note) < 20:
        raise TranslationReviewError("Méthode, relecteur ou note de convergence insuffisamment documentés")
    if not isinstance(new_certain_errors, int) or new_certain_errors < 0:
        raise TranslationReviewError("new_certain_errors doit être un entier positif ou nul")
    path = workspace / RECEIPT_REL
    if path.is_file():
        receipt = load_json(path, "reçu de convergence")
        # Any previously valid receipt is only reusable for this exact immutable review.
        # A legacy 1.0 receipt is readable, but a new pass starts a fresh 1.1 proof chain
        # so every current pass carries a normalized method family.
        if (receipt.get("translation_review_sha256") != review_sha
                or receipt.get("semantic_content_sha256") != semantic_sha
                or receipt.get("schema") != SEMANTIC_CONVERGENCE_SCHEMA
                or receipt.get("schema_version") != "1.1"):
            receipt = {}
    else:
        receipt = {}
    if not receipt:
        receipt = {
            "schema": SEMANTIC_CONVERGENCE_SCHEMA,
            "schema_version": "1.1",
            "normative_revision": NORM_VERSION,
            "kit_version": KIT_VERSION,
            "debate_id": debate_id,
            "work_id": work_id,
            "translation_review_sha256": review_sha,
            "semantic_content_sha256": semantic_sha,
            "status": "in_progress",
            "passes": [],
            "converged_at": None,
            "receipt_sha256": None,
        }
    pass_row = {
        "pass_id": f"P{len(receipt['passes']) + 1:03d}",
        "method_family": method_family,
        "method": method,
        "reviewer": reviewer,
        "reviewed_at": now_iso(),
        "note": note,
        "new_certain_errors": new_certain_errors,
        "translation_review_sha256": review_sha,
        "semantic_content_sha256": semantic_sha,
    }
    receipt["passes"].append(pass_row)
    trailing = []
    for row in reversed(receipt["passes"]):
        if row.get("new_certain_errors") != 0:
            break
        trailing.append(row)
    trailing.reverse()
    converged = (
        len(trailing) >= 2
        and str(trailing[-2].get("method") or "").strip().casefold()
            != str(trailing[-1].get("method") or "").strip().casefold()
        and str(trailing[-2].get("method_family") or "").strip()
            != str(trailing[-1].get("method_family") or "").strip()
    )
    receipt["status"] = "converged" if converged else ("requires_revision" if new_certain_errors else "in_progress")
    receipt["converged_at"] = pass_row["reviewed_at"] if converged else None
    receipt["receipt_sha256"] = None
    receipt["receipt_sha256"] = convergence_receipt_sha256(receipt)
    write_json(path, receipt)
    meta = copy.deepcopy(meta)
    meta["kit_version"] = KIT_VERSION
    meta["semantic_convergence"] = {
        "status": receipt["status"],
        "receipt_path": str(RECEIPT_REL).replace("\\", "/"),
        "receipt_sha256": receipt["receipt_sha256"],
        "semantic_content_sha256": semantic_sha,
        "pass_count": len(receipt["passes"]),
    }
    meta["workspace_sha256"] = None
    meta["workspace_sha256"] = workspace_receipt_hash(meta)
    write_json(workspace / "workspace.json", meta)
    return {
        "status": receipt["status"], "debate_id": debate_id, "work_id": work_id,
        "pass_count": len(receipt["passes"]), "receipt_sha256": receipt["receipt_sha256"],
        "semantic_content_sha256": semantic_sha,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Record a semantic convergence pass")
    parser.add_argument("debate_id")
    parser.add_argument("--work-id", required=True)
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--method-family", required=True, choices=sorted(SEMANTIC_CONVERGENCE_METHOD_FAMILIES))
    parser.add_argument("--method", required=True)
    parser.add_argument("--reviewer", required=True)
    parser.add_argument("--note", required=True)
    parser.add_argument("--new-certain-errors", type=int, default=0)
    parser.add_argument("--machine-readable", action="store_true")
    args = parser.parse_args()
    try:
        result = record_pass(Path(args.project_root).resolve(), args.debate_id, args.work_id,
                             method_family=args.method_family, method=args.method, reviewer=args.reviewer, note=args.note,
                             new_certain_errors=args.new_certain_errors)
    except TranslationReviewError as exc:
        if args.machine_readable:
            print(json.dumps({"status": "blocked", "error": str(exc)}, ensure_ascii=False))
        else:
            print(f"BLOQUÉ: {exc}")
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True) if args.machine_readable else result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
