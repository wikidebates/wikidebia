from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from collections import Counter, defaultdict, deque
from typing import Any

from .package import PackageContext



CONTEXTUAL_TITLE_PATTERNS_120 = {
    "fr": [
        re.compile(r"\b(?:ce|cet|cette|ces)\s+(?:protocole|projet|programme|étude|expérience|méthode|résultats?|dispositif|institution|théorie|modèle|analyse|essai|article|ouvrage|rapport)\b", re.I),
        re.compile(r"^(?:Il|Elle|Ils|Elles|Cela|Ceci|Ça|Celui|Celle)\b", re.I),
    ],
    "en": [
        re.compile(r"\b(?:this|these|those)\s+(?:protocol|project|program|study|experiment|method|results?|findings?|device|institution|theory|model|analysis|trial|article|book|report)\b", re.I),
        re.compile(r"^(?:It|They|This|That|These|Those)\b", re.I),
    ],
}

CONTEXTUAL_TITLE_PATTERNS_121 = {
    "fr": {
        "initial": re.compile(r"^(?:(?:Il|Elle|Ils|Elles|Cela|Ceci|Ça|Celui(?:-ci|-là)?|Celle(?:-ci|-là)?)\b|(?:Ce|Cet|Cette|Ces)\s+(?!(?:que|qui|dont)\b)[a-zà-öø-ÿ][\w'’-]*)", re.I),
        "internal": re.compile(r"\b(?:ce|cet|cette|ces)\s+(?:protocole|projet|programme|étude|expérience|méthode|résultats?|dispositif|institution|théorie|modèle|analyse|essai|article|ouvrage|rapport)\b", re.I),
    },
    "en": {
        "initial": re.compile(r"^(?:(?:It|They)\b|(?:This|That|These|Those)\s+(?!(?:which|that)\b)[a-z][\w'-]*)", re.I),
        "internal": re.compile(r"\b(?:this|that|these|those)\s+(?:protocol|project|program|study|experiment|method|results?|findings?|device|institution|theory|model|analysis|trial|article|book|report)\b", re.I),
    },
}


def contextual_title_issues(title: str, language: str, revision: str = "1.2.0") -> list[str]:
    value = title or ""
    if revision == "1.2.0":
        return ["implicit_referent"] if any(p.search(value) for p in CONTEXTUAL_TITLE_PATTERNS_120.get(language, [])) else []
    patterns = CONTEXTUAL_TITLE_PATTERNS_121.get(language) or {}
    issues: list[str] = []
    initial_match = patterns.get("initial") and patterns["initial"].search(value)
    if initial_match:
        # French impersonal constructions do not contain an anaphoric referent.
        impersonal_fr = language == "fr" and re.match(
            r"^(?:Il\s+(?:existe|n['’]existe|faut|y\s+a|n['’]y\s+a|est|n['’]est|ne\s+devrait|reste)|Ce\s+(?:qu['’]|n['’]est))",
            value, re.I,
        )
        if not impersonal_fr:
            issues.append("initial_contextual_referent")
    # Internal demonstratives remain a review signal. They are not automatically
    # blocking, but the title must explicitly name the referent or document the
    # contextual shortening in its page-level review.
    internal_match = patterns.get("internal") and patterns["internal"].search(value)
    if internal_match and not initial_match:
        issues.append("possible_contextual_referent")
    return issues


STATE_ORDER = [
    "initialized", "graph_draft", "graph_validated", "graph_locked", "fr_debate_validated",
    "fr_arguments_in_progress", "fr_content_complete", "fr_validated", "en_titles_locked",
    "en_debate_validated", "en_arguments_in_progress", "en_content_complete", "en_validated",
    "bilingual_validated", "interlanguage_prepared", "release_ready", "published",
    "interlanguage_applied", "released", "archived",
]


def state_at_least(status: str | None, target: str) -> bool:
    if status in {"migration_required", "blocked"}:
        return False
    try:
        return STATE_ORDER.index(status or "") >= STATE_ORDER.index(target)
    except ValueError:
        return False


def normalized_title(value: str) -> str:
    return " ".join(unicodedata.normalize("NFC", value).split()).casefold()


def _duplicates(values: list[str]) -> set[str]:
    c = Counter(values)
    return {v for v, n in c.items() if n > 1}


