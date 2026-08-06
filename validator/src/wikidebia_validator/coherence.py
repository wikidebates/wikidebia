from __future__ import annotations

from pathlib import Path
from typing import Any

from .graph import state_at_least, structural_sha256
from .package import PackageContext
from .translation import english_translation_deferred
from .wikicode import WikiParseError, parse_template


def validate_coherence(ctx: PackageContext) -> None:
    manifest = ctx.manifest()
    registry = ctx.registry()
    if not manifest or not registry:
        return
    debate_id = manifest.get("debate_id")
    registry_id = (registry.get("debate") or {}).get("id")
    if registry_id != debate_id:
        ctx.report.error("WDV-WF-004", "Identifiant du débat divergent entre manifeste et registre", details={"manifest": debate_id, "registry": registry_id})
    core = ctx.core_paths()
    scope = ctx.load_json(core["scope"])
    if isinstance(scope, dict):
        if scope.get("debate_id") != debate_id:
            ctx.report.error("WDV-WF-004", "Identifiant du débat divergent dans scope.json", path=core["scope"])
        reg_scope = (registry.get("debate") or {}).get("scope") or {}
        pairs = {
            "proposition_fr": scope.get("proposition_fr"),
            "scope_summary_fr": scope.get("scope_summary_fr"),
            "jurisdiction": scope.get("jurisdiction"),
            "timeframe": scope.get("timeframe"),
            "included_topics": scope.get("included_topics"),
            "excluded_topics": scope.get("excluded_topics"),
            "residual_ambiguities": scope.get("residual_ambiguities"),
        }
        for key, value in pairs.items():
            if reg_scope.get(key) != value:
                ctx.report.error("WDV-WF-004", f"Cadrage divergent pour {key}", path=core["scope"], details={"scope": value, "registry": reg_scope.get(key)})
    sources = ctx.sources()
    if isinstance(sources, dict) and sources.get("debate_id") != debate_id:
        ctx.report.error("WDV-WF-004", "Identifiant du débat divergent dans le registre documentaire", path=core["sources"])
    projection = ctx.graph_projection()
    if isinstance(projection, dict):
        pdebate = projection.get("debate") or {}
        rdebate = registry.get("debate") or {}
        if pdebate.get("title_fr") != ((rdebate.get("pages") or {}).get("fr") or {}).get("canonical_title"):
            ctx.report.error("WDV-GRA-014", "Titre du débat divergent dans la projection du graphe", path=core["graph_json"])
        if pdebate.get("labels") != rdebate.get("labels"):
            ctx.report.error("WDV-GRA-014", "Libellés de camps divergents dans la projection du graphe", path=core["graph_json"])
    # Normative version cross-check.
    norm = manifest.get("normative_versions") or {}
    rschema = registry.get("schema") or {}
    expected = {
        "mediawiki_structure": rschema.get("mediawiki_structure_version"),
        "render_profile": rschema.get("render_profile_version"),
        "registry": rschema.get("registry_version"),
        "graph": rschema.get("graph_version"),
        "validator": rschema.get("validator_version"),
    }
    for key, value in expected.items():
        if norm.get(key) != value:
            ctx.report.error("WDV-WF-005", f"Version divergente entre manifeste et registre : {key}", details={"manifest": norm.get(key), "registry": value})

    # Page manifest IDs and titles against registry.
    title_by_key: dict[tuple[str, str], str | None] = {}
    debate = registry.get("debate") or {}
    for lang in ("fr", "en"):
        title_by_key[(debate_id, lang)] = (((debate.get("pages") or {}).get(lang) or {}).get("canonical_title"))
    for node in (registry.get("graph") or {}).get("nodes", []):
        for lang in ("fr", "en"):
            title_by_key[(node.get("id"), lang)] = (node.get(lang) or {}).get("canonical_title")
    deferred = english_translation_deferred(manifest)
    registry_nodes = {n.get("id"): n for n in (registry.get("graph") or {}).get("nodes", [])}
    for page in manifest.get("pages", []):
        key = (page.get("page_id"), page.get("language"))
        if key not in title_by_key:
            ctx.report.error("WDV-FS-006", f"Manifeste de page sans objet correspondant dans le registre : {key}")
            continue
        if page.get("language") == "en" and deferred:
            if page.get("page_id") == debate_id:
                english_record = (((debate.get("pages") or {}).get("en") or {}))
            else:
                english_record = (registry_nodes.get(page.get("page_id"), {}).get("en") or {})
            if english_record.get("title_status") != "locked" or not english_record.get("canonical_title"):
                ctx.report.error("WDV-WF-005", f"Page anglaise présente sans titre anglais verrouillé : {page.get('page_id')}", path="manifest.json")
        if title_by_key[key] and page.get("canonical_title") != title_by_key[key]:
            ctx.report.error("WDV-FS-006", f"Titre de page divergent pour {key}", details={"manifest": page.get("canonical_title"), "registry": title_by_key[key]})

    validate_interlanguage_patch(ctx, manifest, registry)
    validate_operation_logs(ctx, manifest)

    release_path = (manifest.get("release") or {}).get("release_manifest_path")
    if release_path and ctx.exists(release_path):
        release = ctx.load_json(release_path)
        if isinstance(release, dict):
            current = structural_sha256(registry)
            if release.get("structural_sha256") != current:
                ctx.report.error("WDV-GRA-015", "Empreinte structurelle divergente dans le manifeste de libération", path=release_path, details={"release": release.get("structural_sha256"), "computed": current})
            if release.get("debate_id") != debate_id:
                ctx.report.error("WDV-WF-004", "Manifeste de libération rattaché à un autre débat", path=release_path)
    ctx.report.metrics["coherence"] = {"debate_id": debate_id, "english_translation_deferred": deferred}


