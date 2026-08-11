#!/usr/bin/env python3
"""Prepare and apply a structural correction after a rejected graph review.

The correction surface is deliberately narrower than the master registry: an
external reviewer may change occurrence placement, parentage, relation, root
branch, order and primary/secondary role. The program then rebuilds edges,
depths, branches, render flags and all derived graph data deterministically.
"""
from __future__ import annotations

import copy
import datetime as dt
from collections import defaultdict
from pathlib import Path
from typing import Any, Mapping

from wikidebia_corpus_build import (
    GRAPH_CORRECTION_REVIEW,
    REVIEW_ENVELOPE,
    REVIEW_REPORT_JSON,
    CorpusBuildError,
    build_payload_sha256,
    load_json,
    now_iso,
    resolve_build,
    validate_debate_id,
    write_json,
)
from wikidebia_corpus_init import compute_derived, _markdown_graph

CORRECTION_SCHEMA = "wikidebia-graph-correction-1.0"


def _active_graph(registry: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    graph = registry.get("graph") or {}
    nodes = [copy.deepcopy(x) for x in graph.get("nodes") or [] if x.get("status") == "active"]
    node_ids = {x.get("id") for x in nodes}
    edges = [copy.deepcopy(x) for x in graph.get("edges") or [] if x.get("status") == "active"]
    edge_ids = {x.get("id") for x in edges}
    occurrences = [
        copy.deepcopy(x) for x in graph.get("occurrences") or []
        if x.get("node_id") in node_ids and (x.get("edge_id") is None or x.get("edge_id") in edge_ids)
    ]
    return nodes, edges, occurrences


def make_correction_template(build: Path, debate_id: str) -> dict[str, Any]:
    debate_id = validate_debate_id(debate_id)
    registry = load_json(build / "data/registre_debat.json", "registre maître")
    rejected = load_json(build / REVIEW_ENVELOPE, "revue du graphe rejetée")
    report = load_json(build / REVIEW_REPORT_JSON, "rapport de revue rejetée")
    if rejected.get("decision") != "rejected" or report.get("status") != "rejected":
        raise CorpusBuildError("Une correction de graphe ne peut être préparée qu'après une revue rejetée")
    rejected_sha = str(rejected.get("review_sha256") or "")
    if not rejected_sha or report.get("review_sha256") != rejected_sha:
        raise CorpusBuildError("La revue rejetée n'est pas scellée de manière cohérente")

    _, edges, occurrences = _active_graph(registry)
    edge_by_id = {x.get("id"): x for x in edges}
    rows = []
    for occ in sorted(occurrences, key=lambda x: str(x.get("id"))):
        edge = edge_by_id.get(occ.get("edge_id")) or {}
        rows.append({
            "occurrence_id": occ.get("id"),
            "node_id": occ.get("node_id"),
            "parent_occurrence_id": occ.get("parent_occurrence_id"),
            "relation": edge.get("relation") if occ.get("parent_occurrence_id") is not None else None,
            "branch": occ.get("branch") if occ.get("parent_occurrence_id") is None else None,
            "order": occ.get("order"),
            "occurrence_role": occ.get("occurrence_role"),
        })
    doc = {
        "schema": CORRECTION_SCHEMA,
        "schema_version": "1.0",
        "debate_id": debate_id,
        "source_build_sha256": build_payload_sha256(build),
        "rejected_review_sha256": rejected_sha,
        "status": "pending",
        "reviewer": "",
        "reviewed_at": None,
        "notes": "",
        "placements": rows,
    }
    write_json(build / GRAPH_CORRECTION_REVIEW, doc)
    return {"status": "correction_prepared", "occurrences": len(rows), "path": GRAPH_CORRECTION_REVIEW}


def _validate_timestamp(value: Any) -> bool:
    try:
        parsed = dt.datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return parsed.utcoffset() is not None
    except Exception:
        return False


def _validate_and_rebuild(registry: dict[str, Any], correction: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    nodes, old_edges, old_occurrences = _active_graph(registry)
    node_ids = {str(x["id"]) for x in nodes}
    old_by_occ = {str(x["id"]): x for x in old_occurrences}
    rows = correction.get("placements")
    if not isinstance(rows, list):
        raise CorpusBuildError("graph_correction.placements doit être une liste")
    by_occ: dict[str, dict[str, Any]] = {}
    for raw in rows:
        if not isinstance(raw, dict):
            raise CorpusBuildError("Entrée de correction de graphe invalide")
        oid = str(raw.get("occurrence_id") or "")
        if oid not in old_by_occ or oid in by_occ:
            raise CorpusBuildError(f"Occurrence de correction inconnue ou dupliquée : {oid!r}")
        if raw.get("node_id") != old_by_occ[oid].get("node_id"):
            raise CorpusBuildError(f"Le node_id de {oid} est immuable pendant la correction de placement")
        by_occ[oid] = dict(raw)
    if set(by_occ) != set(old_by_occ):
        missing = sorted(set(old_by_occ) - set(by_occ))
        extra = sorted(set(by_occ) - set(old_by_occ))
        raise CorpusBuildError(f"Couverture de correction incomplète (missing={missing[:5]}, extra={extra[:5]})")

    # Basic field and parent validation.
    children: dict[str, list[str]] = defaultdict(list)
    roots: list[str] = []
    primaries_by_node: dict[str, list[str]] = defaultdict(list)
    for oid, row in by_occ.items():
        try:
            order = int(row.get("order"))
        except Exception as exc:
            raise CorpusBuildError(f"order invalide pour {oid}") from exc
        if order < 1:
            raise CorpusBuildError(f"order doit être >= 1 pour {oid}")
        row["order"] = order
        role = row.get("occurrence_role")
        if role not in {"primary", "secondary"}:
            raise CorpusBuildError(f"occurrence_role invalide pour {oid}")
        primaries_by_node[str(row["node_id"])].append(oid) if role == "primary" else None
        parent = row.get("parent_occurrence_id")
        if parent is None:
            if row.get("relation") is not None:
                raise CorpusBuildError(f"Une racine ne peut pas avoir de relation : {oid}")
            if row.get("branch") not in {"pro", "con"}:
                raise CorpusBuildError(f"Branche racine invalide pour {oid}")
            if role != "primary":
                raise CorpusBuildError(f"Une racine doit être une occurrence primaire : {oid}")
            roots.append(oid)
        else:
            parent = str(parent)
            if parent not in by_occ or parent == oid:
                raise CorpusBuildError(f"Parent invalide pour {oid}: {parent!r}")
            if row.get("relation") not in {"justification", "objection"}:
                raise CorpusBuildError(f"Relation invalide pour {oid}")
            if row.get("branch") is not None:
                raise CorpusBuildError(f"La branche des occurrences subordonnées est dérivée et doit rester null : {oid}")
            children[parent].append(oid)

    for node_id in node_ids:
        primaries = primaries_by_node.get(node_id, [])
        if len(primaries) != 1:
            raise CorpusBuildError(f"Le nœud {node_id} doit posséder exactement une occurrence primaire; trouvé {len(primaries)}")
    for parent, child_ids in children.items():
        if by_occ[parent].get("occurrence_role") != "primary":
            raise CorpusBuildError(f"Une occurrence secondaire ne peut pas porter d'enfants : {parent}")

    # Traverse occurrence forest to detect cycles/unreachable entries and derive depth/branch.
    depth: dict[str, int] = {}
    branch: dict[str, str] = {}
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(oid: str) -> None:
        if oid in visiting:
            raise CorpusBuildError(f"Cycle d'occurrences détecté autour de {oid}")
        if oid in visited:
            return
        visiting.add(oid)
        row = by_occ[oid]
        parent = row.get("parent_occurrence_id")
        if parent is None:
            depth[oid] = 1
            branch[oid] = str(row["branch"])
        else:
            parent = str(parent)
            visit(parent)
            depth[oid] = depth[parent] + 1
            branch[oid] = branch[parent]
        visiting.remove(oid)
        visited.add(oid)

    for oid in sorted(by_occ):
        visit(oid)
    if set(visited) != set(by_occ):
        raise CorpusBuildError("Certaines occurrences sont inaccessibles après correction")

    # Rebuild unique active edges deterministically from occurrence placements.
    triples: dict[tuple[str, str, str], dict[str, Any]] = {}
    for oid, row in by_occ.items():
        parent_id = row.get("parent_occurrence_id")
        if parent_id is None:
            continue
        parent_node = str(by_occ[str(parent_id)]["node_id"])
        child_node = str(row["node_id"])
        relation = str(row["relation"])
        if parent_node == child_node:
            raise CorpusBuildError(f"Auto-relation interdite via {oid} ({parent_node})")
        key = (parent_node, child_node, relation)
        triples.setdefault(key, {"order": int(row["order"])})
        triples[key]["order"] = min(int(triples[key]["order"]), int(row["order"]))
    sorted_triples = sorted(triples, key=lambda x: (x[0], int(triples[x]["order"]), 0 if x[2] == "justification" else 1, x[1]))
    edge_by_triple: dict[tuple[str, str, str], dict[str, Any]] = {}
    edges: list[dict[str, Any]] = []
    for index, key in enumerate(sorted_triples, 1):
        parent_node, child_node, relation = key
        edge = {
            "id": f"E{index:05d}",
            "parent_node_id": parent_node,
            "child_node_id": child_node,
            "relation": relation,
            "order": int(triples[key]["order"]),
            "status": "active",
            "introduced_in_pass": "graph_correction_chatgpt",
        }
        edges.append(edge)
        edge_by_triple[key] = edge

    occurrences: list[dict[str, Any]] = []
    for oid in sorted(by_occ):
        row = by_occ[oid]
        parent_id = row.get("parent_occurrence_id")
        edge_id = None
        if parent_id is not None:
            key = (str(by_occ[str(parent_id)]["node_id"]), str(row["node_id"]), str(row["relation"]))
            edge_id = edge_by_triple[key]["id"]
        occurrences.append({
            "id": oid,
            "node_id": str(row["node_id"]),
            "parent_occurrence_id": str(parent_id) if parent_id is not None else None,
            "edge_id": edge_id,
            "branch": branch[oid],
            "depth": depth[oid],
            "order": int(row["order"]),
            "occurrence_role": str(row["occurrence_role"]),
            "render_children": bool(children.get(oid)) and row.get("occurrence_role") == "primary",
        })

    counts, per_node = compute_derived(nodes, edges, occurrences)
    for node in nodes:
        node["derived"] = per_node[str(node["id"])]
    return edges, occurrences, {"counts": counts, "nodes": nodes}


def apply_correction(project_root: Path, build: Path, debate_id: str) -> dict[str, Any]:
    debate_id = validate_debate_id(debate_id)
    build = resolve_build(project_root, debate_id)
    manifest = load_json(build / "manifest.json", "manifest")
    registry = load_json(build / "data/registre_debat.json", "registre maître")
    projection = load_json(build / "graph/graphe_argumentatif.json", "projection graphe")
    correction = load_json(build / GRAPH_CORRECTION_REVIEW, "correction du graphe")
    rejected = load_json(build / REVIEW_ENVELOPE, "revue rejetée")

    if manifest.get("global_status") != "graph_draft":
        raise CorpusBuildError("Une correction de graphe exige global_status=graph_draft")
    if correction.get("schema") != CORRECTION_SCHEMA or correction.get("debate_id") != debate_id:
        raise CorpusBuildError("Document de correction de graphe invalide")
    if correction.get("source_build_sha256") != build_payload_sha256(build):
        raise CorpusBuildError("Le graphe local a changé depuis la préparation de la correction")
    if correction.get("rejected_review_sha256") != rejected.get("review_sha256") or rejected.get("decision") != "rejected":
        raise CorpusBuildError("La correction ne correspond pas à la revue rejetée courante")
    if correction.get("status") != "corrected":
        raise CorpusBuildError("graph_correction.status doit valoir corrected")
    if not isinstance(correction.get("reviewer"), str) or len(correction["reviewer"].strip()) < 2:
        raise CorpusBuildError("Un reviewer est obligatoire pour la correction du graphe")
    if not _validate_timestamp(correction.get("reviewed_at")):
        raise CorpusBuildError("reviewed_at invalide ou sans fuseau pour la correction du graphe")
    if not isinstance(correction.get("notes"), str) or len(correction["notes"].strip()) < 3:
        raise CorpusBuildError("Des notes de correction sont obligatoires")

    edges, occurrences, derived = _validate_and_rebuild(registry, correction)
    graph = registry.setdefault("graph", {})
    graph["nodes"] = derived["nodes"]
    graph["edges"] = edges
    graph["occurrences"] = occurrences
    graph["derived_counts"] = derived["counts"]
    graph.setdefault("depth_policy", {})["limit_policy"] = "unbounded"
    graph["depth_policy"]["maximum_observed"] = derived["counts"]["maximum_depth"]
    lifecycle = graph.setdefault("lifecycle", {})
    lifecycle.update({"status": "draft", "validated_at": None, "locked_at": None, "locked_by_stage": None, "structural_sha256": None})

    for key in ("lifecycle", "depth_policy", "nodes", "edges", "occurrences", "derived_counts"):
        projection[key] = copy.deepcopy(graph.get(key))
    manifest["global_status"] = "graph_draft"
    manifest["updated_at"] = now_iso()

    correction = dict(correction)
    correction["status"] = "applied"
    correction["applied_at"] = now_iso()
    correction["resulting_build_sha256"] = None

    write_json(build / "manifest.json", manifest)
    write_json(build / "data/registre_debat.json", registry)
    write_json(build / "graph/graphe_argumentatif.json", projection)
    title = str((projection.get("debate") or {}).get("title_fr") or debate_id)
    (build / "graph/graphe_argumentatif.md").write_text(
        _markdown_graph(title, graph["nodes"], edges, occurrences, derived["counts"]),
        encoding="utf-8", newline="\n",
    )
    correction["resulting_build_sha256"] = build_payload_sha256(build)
    write_json(build / GRAPH_CORRECTION_REVIEW, correction)
    return {
        "status": "corrected",
        "debate_id": debate_id,
        "occurrences": len(occurrences),
        "edges": len(edges),
        "maximum_depth": derived["counts"]["maximum_depth"],
        "resulting_build_sha256": correction["resulting_build_sha256"],
    }
