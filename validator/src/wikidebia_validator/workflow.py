from __future__ import annotations

from datetime import datetime
from typing import Any

from .graph import STATE_ORDER, state_at_least
from .package import PackageContext
from .translation import english_translation_deferred, english_translation_status


VALIDATION_FOR_STATE = {
    "graph_validated": "graph",
    "graph_locked": "graph",
    "fr_debate_validated": "fr_debate",
    "fr_validated": "fr_global",
    "en_titles_locked": "en_titles",
    "en_debate_validated": "en_debate",
    "en_validated": "en_global",
    "bilingual_validated": "bilingual",
    "interlanguage_prepared": "interlanguage",
    "release_ready": "interlanguage",
    "released": "release",
}

WORK_MIN_STATE = {
    "initialization": "initialized",
    "graph": "graph_locked",
    "fr_debate_page": "fr_debate_validated",
    "fr_argument_batch": "fr_arguments_in_progress",
    "fr_global_validation": "fr_validated",
    "en_titles": "en_titles_locked",
    "en_debate_page": "en_debate_validated",
    "en_argument_batch": "en_arguments_in_progress",
    "en_global_validation": "en_validated",
    "bilingual_validation": "bilingual_validated",
    "interlanguage": "interlanguage_prepared",
    "release_archive": "published",
    "corrective_prepublication": "release_ready",
}


def allowed_transition(old: str, new: str) -> bool:
    if old == new:
        return True
    if new in {"blocked", "migration_required"}:
        return True
    if old in {"blocked", "migration_required"}:
        return new in {old, "graph_draft", "graph_validated", "graph_locked"}
    try:
        return STATE_ORDER.index(new) == STATE_ORDER.index(old) + 1
    except ValueError:
        return False


def passed_scopes(manifest: dict[str, Any]) -> set[str]:
    return {v.get("scope") for v in manifest.get("validations", []) if v.get("result") in {"passed", "passed_with_warnings"} and v.get("blocking_errors") == 0}