def active_graph(registry: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    graph = registry.get("graph", {})
    nodes = [n for n in graph.get("nodes", []) if n.get("status") == "active"]
    node_ids = {n.get("id") for n in nodes}
    edges = [e for e in graph.get("edges", []) if e.get("status") == "active"]
    edge_ids = {e.get("id") for e in edges}
    occurrences = [o for o in graph.get("occurrences", []) if o.get("node_id") in node_ids and (o.get("edge_id") is None or o.get("edge_id") in edge_ids)]
    return nodes, edges, occurrences


def compute_derived(registry: dict[str, Any]) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    nodes, edges, occurrences = active_graph(registry)
    node_ids = {n["id"] for n in nodes}
    edge_by_id = {e["id"]: e for e in edges}
    by_node: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for occ in occurrences:
        by_node[occ["node_id"]].append(occ)
    outgoing = Counter(e["parent_node_id"] for e in edges if e["parent_node_id"] in node_ids)
    just = Counter()
    obj = Counter()
    for occ in occurrences:
        edge = edge_by_id.get(occ.get("edge_id"))
        if edge:
            (just if edge.get("relation") == "justification" else obj)[str(occ.get("depth"))] += 1
    per_node: dict[str, dict[str, Any]] = {}
    for node in nodes:
        occs = by_node.get(node["id"], [])
        if not occs:
            continue
        primaries = [o for o in occs if o.get("occurrence_role") == "primary"]
        per_node[node["id"]] = {
            "occurrence_count": len(occs),
            "minimum_depth": min(o["depth"] for o in occs),
            "maximum_depth": max(o["depth"] for o in occs),
            "is_main_argument_anywhere": any(o["depth"] == 1 for o in occs),
            "is_reused": len(occs) >= 2,
            "primary_occurrence_id": primaries[0]["id"] if len(primaries) == 1 else None,
        }
    counts = {
        "main_pro": sum(o.get("depth") == 1 and o.get("branch") == "pro" for o in occurrences),
        "main_con": sum(o.get("depth") == 1 and o.get("branch") == "con" for o in occurrences),
        "justifications_by_depth": dict(sorted(just.items(), key=lambda x: int(x[0]))),
        "objections_by_depth": dict(sorted(obj.items(), key=lambda x: int(x[0]))),
        "distinct_nodes": len(nodes),
        "total_occurrences": len(occurrences),
        "reused_nodes": sum(len(v) >= 2 for v in by_node.values()),
        "additional_reuses": len(occurrences) - len(nodes),
        "developed_nodes": sum(outgoing.get(n["id"], 0) > 0 for n in nodes),
        "leaf_nodes": sum(outgoing.get(n["id"], 0) == 0 for n in nodes),
        "maximum_depth": max((o.get("depth", 0) for o in occurrences), default=0),
    }
    return counts, per_node


def structural_payload(registry: dict[str, Any]) -> dict[str, Any]:
    nodes, edges, occurrences = active_graph(registry)
    payload_nodes = []
    for n in sorted(nodes, key=lambda x: x["id"]):
        fr = n.get("fr", {})
        payload_nodes.append({
            "id": n["id"],
            "canonical_title_fr": unicodedata.normalize("NFC", fr.get("canonical_title", "")),
            "displayed_title_fr": unicodedata.normalize("NFC", fr.get("displayed_title", "")),
        })
    payload_edges = [
        {k: e.get(k) for k in ("id", "parent_node_id", "child_node_id", "relation", "order")}
        for e in sorted(edges, key=lambda x: x["id"])
    ]
    payload_occ = [
        {k: o.get(k) for k in ("id", "node_id", "parent_occurrence_id", "edge_id", "branch", "depth", "order", "occurrence_role", "render_children")}
        for o in sorted(occurrences, key=lambda x: x["id"])
    ]
    return {"nodes": payload_nodes, "edges": payload_edges, "occurrences": payload_occ}


def structural_sha256(registry: dict[str, Any]) -> str:
    payload = structural_payload(registry)
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def validate_graph(ctx: PackageContext) -> None:
    registry = ctx.registry()
    if not registry:
        return
    manifest = ctx.manifest() or {}
    status = manifest.get("global_status")
    strict = state_at_least(status, "graph_validated") or registry.get("graph", {}).get("lifecycle", {}).get("status") in {"validated", "locked"}
    graph = registry.get("graph") or {}
    nodes_all = graph.get("nodes", [])
    edges_all = graph.get("edges", [])
    occ_all = graph.get("occurrences", [])

    for label, items in (("nœud", nodes_all), ("relation", edges_all), ("occurrence", occ_all)):
        ids = [x.get("id") for x in items if isinstance(x, dict)]
        for dup in sorted(_duplicates(ids)):
            ctx.report.error("WDV-GRA-001", f"Identifiant de {label} dupliqué : {dup}", path=ctx.core_paths()["registry"])

    nodes, edges, occurrences = active_graph(registry)
    node_by_id = {n.get("id"): n for n in nodes}
    edge_by_id = {e.get("id"): e for e in edges}
    occ_by_id = {o.get("id"): o for o in occurrences}

    norm = ((manifest.get("normative_versions") or {}).get("consolidated_norm"))
    for lang in ("fr", "en"):
        seen: dict[str, str] = {}
        for node in nodes:
            title = (node.get(lang) or {}).get("canonical_title")
            if not title:
                continue
            if title.endswith(".") or "’" in title:
                ctx.report.error("WDV-GRA-016", f"Titre {lang} non conforme : {title}", path=ctx.core_paths()["registry"], pointer=f"/graph/nodes/{node.get('id')}/{lang}/canonical_title")
            if norm in {"1.2.0", "1.2.1", "1.2.2", "1.2.3", "1.2.4", "1.2.5", "1.2.6", "1.2.7", "1.2.8", "1.2.9", "1.2.10", "1.2.11", "1.2.12", "1.2.13", "1.2.14", "1.2.15", "1.2.16", "1.2.17", "1.2.18", "1.2.19", "1.2.20", "1.2.21", "1.2.22", "1.2.23", "1.2.24", "1.2.25", "1.2.26", "1.2.27", "1.2.28", "1.2.29", "1.2.30", "1.2.31", "1.2.32", "1.2.33", "1.2.34", "1.2.35", "1.2.36", "1.2.37", "1.2.38", "1.2.39", "1.2.40", "1.2.41", "1.2.42", "1.2.43", "1.2.44", "1.2.45", "1.2.46", "1.2.47", "1.2.48"}:
                contextual = contextual_title_issues(title, lang, norm)
                details = {"node_id": node.get("id"), "language": lang, "issues": contextual}
                if "implicit_referent" in contextual or "initial_contextual_referent" in contextual:
                    ctx.report.error("WDV-EDT-016", f"Titre {lang} non autonome : le référent initial dépend du contexte extérieur : {title}", path=ctx.core_paths()["registry"], pointer=f"/graph/nodes/{node.get('id')}/{lang}/canonical_title", details=details)
                elif "possible_contextual_referent" in contextual:
                    ctx.report.warning("WDV-EDT-016", f"Titre {lang} à vérifier : un démonstratif interne peut dépendre du contexte extérieur : {title}", path=ctx.core_paths()["registry"], pointer=f"/graph/nodes/{node.get('id')}/{lang}/canonical_title", details=details)
            key = normalized_title(title)
            if key in seen and seen[key] != node.get("id"):
                ctx.report.error("WDV-GRA-002", f"Collision de titre canonique {lang} entre {seen[key]} et {node.get('id')} : {title}", path=ctx.core_paths()["registry"])
            seen[key] = node.get("id")

    relation_keys: set[tuple[Any, ...]] = set()
    outgoing: dict[str, list[str]] = defaultdict(list)
    for edge in edges:
        p, c = edge.get("parent_node_id"), edge.get("child_node_id")
        if p not in node_by_id or c not in node_by_id:
            ctx.report.error("WDV-GRA-003", f"Relation {edge.get('id')} vers un nœud inexistant", path=ctx.core_paths()["registry"])
            continue
        if p == c:
            ctx.report.error("WDV-GRA-006", f"Auto-relation {edge.get('id')} sur {p}", path=ctx.core_paths()["registry"])
        key = (p, c, edge.get("relation"))
        if key in relation_keys:
            ctx.report.error("WDV-GRA-007", f"Relation directe dupliquée : {p} -> {c} ({edge.get('relation')})", path=ctx.core_paths()["registry"])
        relation_keys.add(key)
        outgoing[p].append(c)

    # Cycle detection on the active node graph.
    colors: dict[str, int] = {node_id: 0 for node_id in node_by_id}
    stack: list[str] = []
    def visit(node_id: str) -> None:
        colors[node_id] = 1
        stack.append(node_id)
        for child in outgoing.get(node_id, []):
            if colors.get(child) == 0:
                visit(child)
            elif colors.get(child) == 1:
                start = stack.index(child) if child in stack else 0
                cycle = stack[start:] + [child]
                ctx.report.error("WDV-GRA-005", "Cycle détecté : " + " -> ".join(cycle), path=ctx.core_paths()["registry"])
        stack.pop()
        colors[node_id] = 2
    for node_id in sorted(node_by_id):
        if colors[node_id] == 0:
            visit(node_id)

    children_by_occ: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for occ in occurrences:
        parent_id = occ.get("parent_occurrence_id")
        if parent_id is not None:
            children_by_occ[parent_id].append(occ)

    for occ in occurrences:
        oid = occ.get("id")
        node_id = occ.get("node_id")
        if node_id not in node_by_id:
            ctx.report.error("WDV-GRA-003", f"Occurrence {oid} vers un nœud inexistant : {node_id}", path=ctx.core_paths()["registry"])
            continue
        parent_id = occ.get("parent_occurrence_id")
        edge_id = occ.get("edge_id")
        depth = occ.get("depth")
        if depth == 1:
            if parent_id is not None or edge_id is not None or occ.get("occurrence_role") != "primary":
                ctx.report.error("WDV-GRA-009", f"Occurrence principale de niveau 1 incohérente : {oid}", path=ctx.core_paths()["registry"])
        else:
            parent = occ_by_id.get(parent_id)
            edge = edge_by_id.get(edge_id)
            if parent is None or edge is None:
                ctx.report.error("WDV-GRA-004", f"Occurrence {oid} référence un parent ou une relation inexistant", path=ctx.core_paths()["registry"])
                continue
            if depth != parent.get("depth", 0) + 1 or occ.get("branch") != parent.get("branch"):
                ctx.report.error("WDV-GRA-009", f"Profondeur ou branche incohérente pour {oid}", path=ctx.core_paths()["registry"], details={"declared_depth": depth, "parent_depth": parent.get("depth")})
            if edge.get("parent_node_id") != parent.get("node_id") or edge.get("child_node_id") != node_id:
                ctx.report.error("WDV-GRA-008", f"Occurrence {oid} incohérente avec la relation {edge_id}", path=ctx.core_paths()["registry"])
        if occ.get("occurrence_role") == "secondary" and (occ.get("render_children") or children_by_occ.get(oid)):
            ctx.report.error("WDV-GRA-011", f"Occurrence secondaire développée : {oid}", path=ctx.core_paths()["registry"])
        if occ.get("render_children") is False and children_by_occ.get(oid):
            ctx.report.error("WDV-GRA-011", f"Occurrence marquée sans enfants mais possédant des enfants : {oid}", path=ctx.core_paths()["registry"])

    roots = [o for o in occurrences if o.get("depth") == 1]
    if strict and (not any(o.get("branch") == "pro" for o in roots) or not any(o.get("branch") == "con" for o in roots)):
        ctx.report.error("WDV-GRA-017", "Le graphe validé doit contenir au moins un argument principal dans chaque branche", path=ctx.core_paths()["registry"])

    by_node: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for occ in occurrences:
        by_node[occ.get("node_id")].append(occ)
    for node_id in node_by_id:
        occs = by_node.get(node_id, [])
        if not occs:
            (ctx.report.error if strict else ctx.report.warning)("WDV-GRA-012", f"Nœud actif sans occurrence : {node_id}", path=ctx.core_paths()["registry"])
            continue
        primaries = [o for o in occs if o.get("occurrence_role") == "primary"]
        if len(primaries) != 1:
            (ctx.report.error if strict else ctx.report.warning)("WDV-GRA-010", f"{node_id} possède {len(primaries)} occurrence(s) primaire(s), une seule requise", path=ctx.core_paths()["registry"])

    # Each active edge must be represented by at least one occurrence.
    used_edges = Counter(o.get("edge_id") for o in occurrences if o.get("edge_id"))
    for edge_id in edge_by_id:
        if used_edges[edge_id] == 0:
            (ctx.report.error if strict else ctx.report.warning)("WDV-GRA-008", f"Relation active sans occurrence : {edge_id}", path=ctx.core_paths()["registry"])

    counts, per_node = compute_derived(registry)
    declared = graph.get("derived_counts") or {}
    if declared != counts:
        (ctx.report.error if strict else ctx.report.warning)("WDV-GRA-013", "Les compteurs dérivés ne correspondent pas au recalcul", path=ctx.core_paths()["registry"], details={"declared": declared, "computed": counts})
    for node in nodes:
        expected = per_node.get(node["id"])
        declared_node = node.get("derived")
        if strict and declared_node is None:
            ctx.report.error("WDV-GRA-013", f"Bloc derived absent pour le nœud validé {node['id']}", path=ctx.core_paths()["registry"])
        elif declared_node is not None and expected != declared_node:
            (ctx.report.error if strict else ctx.report.warning)("WDV-GRA-013", f"Données dérivées incorrectes pour {node['id']}", path=ctx.core_paths()["registry"], details={"declared": declared_node, "computed": expected})

    policy = graph.get("depth_policy") or {}
    observed = counts["maximum_depth"]
    if policy.get("maximum_observed") != observed:
        (ctx.report.error if strict else ctx.report.warning)("WDV-GRA-013", "maximum_observed incorrect", path=ctx.core_paths()["registry"], details={"declared": policy.get("maximum_observed"), "computed": observed})
    if norm in {"1.2.31", "1.2.32", "1.2.33", "1.2.34", "1.2.35", "1.2.36", "1.2.37", "1.2.38", "1.2.39", "1.2.40", "1.2.41", "1.2.42", "1.2.43", "1.2.44", "1.2.45", "1.2.46", "1.2.47", "1.2.48"}:
        if policy.get("limit_policy") != "unbounded":
            ctx.report.error("WDV-GRA-009", "La politique de profondeur 1.2.31+ doit être non limitée", path=ctx.core_paths()["registry"], details={"limit_policy": policy.get("limit_policy")})
        legacy_fields = [key for key in ("normal_target", "declared_maximum", "exception_reason") if key in policy]
        if legacy_fields:
            ctx.report.error("WDV-GRA-009", "Les champs historiques de limitation de profondeur sont interdits sous 1.2.31+", path=ctx.core_paths()["registry"], details={"legacy_fields": legacy_fields})
    else:
        declared_max = policy.get("declared_maximum")
        if isinstance(declared_max, int) and observed > declared_max:
            ctx.report.error("WDV-GRA-009", f"Profondeur observée {observed} supérieure au maximum déclaré {declared_max}", path=ctx.core_paths()["registry"])
        if observed > 5:
            exception_reason = str(policy.get("exception_reason") or "").strip()
            if len(exception_reason) < 40:
                ctx.report.warning("WDV-GRA-009", f"Profondeur exceptionnelle élevée : {observed}", path=ctx.core_paths()["registry"])

    lifecycle = graph.get("lifecycle") or {}
    declared_hash = lifecycle.get("structural_sha256")
    computed_hash = structural_sha256(registry)
    if declared_hash and declared_hash != computed_hash:
        ctx.report.error("WDV-GRA-015", "Empreinte structurelle incorrecte", path=ctx.core_paths()["registry"], details={"declared": declared_hash, "computed": computed_hash})
    if lifecycle.get("status") == "locked" and not declared_hash:
        ctx.report.error("WDV-GRA-015", "Un graphe verrouillé doit posséder une empreinte structurelle", path=ctx.core_paths()["registry"])

    projection = ctx.graph_projection()
    if projection:
        projection_graph = {k: projection.get(k) for k in ("lifecycle", "depth_policy", "nodes", "edges", "occurrences", "derived_counts")}
        registry_graph = {k: graph.get(k) for k in ("lifecycle", "depth_policy", "nodes", "edges", "occurrences", "derived_counts")}
        if projection_graph != registry_graph:
            ctx.report.error("WDV-GRA-014", "La projection du graphe diverge du registre maître", path=ctx.core_paths()["graph_json"])
        debate_id = (registry.get("debate") or {}).get("id")
        if (projection.get("debate") or {}).get("id") != debate_id:
            ctx.report.error("WDV-GRA-014", "L'identifiant du débat diffère dans la projection", path=ctx.core_paths()["graph_json"])

    ctx.report.metrics["graph"] = counts