def validate_interlanguage_patch(ctx: PackageContext, manifest: dict[str, Any], registry: dict[str, Any]) -> None:
    norm = (manifest.get("normative_versions") or {}).get("consolidated_norm")
    if norm in {"1.2.0", "1.2.1", "1.2.2", "1.2.3", "1.2.4", "1.2.5", "1.2.6", "1.2.7", "1.2.8", "1.2.9", "1.2.10", "1.2.11", "1.2.12", "1.2.13", "1.2.14", "1.2.15", "1.2.16", "1.2.17", "1.2.18", "1.2.19", "1.2.20", "1.2.21", "1.2.22", "1.2.23", "1.2.24", "1.2.25", "1.2.26", "1.2.27", "1.2.28", "1.2.29", "1.2.30", "1.2.31", "1.2.32", "1.2.33", "1.2.34", "1.2.35", "1.2.36", "1.2.37", "1.2.38", "1.2.39", "1.2.40", "1.2.41"}:
        # New packages carry their links in the canonical French files; no patch is required.
        return
    rel = "patches/interlanguage_fr.validated.json" if ctx.exists("patches/interlanguage_fr.validated.json") else "patches/interlanguage_fr.json"
    if not ctx.exists(rel):
        return
    patch = ctx.load_json(rel)
    if not isinstance(patch, dict):
        return
    if patch.get("debate_id") != manifest.get("debate_id"):
        ctx.report.error("WDV-WF-004", "Patch interlangue rattaché à un autre débat", path=rel)
    current_structural = structural_sha256(registry)
    if patch.get("structural_sha256") != current_structural:
        ctx.report.error("WDV-GRA-015", "Patch interlangue basé sur une autre structure", path=rel, details={"patch": patch.get("structural_sha256"), "computed": current_structural})
    entries = patch.get("entries", [])
    entry_by_id: dict[str, dict[str, Any]] = {}
    for entry in entries:
        pid = entry.get("page_id")
        if pid in entry_by_id:
            ctx.report.error("WDV-BIL-005", f"Entrée interlangue dupliquée : {pid}", path=rel)
        entry_by_id[pid] = entry
    pages = [p for p in manifest.get("pages", []) if p.get("language") == "fr"]
    if state_at_least(manifest.get("global_status"), "interlanguage_prepared"):
        missing = sorted({p.get("page_id") for p in pages} - set(entry_by_id))
        if missing:
            ctx.report.error("WDV-BIL-005", "Pages françaises absentes du patch interlangue", path=rel, details={"page_ids": missing})
    registry_nodes = {n.get("id"): n for n in (registry.get("graph") or {}).get("nodes", [])}
    debate_id = (registry.get("debate") or {}).get("id")
    page_by_id = {p.get("page_id"): p for p in pages}
    for pid, entry in entry_by_id.items():
        page = page_by_id.get(pid)
        if not page:
            ctx.report.error("WDV-BIL-005", f"Patch visant une page française non déclarée : {pid}", path=rel)
            continue
        if entry.get("source_path") != page.get("file_path") or entry.get("source_sha256") != page.get("sha256"):
            ctx.report.error("WDV-BIL-005", f"Source du patch incohérente pour {pid}", path=rel)
        if ctx.sha256(entry.get("source_path")) != entry.get("source_sha256"):
            ctx.report.error("WDV-FS-003", f"Empreinte source du patch incorrecte pour {pid}", path=entry.get("source_path"))
        if ctx.sha256(entry.get("staged_path")) != entry.get("staged_sha256"):
            ctx.report.error("WDV-FS-003", f"Empreinte de staging incorrecte pour {pid}", path=entry.get("staged_path"))
        if pid == debate_id:
            expected_title = ((((registry.get("debate") or {}).get("pages") or {}).get("en") or {}).get("canonical_title"))
        else:
            expected_title = (registry_nodes.get(pid, {}).get("en") or {}).get("canonical_title")
        if entry.get("target_title") != expected_title:
            ctx.report.error("WDV-BIL-005", f"Cible anglaise incorrecte dans le patch pour {pid}", path=rel, details={"expected": expected_title, "actual": entry.get("target_title")})
        if entry.get("creation_date") != page.get("creation_date"):
            ctx.report.error("WDV-MWK-010", f"Date de création modifiée dans le patch pour {pid}", path=rel)
        compare_patch_only(ctx, entry.get("source_path"), entry.get("staged_path"), pid)


