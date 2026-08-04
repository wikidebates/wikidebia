#!/usr/bin/env python3
"""Amorce une première reprise Wikidéb’IA à partir du corpus réellement publié auparavant.

Le script n'écrit jamais sur MediaWiki. Il installe uniquement une copie de l'ancien
corpus sous corpus/<debate_id>.previous-<label>/, emplacement reconnu par le kit 2.2.13.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath


def fail(message: str) -> "NoReturn":
    raise SystemExit(f"ERREUR: {message}")


def safe_extract(archive: Path, target: Path) -> None:
    with zipfile.ZipFile(archive) as zf:
        for info in zf.infolist():
            name = info.filename
            pure = PurePosixPath(name)
            if pure.is_absolute() or ".." in pure.parts:
                fail(f"entrée ZIP dangereuse: {name}")
            destination = (target / Path(*pure.parts)).resolve()
            try:
                destination.relative_to(target.resolve())
            except ValueError:
                fail(f"entrée ZIP hors staging: {name}")
        zf.extractall(target)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Installer l'ancien corpus comme manifeste précédent pour ./wikidebia update"
    )
    parser.add_argument("old_archive", type=Path, help="ZIP exact de la version précédemment publiée")
    parser.add_argument("--project-root", type=Path, default=Path.cwd(), help="racine de l'installation Wikidéb’IA")
    parser.add_argument("--debate-id", default="interdiction_licenciements")
    parser.add_argument("--label", default="2026-07-31")
    args = parser.parse_args()

    archive = args.old_archive.expanduser().resolve()
    root = args.project_root.expanduser().resolve()
    if not archive.is_file():
        fail(f"archive introuvable: {archive}")
    if not (root / "wikidebia").exists():
        fail(f"la racine ne contient pas le lanceur wikidebia: {root}")

    destination = root / "corpus" / f"{args.debate_id}.previous-{args.label}"
    if destination.exists():
        fail(f"destination déjà présente: {destination}")

    with tempfile.TemporaryDirectory(prefix="wikidebia-previous-") as tmp_name:
        stage = Path(tmp_name)
        safe_extract(archive, stage)
        manifests = sorted(stage.rglob("manifest.json"))
        if len(manifests) != 1:
            fail(f"le ZIP doit contenir exactement un manifest.json; trouvé: {len(manifests)}")
        package_root = manifests[0].parent
        manifest = json.loads(manifests[0].read_text(encoding="utf-8"))
        actual_id = str(manifest.get("debate_id") or "")
        if actual_id != args.debate_id:
            fail(f"debate_id inattendu: {actual_id!r} au lieu de {args.debate_id!r}")
        pages = manifest.get("pages") or []
        if not pages:
            fail("le manifeste précédent ne contient aucune page")
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(package_root, destination)

    result = {
        "status": "previous_corpus_installed",
        "debate_id": args.debate_id,
        "destination": str(destination.relative_to(root)),
        "page_count": len(pages),
        "next_step": "relancer ./wikidebia update --archive <nouvelle_archive> --scope all --dry-run",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
