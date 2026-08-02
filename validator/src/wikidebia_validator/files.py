from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from .graph import state_at_least
from .package import PackageContext


def validate_hash(ctx: PackageContext, rel: str, declared: str | None, *, required: bool = False) -> None:
    if required and not ctx.exists(rel):
        ctx.report.error("WDV-FS-004", "Fichier déclaré mais absent", path=rel)
        return
    if declared:
        actual = ctx.sha256(rel)
        if actual != declared:
            ctx.report.error("WDV-FS-003", "Empreinte SHA-256 incorrecte", path=rel, details={"declared": declared, "computed": actual})


def validate_files(ctx: PackageContext) -> None:
    manifest = ctx.manifest()
    registry = ctx.registry()
    if not manifest or not registry:
        return
    status = manifest.get("global_status")
    core = ctx.core_paths()
    # Core files become required progressively.
    ctx.read_text("manifest.json", required=True)
    for key, rel in core.items():
        required = key in {"scope", "registry"} or state_at_least(status, "graph_draft")
        if required and not ctx.exists(rel):
            ctx.report.error("WDV-FS-001", f"Fichier cœur obligatoire absent : {key}", path=rel)

    pages = manifest.get("pages", [])
    keys = [(p.get("page_id"), p.get("language")) for p in pages]
    for key, n in Counter(keys).items():
        if n > 1:
            ctx.report.error("WDV-FS-006", f"Manifeste de page dupliqué : {key}", path="manifest.json")
    declared_file_paths: dict[str, tuple[str, str]] = {}
    for p in pages:
        rel = p.get("file_path")
        if not rel:
            continue
        key = (p.get("page_id"), p.get("language"))
        if rel in declared_file_paths and declared_file_paths[rel] != key:
            ctx.report.error("WDV-FS-006", f"Même fichier déclaré pour plusieurs pages : {rel}", path="manifest.json")
        declared_file_paths[rel] = key
        generated = p.get("status") in {"generated", "validated", "published"}
        validate_hash(ctx, rel, p.get("sha256"), required=generated)
        if generated and not p.get("sha256"):
            ctx.report.error("WDV-FS-003", "Empreinte absente pour une page générée", path=rel)

    # Cross-check page manifests with registry page records.
    reg_pages: dict[tuple[str, str], dict[str, Any]] = {}
    debate = registry.get("debate") or {}
    debate_id = debate.get("id")
    for lang in ("fr", "en"):
        rec = ((debate.get("pages") or {}).get(lang) or {})
        reg_pages[(debate_id, lang)] = rec
    for n in registry.get("graph", {}).get("nodes", []):
        if n.get("status") != "active":
            continue
        for lang in ("fr", "en"):
            reg_pages[(n.get("id"), lang)] = ((n.get("pages") or {}).get(lang) or {})
    page_map = {(p.get("page_id"), p.get("language")): p for p in pages}
    for key, rec in reg_pages.items():
        generation = rec.get("generation") or {}
        file_rec = rec.get("file") or {}
        page = page_map.get(key)
        generated = generation.get("status") in {"generated", "validated"} or file_rec.get("status") in {"present", "validated"}
        if generated and not page:
            ctx.report.error("WDV-FS-004", f"Page {key[0]}/{key[1]} générée dans le registre mais absente du manifeste", path="manifest.json")
            continue
        if page:
            expected_title = rec.get("canonical_title")
            if expected_title and page.get("canonical_title") != expected_title:
                ctx.report.error("WDV-FS-006", f"Titre divergent entre registre et manifeste pour {key[0]}/{key[1]}", details={"registry": expected_title, "manifest": page.get("canonical_title")})
            if file_rec.get("path") and page.get("file_path") != file_rec.get("path"):
                ctx.report.error("WDV-FS-006", f"Chemin divergent entre registre et manifeste pour {key[0]}/{key[1]}")
            if file_rec.get("sha256") and page.get("sha256") != file_rec.get("sha256"):
                ctx.report.error("WDV-FS-003", f"Empreinte divergente entre registre et manifeste pour {key[0]}/{key[1]}")
            if generation.get("creation_date") and page.get("creation_date") != generation.get("creation_date"):
                ctx.report.error("WDV-MWK-010", f"Date de création divergente entre registre et manifeste pour {key[0]}/{key[1]}")

    # Release manifest exact file inventory.
    release_path = (manifest.get("release") or {}).get("release_manifest_path") or ("release_manifest.json" if ctx.exists("release_manifest.json") else None)
    if release_path and ctx.exists(release_path):
        release = ctx.load_json(release_path)
        if isinstance(release, dict):
            seen: set[str] = set()
            for item in release.get("files", []):
                rel = item.get("path")
                if rel in seen:
                    ctx.report.error("WDV-FS-006", f"Fichier dupliqué dans le manifeste de libération : {rel}", path=release_path)
                seen.add(rel)
                p = ctx.safe_path(rel)
                if not p or not p.is_file():
                    ctx.report.error("WDV-FS-004", "Fichier du manifeste de libération absent", path=rel)
                    continue
                actual_size = p.stat().st_size
                if actual_size != item.get("size_bytes"):
                    ctx.report.error("WDV-FS-003", "Taille incorrecte dans le manifeste de libération", path=rel, details={"declared": item.get("size_bytes"), "computed": actual_size})
                validate_hash(ctx, rel, item.get("sha256"), required=True)
            if release_path in seen:
                ctx.report.error("WDV-FS-006", "release_manifest.json doit s'exclure lui-même", path=release_path)

    # Historical handoffs remain immutable traces during a 1.1 corrective reprise.
    # Their hashes describe the input state of their original Work, not the current files.
    corrective = (manifest.get("normative_versions") or {}).get("consolidated_norm") in {"1.1.0", "1.1.1", "1.1.2", "1.1.3", "1.1.4", "1.1.5", "1.1.6", "1.1.7", "1.1.8", "1.1.9", "1.2.0", "1.2.1", "1.2.2", "1.2.3", "1.2.4", "1.2.5", "1.2.6", "1.2.7", "1.2.8", "1.2.9", "1.2.10", "1.2.11", "1.2.12", "1.2.13", "1.2.14", "1.2.15", "1.2.16", "1.2.17", "1.2.18", "1.2.19", "1.2.20", "1.2.21", "1.2.22", "1.2.23", "1.2.24", "1.2.25", "1.2.26"}
    if not corrective:
        for path in sorted(ctx.iter_files("handoff/*.json")):
            rel = ctx.relative(path)
            data = ctx.load_json(rel)
            if not isinstance(data, dict) or data.get("template_mode"):
                continue
            for item in data.get("required_files", []):
                required = bool(item.get("required"))
                validate_hash(ctx, item.get("path"), item.get("sha256"), required=required)

    ctx.report.metrics["files"] = {"declared_pages": len(pages), "core_files": len(core)}
