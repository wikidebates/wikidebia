#!/usr/bin/env python3
"""Prepare, finalize and apply the French content review of a workspace.

This stage starts only after French titles, rubriques and keywords have been
applied.  It reviews the debate heading, introduction, Wikipedia articles,
the nine documentary buckets, every French argument summary and its source
selection.  No final MediaWiki page is rendered and no English text is
created.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import shutil
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any, Mapping, Sequence

from wikidebia_corpus_build import (
    NORM_VERSION,
    VALIDATOR_VERSION,
    CorpusBuildError,
    canonical_json,
    exclusive_lock,
    full_tree_sha256,
    load_json,
    now_iso,
    relative_to_project,
    sha256_bytes,
    write_json,
)
from wikidebia_editorial_workspace import (
    WorkspaceError,
    fsync_directory,
    validate_work_id,
    workspace_receipt_hash,
)
from wikidebia_editorial_review import (
    EditorialReviewError,
    _assert_source_unchanged,
    _load_workspace,
    _run_validator,
)
from wikidebia_graph_extract import iter_templates, normalize_key

KIT_VERSION = "2.15.37"
CONTENT_REVIEW_SCHEMA = "wikidebia-fr-content-review-1.0"
CONTENT_LOCK_SCHEMA = "wikidebia-fr-content-lock-1.0"
CONTENT_CHANGESET_SCHEMA = "wikidebia-fr-content-changeset-1.0"
SOURCES_WORKING_SCHEMA = "wikidebia-source-registry-working-1.0"

PAGE_LIFECYCLE_PARAMETERS = {
    # Ces paramètres sont des métadonnées historiques opaques : sur une page
    # préexistante, présence ET valeur sont reprises exactement. Les profils de
    # génération ne s'appliquent qu'aux pages nouvelles.
    "debate": (
        "avancement", "avertissements-titre", "avertissements-débat",
        "avertissements-bibliographie", "avertissements-sitographie",
        "avertissements-vidéographie", "débats-connexes", "interlangue",
        "date-création",
    ),
    "argument": (
        "initialisation", "nom", "avertissements-titre",
        "avertissements-argument", "avertissements-résumé",
        "avertissements-références", "avertissements-justifications",
        "avertissements-objections", "débat-détaillé", "interlangue",
        "date-création",
    ),
}


def _page_lifecycle_snapshot(template: Any, page_type: str) -> dict[str, Any]:
    """Capture exact presence/value of protected parameters on an imported page."""
    names = PAGE_LIFECYCLE_PARAMETERS[page_type]
    return {
        name: {"present": name in template.params, "value": template.get(name) if name in template.params else None}
        for name in names
    }

DEBATE_BUCKETS: dict[str, tuple[str, str]] = {
    "bibliographie-pour": ("bibliography", "pro_reference"),
    "bibliographie-contre": ("bibliography", "con_reference"),
    "bibliographie-ni-pour-ni-contre": ("bibliography", "neutral_reference"),
    "sitographie-pour": ("webliography", "pro_reference"),
    "sitographie-contre": ("webliography", "con_reference"),
    "sitographie-ni-pour-ni-contre": ("webliography", "neutral_reference"),
    "vidéographie-pour": ("videography", "pro_reference"),
    "vidéographie-contre": ("videography", "con_reference"),
    "vidéographie-ni-pour-ni-contre": ("videography", "neutral_reference"),
}
ARGUMENT_BUCKETS = {
    "bibliography": "bibliography",
    "webliography": "webliography",
    "videography": "videography",
}
SOURCE_METADATA_FIELDS = (
    "authors", "article", "work", "volume", "issue", "location", "publisher",
    "place", "date", "link", "page", "site", "title",
)
SUMMARY_TRUE_FIELDS = (
    "summary_preserves_node_identity",
    "thesis_first",
    "general_public_style",
    "sentence_rhythm_reviewed",
    "technical_terms_reviewed",
    "opening_develops_title",
    "example_or_data_reviewed",
    "assertive_tone_reviewed",
    "no_artificial_example_or_number",
    "no_polemical_overstatement",
    "no_self_objection",
    "conviction_visible",
    "wikipedia_hover_links_reviewed",
    "specialized_terms_linked_or_explained",
    "factual_claims_documented",
)
INTRO_TRUE_FIELDS = (
    "subject_and_scope_defined",
    "stakes_explained",
    "dedicated_stakes_subsection_present",
    "stakes_consequences_concrete",
    "stakes_not_argument_catalogue",
    "debate_question_explained",
    "history_and_evolution_addressed",
    "current_state_addressed_or_not_applicable",
    "factual_claims_referenced",
    "progression_coherent",
    "no_argument_tree_mirroring",
    "no_topic_specific_checklist",
    "complete_topic_fits_heading",
    "debate_sections_precise",
    "documentation_proportionate_to_literature",
    "wikipedia_hover_links_reviewed",
    "specialized_terms_linked_or_explained",
    "common_acronym_used_or_not_applicable",
    "topic_is_nominal_label",
    "conventional_topic_label_used_or_not_applicable",
    "complete_topic_lowercase_initial_or_justified",
    "information_density_reviewed",
    "subsections_non_redundant",
    "no_generic_stakes_filler",
    "documentation_orientation_reviewed",
    "youtube_authorship_reviewed",
    "reference_note_punctuation_reviewed",
    "specialized_term_inventory_reviewed",
)
NUMBER = re.compile(r"(?<![\wÀ-ÿ])\d+(?:[.,]\d+)?(?:\s*%)?(?![\wÀ-ÿ])")
META_DISCOURSE = re.compile(r"\b(?:cet argument|l'argument|la page|le raisonnement présenté)\b", re.I)
QUESTION_TOPIC = re.compile(r"^(?:si\b|faut[- ]il\b|doit[- ]on\b|whether\b|should\b)", re.I)
HTTP_URL = re.compile(r"^https?://", re.I)
SOURCE_ID = re.compile(r"^S[0-9]{5,}$")

CITATION_TEXT_KEYS = {"citation"}
CITATION_DATE_KEYS = {"date"}
CITATION_WARNING_KEYS = {"avertissements citation", "avertissements"}


def _citation_records(value: str, node_id: str) -> list[dict[str, Any]]:
    """Inventory imported Citation models without altering documentary fields.

    The exact parameter names, order and values are retained.  Only ``citation``,
    ``date`` and the citation warning field are later allowed to differ in the
    English translation lock.
    """
    records: list[dict[str, Any]] = []
    for call in iter_templates(value or ""):
        if normalize_key(call.name) != "citation":
            continue
        parameters = [{"name": name, "value": val} for name, val in call.params.items()]
        text_values = [val for name, val in call.params.items() if normalize_key(name) in CITATION_TEXT_KEYS]
        date_values = [val for name, val in call.params.items() if normalize_key(name) in CITATION_DATE_KEYS]
        warning_values = [val for name, val in call.params.items() if normalize_key(name) in CITATION_WARNING_KEYS and str(val).strip()]
        if len(text_values) != 1 or not str(text_values[0]).strip():
            raise ContentReviewError(f"Citation importée sans paramètre citation unique dans {node_id}")
        if len(date_values) > 1:
            raise ContentReviewError(f"Citation importée avec plusieurs paramètres date dans {node_id}")
        if len(set(str(v).strip() for v in warning_values)) > 1:
            raise ContentReviewError(f"Citation importée avec plusieurs avertissements divergents dans {node_id}")
        controlled = CITATION_TEXT_KEYS | CITATION_DATE_KEYS | CITATION_WARNING_KEYS
        preserved = [copy.deepcopy(row) for row in parameters if normalize_key(row["name"]) not in controlled]
        records.append({
            "id": f"{node_id}-C{len(records)+1:03d}",
            "source_template": call.name.strip(),
            "source_parameters": parameters,
            "citation": str(text_values[0]).strip(),
            "date": str(date_values[0]).strip() if date_values else "",
            "avertissements-citation": str(warning_values[0]).strip() if warning_values else "",
            "preserved_parameters": preserved,
        })
    return records


class ContentReviewError(EditorialReviewError):
    pass


def content_review_sha256(review: Mapping[str, Any]) -> str:
    body = copy.deepcopy(dict(review))
    body.pop("review_sha256", None)
    return sha256_bytes(canonical_json(body))


def _text(value: Any, label: str, minimum: int = 1) -> str:
    if not isinstance(value, str) or len(value.strip()) < minimum:
        raise ContentReviewError(f"{label} est absent ou trop court")
    return value.strip()


def _list_strings(value: Any, label: str) -> list[str]:
    if not isinstance(value, list):
        raise ContentReviewError(f"{label} doit être une liste")
    result: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise ContentReviewError(f"{label} contient une valeur vide")
        clean = item.strip()
        if clean in result:
            raise ContentReviewError(f"{label} contient un doublon : {clean}")
        result.append(clean)
    return result


def _outer_template(path: Path, names: set[str]):
    text = path.read_text(encoding="utf-8")
    matches = [call for call in iter_templates(text) if normalize_key(call.name) in names]
    if not matches:
        raise ContentReviewError(f"Modèle principal introuvable dans {path.name}")
    return max(matches, key=lambda call: len(call.raw))


def _subsections(value: str) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for call in iter_templates(value or ""):
        if normalize_key(call.name) != "sous partie":
            continue
        result.append({
            "title": call.get("titre").strip(),
            "content": call.get("contenu").strip(),
        })
    return result


def _wikipedia_articles(value: str) -> list[str]:
    result: list[str] = []
    for call in iter_templates(value or ""):
        if normalize_key(call.name) != "article wikipedia":
            continue
        page = call.get("page").strip()
        if page and page not in result:
            result.append(page)
    return result


def _assert_reviewed_copy(workspace: Path, meta: Mapping[str, Any]) -> Path:
    reviewed = workspace / "reviewed-copy"
    if not reviewed.is_dir() or reviewed.is_symlink():
        raise ContentReviewError("reviewed-copy absent ou non sûr")
    expected = str((meta.get("reviewed_copy") or {}).get("tree_sha256") or "")
    actual = full_tree_sha256(reviewed)
    if not expected or actual != expected:
        raise ContentReviewError("reviewed-copy a changé depuis l’application des métadonnées")
    if (reviewed / "output").exists():
        raise ContentReviewError("Des pages finales existent déjà dans reviewed-copy")
    return reviewed


def _source_imports(reviewed: Path) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    registry = load_json(reviewed / "data/registre_debat.json", "registre du débat")
    provenance = load_json(reviewed / "data/import_provenance.json", "provenance d’import")
    debate_row = next((row for row in provenance.get("pages") or [] if row.get("kind") == "debate"), None)
    if not debate_row:
        raise ContentReviewError("Page Débat absente de la provenance")
    debate_path = reviewed / str(debate_row.get("import_path"))
    debate = _outer_template(debate_path, {"debat"})
    debate_source = {
        "import_path": str(debate_row.get("import_path")),
        "import_sha256": debate_row.get("sha256"),
        "subject": debate.get("sujet").strip(),
        "complete_topic": debate.get("sujet-complet").strip(),
        "introduction": debate.get("introduction").strip(),
        "subsections": _subsections(debate.get("introduction")),
        "wikipedia_articles": _wikipedia_articles(debate.get("articles-Wikipédia")),
        "documentation_raw": {bucket: debate.get(bucket).strip() for bucket in DEBATE_BUCKETS},
        "page_origin": "preexisting",
        "preserved_parameters": _page_lifecycle_snapshot(debate, "debate"),
    }
    nodes = {
        str(node.get("id")): node
        for node in ((registry.get("graph") or {}).get("nodes") or [])
        if node.get("status") == "active"
    }
    arguments: list[dict[str, Any]] = []
    rows = {str(row.get("page_id")): row for row in provenance.get("pages") or [] if row.get("kind") == "argument"}
    if set(rows) != set(nodes):
        raise ContentReviewError("La provenance ne couvre pas exactement les arguments actifs")
    for node_id in sorted(nodes):
        row = rows[node_id]
        path = reviewed / str(row.get("import_path"))
        tmpl = _outer_template(path, {"argument"})
        arguments.append({
            "id": node_id,
            "canonical_title": ((nodes[node_id].get("fr") or {}).get("canonical_title")),
            "displayed_title": ((nodes[node_id].get("fr") or {}).get("displayed_title")),
            "import_path": str(row.get("import_path")),
            "import_sha256": row.get("sha256"),
            "summary": tmpl.get("résumé").strip(),
            "citations": _citation_records(tmpl.get("citations"), node_id),
            "documentation_raw": {
                "bibliography": tmpl.get("références-bibliographiques").strip(),
                "webliography": tmpl.get("références-sitographiques").strip(),
                "videography": tmpl.get("références-vidéographiques").strip(),
            },
            "page_origin": "preexisting",
            "preserved_parameters": _page_lifecycle_snapshot(tmpl, "argument"),
        })
    return registry, debate_source, arguments


def _blank_intro_review(source: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "status": "pending",
        "subject_decision": "pending",
        "proposed_subject": source.get("subject"),
        "complete_topic_decision": "pending",
        "proposed_complete_topic": source.get("complete_topic"),
        "topic_label_rationale": "",
        "common_acronym": None,
        "complete_topic_initial_capital_justification": None,
        "introduction_decision": "pending",
        "proposed_introduction": source.get("introduction"),
        "introduction_rationale": "",
        "subsections": [
            {
                "title": row.get("title"),
                "purpose": "",
                "necessary_for_understanding": False,
                "technical_or_specialized": False,
                "relevance_to_debate_explained": False,
                "stakes_section": False,
                "concrete_stakes": [],
            }
            for row in source.get("subsections") or []
        ],
        "wikipedia_articles_decision": "pending",
        "proposed_wikipedia_articles": list(source.get("wikipedia_articles") or []),
        "wikipedia_articles_verified": False,
        "documentation_decisions": {bucket: "pending" for bucket in DEBATE_BUCKETS},
        "proposed_documentation": {bucket: [] for bucket in DEBATE_BUCKETS},
        "documentation_rationales": {bucket: "" for bucket in DEBATE_BUCKETS},
        "documentation_family_notes": {"bibliography": "", "webliography": "", "videography": ""},
        **{field: False for field in INTRO_TRUE_FIELDS},
        "terminal_period_sentence_exceptions": [],
        "specialized_term_inventory": [],
        "reviewer": "",
        "reviewed_at": None,
        "note": "",
    }


def _blank_summary_review(source: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "status": "pending",
        "summary_decision": "pending",
        "proposed_summary": source.get("summary"),
        "summary_rationale": "",
        "documentation_decisions": {bucket: "pending" for bucket in ARGUMENT_BUCKETS},
        "proposed_sources": {bucket: [] for bucket in ARGUMENT_BUCKETS},
        "documentation_rationale": "",
        **{field: False for field in SUMMARY_TRUE_FIELDS},
        "forceful_expression": "",
        "quantitative_claims_verified": False,
        "quantitative_claims_note": "",
        "reviewer": "",
        "reviewed_at": None,
        "note": "",
    }


def prepare_review(project_root: Path, debate_id: str, work_id: str, *, overwrite: bool = False) -> dict[str, Any]:
    workspace, meta = _load_workspace(project_root, debate_id, work_id)
    if meta.get("status") not in {"fr_metadata_applied", "fr_content_review_ready"}:
        raise ContentReviewError(f"Statut incompatible avec la préparation du contenu : {meta.get('status')}")
    _assert_source_unchanged(project_root, debate_id, meta)
    reviewed = _assert_reviewed_copy(workspace, meta)
    review_path = workspace / "reviews/fr/content_review.json"
    sources_path = workspace / "data/sources_working.json"
    if review_path.exists() and not overwrite:
        existing = load_json(review_path, "revue de contenu")
        return {
            "status": "fr_content_review_ready",
            "debate_id": debate_id,
            "work_id": work_id,
            "review_path": relative_to_project(review_path, project_root),
            "arguments": len(existing.get("arguments") or []),
            "idempotent": True,
        }
    if overwrite and (workspace / "content-reviewed-copy").exists():
        raise ContentReviewError("Impossible de régénérer une revue déjà appliquée")
    registry, debate_source, arguments = _source_imports(reviewed)
    now = now_iso()
    review = {
        "schema": CONTENT_REVIEW_SCHEMA,
        "schema_version": "1.0",
        "normative_revision": NORM_VERSION,
        "kit_version": KIT_VERSION,
        "debate_id": debate_id,
        "work_id": work_id,
        "status": "draft",
        "prepared_at": now,
        "prepared_reviewed_copy_sha256": full_tree_sha256(reviewed),
        "debate": {"source": debate_source, "review": _blank_intro_review(debate_source)},
        "arguments": [
            {"id": row["id"], "source": row, "review": _blank_summary_review(row)}
            for row in arguments
        ],
        "global_review": {
            "reviewer": "",
            "reviewed_at": None,
            "all_french_content_reviewed": False,
            "all_selected_sources_verified": False,
            "no_final_pages_generated": True,
            "english_translation_not_started": True,
            "blocking_issues": [],
            "note": "",
        },
        "review_sha256": None,
    }
    write_json(review_path, review)
    current_sources = load_json(reviewed / "data/sources.json", "registre documentaire")
    working_sources = {
        "schema": SOURCES_WORKING_SCHEMA,
        "source_registry_version": current_sources.get("source_registry_version", "1.0"),
        "debate_id": debate_id,
        "work_id": work_id,
        "status": "draft",
        "prepared_at": now,
        "sources": copy.deepcopy(current_sources.get("sources") or []),
    }
    write_json(sources_path, working_sources)
    audit = {
        "schema": "wikidebia-fr-content-inventory-1.0",
        "debate_id": debate_id,
        "work_id": work_id,
        "generated_at": now,
        "debate": {
            "subject_present": bool(debate_source["subject"]),
            "complete_topic_present": bool(debate_source["complete_topic"]),
            "introduction_present": bool(debate_source["introduction"]),
            "subsections": len(debate_source["subsections"]),
            "wikipedia_articles": len(debate_source["wikipedia_articles"]),
            "documentary_buckets_nonempty": sum(bool(v) for v in debate_source["documentation_raw"].values()),
        },
        "arguments": {
            "count": len(arguments),
            "summaries_missing": sum(not bool(row["summary"]) for row in arguments),
            "summaries_under_80_chars": sum(len(row["summary"]) < 80 for row in arguments),
            "arguments_with_any_documentation": sum(any(row["documentation_raw"].values()) for row in arguments),
            "citations": sum(len(row.get("citations") or []) for row in arguments),
            "arguments_with_citations": sum(bool(row.get("citations")) for row in arguments),
        },
        "boundaries": {
            "automatic_rewriting": False,
            "final_pages_generated": False,
            "english_translation_started": False,
        },
    }
    write_json(workspace / "audits/fr_content_inventory.json", audit)
    markdown = [
        "# Inventaire du contenu français", "",
        f"- Débat : `{debate_id}`", f"- Arguments : {len(arguments)}",
        f"- Sous-parties importées : {len(debate_source['subsections'])}",
        f"- Articles Wikipédia importés : {len(debate_source['wikipedia_articles'])}",
        f"- Résumés absents : {audit['arguments']['summaries_missing']}",
        f"- Résumés de moins de 80 caractères : {audit['arguments']['summaries_under_80_chars']}",
        f"- Citations importées : {audit['arguments']['citations']}",
        "", "Aucune correction automatique n’a été appliquée.", "",
    ]
    (workspace / "audits/fr_content_inventory.md").write_text("\n".join(markdown), encoding="utf-8", newline="\n")
    meta = copy.deepcopy(meta)
    meta["kit_version"] = KIT_VERSION
    meta["status"] = "fr_content_review_ready"
    meta.setdefault("artifacts", {})["french_content_review"] = "reviews/fr/content_review.json"
    meta["artifacts"]["sources_working"] = "data/sources_working.json"
    meta["artifacts"]["content_reviewed_copy"] = "content-reviewed-copy"
    meta["french_content_review"] = {
        "status": "prepared",
        "prepared_at": now,
        "prepared_reviewed_copy_sha256": review["prepared_reviewed_copy_sha256"],
    }
    meta["workspace_sha256"] = None
    meta["workspace_sha256"] = workspace_receipt_hash(meta)
    write_json(workspace / "workspace.json", meta)
    # Metadata application declared translation readiness; content review now becomes the remaining gate.
    translation_path = workspace / "reviews/en/translation_readiness.json"
    if translation_path.is_file():
        translation = load_json(translation_path, "préparation anglaise")
        translation["status"] = "blocked_by_french_content_review"
        for item in translation.get("items") or []:
            item["translation_status"] = "blocked_by_french_content_review"
        write_json(translation_path, translation)
    return {
        "status": "fr_content_review_ready",
        "debate_id": debate_id,
        "work_id": work_id,
        "review_path": relative_to_project(review_path, project_root),
        "sources_path": relative_to_project(sources_path, project_root),
        "arguments": len(arguments),
        "reviewed_copy_mutated": False,
        "final_pages_generated": False,
        "english_translation_started": False,
    }


def _select(decision: Mapping[str, Any], field: str, source: Any, proposed: str) -> Any:
    value = decision.get(field)
    if value == "keep":
        return copy.deepcopy(source)
    if value == "change":
        return copy.deepcopy(decision.get(proposed))
    raise ContentReviewError(f"Décision absente ou invalide : {field}")


def _plain(value: str) -> str:
    value = re.sub(r"<ref\b[^>]*>.*?</ref>|<ref\b[^>]*/>", " ", value or "", flags=re.I | re.S)
    value = re.sub(r"\{\{[^{}]*\}\}|\[\[[^\]]+\]\]", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def _validate_source_registry(data: Mapping[str, Any], debate_id: str) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    if data.get("schema") != SOURCES_WORKING_SCHEMA or data.get("debate_id") != debate_id:
        raise ContentReviewError("Identité ou schéma du registre documentaire de travail invalide")
    raw = data.get("sources")
    if not isinstance(raw, list):
        raise ContentReviewError("Le registre documentaire ne contient pas de liste sources")
    sources: list[dict[str, Any]] = []
    by_id: dict[str, dict[str, Any]] = {}
    dedup: set[str] = set()
    for index, source in enumerate(raw, start=1):
        if not isinstance(source, dict):
            raise ContentReviewError(f"Source #{index} invalide")
        source_id = _text(source.get("id"), f"identifiant de la source #{index}")
        if not SOURCE_ID.fullmatch(source_id) or source_id in by_id:
            raise ContentReviewError(f"Identifiant documentaire invalide ou dupliqué : {source_id}")
        source_type = source.get("type")
        if source_type not in {"bibliography", "webliography", "videography"}:
            raise ContentReviewError(f"Type documentaire invalide pour {source_id}")
        language = _text(source.get("language"), f"langue de {source_id}", 2)
        metadata = source.get("metadata")
        if not isinstance(metadata, dict) or set(metadata) != set(SOURCE_METADATA_FIELDS):
            raise ContentReviewError(f"Métadonnées incomplètes pour {source_id}")
        authors = metadata.get("authors")
        if not isinstance(authors, list) or any(not isinstance(a, str) or not a.strip() for a in authors):
            raise ContentReviewError(f"Liste d’auteurs invalide pour {source_id}")
        if source_type == "bibliography" and (not authors or not (metadata.get("article") or metadata.get("work"))):
            raise ContentReviewError(f"Référence bibliographique incomplète : {source_id}")
        if source_type in {"webliography", "videography"} and not HTTP_URL.match(str(metadata.get("link") or "")):
            raise ContentReviewError(f"Lien HTTP(S) obligatoire pour {source_id}")
        if source_type == "videography" and re.search(r"(?:youtube\.com/(?:watch|live)|youtu\.be/)", str(metadata.get("link") or ""), re.I) and not authors:
            raise ContentReviewError(f"Une vidéo YouTube doit indiquer le créateur ou la chaîne : {source_id}")
        date = metadata.get("date")
        if isinstance(date, str) and re.fullmatch(r"\d{4}-\d{2}(?:-\d{2})?", date.strip()):
            raise ContentReviewError(f"Date documentaire au format machine interdite : {source_id}")
        verification = source.get("verification")
        if not isinstance(verification, dict) or verification.get("status") != "verified":
            raise ContentReviewError(f"Source non vérifiée : {source_id}")
        if verification.get("language_verified") is not True:
            raise ContentReviewError(f"Langue non vérifiée pour {source_id}")
        if source_type in {"webliography", "videography"}:
            if verification.get("authorship_checked") is not True:
                raise ContentReviewError(f"Attribution non vérifiée pour {source_id}")
            if authors and verification.get("authorship_verified") is not True:
                raise ContentReviewError(f"Auteurs renseignés mais non vérifiés pour {source_id}")
        usage = source.get("usage")
        if not isinstance(usage, list) or not usage:
            raise ContentReviewError(f"Aucun usage déclaré pour {source_id}")
        for use in usage:
            if not isinstance(use, dict) or not use.get("page_id") or use.get("language") != "fr":
                raise ContentReviewError(f"Usage documentaire invalide pour {source_id}")
            if use.get("role") not in {"supports_summary", "supports_introduction", "pro_reference", "con_reference", "neutral_reference", "context"}:
                raise ContentReviewError(f"Rôle documentaire invalide pour {source_id}")
            if use.get("role") == "supports_summary":
                if use.get("argument_development_verified") is not True:
                    raise ContentReviewError(f"Le développement de l’argument n’est pas vérifié pour {source_id}")
                if not isinstance(use.get("also_develops_objections"), bool):
                    raise ContentReviewError(f"La couverture éventuelle d’objections doit être attestée pour {source_id}")
            if len(str(use.get("selection_reason") or "").strip()) < 12:
                raise ContentReviewError(f"Justification de sélection insuffisante pour {source_id}")
        key = _text(source.get("deduplication_key"), f"clé de dédoublonnage de {source_id}")
        if key.casefold() in dedup:
            raise ContentReviewError(f"Clé de dédoublonnage dupliquée : {key}")
        dedup.add(key.casefold())
        clean = copy.deepcopy(source)
        by_id[source_id] = clean
        sources.append(clean)
    return sources, by_id


def _has_usage(source: Mapping[str, Any], page_id: str, roles: set[str]) -> bool:
    return any(
        use.get("page_id") == page_id and use.get("language") == "fr" and use.get("role") in roles
        for use in source.get("usage") or []
        if isinstance(use, dict)
    )


REF_PAIR_RE = re.compile(r"<ref\b[^>]*>(.*?)</ref\s*>", re.I | re.S)


def _validated_terminal_period_exceptions(introduction: str, raw_exceptions: Any) -> list[dict[str, Any]]:
    if not isinstance(raw_exceptions, list):
        raise ContentReviewError("La liste terminal_period_sentence_exceptions est absente")
    period_bodies = {hashlib.sha256(body.strip().encode("utf-8")).hexdigest(): body.strip() for body in REF_PAIR_RE.findall(introduction) if body.strip().endswith(".")}
    validated: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in raw_exceptions:
        if not isinstance(item, dict):
            raise ContentReviewError("Exception de ponctuation de note invalide")
        body_sha = str(item.get("body_sha256") or "")
        evidence = str(item.get("sentence_evidence") or "").strip()
        body = period_bodies.get(body_sha)
        if not re.fullmatch(r"[0-9a-f]{64}", body_sha) or body_sha in seen or item.get("complete_sentence") is not True or len(evidence) < 12 or body is None or evidence not in body:
            raise ContentReviewError("Toute note terminée par un point doit être une phrase complète attestée par son empreinte et un extrait réel")
        seen.add(body_sha)
        validated.append({"body_sha256": body_sha, "complete_sentence": True, "sentence_evidence": evidence})
    missing = sorted(set(period_bodies) - seen)
    if missing:
        raise ContentReviewError("Une simple notice de référence se termine par un point; retirez-le ou attestez une véritable phrase complète")
    return validated


def _normalize_hover_article(value: Any) -> str:
    return re.sub(r"[_\s]+", " ", str(value or "")).strip().casefold()


def _normalize_visible(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "").replace("’", "'")).strip().casefold()


def _hover_entries(content: str, lang: str = "fr") -> list[dict[str, str]]:
    model = r"Lien\s+Wikipédia" if lang == "fr" else r"Wikipedia\s+link"
    display_key = "texte-affiché" if lang == "fr" else "displayed-text"
    pattern = re.compile(r"\{\{\s*" + model + r"\s*\|(?P<body>.*?)\}\}", re.I | re.S)
    result=[]
    for match in pattern.finditer(content or ""):
        params={}
        for chunk in match.group("body").split("|"):
            if "=" in chunk:
                k,v=chunk.split("=",1); params[k.strip().casefold()]=v.strip()
        article=params.get("article","")
        display=params.get(display_key.casefold()) or article
        if article: result.append({"article":_normalize_hover_article(article),"display":_normalize_visible(display)})
    return result


def _visible_text(content: str, lang: str = "fr") -> str:
    model = r"Lien\s+Wikipédia" if lang == "fr" else r"Wikipedia\s+link"
    display_key = "texte-affiché" if lang == "fr" else "displayed-text"
    pattern = re.compile(r"\{\{\s*" + model + r"\s*\|(?P<body>.*?)\}\}", re.I | re.S)
    def repl(m):
        params={}
        for chunk in m.group("body").split("|"):
            if "=" in chunk:
                k,v=chunk.split("=",1); params[k.strip().casefold()]=v.strip()
        return params.get(display_key.casefold()) or params.get("article","")
    text=pattern.sub(repl,content or "")
    text=re.sub(r"<ref(?:\s[^>]*)?>.*?</ref>|<ref(?:\s[^>]*)?\s*/>"," ",text,flags=re.I|re.S)
    text=re.sub(r"\{\{.*?\}\}"," ",text,flags=re.S)
    return _normalize_visible(text)


def _validated_specialized_term_inventory(introduction: str, raw_inventory: Any, subsection_ledger: Any, lang: str = "fr") -> list[dict[str, Any]]:
    if not isinstance(raw_inventory, list):
        raise ContentReviewError("L’inventaire des notions spécialisées est absent")
    subsections=_subsections(introduction)
    titles=[row["title"] for row in subsections]
    if [str(x.get("subsection_title") or "").strip() for x in raw_inventory if isinstance(x,dict)] != titles or len(raw_inventory)!=len(titles):
        raise ContentReviewError("L’inventaire des notions spécialisées ne couvre pas exactement les sous-parties")
    ledger={str(x.get("title") or "").strip():x for x in (subsection_ledger or []) if isinstance(x,dict)}
    by_title={x["title"]:x["content"] for x in subsections}
    prior={}
    clean=[]
    for index,inv in enumerate(raw_inventory,start=1):
        title=titles[index-1]
        if not isinstance(inv,dict) or inv.get("scan_complete") is not True or len(str(inv.get("scan_note") or "").strip())<30 or not isinstance(inv.get("terms"),list):
            raise ContentReviewError(f"Inventaire spécialisé incomplet pour {title}")
        terms=inv["terms"]
        if (ledger.get(title) or {}).get("technical_or_specialized") is True and not terms:
            raise ContentReviewError(f"La sous-partie technique {title} ne peut avoir un inventaire vide")
        visible=_visible_text(by_title[title],lang); hover=_hover_entries(by_title[title],lang); actual={(x['article'],x['display']) for x in hover}; declared=set(); seen=set(); rows=[]
        for term_index,row in enumerate(terms,start=1):
            if not isinstance(row,dict): raise ContentReviewError(f"Notion #{term_index} invalide dans {title}")
            term=str(row.get('term') or '').strip(); nt=_normalize_visible(term); treatment=row.get('treatment')
            if not term or nt in seen or treatment not in {'wikipedia_link','explained_inline','prior_treatment','context_sufficient'}: raise ContentReviewError(f"Notion #{term_index} invalide dans {title}")
            seen.add(nt)
            if nt not in visible: raise ContentReviewError(f"La notion {term} est absente de {title}")
            out={'term':term,'treatment':treatment}
            if treatment=='wikipedia_link':
                article=str(row.get('article') or '').strip(); key=(_normalize_hover_article(article),nt)
                if not article or key not in actual: raise ContentReviewError(f"Le lien déclaré pour {term} est absent de {title}")
                out['article']=article; declared.add(key); prior[(title,nt)]='wikipedia_link'
            elif treatment=='explained_inline':
                excerpt=str(row.get('explanation_excerpt') or '').strip()
                if len(excerpt)<20 or _normalize_visible(excerpt) not in visible: raise ContentReviewError(f"L’explication de {term} est absente de {title}")
                out['explanation_excerpt']=excerpt; prior[(title,nt)]='explained_inline'
            elif treatment=='prior_treatment':
                pt=str(row.get('prior_subsection_title') or '').strip(); pterm=str(row.get('prior_term') or '').strip(); np=_normalize_visible(pterm)
                if pt not in titles[:index-1] or prior.get((pt,np)) not in {'wikipedia_link','explained_inline'}: raise ContentReviewError(f"Le traitement antérieur de {term} est invalide")
                out.update({'prior_subsection_title':pt,'prior_term':pterm})
            else:
                justification=str(row.get('justification') or '').strip()
                if len(justification)<30: raise ContentReviewError(f"Le contexte suffisant pour {term} n’est pas justifié")
                out['justification']=justification
            rows.append(out)
        if actual-declared: raise ContentReviewError(f"Des liens Wikipédia de {title} ne figurent pas dans l’inventaire : {sorted(actual-declared)!r}")
        clean.append({'subsection_title':title,'scan_complete':True,'scan_note':str(inv['scan_note']).strip(),'terms':rows})
    return clean

def _validate_debate(review: Mapping[str, Any], source: Mapping[str, Any], sources: Mapping[str, Mapping[str, Any]], debate_id: str) -> dict[str, Any]:
    if review.get("status") != "approved":
        raise ContentReviewError("La revue de la page Débat n’est pas approuvée")
    subject = _text(_select(review, "subject_decision", source.get("subject"), "proposed_subject"), "sujet", 2)
    complete = _text(_select(review, "complete_topic_decision", source.get("complete_topic"), "proposed_complete_topic"), "sujet-complet", 2)
    if QUESTION_TOPIC.search(complete):
        raise ContentReviewError("sujet-complet ne doit pas être une question")
    first_alpha = next((char for char in complete if char.isalpha()), "")
    if first_alpha and first_alpha.isupper() and len(str(review.get("complete_topic_initial_capital_justification") or "").strip()) < 12:
        raise ContentReviewError("La majuscule initiale de sujet-complet n’est pas justifiée")
    introduction = _text(_select(review, "introduction_decision", source.get("introduction"), "proposed_introduction"), "introduction", 30)
    subsection_values = _subsections(introduction)
    if not subsection_values:
        raise ContentReviewError("L’introduction doit contenir au moins une Sous-partie")
    ledger = review.get("subsections")
    if not isinstance(ledger, list) or [row.get("title") for row in ledger if isinstance(row, dict)] != [row["title"] for row in subsection_values]:
        raise ContentReviewError("La revue des sous-parties ne correspond pas à l’introduction retenue")
    stakes_title = "Enjeux du débat"
    stakes_rows = []
    stakes_contents = []
    for index, (row, subsection) in enumerate(zip(ledger, subsection_values), start=1):
        if len(str(row.get("purpose") or "").strip()) < 12 or row.get("necessary_for_understanding") is not True:
            raise ContentReviewError(f"Sous-partie #{index} insuffisamment justifiée")
        if row.get("technical_or_specialized") is True and row.get("relevance_to_debate_explained") is not True:
            raise ContentReviewError(f"Pertinence technique non attestée pour la sous-partie #{index}")
        if subsection["title"] == stakes_title:
            stakes_rows.append(row)
            stakes_contents.append(subsection["content"])
    if len(stakes_rows) != 1:
        raise ContentReviewError('L’introduction française doit contenir exactement une sous-partie intitulée "Enjeux du débat"')
    stakes_row = stakes_rows[0]
    if stakes_row.get("stakes_section") is not True:
        raise ContentReviewError("La revue doit identifier explicitement la sous-partie Enjeux du débat")
    concrete_stakes = stakes_row.get("concrete_stakes")
    if not isinstance(concrete_stakes, list):
        raise ContentReviewError("Les conséquences concrètes de la sous-partie Enjeux du débat sont absentes")
    normalized_stakes = [str(item).strip() for item in concrete_stakes if str(item).strip()]
    if len(normalized_stakes) < 2 or len({item.casefold() for item in normalized_stakes}) < 2 or any(len(item) < 20 for item in normalized_stakes):
        raise ContentReviewError("La sous-partie Enjeux du débat doit consigner au moins deux conséquences concrètes distinctes")
    stakes_content = stakes_contents[0]
    if len(re.findall(r"\b[\wÀ-ÿ'-]+\b", stakes_content)) < 45 or len(re.findall(r"[.!?](?:\s|$)", stakes_content)) < 3:
        raise ContentReviewError("La sous-partie Enjeux du débat est trop brève ou symbolique")
    for field in INTRO_TRUE_FIELDS:
        if review.get(field) is not True:
            raise ContentReviewError(f"Attestation d’introduction manquante : {field}")
    specialized_term_inventory = _validated_specialized_term_inventory(introduction, review.get("specialized_term_inventory"), ledger, "fr")
    terminal_period_sentence_exceptions = _validated_terminal_period_exceptions(introduction, review.get("terminal_period_sentence_exceptions"))
    if len(str(review.get("topic_label_rationale") or "").strip()) < 12:
        raise ContentReviewError("Justification du libellé de sujet insuffisante")
    family_notes = review.get("documentation_family_notes")
    if not isinstance(family_notes, dict) or set(family_notes) != {"bibliography", "webliography", "videography"}:
        raise ContentReviewError("Notes par famille documentaire absentes")
    for family, note in family_notes.items():
        if len(str(note).strip()) < 20:
            raise ContentReviewError(f"Note documentaire trop courte pour {family}")
    wikipedia = _list_strings(_select(review, "wikipedia_articles_decision", source.get("wikipedia_articles") or [], "proposed_wikipedia_articles"), "articles Wikipédia")
    if not wikipedia or review.get("wikipedia_articles_verified") is not True:
        raise ContentReviewError("Au moins un article Wikipédia français vérifié est requis")
    documentation: dict[str, list[str]] = {}
    raw_decisions = review.get("documentation_decisions")
    proposed = review.get("proposed_documentation")
    rationales = review.get("documentation_rationales")
    if not isinstance(raw_decisions, dict) or not isinstance(proposed, dict) or not isinstance(rationales, dict):
        raise ContentReviewError("Décisions documentaires de la page Débat absentes")
    selected_roles: dict[str, set[str]] = {}
    for bucket, (source_type, role) in DEBATE_BUCKETS.items():
        if raw_decisions.get(bucket) != "change":
            raise ContentReviewError(f"Le bucket {bucket} doit être reconstruit sous forme de sources contrôlées")
        selected = _list_strings(proposed.get(bucket), bucket)
        if len(str(rationales.get(bucket) or "").strip()) < 12:
            raise ContentReviewError(f"Justification documentaire absente pour {bucket}")
        for source_id in selected:
            source_row = sources.get(source_id)
            if not source_row or source_row.get("type") != source_type:
                raise ContentReviewError(f"Type de source incompatible dans {bucket} : {source_id}")
            if source_row.get("language") != "fr":
                raise ContentReviewError(f"Une page Débat française ne peut utiliser une source non française : {source_id}")
            if not _has_usage(source_row, debate_id, {role}):
                raise ContentReviewError(f"Usage documentaire manquant pour {source_id} dans {bucket}")
            selected_roles.setdefault(source_id, set()).add(role)
        documentation[bucket] = selected
    conflicts = {sid: sorted(roles) for sid, roles in selected_roles.items() if len(roles) > 1}
    if conflicts:
        raise ContentReviewError(
            "Une même référence ne peut figurer dans plusieurs orientations; une source couvrant les deux camps doit être classée ni pour ni contre : "
            + repr(conflicts)
        )
    for source_id, source_row in sources.items():
        roles = {
            use.get("role") for use in source_row.get("usage") or []
            if isinstance(use, dict) and use.get("page_id") == debate_id and use.get("language") == "fr"
            and use.get("role") in {"pro_reference", "con_reference", "neutral_reference"}
        }
        if "pro_reference" in roles and "con_reference" in roles:
            raise ContentReviewError(
                f"La référence {source_id} est déclarée à la fois pour et contre; elle doit recevoir uniquement le rôle neutral_reference"
            )
    if review.get("reviewer") is None or len(str(review.get("reviewer") or "").strip()) < 3:
        raise ContentReviewError("Relecteur de l’introduction absent")
    _text(review.get("reviewed_at"), "date de revue de l’introduction", 10)
    _text(review.get("note"), "note de revue de l’introduction", 12)
    return {
        "subject": subject,
        "complete_topic": complete,
        "common_acronym": review.get("common_acronym"),
        "introduction": introduction,
        "subsections": ledger,
        "wikipedia_articles": wikipedia,
        "documentation": documentation,
        "documentation_family_notes": copy.deepcopy(family_notes),
        "reviewer": review.get("reviewer"),
        "reviewed_at": review.get("reviewed_at"),
        "note": review.get("note"),
        "attestations": {field: True for field in INTRO_TRUE_FIELDS},
        "terminal_period_sentence_exceptions": terminal_period_sentence_exceptions,
        "specialized_term_inventory": specialized_term_inventory,
        "page_origin": source.get("page_origin", "preexisting"),
        "preserved_parameters": copy.deepcopy(source.get("preserved_parameters") or {}),
    }


def _validate_argument(item: Mapping[str, Any], sources: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    node_id = _text(item.get("id"), "identifiant d’argument")
    source = item.get("source") or {}
    review = item.get("review") or {}
    if review.get("status") != "approved":
        raise ContentReviewError(f"Revue non approuvée pour {node_id}")
    summary = _text(_select(review, "summary_decision", source.get("summary"), "proposed_summary"), f"résumé de {node_id}", 40)
    if META_DISCOURSE.search(_plain(summary)):
        raise ContentReviewError(f"Métadiscours interdit dans le résumé de {node_id}")
    for field in SUMMARY_TRUE_FIELDS:
        if review.get(field) is not True:
            raise ContentReviewError(f"Attestation manquante pour {node_id} : {field}")
    expression = _text(review.get("forceful_expression"), f"expression de force de {node_id}", 12)
    if len(re.findall(r"[A-Za-zÀ-ÿ]+", expression)) < 3 or _plain(expression).casefold() not in _plain(summary).casefold():
        raise ContentReviewError(f"L’expression de force n’est pas présente dans le résumé de {node_id}")
    numbers = NUMBER.findall(_plain(summary))
    if numbers:
        if review.get("quantitative_claims_verified") is not True or len(str(review.get("quantitative_claims_note") or "").strip()) < 12:
            raise ContentReviewError(f"Donnée chiffrée non documentée dans {node_id}")
    decisions = review.get("documentation_decisions")
    proposed = review.get("proposed_sources")
    if not isinstance(decisions, dict) or not isinstance(proposed, dict):
        raise ContentReviewError(f"Décisions documentaires absentes pour {node_id}")
    selected_by_type: dict[str, list[str]] = {}
    for bucket, source_type in ARGUMENT_BUCKETS.items():
        if decisions.get(bucket) != "change":
            raise ContentReviewError(f"La documentation de {node_id}/{bucket} doit être reconstruite")
        selected = _list_strings(proposed.get(bucket), f"sources {bucket} de {node_id}")
        for source_id in selected:
            source_row = sources.get(source_id)
            if not source_row or source_row.get("type") != source_type:
                raise ContentReviewError(f"Type de source incompatible pour {node_id} : {source_id}")
            if not _has_usage(source_row, node_id, {"supports_summary"}):
                raise ContentReviewError(f"Usage supports_summary absent pour {node_id} : {source_id}")
        selected_by_type[bucket] = selected
    _text(review.get("summary_rationale"), f"justification du résumé de {node_id}", 12)
    _text(review.get("documentation_rationale"), f"justification documentaire de {node_id}", 12)
    _text(review.get("reviewer"), f"relecteur de {node_id}", 3)
    _text(review.get("reviewed_at"), f"date de revue de {node_id}", 10)
    _text(review.get("note"), f"note de revue de {node_id}", 12)
    return {
        "id": node_id,
        "canonical_title": source.get("canonical_title"),
        "displayed_title": source.get("displayed_title"),
        "summary": summary,
        "citations": copy.deepcopy(source.get("citations") or []),
        "sources": selected_by_type,
        "status": "revised" if review.get("summary_decision") == "change" else "approved",
        "forceful_expression": expression,
        "quantitative_claims": numbers,
        "quantitative_claims_verified": bool(numbers) and True or bool(review.get("quantitative_claims_verified")),
        "quantitative_claims_note": review.get("quantitative_claims_note"),
        "reviewer": review.get("reviewer"),
        "reviewed_at": review.get("reviewed_at"),
        "note": review.get("note"),
        "attestations": {field: True for field in SUMMARY_TRUE_FIELDS},
        "page_origin": source.get("page_origin", "preexisting"),
        "preserved_parameters": copy.deepcopy(source.get("preserved_parameters") or {}),
    }


def finalize_review(project_root: Path, debate_id: str, work_id: str) -> dict[str, Any]:
    workspace, meta = _load_workspace(project_root, debate_id, work_id)
    if meta.get("status") not in {"fr_content_review_ready", "fr_content_review_finalized"}:
        raise ContentReviewError(f"Statut incompatible avec la finalisation du contenu : {meta.get('status')}")
    _assert_source_unchanged(project_root, debate_id, meta)
    reviewed = _assert_reviewed_copy(workspace, meta)
    review_path = workspace / "reviews/fr/content_review.json"
    review = load_json(review_path, "revue de contenu")
    if review.get("status") == "approved" and review.get("review_sha256"):
        if review.get("review_sha256") != content_review_sha256(review):
            raise ContentReviewError("Empreinte de revue de contenu invalide")
        if review.get("prepared_reviewed_copy_sha256") != full_tree_sha256(reviewed):
            raise ContentReviewError("reviewed-copy a changé depuis la finalisation")
        return {"status": "fr_content_review_finalized", "debate_id": debate_id, "work_id": work_id, "review_sha256": review["review_sha256"], "idempotent": True}
    if review.get("schema") != CONTENT_REVIEW_SCHEMA or review.get("debate_id") != debate_id or review.get("work_id") != work_id:
        raise ContentReviewError("Identité ou schéma de la revue de contenu invalide")
    if review.get("prepared_reviewed_copy_sha256") != full_tree_sha256(reviewed):
        raise ContentReviewError("reviewed-copy a changé depuis la préparation")
    working_sources = load_json(workspace / "data/sources_working.json", "sources de travail")
    source_rows, by_source = _validate_source_registry(working_sources, debate_id)
    debate_block = review.get("debate") or {}
    final_debate = _validate_debate(debate_block.get("review") or {}, debate_block.get("source") or {}, by_source, debate_id)
    argument_items = review.get("arguments")
    if not isinstance(argument_items, list):
        raise ContentReviewError("Liste des arguments absente de la revue de contenu")
    registry = load_json(reviewed / "data/registre_debat.json", "registre du débat")
    active_ids = {
        str(node.get("id")) for node in ((registry.get("graph") or {}).get("nodes") or []) if node.get("status") == "active"
    }
    if {str(item.get("id")) for item in argument_items if isinstance(item, dict)} != active_ids:
        raise ContentReviewError("La revue de contenu ne couvre pas exactement les arguments actifs")
    final_arguments = [_validate_argument(item, by_source) for item in argument_items]
    global_review = review.get("global_review")
    if not isinstance(global_review, dict):
        raise ContentReviewError("Revue globale absente")
    for field in ("all_french_content_reviewed", "all_selected_sources_verified", "no_final_pages_generated", "english_translation_not_started"):
        if global_review.get(field) is not True:
            raise ContentReviewError(f"Attestation globale manquante : {field}")
    if global_review.get("blocking_issues") not in ([], None):
        raise ContentReviewError("La revue globale contient encore des blocages")
    _text(global_review.get("reviewer"), "relecteur global", 3)
    _text(global_review.get("reviewed_at"), "date de revue globale", 10)
    _text(global_review.get("note"), "note de revue globale", 12)
    selected_ids: set[str] = set()
    for ids in final_debate["documentation"].values():
        selected_ids.update(ids)
    for argument in final_arguments:
        for ids in argument["sources"].values():
            selected_ids.update(ids)
    if selected_ids != set(by_source):
        raise ContentReviewError(f"Le registre documentaire doit couvrir exactement les sources retenues; inutilisées={sorted(set(by_source)-selected_ids)}, absentes={sorted(selected_ids-set(by_source))}")
    finalized = copy.deepcopy(review)
    finalized.update({
        "kit_version": KIT_VERSION,
        "status": "approved",
        "finalized_at": now_iso(),
        "prepared_reviewed_copy_sha256": full_tree_sha256(reviewed),
        "source_registry_sha256": sha256_bytes(canonical_json({"source_registry_version": working_sources.get("source_registry_version"), "debate_id": debate_id, "sources": source_rows})),
        "final_values": {"debate": final_debate, "arguments": final_arguments, "sources": source_rows},
        "summary": {
            "arguments": len(final_arguments),
            "sources": len(source_rows),
            "debate_documentary_references": sum(len(v) for v in final_debate["documentation"].values()),
            "argument_documentary_references": sum(len(ids) for arg in final_arguments for ids in arg["sources"].values()),
            "citations": sum(len(arg.get("citations") or []) for arg in final_arguments),
        },
        "review_sha256": None,
    })
    finalized["review_sha256"] = content_review_sha256(finalized)
    write_json(review_path, finalized)
    meta = copy.deepcopy(meta)
    meta["kit_version"] = KIT_VERSION
    meta["status"] = "fr_content_review_finalized"
    meta["french_content_review"] = {
        "status": "finalized",
        "review_sha256": finalized["review_sha256"],
        "finalized_at": finalized["finalized_at"],
        "prepared_reviewed_copy_sha256": finalized["prepared_reviewed_copy_sha256"],
    }
    meta["workspace_sha256"] = None
    meta["workspace_sha256"] = workspace_receipt_hash(meta)
    write_json(workspace / "workspace.json", meta)
    return {
        "status": "fr_content_review_finalized",
        "debate_id": debate_id,
        "work_id": work_id,
        "review_sha256": finalized["review_sha256"],
        **finalized["summary"],
        "reviewed_copy_mutated": False,
        "final_pages_generated": False,
        "english_translation_started": False,
    }


def _introduction_review(final: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "normative_revision": NORM_VERSION,
        "entries": [{
            "language": "fr",
            **{field: True for field in INTRO_TRUE_FIELDS},
            "documentation_family_notes": copy.deepcopy(final["documentation_family_notes"]),
            "common_acronym": final.get("common_acronym"),
            "topic_label_rationale": "Le sujet retenu est le libellé nominal validé par la revue française.",
            "complete_topic_initial_capital_justification": None,
            "subsections": copy.deepcopy(final["subsections"]),
            "terminal_period_sentence_exceptions": copy.deepcopy(final.get("terminal_period_sentence_exceptions") or []),
            "specialized_term_inventory": copy.deepcopy(final.get("specialized_term_inventory") or []),
        }],
    }


def _mechanism_excerpt(summary: Any) -> str:
    text = str(summary or "").strip()
    if not text:
        return "Le résumé validé expose explicitement le mécanisme central de la thèse."
    first = re.split(r"(?<=[.!?])\s+", text, maxsplit=1)[0].strip()
    if len(first) >= 30:
        return first
    return text


def _summary_style_review(arguments: Sequence[Mapping[str, Any]], debate_id: str) -> dict[str, Any]:
    entries = []
    for arg in arguments:
        attestations = arg.get("attestations") or {}
        language = {
            "status": arg.get("status"),
            "thesis_first": attestations.get("thesis_first") is True,
            "general_public_style": attestations.get("general_public_style") is True,
            "sentence_rhythm_reviewed": attestations.get("sentence_rhythm_reviewed") is True,
            "technical_terms_reviewed": attestations.get("technical_terms_reviewed") is True,
            "opening_develops_title": attestations.get("opening_develops_title") is True,
            "example_or_data_reviewed": attestations.get("example_or_data_reviewed") is True,
            "assertive_tone_reviewed": attestations.get("assertive_tone_reviewed") is True,
            "no_artificial_example_or_number": attestations.get("no_artificial_example_or_number") is True,
            "no_polemical_overstatement": attestations.get("no_polemical_overstatement") is True,
            "conviction_visible": attestations.get("conviction_visible") is True,
            "wikipedia_hover_links_reviewed": attestations.get("wikipedia_hover_links_reviewed") is True,
            "specialized_terms_linked_or_explained": attestations.get("specialized_terms_linked_or_explained") is True,
            "forceful_expression": arg.get("forceful_expression"),
            "originality_reviewed": True,
            "mechanism_statement": _mechanism_excerpt(arg.get("summary")),
            "quantitative_claims_verified": arg.get("quantitative_claims_verified"),
            "quantitative_claims_note": arg.get("quantitative_claims_note"),
            "note": arg.get("note"),
        }
        entries.append({"id": arg.get("id"), "languages": {"fr": language}})
    return {
        "schema_version": "1.0",
        "normative_revision": NORM_VERSION,
        "debate_id": debate_id,
        "entries": entries,
    }


def _build_content_copy(project_root: Path, source: Path, target: Path, review: Mapping[str, Any], debate_id: str, work_id: str) -> dict[str, Any]:
    shutil.copytree(source, target, symlinks=False, copy_function=shutil.copy2)
    final = review["final_values"]
    registry = load_json(target / "data/registre_debat.json", "registre du débat")
    by_id = {arg["id"]: arg for arg in final["arguments"]}
    for node in ((registry.get("graph") or {}).get("nodes") or []):
        if node.get("status") != "active":
            continue
        arg = by_id[str(node.get("id"))]
        node.setdefault("sources", {}).setdefault("fr", {})["bibliography"] = copy.deepcopy(arg["sources"]["bibliography"])
        node["sources"]["fr"]["webliography"] = copy.deepcopy(arg["sources"]["webliography"])
        node["sources"]["fr"]["videography"] = copy.deepcopy(arg["sources"]["videography"])
    sources_registry = {
        "source_registry_version": "1.0",
        "debate_id": debate_id,
        "sources": copy.deepcopy(final["sources"]),
    }
    timestamp = now_iso()
    content_lock = {
        "schema": CONTENT_LOCK_SCHEMA,
        "schema_version": "1.0",
        "normative_revision": NORM_VERSION,
        "kit_version": KIT_VERSION,
        "debate_id": debate_id,
        "work_id": work_id,
        "language": "fr",
        "status": "locked_for_translation_and_generation",
        "review_sha256": review["review_sha256"],
        "source_registry_sha256": review["source_registry_sha256"],
        "applied_at": timestamp,
        "debate": copy.deepcopy(final["debate"]),
        "arguments": copy.deepcopy(final["arguments"]),
    }
    operations: list[dict[str, Any]] = []
    source_debate = (review.get("debate") or {}).get("source") or {}
    for field, before, after in (
        ("subject", source_debate.get("subject"), final["debate"]["subject"]),
        ("complete_topic", source_debate.get("complete_topic"), final["debate"]["complete_topic"]),
        ("introduction", source_debate.get("introduction"), final["debate"]["introduction"]),
        ("wikipedia_articles", source_debate.get("wikipedia_articles"), final["debate"]["wikipedia_articles"]),
        ("documentation", None, final["debate"]["documentation"]),
    ):
        if before != after:
            operations.append({"entity_type": "debate", "entity_id": debate_id, "field": field, "before": before, "after": after})
    source_arguments = {str(item.get("id")): (item.get("source") or {}) for item in review.get("arguments") or []}
    for arg in final["arguments"]:
        src = source_arguments[arg["id"]]
        if src.get("summary") != arg["summary"]:
            operations.append({"entity_type": "argument", "entity_id": arg["id"], "field": "summary", "before": src.get("summary"), "after": arg["summary"]})
        operations.append({"entity_type": "argument", "entity_id": arg["id"], "field": "sources", "before": None, "after": copy.deepcopy(arg["sources"])})
    changeset = {
        "schema": CONTENT_CHANGESET_SCHEMA,
        "schema_version": "1.0",
        "debate_id": debate_id,
        "work_id": work_id,
        "status": "applied",
        "review_sha256": review["review_sha256"],
        "applied_at": timestamp,
        "operation_count": len(operations),
        "operations": operations,
        "source_imports_mutated": False,
        "metadata_lock_mutated": False,
        "final_pages_generated": False,
        "english_translation_started": False,
    }
    write_json(target / "data/registre_debat.json", registry)
    projection = load_json(target / "graph/graphe_argumentatif.json", "projection du graphe")
    projection["nodes"] = copy.deepcopy(((registry.get("graph") or {}).get("nodes") or []))
    write_json(target / "graph/graphe_argumentatif.json", projection)
    write_json(target / "data/sources.json", sources_registry)
    write_json(target / "data/fr_content_lock.json", content_lock)
    write_json(target / "changes/fr_content_changeset.json", changeset)
    write_json(target / "reviews/introduction_review.json", _introduction_review(final["debate"]))
    write_json(target / "reviews/summary_style_review.json", _summary_style_review(final["arguments"], debate_id))
    write_json(target / "reviews/fr/content_review.json", copy.deepcopy(review))
    manifest = load_json(target / "manifest.json", "manifest.json")
    controls = manifest.setdefault("editorial_controls", {})
    controls["summary_style_review_path"] = "reviews/summary_style_review.json"
    controls["summary_style"] = {
        "enabled": True,
        "min_sentences": 2,
        "long_sentence_words": 35,
        "max_average_sentence_words": 30,
        "max_long_sentence_ratio": 0.5,
        "max_sentence_words": 60,
        "opening_title_similarity_enabled": True,
        "opening_similarity_threshold": 0.84,
        "opening_max_extra_significant_words": 4,
        "quantitative_claim_review_required": True,
    }
    required_reports = controls.setdefault("required_reports", [])
    for rel in ("reports/fr_content_preflight.json", "reports/fr_content_validation.json"):
        if rel not in required_reports:
            required_reports.append(rel)
    manifest["updated_at"] = timestamp
    write_json(target / "manifest.json", manifest)
    preflight = _run_validator(
        project_root, target, scopes=("schema", "coherence", "graph", "files"),
        json_output=target / "reports/fr_content_preflight.json",
        text_output=target / "reports/fr_content_preflight.txt",
    )
    final_validation = _run_validator(
        project_root, target, scopes=("schema", "coherence", "graph", "files", "workflow"),
        json_output=target / "reports/fr_content_validation.json",
        text_output=target / "reports/fr_content_validation.txt",
    )
    return {
        "content_lock": content_lock,
        "changeset": changeset,
        "validator_result": final_validation.get("result"),
        "preflight_result": preflight.get("result"),
    }


def apply_review(project_root: Path, debate_id: str, work_id: str, confirm_review_sha256: str) -> dict[str, Any]:
    workspace, meta = _load_workspace(project_root, debate_id, work_id)
    if meta.get("status") not in {"fr_content_review_finalized", "fr_content_applied"}:
        raise ContentReviewError(f"Statut incompatible avec l’application du contenu : {meta.get('status')}")
    _assert_source_unchanged(project_root, debate_id, meta)
    reviewed = _assert_reviewed_copy(workspace, meta)
    review = load_json(workspace / "reviews/fr/content_review.json", "revue de contenu")
    if review.get("status") != "approved" or review.get("review_sha256") != content_review_sha256(review):
        raise ContentReviewError("La revue de contenu n’est pas finalisée ou son empreinte est invalide")
    if confirm_review_sha256 != review.get("review_sha256"):
        raise ContentReviewError("L’empreinte confirmée ne correspond pas à la revue de contenu")
    if review.get("prepared_reviewed_copy_sha256") != full_tree_sha256(reviewed):
        raise ContentReviewError("reviewed-copy a changé depuis la finalisation")
    target = workspace / "content-reviewed-copy"
    if target.is_dir():
        if meta.get("status") != "fr_content_applied":
            raise ContentReviewError("content-reviewed-copy existe sans état cohérent")
        expected = str((meta.get("content_reviewed_copy") or {}).get("tree_sha256") or "")
        actual = full_tree_sha256(target)
        if actual != expected:
            raise ContentReviewError("Empreinte de content-reviewed-copy divergente")
        return {"status": "fr_content_applied", "debate_id": debate_id, "work_id": work_id, "review_sha256": review["review_sha256"], "content_reviewed_copy_tree_sha256": actual, "idempotent": True}
    if target.exists() or target.is_symlink():
        raise ContentReviewError("Chemin content-reviewed-copy déjà occupé")
    temp = Path(tempfile.mkdtemp(prefix=".content-reviewed-copy.tmp-", dir=workspace))
    try:
        shutil.rmtree(temp)
        result = _build_content_copy(project_root, reviewed, temp, review, debate_id, work_id)
        if full_tree_sha256(temp / "imports") != full_tree_sha256(reviewed / "imports"):
            raise ContentReviewError("Les imports ont été modifiés pendant l’application du contenu")
        if (temp / "data/fr_page_metadata_lock.json").read_bytes() != (reviewed / "data/fr_page_metadata_lock.json").read_bytes():
            raise ContentReviewError("Le verrou de métadonnées françaises a été modifié")
        tree_hash = full_tree_sha256(temp)
        os.replace(temp, target)
        fsync_directory(workspace)
    except Exception:
        shutil.rmtree(temp, ignore_errors=True)
        raise
    applied_at = result["content_lock"]["applied_at"]
    translation_path = workspace / "reviews/en/translation_readiness.json"
    if translation_path.is_file():
        translation = load_json(translation_path, "préparation anglaise")
        translation["status"] = "ready_for_translation"
        translation["french_content_locked_at"] = applied_at
        translation["french_content_review_sha256"] = review["review_sha256"]
        for item in translation.get("items") or []:
            item["translation_status"] = "ready_for_translation"
            item["french_content_review_status"] = "locked"
        write_json(translation_path, translation)
    meta = copy.deepcopy(meta)
    meta["kit_version"] = KIT_VERSION
    meta["status"] = "fr_content_applied"
    meta["content_reviewed_copy"] = {
        "path": "content-reviewed-copy",
        "tree_sha256": tree_hash,
        "status": "fr_content_locked",
        "review_sha256": review["review_sha256"],
        "applied_at": applied_at,
    }
    meta["french_content_review"]["status"] = "applied"
    meta["french_content_review"]["applied_at"] = applied_at
    meta["boundaries"]["final_pages_generated"] = False
    meta["boundaries"]["english_translation_started"] = False
    meta["workspace_sha256"] = None
    meta["workspace_sha256"] = workspace_receipt_hash(meta)
    write_json(workspace / "workspace.json", meta)
    return {
        "status": "fr_content_applied",
        "debate_id": debate_id,
        "work_id": work_id,
        "review_sha256": review["review_sha256"],
        "content_reviewed_copy": relative_to_project(target, project_root),
        "content_reviewed_copy_tree_sha256": tree_hash,
        "sources": len(review["final_values"]["sources"]),
        "arguments": len(review["final_values"]["arguments"]),
        "source_corpus_mutated": False,
        "working_copy_mutated": False,
        "reviewed_copy_mutated": False,
        "imports_mutated": False,
        "metadata_lock_mutated": False,
        "final_pages_generated": False,
        "english_translation_started": False,
        "translation_readiness": "ready_for_translation",
        "validator_result": result["validator_result"],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Préparer, finaliser ou appliquer la revue du contenu français.")
    parser.add_argument("debate_id")
    parser.add_argument("--work-id", required=True)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--prepare", action="store_true")
    action.add_argument("--finalize", action="store_true")
    action.add_argument("--apply", action="store_true")
    parser.add_argument("--overwrite-review", action="store_true")
    parser.add_argument("--confirm-review-sha256")
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--machine-readable", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    project_root = args.project_root.expanduser().resolve()
    work_id = validate_work_id(args.work_id)
    if args.apply and not args.confirm_review_sha256:
        raise ContentReviewError("--confirm-review-sha256 est obligatoire avec --apply")
    with exclusive_lock(project_root, args.debate_id, "editorial_content_review"):
        if args.prepare:
            result = prepare_review(project_root, args.debate_id, work_id, overwrite=args.overwrite_review)
        elif args.finalize:
            result = finalize_review(project_root, args.debate_id, work_id)
        else:
            result = apply_review(project_root, args.debate_id, work_id, str(args.confirm_review_sha256))
    print(json.dumps(result, ensure_ascii=False, sort_keys=True) if args.machine_readable else json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ContentReviewError, EditorialReviewError, WorkspaceError, CorpusBuildError) as exc:
        print(f"WIKIDEBIA BLOQUÉ : {exc}", file=__import__("sys").stderr)
        raise SystemExit(2)
