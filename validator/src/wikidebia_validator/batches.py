from __future__ import annotations

from collections import defaultdict
from typing import Any

from .graph import state_at_least, structural_sha256
from .package import PackageContext


def collect_batches(ctx: PackageContext) -> dict[str, dict[str, Any]]:
    sources: list[tuple[str, dict[str, Any]]] = []
    manifest = ctx.manifest() or {}
    for b in manifest.get("batches", []):
        sources.append(("manifest.json", b))
    registry = ctx.registry() or {}
    for b in registry.get("batches", []):
        sources.append((ctx.core_paths()["registry"], b))
    for rel in ("data/lots_fr.json", "data/lots_en.json"):
        data = ctx.load_json(rel)
        if isinstance(data, dict):
            for b in data.get("batches", []):
                sources.append((rel, b))
    out: dict[str, dict[str, Any]] = {}
    origin: dict[str, str] = {}
    for rel, batch in sources:
        bid = batch.get("id")
        if not bid:
            continue
        if bid in out and out[bid] != batch:
            ctx.report.error("WDV-BAT-001", f"Définitions divergentes du lot {bid}", path=rel, details={"first_origin": origin[bid]})
        else:
            out[bid] = batch
            origin[bid] = rel
    return out


def validate_batches(ctx: PackageContext) -> None:
    registry = ctx.registry()
    if not registry:
        return
    batches = collect_batches(ctx)
    nodes = {n.get("id"): n for n in registry.get("graph", {}).get("nodes", []) if n.get("status") == "active"}
    manifest = ctx.manifest() or {}
    debate_id = manifest.get("debate_id") or (registry.get("debate") or {}).get("id")
    structure_hash = structural_sha256(registry)
    ownership: dict[str, dict[str, list[str]]] = {"fr": defaultdict(list), "en": defaultdict(list)}

    for bid, b in batches.items():
        lang = b.get("language")
        if b.get("debate_id") != debate_id:
            ctx.report.error("WDV-BAT-001", f"Lot {bid} rattaché au mauvais débat", details={"declared": b.get("debate_id"), "expected": debate_id})
        node_ids = b.get("node_ids", [])
        deps = b.get("dependency_node_ids", [])
        roots = b.get("root_node_ids", [])
        for nid in node_ids + deps + roots:
            if nid not in nodes:
                ctx.report.error("WDV-BAT-001", f"Lot {bid} référence un nœud actif inexistant : {nid}")
        if not set(roots).issubset(set(node_ids)):
            ctx.report.error("WDV-BAT-004", f"Les racines du lot {bid} doivent appartenir à node_ids")
        overlap_deps = set(node_ids) & set(deps)
        if overlap_deps:
            ctx.report.error("WDV-BAT-004", f"Le lot {bid} déclare comme dépendances des pages qu'il possède", details={"node_ids": sorted(overlap_deps)})
        if lang in ownership and b.get("status") not in {"obsolete", "failed"}:
            for nid in node_ids:
                ownership[lang][nid].append(bid)
        inputs = b.get("inputs") or {}
        # registry_sha256 identifies the immutable input snapshot. The current registry
        # normally changes when the batch writes its results, so comparing it to the
        # current file would create false positives. Compare it to the input handoff.
        input_registry_hash = inputs.get("registry_sha256")
        handoff_path = inputs.get("handoff_path")
        if input_registry_hash and handoff_path and ctx.exists(handoff_path):
            handoff = ctx.load_json(handoff_path)
            if isinstance(handoff, dict):
                candidates = [x.get("sha256") for x in handoff.get("required_files", []) if x.get("path") == ctx.core_paths()["registry"]]
                if candidates and candidates[0] != input_registry_hash:
                    ctx.report.error("WDV-BAT-005", f"Empreinte d'entrée du registre incohérente entre le lot et le handoff {bid}", details={"batch": input_registry_hash, "handoff": candidates[0]})
        corrective = ((manifest.get("normative_versions") or {}).get("consolidated_norm") in {"1.1.0", "1.1.1", "1.1.2", "1.1.3", "1.1.4", "1.1.5", "1.1.6", "1.1.7", "1.1.8", "1.1.9", "1.2.0", "1.2.1", "1.2.2", "1.2.3", "1.2.4", "1.2.5", "1.2.6", "1.2.7", "1.2.8", "1.2.9", "1.2.10", "1.2.11", "1.2.12", "1.2.13", "1.2.14", "1.2.15", "1.2.16", "1.2.17", "1.2.18", "1.2.19", "1.2.20"})
        if inputs.get("structural_sha256") and inputs["structural_sha256"] != structure_hash and not corrective:
            level = "ERROR" if b.get("status") in {"generated", "validated", "released"} else "WARNING"
            ctx.report.add("WDV-BAT-005", level, f"Empreinte structurelle obsolète pour le lot {bid}", details={"declared": inputs["structural_sha256"], "computed": structure_hash})
        aggregate = (b.get("outputs") or {}).get("aggregate_path")
        aggregate_hash = (b.get("outputs") or {}).get("aggregate_sha256")
        if aggregate_hash:
            actual = ctx.sha256(aggregate)
            if actual != aggregate_hash:
                ctx.report.error("WDV-FS-003", f"Empreinte de l'agrégat incorrecte pour {bid}", path=aggregate, details={"declared": aggregate_hash, "computed": actual})

    for lang in ("fr", "en"):
        for nid, owners in ownership[lang].items():
            if len(owners) > 1:
                ctx.report.error("WDV-BAT-002", f"Le nœud {nid} appartient à plusieurs lots {lang}", details={"batches": owners})
        stage = "fr_arguments_in_progress" if lang == "fr" else "en_arguments_in_progress"
        if state_at_least(manifest.get("global_status"), stage):
            missing = sorted(set(nodes) - set(ownership[lang]))
            if missing:
                ctx.report.error("WDV-BAT-003", f"Nœuds actifs non couverts par les lots {lang}", details={"node_ids": missing})

    # Cross-check page manifests.
    pages = manifest.get("pages", [])
    by_key = {(p.get("page_id"), p.get("language")): p for p in pages if p.get("page_type") == "argument"}
    for lang in ("fr", "en"):
        for nid, owners in ownership[lang].items():
            page = by_key.get((nid, lang))
            if page and owners and page.get("batch_id") != owners[0]:
                ctx.report.error("WDV-BAT-004", f"Le manifeste de page {nid}/{lang} indique un autre lot", details={"page_batch": page.get("batch_id"), "owner": owners[0]})
    ctx.report.metrics["batches"] = {"count": len(batches), "fr_owned": len(ownership["fr"]), "en_owned": len(ownership["en"])}
