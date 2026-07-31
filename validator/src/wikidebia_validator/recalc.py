from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from . import __version__
from .batches import collect_batches
from .graph import compute_derived, structural_sha256
from .package import PackageContext
from .report import Report, portable_display_path


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=False, allow_nan=False) + "\n", encoding="utf-8", newline="\n")


def recalc_graph(ctx: PackageContext) -> list[str]:
    registry = ctx.registry()
    if not registry:
        return []
    graph = registry.get("graph") or {}
    counts, per_node = compute_derived(registry)
    graph["derived_counts"] = counts
    graph.setdefault("depth_policy", {})["maximum_observed"] = counts["maximum_depth"]
    for node in graph.get("nodes", []):
        if node.get("status") == "active" and node.get("id") in per_node:
            node["derived"] = per_node[node["id"]]
        elif node.get("status") != "active":
            node.pop("derived", None)
    if (graph.get("lifecycle") or {}).get("status") == "locked":
        graph["lifecycle"]["structural_sha256"] = structural_sha256(registry)
    registry_path = ctx.safe_path(ctx.core_paths()["registry"])
    if not registry_path:
        return []
    write_json(registry_path, registry)
    changed = [ctx.core_paths()["registry"]]
    projection = ctx.graph_projection()
    if projection is not None:
        for key in ("lifecycle", "depth_policy", "nodes", "edges", "occurrences", "derived_counts"):
            projection[key] = graph.get(key)
        proj_path = ctx.safe_path(ctx.core_paths()["graph_json"])
        if proj_path:
            write_json(proj_path, projection)
            changed.append(ctx.core_paths()["graph_json"])
    return changed


def recalc_aggregates(ctx: PackageContext) -> list[str]:
    manifest = ctx.manifest() or {}
    pages = manifest.get("pages", [])
    page_by_key = {(p.get("page_id"), p.get("language")): p for p in pages}
    changed: list[str] = []
    for batch in collect_batches(ctx).values():
        rel = (batch.get("outputs") or {}).get("aggregate_path")
        if not rel:
            continue
        chunks = []
        for nid in batch.get("node_ids", []):
            page = page_by_key.get((nid, batch.get("language")))
            if not page:
                continue
            text = ctx.read_text(page.get("file_path"))
            if text is None:
                continue
            chunks.append(f"===== PAGE : {page.get('canonical_title')} =====\n{text.rstrip()}\n")
        output = "\n".join(chunks)
        path = ctx.safe_path(rel)
        if path:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(output, encoding="utf-8", newline="\n")
            changed.append(rel)
    return changed


def recalc_hashes(ctx: PackageContext) -> list[str]:
    manifest = ctx.manifest()
    registry = ctx.registry()
    if not manifest or not registry:
        return []
    for page in manifest.get("pages", []):
        rel = page.get("file_path")
        if rel and ctx.exists(rel):
            page["sha256"] = ctx.sha256(rel)
    page_map = {(p.get("page_id"), p.get("language")): p for p in manifest.get("pages", [])}
    debate = registry.get("debate") or {}
    debate_id = debate.get("id")
    for lang in ("fr", "en"):
        rec = ((debate.get("pages") or {}).get(lang) or {})
        page = page_map.get((debate_id, lang))
        if page:
            rec.setdefault("file", {})["sha256"] = page.get("sha256")
    for node in registry.get("graph", {}).get("nodes", []):
        for lang in ("fr", "en"):
            page = page_map.get((node.get("id"), lang))
            if page:
                ((node.setdefault("pages", {}).setdefault(lang, {})).setdefault("file", {}))["sha256"] = page.get("sha256")
    for batch in manifest.get("batches", []):
        rel = (batch.get("outputs") or {}).get("aggregate_path")
        if rel and ctx.exists(rel):
            batch["outputs"]["aggregate_sha256"] = ctx.sha256(rel)
    write_json(ctx.root / "manifest.json", manifest)
    reg_path = ctx.safe_path(ctx.core_paths()["registry"])
    if reg_path:
        write_json(reg_path, registry)
    return ["manifest.json", ctx.core_paths()["registry"]]


def recalculate(root: str | Path, *, graph: bool, aggregates: bool, hashes: bool, write: bool) -> tuple[list[str], Report]:
    root_path = Path(root).resolve()
    report = Report(__version__, portable_display_path(root), ["recalc"])
    if not write:
        report.error("WDV-WF-002", "Le mode recalcul exige --write ; aucune modification n'a été effectuée")
        return [], report
    ctx = PackageContext(root_path, report)
    changed: list[str] = []
    if graph:
        changed.extend(recalc_graph(ctx))
        ctx.cache.clear()
    if aggregates:
        changed.extend(recalc_aggregates(ctx))
        ctx.cache.clear()
    if hashes:
        changed.extend(recalc_hashes(ctx))
    report.metrics["changed_files"] = sorted(set(changed))
    return sorted(set(changed)), report
