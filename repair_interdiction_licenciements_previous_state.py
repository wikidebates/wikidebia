#!/usr/bin/env python3
"""Create a normalized historical corpus for the first Wikidéb'IA update.

This script does not contact MediaWiki and does not modify the active corpus.
It reads an already generated update plan, verifies that every manual-review
page is textually identical between the historical corpus and the remote wiki
under the kit's own wikicode normalization, then copies the historical corpus
into a new ``*.previous-normalized-*`` directory and replaces only the page
``sha256`` values in its manifest with normalized-content hashes.

The original historical corpus remains untouched.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import shutil
import sys
from pathlib import Path
from typing import Any


def normalize_wikicode(text: str) -> str:
    """Match Wikidéb'IA kit 2.2.13 normalization exactly."""
    return text.replace("\r\n", "\n").replace("\r", "\n").rstrip("\n")


def sha_text(text: str) -> str:
    return hashlib.sha256(normalize_wikicode(text).encode("utf-8")).hexdigest()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha_object(value: Any) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"JSON illisible : {path}") from exc
    if not isinstance(value, dict):
        raise RuntimeError(f"Objet JSON attendu : {path}")
    return value


def write_json(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def derive_destination(source_root: Path) -> Path:
    name = source_root.name
    marker = ".previous-"
    if marker in name:
        return source_root.with_name(name.replace(marker, ".previous-normalized-", 1))
    return source_root.with_name(name + ".normalized")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Répare les empreintes d'un ancien manifeste sans toucher au corpus actif."
    )
    parser.add_argument("--project-root", default=".", help="Racine de l'installation Wikidéb'IA")
    parser.add_argument("--plan", required=True, help="Chemin du update-plan.json ayant produit manual_review")
    parser.add_argument(
        "--destination",
        help="Dossier de corpus historique corrigé (par défaut : *.previous-normalized-*)",
    )
    parser.add_argument(
        "--replace-existing",
        action="store_true",
        help="Remplacer un dossier de destination déjà présent",
    )
    args = parser.parse_args()

    project_root = Path(args.project_root).expanduser().resolve()
    plan_path = Path(args.plan).expanduser()
    if not plan_path.is_absolute():
        plan_path = (project_root / plan_path).resolve()
    plan = load_json(plan_path)

    if plan.get("debate_id") != "interdiction_licenciements":
        raise RuntimeError("Le plan ne concerne pas interdiction_licenciements")
    if plan.get("kit_version") != "2.2.13":
        raise RuntimeError(f"Kit inattendu dans le plan : {plan.get('kit_version')!r}")
    state_source = plan.get("state_source") or {}
    if state_source.get("kind") != "previous_installed_manifest":
        raise RuntimeError("Le plan n'utilise pas un ancien manifeste installé")

    manifest_rel = state_source.get("manifest")
    if not isinstance(manifest_rel, str) or not manifest_rel:
        raise RuntimeError("Chemin du manifeste historique absent du plan")
    source_manifest = (project_root / manifest_rel).resolve()
    if not source_manifest.is_file():
        raise RuntimeError(f"Manifeste historique introuvable : {source_manifest}")
    source_root = source_manifest.parent

    destination = Path(args.destination).expanduser() if args.destination else derive_destination(source_root)
    if not destination.is_absolute():
        destination = (project_root / destination).resolve()
    if destination == source_root:
        raise RuntimeError("La destination doit être distincte du corpus historique original")
    if destination.exists():
        if not args.replace_existing:
            raise RuntimeError(f"Destination déjà présente : {destination} (utiliser --replace-existing)")
        shutil.rmtree(destination)

    manifest = load_json(source_manifest)
    if manifest.get("debate_id") != plan.get("debate_id"):
        raise RuntimeError("debate_id divergent entre le plan et le manifeste historique")

    pages = manifest.get("pages") or []
    if not isinstance(pages, list) or not pages:
        raise RuntimeError("Aucune page dans le manifeste historique")
    page_rows: dict[tuple[str, str], dict[str, Any]] = {}
    for row in pages:
        if not isinstance(row, dict):
            raise RuntimeError("Entrée de page invalide dans le manifeste")
        key = (str(row.get("language") or ""), str(row.get("page_id") or ""))
        if not all(key) or key in page_rows:
            raise RuntimeError(f"Clé de page absente ou dupliquée : {key}")
        page_rows[key] = row

    manual_ops = ((plan.get("operations") or {}).get("manual_review") or [])
    comparisons = plan.get("comparisons") or []
    if len(manual_ops) != len(comparisons) or not comparisons:
        raise RuntimeError("Le plan ne contient pas un ensemble cohérent de comparaisons manual_review")

    checked: list[dict[str, Any]] = []
    for comparison in comparisons:
        if not isinstance(comparison, dict):
            raise RuntimeError("Comparaison invalide")
        language = str(comparison.get("language") or "")
        page_id = str(comparison.get("page_id") or "")
        row = page_rows.get((language, page_id))
        if row is None:
            raise RuntimeError(f"Page absente du manifeste historique : {language}/{page_id}")
        diffs = comparison.get("diffs") or {}
        if str(diffs.get("published_to_remote") or ""):
            raise RuntimeError(
                f"Différence réelle entre l'ancien corpus et le wiki : {language}/{page_id}. "
                "La normalisation automatique est refusée."
            )
        rel = str(row.get("file_path") or row.get("source_path") or "")
        source_file = source_root / rel
        if not source_file.is_file():
            raise RuntimeError(f"Fichier historique absent : {source_file}")
        text = source_file.read_text(encoding="utf-8")
        normalized_sha = sha_text(text)
        remote_sha = str(comparison.get("remote_sha256") or "")
        published_sha = str(comparison.get("published_sha256") or "")
        manifest_sha = str(row.get("sha256") or "")
        if published_sha != manifest_sha:
            raise RuntimeError(f"Le plan ne correspond plus au manifeste : {language}/{page_id}")
        if normalized_sha != remote_sha:
            raise RuntimeError(
                f"L'ancien texte normalisé ne correspond pas au wiki : {language}/{page_id}"
            )
        checked.append(
            {
                "language": language,
                "page_id": page_id,
                "title": comparison.get("title"),
                "raw_manifest_sha256": manifest_sha,
                "normalized_content_sha256": normalized_sha,
                "remote_sha256": remote_sha,
                "comparison_id": comparison.get("comparison_id"),
            }
        )

    # All manual-review pages are proven equivalent to the historical files.
    shutil.copytree(source_root, destination)
    destination_manifest = destination / source_manifest.name
    corrected = load_json(destination_manifest)

    changed = 0
    for row in corrected.get("pages") or []:
        rel = str(row.get("file_path") or row.get("source_path") or "")
        page_path = destination / rel
        if not page_path.is_file():
            raise RuntimeError(f"Fichier absent dans la copie : {page_path}")
        normalized_sha = sha_text(page_path.read_text(encoding="utf-8"))
        if row.get("sha256") != normalized_sha:
            row["sha256"] = normalized_sha
            changed += 1

    original_manifest_sha = sha_file(source_manifest)
    write_json(destination_manifest, corrected)
    corrected_manifest_sha = sha_file(destination_manifest)

    receipt: dict[str, Any] = {
        "receipt_version": "wikidebia-historical-manifest-normalization-1.0",
        "created_at": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "debate_id": plan.get("debate_id"),
        "kit_version_observed": plan.get("kit_version"),
        "plan_path": str(plan_path.relative_to(project_root)) if plan_path.is_relative_to(project_root) else plan_path.name,
        "plan_sha256": plan.get("plan_sha256"),
        "source_manifest": str(source_manifest.relative_to(project_root)) if source_manifest.is_relative_to(project_root) else source_manifest.name,
        "source_manifest_file_sha256": original_manifest_sha,
        "destination_manifest": str(destination_manifest.relative_to(project_root)) if destination_manifest.is_relative_to(project_root) else destination_manifest.name,
        "destination_manifest_file_sha256": corrected_manifest_sha,
        "normalization": "CRLF/CR converted to LF, then all trailing LF removed before UTF-8 SHA-256",
        "historical_page_count": len(corrected.get("pages") or []),
        "manifest_page_hashes_changed": changed,
        "manual_review_pages_proven_textually_identical": len(checked),
        "remote_write_performed": False,
        "verification": checked,
    }
    receipt["receipt_sha256"] = sha_object(receipt)
    receipt_path = destination / "HISTORICAL_STATE_NORMALIZATION_RECEIPT.json"
    write_json(receipt_path, receipt)

    output = {
        "status": "normalized_previous_corpus_created",
        "debate_id": plan.get("debate_id"),
        "source": str(source_root.relative_to(project_root)) if source_root.is_relative_to(project_root) else str(source_root),
        "destination": str(destination.relative_to(project_root)) if destination.is_relative_to(project_root) else str(destination),
        "page_count": len(corrected.get("pages") or []),
        "page_hashes_changed": changed,
        "manual_review_pages_verified": len(checked),
        "receipt": str(receipt_path.relative_to(project_root)) if receipt_path.is_relative_to(project_root) else str(receipt_path),
        "next_step": "Relancer exactement la commande update --dry-run avec la même archive et --no-delete.",
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERREUR : {exc}", file=sys.stderr)
        raise SystemExit(1)
