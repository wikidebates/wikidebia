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

    validate_manual_remote_adoptions(ctx, manifest)
    validate_argument_name_assignments(ctx, manifest)
    validate_argument_name_discovery(ctx, manifest)
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



def validate_manual_remote_adoptions(ctx: PackageContext, manifest: dict[str, Any]) -> None:
    controls = manifest.get("editorial_controls") or {}
    rel = controls.get("manual_remote_adoption_path")
    if not rel:
        return
    data = ctx.load_json(str(rel))
    if not isinstance(data, dict):
        return
    if data.get("debate_id") != manifest.get("debate_id"):
        ctx.report.error("WDV-RMT-007", "Registre d’adoption distante rattaché à un autre débat", path=str(rel))
    if not str(data.get("decision") or "").strip():
        ctx.report.error("WDV-RMT-007", "Décision propriétaire absente du registre d’adoption distante", path=str(rel))
    pages = {(str(row.get("language")), str(row.get("page_id"))): row for row in manifest.get("pages") or []}
    seen: set[tuple[str, str]] = set()
    for row in data.get("entries") or []:
        key = (str(row.get("language") or ""), str(row.get("page_id") or ""))
        if key in seen:
            ctx.report.error("WDV-RMT-007", "Adoption distante dupliquée", path=str(rel), details={"language": key[0], "page_id": key[1]})
            continue
        seen.add(key)
        page = pages.get(key)
        if page is None:
            ctx.report.error("WDV-RMT-007", "Adoption distante visant une page absente du manifeste", path=str(rel), details={"language": key[0], "page_id": key[1]})
            continue
        if row.get("title") != page.get("canonical_title"):
            ctx.report.error("WDV-RMT-007", "Titre divergent dans l’adoption distante", path=str(rel), details={"page_id": key[1], "expected": page.get("canonical_title"), "actual": row.get("title")})
        external_seen: set[tuple[str, str]] = set()
        for external in row.get("external_relations") or []:
            external_key = (str(external.get("relation") or ""), str(external.get("page") or ""))
            if external_key in external_seen:
                ctx.report.error("WDV-RMT-007", "Relation externe distante dupliquée", path=str(rel), details={"page_id": key[1], "relation": external_key[0], "target": external_key[1]})
            external_seen.add(external_key)
            if external_key[1] == row.get("title"):
                ctx.report.error("WDV-RMT-007", "Une relation externe ne peut pas viser sa propre page", path=str(rel), details={"page_id": key[1], "target": external_key[1]})
    ctx.report.metrics.setdefault("coherence", {})["manual_remote_adoptions"] = len(seen)


def validate_argument_name_assignments(ctx: PackageContext, manifest: dict[str, Any]) -> None:
    controls = manifest.get("editorial_controls") or {}
    rel = controls.get("argument_name_assignment_path")
    if not rel:
        return
    data = ctx.load_json(str(rel))
    if not isinstance(data, dict):
        return
    if data.get("debate_id") != manifest.get("debate_id"):
        ctx.report.error("WDV-EDT-031", "Registre d’attribution de noms rattaché à un autre débat", path=str(rel))
    if not str(data.get("decision") or "").strip():
        ctx.report.error("WDV-EDT-031", "Décision propriétaire absente du registre d’attribution de noms", path=str(rel))
    pages = {(str(row.get("language")), str(row.get("page_id"))): row for row in manifest.get("pages") or []}
    seen: set[tuple[str, str]] = set()
    for row in data.get("entries") or []:
        key = (str(row.get("language") or ""), str(row.get("page_id") or ""))
        if key in seen:
            ctx.report.error("WDV-EDT-031", "Attribution de nom dupliquée", path=str(rel), details={"language": key[0], "page_id": key[1]})
            continue
        seen.add(key)
        page = pages.get(key)
        if page is None or page.get("page_type") != "argument":
            ctx.report.error("WDV-EDT-031", "Attribution visant une page Argument absente du manifeste", path=str(rel), details={"language": key[0], "page_id": key[1]})
            continue
        if row.get("title") != page.get("canonical_title"):
            ctx.report.error("WDV-EDT-031", "Titre divergent dans l’attribution de nom", path=str(rel), details={"page_id": key[1], "expected": page.get("canonical_title"), "actual": row.get("title")})
        if row.get("owner_approved") is not True or not str(row.get("name") or "").strip() or not str(row.get("reason") or "").strip():
            ctx.report.error("WDV-EDT-031", "Attribution de nom incomplète ou non approuvée", path=str(rel), details={"page_id": key[1]})
        current_name_param, legacy_name_param = (("nom-consacré", "nom") if key[0] == "fr" else ("established-name", "name"))
        preserved = page.get("preserved_parameters") or {}
        name_states = [preserved.get(current_name_param), preserved.get(legacy_name_param)]
        if page.get("page_origin") == "preexisting" and any(isinstance(state, dict) and state.get("present") is True for state in name_states):
            ctx.report.error("WDV-EDT-031", "Une attribution explicite ne peut pas remplacer un nom consacré historique déjà présent", path=str(rel), details={"page_id": key[1]})
    ctx.report.metrics.setdefault("coherence", {})["argument_name_assignments"] = len(seen)

