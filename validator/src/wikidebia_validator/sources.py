from __future__ import annotations

from collections import Counter
from typing import Any

from .package import PackageContext
from .wikicode import documentary_date_is_machine


def _norm(ctx: PackageContext) -> str | None:
    return (((ctx.manifest() or {}).get("normative_versions") or {}).get("consolidated_norm"))


def _fold(value: Any) -> str:
    return " ".join(str(value or "").split()).casefold()


def _norm_at_least(norm: str | None, minimum: str) -> bool:
    def parts(value: str | None) -> tuple[int, ...]:
        try:
            return tuple(int(piece) for piece in str(value or "").split("."))
        except ValueError:
            return ()
    return parts(norm) >= parts(minimum)


def validate_sources(ctx: PackageContext) -> None:
    registry = ctx.registry()
    sources_doc = ctx.sources()
    if not registry or not sources_doc:
        return
    norm = _norm(ctx)
    is_120 = norm in {"1.2.0", "1.2.1", "1.2.2", "1.2.3", "1.2.4", "1.2.5", "1.2.6", "1.2.7", "1.2.8", "1.2.9", "1.2.10", "1.2.11", "1.2.12", "1.2.13", "1.2.14", "1.2.15", "1.2.16", "1.2.17", "1.2.18", "1.2.19", "1.2.20", "1.2.21", "1.2.22", "1.2.23", "1.2.24", "1.2.25", "1.2.26", "1.2.27", "1.2.28", "1.2.29", "1.2.30", "1.2.31", "1.2.32", "1.2.33", "1.2.34", "1.2.35"}
    sources = sources_doc.get("sources", [])
    ids = [s.get("id") for s in sources]
    for sid, count in Counter(ids).items():
        if sid and count > 1:
            ctx.report.error("WDV-SRC-001", f"Identifiant de source dupliqué : {sid}", path=ctx.core_paths()["sources"])
    seen_keys: dict[tuple[str, str], str] = {}
    source_by_id: dict[str, dict[str, Any]] = {s.get("id"): s for s in sources if s.get("id")}
    by_equivalence: dict[str, list[dict[str, Any]]] = {}
    for source in sources:
        eq = source.get("equivalence_group")
        if isinstance(eq, str) and eq:
            by_equivalence.setdefault(eq, []).append(source)
    registry_nodes = {n.get("id") for n in registry.get("graph", {}).get("nodes", [])}
    debate_id = (registry.get("debate") or {}).get("id")
    valid_pages = registry_nodes | {debate_id}
    for source in sources:
        sid = source.get("id")
        key = (source.get("language"), source.get("deduplication_key"))
        if key[1] and key in seen_keys:
            ctx.report.error("WDV-SRC-001", f"Clé de dédoublonnage documentaire dupliquée : {key[1]}", path=ctx.core_paths()["sources"], details={"sources": [seen_keys[key], sid]})
        elif key[1]:
            seen_keys[key] = sid
        usage = source.get("usage", [])
        verification = source.get("verification") or {}
        metadata = source.get("metadata") or {}
        if norm in {"1.2.9", "1.2.10", "1.2.11", "1.2.12", "1.2.13", "1.2.14", "1.2.15", "1.2.16", "1.2.17", "1.2.18", "1.2.19", "1.2.20", "1.2.21", "1.2.22", "1.2.23", "1.2.24", "1.2.25", "1.2.26", "1.2.27", "1.2.28", "1.2.29", "1.2.30", "1.2.31", "1.2.32", "1.2.33", "1.2.34", "1.2.35"}:
            documentary_date = metadata.get("date")
            if isinstance(documentary_date, str) and documentary_date_is_machine(documentary_date):
                ctx.report.error("WDV-DOC-005", f"La date documentaire de la source {sid} est au format machine; utiliser le langage naturel", path=ctx.core_paths()["sources"], details={"source_id": sid, "value": documentary_date})
        if is_120:
            if verification.get("language_verified") is not True:
                ctx.report.error("WDV-SRC-004", f"Langue documentaire non vérifiée pour la source {sid}", path=ctx.core_paths()["sources"])
            if source.get("type") == "webliography":
                page = _fold(metadata.get("page"))
                site = _fold(metadata.get("site"))
                authors = [_fold(a) for a in metadata.get("authors") or []]
                if page and site and page == site:
                    ctx.report.error("WDV-DOC-004", f"La source {sid} duplique le site dans le champ page", path=ctx.core_paths()["sources"])
                if verification.get("authorship_checked") is not True:
                    ctx.report.error("WDV-DOC-004", f"L'attribution d'auteur n'a pas été vérifiée pour la source {sid}", path=ctx.core_paths()["sources"])
                if site and site in authors and verification.get("authorship_verified") is not True:
                    ctx.report.error("WDV-DOC-004", f"Le nom du site est utilisé comme auteur sans preuve pour la source {sid}", path=ctx.core_paths()["sources"])
        for use in usage:
            page_id = use.get("page_id")
            page_lang = use.get("language")
            if page_id not in valid_pages:
                ctx.report.error("WDV-SRC-002", f"La source {sid} est utilisée par une page inexistante : {page_id}", path=ctx.core_paths()["sources"])
            if _norm_at_least(norm, "1.2.33") and page_id != debate_id and use.get("role") == "supports_summary":
                if use.get("argument_development_verified") is not True:
                    ctx.report.error("WDV-SRC-006", f"La source {sid} n’est pas attestée comme développant l’argument {page_id}", path=ctx.core_paths()["sources"], details={"page_id": page_id})
                if not isinstance(use.get("also_develops_objections"), bool):
                    ctx.report.error("WDV-SRC-006", f"La couverture éventuelle d’objections n’est pas renseignée pour {sid}/{page_id}", path=ctx.core_paths()["sources"], details={"page_id": page_id})
            if not is_120 and page_lang != source.get("language"):
                ctx.report.error("WDV-SRC-002", f"Langue d'usage incohérente pour la source {sid}", path=ctx.core_paths()["sources"])
            if is_120:
                source_lang = source.get("language")
                if page_id == debate_id and source_lang != page_lang:
                    ctx.report.error("WDV-SRC-004", f"La page de débat {page_lang} ne peut utiliser que des sources réellement disponibles dans sa langue : {sid}", path=ctx.core_paths()["sources"], details={"source_language": source_lang, "page_language": page_lang})
                elif page_id != debate_id and source_lang != page_lang:
                    fit = use.get("language_fit")
                    if fit not in {"original_no_equivalent", "object_of_analysis"}:
                        ctx.report.error("WDV-SRC-004", f"Usage translingue non justifié pour la source {sid}", path=ctx.core_paths()["sources"], details={"source_language": source_lang, "page_language": page_lang, "language_fit": fit})
                    eq = source.get("equivalence_group")
                    equivalents = [s for s in by_equivalence.get(eq, []) if s.get("language") == page_lang and (s.get("verification") or {}).get("status") == "verified"] if eq else []
                    if equivalents:
                        ctx.report.error("WDV-SRC-004", f"Un équivalent {page_lang} vérifié existe pour la source {sid}", path=ctx.core_paths()["sources"], details={"equivalents": [s.get("id") for s in equivalents]})
                if page_id == debate_id and source.get("type") == "bibliography":
                    kind = source.get("document_kind")
                    scope = use.get("documentary_scope")
                    reason = str(use.get("selection_reason") or "").strip()
                    allowed_kinds = {"book", "monograph", "handbook", "edited_volume", "synthesis_report", "review_article"}
                    if kind not in allowed_kinds or scope not in {"foundational_work", "broad_synthesis"} or len(reason) < 12:
                        ctx.report.error("WDV-SRC-005", f"Référence bibliographique du débat insuffisamment synthétique ou non justifiée : {sid}", path=ctx.core_paths()["sources"], details={"document_kind": kind, "documentary_scope": scope})
        vstatus = verification.get("status")
        if usage and vstatus != "verified":
            ctx.report.error("WDV-SRC-003", f"La source {sid} est utilisée sans être vérifiée", path=ctx.core_paths()["sources"])
        if vstatus == "verified" and not usage:
            ctx.report.warning("WDV-SRC-003", f"La source vérifiée {sid} n'est utilisée par aucune page", path=ctx.core_paths()["sources"])
        if vstatus == "rejected" and usage:
            ctx.report.error("WDV-SRC-003", f"La source rejetée {sid} est encore utilisée", path=ctx.core_paths()["sources"])

    # Cross-check source IDs referenced by nodes.
    for node in registry.get("graph", {}).get("nodes", []):
        for lang in ("fr", "en"):
            refs = (node.get("sources") or {}).get(lang) or {}
            for category, source_ids in refs.items():
                expected_type = {"bibliography": "bibliography", "webliography": "webliography", "videography": "videography"}.get(category)
                for sid in source_ids:
                    src = source_by_id.get(sid)
                    if not src:
                        ctx.report.error("WDV-SRC-002", f"Le nœud {node.get('id')} référence une source inexistante : {sid}", path=ctx.core_paths()["registry"])
                        continue
                    if src.get("type") != expected_type or (not is_120 and src.get("language") != lang):
                        ctx.report.error("WDV-SRC-002", f"Type ou langue incohérents pour la source {sid} du nœud {node.get('id')}", path=ctx.core_paths()["registry"])
                    matching_usage = [u for u in src.get("usage", []) if u.get("page_id") == node.get("id") and u.get("language") == lang]
                    if not matching_usage:
                        ctx.report.error("WDV-SRC-002", f"Usage réciproque absent pour la source {sid} et le nœud {node.get('id')}/{lang}", path=ctx.core_paths()["sources"])
                    elif _norm_at_least(norm, "1.2.33"):
                        supporting = [u for u in matching_usage if u.get("role") == "supports_summary"]
                        if not supporting:
                            ctx.report.error("WDV-SRC-006", f"La source {sid} est sélectionnée pour {node.get('id')}/{lang} sans développer l’argument", path=ctx.core_paths()["sources"])
                        elif not any(u.get("argument_development_verified") is True for u in supporting):
                            ctx.report.error("WDV-SRC-006", f"Le développement de l’argument n’est pas vérifié pour {sid} et {node.get('id')}/{lang}", path=ctx.core_paths()["sources"])
    ctx.report.metrics["sources"] = {"count": len(sources), "verified": sum((s.get("verification") or {}).get("status") == "verified" for s in sources)}