def compare_patch_only(ctx: PackageContext, source_path: str, staged_path: str, page_id: str) -> None:
    source = ctx.read_text(source_path)
    staged = ctx.read_text(staged_path)
    if source is None or staged is None:
        return
    try:
        a = parse_template(source)
        b = parse_template(staged)
    except WikiParseError:
        return
    a_params = [(k, v) for k, v in a.params if k != "interlangue"]
    b_params = [(k, v) for k, v in b.params if k != "interlangue"]
    if a.name != b.name or a_params != b_params:
        ctx.report.error("WDV-BIL-005", f"La copie de staging {page_id} diffère de la source au-delà du lien interlangue", path=staged_path)
    if sum(k == "interlangue" for k, _ in b.params) != 1:
        ctx.report.error("WDV-MWK-011", f"La copie de staging {page_id} ne contient pas exactement un paramètre interlangue", path=staged_path)


def validate_operation_logs(ctx: PackageContext, manifest: dict[str, Any]) -> None:
    pages = {(p.get("page_id"), p.get("language")): p for p in manifest.get("pages", [])}
    debate_id = manifest.get("debate_id")
    for path in sorted(ctx.iter_files("logs/*.jsonl")):
        rel = ctx.relative(path)
        for line_no, entry in ctx.load_jsonl(rel):
            if not isinstance(entry, dict):
                continue
            if entry.get("debate_id") != debate_id:
                ctx.report.error("WDV-WF-004", "Entrée de journal rattachée à un autre débat", path=rel, pointer=f"ligne {line_no}")
            key = (entry.get("page_id"), entry.get("language"))
            page = pages.get(key)
            if page:
                if entry.get("title") != page.get("canonical_title"):
                    ctx.report.error("WDV-FS-006", "Titre de journal divergent du manifeste de page", path=rel, pointer=f"ligne {line_no}")
                if entry.get("source_path") == page.get("file_path") and entry.get("local_sha256") != page.get("sha256"):
                    ctx.report.error("WDV-FS-003", "Empreinte locale du journal divergente du manifeste", path=rel, pointer=f"ligne {line_no}")