def validate_argument_name_discovery(ctx: PackageContext, manifest: dict[str, Any]) -> None:
    controls = manifest.get("editorial_controls") or {}
    rel = controls.get("argument_name_discovery_path")
    new_arguments = {
        (str(page.get("language") or ""), str(page.get("page_id") or "")): page
        for page in manifest.get("pages") or []
        if page.get("page_type") == "argument" and page.get("page_origin") == "new"
    }
    if not new_arguments and not rel:
        return
    if new_arguments and not rel:
        ctx.report.error("WDV-EDT-032", "La recherche d’un nom consacré n’est pas attestée pour les arguments nouveaux", path="manifest.json")
        return
    if not rel:
        return
    data = ctx.load_json(str(rel))
    if not isinstance(data, dict):
        return
    if data.get("debate_id") != manifest.get("debate_id"):
        ctx.report.error("WDV-EDT-032", "Revue de recherche des noms rattachée à un autre débat", path=str(rel))
    seen: set[tuple[str, str]] = set()
    for row in data.get("entries") or []:
        key = (str(row.get("language") or ""), str(row.get("page_id") or ""))
        if key in seen:
            ctx.report.error("WDV-EDT-032", "Revue de nom d’argument dupliquée", path=str(rel), details={"language": key[0], "page_id": key[1]})
            continue
        seen.add(key)
        page = new_arguments.get(key)
        if page is None:
            ctx.report.error("WDV-EDT-032", "La revue de recherche de nom doit viser uniquement une page Argument nouvelle", path=str(rel), details={"language": key[0], "page_id": key[1]})
            continue
        if row.get("title") != page.get("canonical_title"):
            ctx.report.error("WDV-EDT-032", "Titre divergent dans la revue de recherche de nom", path=str(rel), details={"page_id": key[1], "expected": page.get("canonical_title"), "actual": row.get("title")})
        if row.get("search_reviewed") is not True or len(row.get("search_queries") or []) < 2:
            ctx.report.error("WDV-EDT-032", "Recherche documentaire insuffisamment attestée pour le nom d’argument", path=str(rel), details={"page_id": key[1]})
        outcome = row.get("outcome")
        if outcome == "known_name":
            if not str(row.get("name") or "").strip() or not (row.get("evidence") or []):
                ctx.report.error("WDV-EDT-032", "Nom consacré déclaré sans appellation ou preuve documentaire", path=str(rel), details={"page_id": key[1]})
            for field in ("same_reasoning_confirmed", "non_invented_label_confirmed", "language_fit_confirmed"):
                if row.get(field) is not True:
                    ctx.report.error("WDV-EDT-032", f"Attestation manquante pour un nom consacré : {field}", path=str(rel), details={"page_id": key[1]})
        elif outcome == "none":
            if row.get("name") is not None:
                ctx.report.error("WDV-EDT-032", "Une recherche conclue sans nom ne peut fournir de valeur d’appellation consacrée", path=str(rel), details={"page_id": key[1]})
        else:
            ctx.report.error("WDV-EDT-032", "Résultat de recherche de nom invalide", path=str(rel), details={"page_id": key[1]})
    missing = sorted(set(new_arguments) - seen)
    extra = sorted(seen - set(new_arguments))
    if missing:
        ctx.report.error("WDV-EDT-032", "La revue ne couvre pas tous les arguments nouveaux", path=str(rel), details={"missing": missing[:20], "count": len(missing)})
    if extra:
        ctx.report.error("WDV-EDT-032", "La revue contient des pages qui ne sont pas des arguments nouveaux", path=str(rel), details={"extra": extra[:20], "count": len(extra)})
    ctx.report.metrics.setdefault("coherence", {})["argument_name_discovery_entries"] = len(seen)


def validate_interlanguage_patch(ctx: PackageContext, manifest: dict[str, Any], registry: dict[str, Any]) -> None:
    """Legacy patch files are provenance only under the current workflow."""
    return

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