def validate_workflow(ctx: PackageContext, previous_status: str | None = None) -> None:
    manifest = ctx.manifest()
    registry = ctx.registry()
    if not manifest or not registry:
        return
    status = manifest.get("global_status")
    english_deferred = english_translation_deferred(manifest)
    norm_versions = manifest.get("normative_versions") or {}
    corrective_mode = status in {"corrective_in_progress", "corrective_blocked"} or norm_versions.get("consolidated_norm") in {"1.1.0", "1.1.1", "1.1.2", "1.1.3", "1.1.4", "1.1.5", "1.1.6", "1.1.7", "1.1.8", "1.1.9", "1.2.0", "1.2.1", "1.2.2", "1.2.3", "1.2.4", "1.2.5", "1.2.6", "1.2.7", "1.2.8", "1.2.9", "1.2.10", "1.2.11", "1.2.12", "1.2.13", "1.2.14", "1.2.15", "1.2.16", "1.2.17", "1.2.18", "1.2.19", "1.2.20", "1.2.21", "1.2.22", "1.2.23", "1.2.24", "1.2.25", "1.2.26", "1.2.27", "1.2.28", "1.2.29", "1.2.30", "1.2.31", "1.2.32", "1.2.33", "1.2.34", "1.2.35", "1.2.36", "1.2.37"}
    if previous_status and not allowed_transition(previous_status, status):
        ctx.report.error("WDV-WF-002", f"Transition interdite : {previous_status} -> {status}", path="manifest.json")
    try:
        created = datetime.fromisoformat(manifest.get("created_at"))
        updated = datetime.fromisoformat(manifest.get("updated_at"))
        if updated < created:
            ctx.report.error("WDV-WF-001", "updated_at est antérieur à created_at", path="manifest.json")
    except Exception:
        pass

    scopes = passed_scopes(manifest)
    deferred_scopes = {"en_titles", "en_debate", "en_global", "bilingual", "interlanguage"}
    for milestone, required_scope in VALIDATION_FOR_STATE.items():
        if english_deferred and required_scope in deferred_scopes:
            continue
        if state_at_least(status, milestone) and required_scope not in scopes:
            ctx.report.error("WDV-WF-003", f"L'état {status} exige une validation réussie de portée {required_scope}", path="manifest.json")

    graph_lifecycle = (registry.get("graph") or {}).get("lifecycle") or {}
    if state_at_least(status, "graph_validated") and graph_lifecycle.get("status") not in {"validated", "locked"}:
        ctx.report.error("WDV-WF-001", "L'état global exige un graphe validé ou verrouillé", path=ctx.core_paths()["registry"])
    if state_at_least(status, "graph_locked") and graph_lifecycle.get("status") != "locked":
        ctx.report.error("WDV-WF-001", "L'état global exige un graphe verrouillé", path=ctx.core_paths()["registry"])

    nodes = [n for n in (registry.get("graph") or {}).get("nodes", []) if n.get("status") == "active"]
    if state_at_least(status, "graph_locked"):
        for n in nodes:
            if (n.get("fr") or {}).get("title_status") != "locked":
                ctx.report.error("WDV-WF-005", f"Titre français non verrouillé à l'état {status} : {n.get('id')}")
    if state_at_least(status, "en_titles_locked") and not english_deferred:
        for n in nodes:
            if (n.get("en") or {}).get("title_status") != "locked":
                ctx.report.error("WDV-WF-005", f"Titre anglais non verrouillé à l'état {status} : {n.get('id')}")

    pages = manifest.get("pages", [])
    for lang, content_state, validated_state in (("fr", "fr_content_complete", "fr_validated"), ("en", "en_content_complete", "en_validated")):
        if lang == "en" and english_deferred:
            continue
        expected_ids = {(registry.get("debate") or {}).get("id")} | {n.get("id") for n in nodes}
        lang_pages = {p.get("page_id"): p for p in pages if p.get("language") == lang}
        if state_at_least(status, content_state):
            missing = sorted(expected_ids - set(lang_pages))
            if missing:
                ctx.report.error("WDV-WF-001", f"Pages {lang} manquantes à l'état {status}", details={"page_ids": missing})
            for pid, page in lang_pages.items():
                if pid in expected_ids and page.get("status") not in {"generated", "validated", "published"}:
                    ctx.report.error("WDV-WF-001", f"Page {pid}/{lang} non générée à l'état {status}")
        if state_at_least(status, validated_state):
            for pid in expected_ids:
                page = lang_pages.get(pid)
                if page and page.get("status") not in {"validated", "published"}:
                    ctx.report.error("WDV-WF-001", f"Page {pid}/{lang} non validée à l'état {status}")

    if norm_versions.get("consolidated_norm") in {"1.2.0", "1.2.1", "1.2.2", "1.2.3", "1.2.4", "1.2.5", "1.2.6", "1.2.7", "1.2.8", "1.2.9", "1.2.10", "1.2.11", "1.2.12", "1.2.13", "1.2.14", "1.2.15", "1.2.16", "1.2.17", "1.2.18", "1.2.19", "1.2.20", "1.2.21", "1.2.22", "1.2.23", "1.2.24", "1.2.25", "1.2.26", "1.2.27", "1.2.28", "1.2.29", "1.2.30", "1.2.31", "1.2.32", "1.2.33", "1.2.34", "1.2.35", "1.2.36", "1.2.37"} and state_at_least(status, "fr_debate_validated") and not english_deferred:
        debate_en = ((((registry.get("debate") or {}).get("pages") or {}).get("en") or {}))
        if debate_en.get("title_status") != "locked" or not debate_en.get("canonical_title"):
            ctx.report.error("WDV-WF-005", "Le titre anglais du débat doit être verrouillé avant la création des pages françaises", path=ctx.core_paths()["registry"])
        for n in nodes:
            en = n.get("en") or {}
            if en.get("title_status") != "locked" or not en.get("canonical_title"):
                ctx.report.error("WDV-WF-005", f"Titre anglais non verrouillé avant production française : {n.get('id')}", path=ctx.core_paths()["registry"])

    if english_deferred:
        english_records = [((((registry.get("debate") or {}).get("pages") or {}).get("en") or {}), "debate")]
        english_records.extend(((n.get("en") or {}), str(n.get("id"))) for n in nodes)
        for record, identifier in english_records:
            if record.get("title_status") == "locked" and not record.get("canonical_title"):
                ctx.report.error("WDV-WF-005", f"Titre anglais déclaré verrouillé mais absent : {identifier}", path=ctx.core_paths()["registry"])

    patch_rel = "patches/interlanguage_fr.validated.json"
    if norm_versions.get("consolidated_norm") not in {"1.2.0", "1.2.1", "1.2.2", "1.2.3", "1.2.4", "1.2.5", "1.2.6", "1.2.7", "1.2.8", "1.2.9", "1.2.10", "1.2.11", "1.2.12", "1.2.13", "1.2.14", "1.2.15", "1.2.16", "1.2.17", "1.2.18", "1.2.19", "1.2.20", "1.2.21", "1.2.22", "1.2.23", "1.2.24", "1.2.25", "1.2.26", "1.2.27", "1.2.28", "1.2.29", "1.2.30", "1.2.31", "1.2.32", "1.2.33", "1.2.34", "1.2.35", "1.2.36", "1.2.37"}:
        if state_at_least(status, "interlanguage_prepared"):
            patch = ctx.load_json(patch_rel, required=True)
            if isinstance(patch, dict) and patch.get("status") not in {"validated", "partially_applied", "applied"}:
                ctx.report.error("WDV-WF-001", "Patch interlangue non validé à l'état interlanguage_prepared", path=patch_rel)
        if state_at_least(status, "interlanguage_applied"):
            patch = ctx.load_json(patch_rel)
            if not isinstance(patch, dict) or patch.get("status") != "applied":
                ctx.report.error("WDV-WF-001", "L'état interlanguage_applied exige un patch appliqué", path=patch_rel)
    if state_at_least(status, "released"):
        release_path = (manifest.get("release") or {}).get("release_manifest_path")
        release = ctx.load_json(release_path, required=True) if release_path else None
        if not isinstance(release, dict) or release.get("global_status") != "released" or not release.get("finalized_at"):
            ctx.report.error("WDV-WF-001", "L'état released exige un manifeste de libération finalisé", path=release_path or "release_manifest.json")
    if status == "archived":
        receipt = (manifest.get("release") or {}).get("release_receipt_path")
        if not receipt or not ctx.exists(receipt):
            ctx.report.error("WDV-WF-001", "L'état archived exige un reçu d'archive externe référencé", path="manifest.json")

    # Work chronology and impossible completed stages.
    works = manifest.get("works", [])
    seen_work_ids: set[str] = set()
    for work in works:
        wid = work.get("work_id")
        if wid in seen_work_ids:
            ctx.report.error("WDV-GRA-001", f"Identifiant de Work dupliqué : {wid}", path="manifest.json")
        seen_work_ids.add(wid)
        if work.get("status") == "completed":
            min_state = WORK_MIN_STATE.get(work.get("work_type"))
            if min_state and not corrective_mode and not state_at_least(status, min_state):
                ctx.report.error("WDV-WF-001", f"Work {wid} terminé mais état global trop ancien : {status}", path="manifest.json")
            if not work.get("completed_at"):
                ctx.report.error("WDV-WF-001", f"Work terminé sans completed_at : {wid}", path="manifest.json")
        if work.get("status") == "blocked" and state_at_least(status, WORK_MIN_STATE.get(work.get("work_type"), "initialized")):
            ctx.report.warning("WDV-WF-001", f"Work bloqué présent dans un paquet ayant progressé : {wid}", path="manifest.json")

    # Handoff compatibility.
    validations_by_scope = {v.get("scope"): v for v in manifest.get("validations", [])}
    for path in sorted(ctx.iter_files("handoff/*.json")):
        rel = ctx.relative(path)
        handoff = ctx.load_json(rel)
        if not isinstance(handoff, dict) or handoff.get("template_mode"):
            continue
        if handoff.get("debate_id") != manifest.get("debate_id"):
            ctx.report.error("WDV-WF-004", "Transmission rattachée à un autre débat", path=rel)
        if not corrective_mode:
            for key, value in (handoff.get("normative_versions") or {}).items():
                if value != norm_versions.get(key):
                    ctx.report.error("WDV-WF-005", f"Version normative incompatible dans la transmission : {key}", path=rel, details={"handoff": value, "manifest": norm_versions.get(key)})
        required_state = (handoff.get("destination") or {}).get("required_global_status")
        if required_state and not corrective_mode and not state_at_least(status, required_state) and status not in {"blocked", "migration_required"}:
            ctx.report.error("WDV-WF-004", f"État global incompatible avec la transmission : {required_state} requis", path=rel)
        for required in handoff.get("required_validations", []):
            scope = required.get("validation_type")
            current = validations_by_scope.get(scope)
            if not current or current.get("result") not in {"passed", "passed_with_warnings"}:
                ctx.report.error("WDV-WF-003", f"Validation préalable absente pour la transmission : {scope}", path=rel)
        if (handoff.get("origin") or {}).get("result") in {"blocked", "failed"} and not corrective_mode and status not in {"blocked", "migration_required"}:
            ctx.report.error("WDV-WF-004", "Le paquet a progressé malgré une transmission d'origine bloquée ou échouée", path=rel)

    ctx.report.metrics["workflow"] = {"global_status": status, "passed_validation_scopes": sorted(scopes), "english_translation_status": english_translation_status(manifest), "english_translation_deferred": english_deferred}
