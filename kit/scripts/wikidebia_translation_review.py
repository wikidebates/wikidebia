#!/usr/bin/env python3
"""Prepare, finalize and apply the English translation review of a workspace.

This phase starts only after French metadata and content have been locked. It
collects English titles, sections, keywords, debate content, argument summaries
and documentary sources in a formal review ledger. Finalization seals the
review; application creates an atomically visible ``translated-copy/``. No
MediaWiki page is rendered and no remote access is performed.
"""

from __future__ import annotations

import argparse
import collections
import copy
import json
import os
import re
import shutil
import tempfile
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
    structural_sha256,
    write_json,
)
from wikidebia_editorial_workspace import WorkspaceError, fsync_directory, validate_work_id, workspace_receipt_hash
from wikidebia_editorial_review import EditorialReviewError, _assert_source_unchanged, _load_workspace, _run_validator
from wikidebia_content_review import (
    ARGUMENT_BUCKETS,
    SOURCE_METADATA_FIELDS,
    SUMMARY_TRUE_FIELDS,
    INTRO_TRUE_FIELDS,
    NUMBER,
    META_DISCOURSE,
)

KIT_VERSION = "2.15.15"
TRANSLATION_REVIEW_SCHEMA = "wikidebia-en-translation-review-1.0"
TRANSLATION_LOCK_SCHEMA = "wikidebia-en-translation-lock-1.0"
EN_METADATA_LOCK_SCHEMA = "wikidebia-en-page-metadata-lock-1.0"
EN_CONTENT_LOCK_SCHEMA = "wikidebia-en-content-lock-1.0"
TRANSLATION_CHANGESET_SCHEMA = "wikidebia-en-translation-changeset-1.0"
EN_SOURCES_WORKING_SCHEMA = "wikidebia-en-source-registry-working-1.0"

EN_PAGE_LIFECYCLE_PARAMETERS = {
    "debate": ("progress", "debate-warnings", "related-debates"),
    "argument": ("argument-warnings",),
}


def _validate_page_lifecycle(row: Mapping[str, Any], page_type: str, label: str) -> dict[str, Any]:
    origin = row.get("page_origin", "new")
    if origin not in {"new", "preexisting"}:
        raise TranslationReviewError(f"Origine de page invalide pour {label}")
    raw = row.get("preserved_parameters") or {}
    if not isinstance(raw, dict):
        raise TranslationReviewError(f"Paramètres préservés invalides pour {label}")
    allowed = EN_PAGE_LIFECYCLE_PARAMETERS[page_type]
    if set(raw) - set(allowed):
        raise TranslationReviewError(f"Paramètre préservé inconnu pour {label}")
    if origin == "new":
        if raw:
            raise TranslationReviewError(f"Une page nouvelle ne peut pas déclarer de paramètres préservés : {label}")
        return {"page_origin": "new", "preserved_parameters": {}}
    if set(raw) != set(allowed):
        raise TranslationReviewError(f"L’état antérieur des paramètres doit être complet pour {label}")
    clean: dict[str, dict[str, Any]] = {}
    for name in allowed:
        state = raw.get(name)
        if not isinstance(state, dict) or not isinstance(state.get("present"), bool):
            raise TranslationReviewError(f"État antérieur invalide pour {label}/{name}")
        value = state.get("value")
        if state["present"]:
            if not isinstance(value, str) or not value.strip():
                raise TranslationReviewError(f"Valeur antérieure absente pour {label}/{name}")
            clean[name] = {"present": True, "value": value}
        else:
            if value is not None:
                raise TranslationReviewError(f"Une valeur ne peut être fournie pour un paramètre absent : {label}/{name}")
            clean[name] = {"present": False, "value": None}
    return {"page_origin": "preexisting", "preserved_parameters": clean}

SECTION_MAP = {
    "Aménagement": "Planning", "Culture": "Culture", "Droit": "Law", "Écologie": "Ecology",
    "Économie": "Economy", "Éducation": "Education", "Éthique": "Ethics", "Géopolitique": "Geopolitics",
    "Histoire": "History", "Philosophie": "Philosophy", "Politique": "Politics", "Psychologie": "Psychology",
    "Religion et spiritualité": "Religion and spirituality", "Santé": "Health", "Science": "Science",
    "Société": "Society", "Sport et loisirs": "Sport and leisure", "Technologie": "Technology",
}
EN_SECTIONS = set(SECTION_MAP.values())
DEBATE_BUCKETS = {
    "pro-bibliography": ("bibliography", "pro_reference"),
    "con-bibliography": ("bibliography", "con_reference"),
    "bibliography": ("bibliography", "neutral_reference"),
    "pro-webliography": ("webliography", "pro_reference"),
    "con-webliography": ("webliography", "con_reference"),
    "webliography": ("webliography", "neutral_reference"),
    "pro-videography": ("videography", "pro_reference"),
    "con-videography": ("videography", "con_reference"),
    "videography": ("videography", "neutral_reference"),
}
SOURCE_ID = re.compile(r"^S[0-9]{5,}$")
HTTP_URL = re.compile(r"^https?://", re.I)
BAD_QUOTES = re.compile(r"[«»“”„‹›]")
BAD_ELLIPSIS = re.compile(r"\.\.\.|…")
VERB_HINT = re.compile(r"\b(?:is|are|was|were|has|have|does|do|can|could|may|might|must|should|would|will|shows?|demonstrates?|proves?|supports?|challenges?|undermines?|refutes?|implies?|indicates?|prevents?|allows?|requires?|depends?|makes?|causes?|explains?|confirms?|weakens?|strengthens?)\b", re.I)
QUESTION_TOPIC = re.compile(r"^(?:whether\b|should\b|must\b|is\b|are\b|does\b|do\b|can\b)", re.I)

FRENCH_TEMPLATE_NAMES = {
    "Sous-partie", "Article Wikipédia", "Argument pour", "Argument contre",
    "Référence bibliographique", "Référence bibliographique pour", "Référence bibliographique contre",
    "Référence sitographique", "Référence sitographique pour", "Référence sitographique contre",
    "Référence vidéographique", "Référence vidéographique pour", "Référence vidéographique contre",
    "Lien Wikipédia", "Lien interlangue", "Débat connexe", "Citation",
}
FRENCH_TEMPLATE_RE = re.compile(
    r"\{\{\s*(" + "|".join(re.escape(name) for name in sorted(FRENCH_TEMPLATE_NAMES, key=len, reverse=True)) + r")(?:\s*[|}])",
    re.I,
)
FRENCH_PARAMETER_NAMES = {
    "titre", "contenu", "texte-affiché", "auteurs", "ouvrage", "numéro", "localisation",
    "édition", "lieu", "lien", "avertissements", "titre-affiché", "langue", "citation",
    "avertissements-citation", "résumé", "rubriques", "mots-clés", "date-création",
}
FRENCH_PARAMETER_RE = re.compile(
    r"\|\s*(" + "|".join(re.escape(name) for name in sorted(FRENCH_PARAMETER_NAMES, key=len, reverse=True)) + r")\s*=",
    re.I,
)

def _assert_english_wikicode_localized(value: str, label: str) -> None:
    template = FRENCH_TEMPLATE_RE.search(value)
    if template:
        raise TranslationReviewError(f"Modèle français interdit dans {label} : {template.group(1)}")
    parameter = FRENCH_PARAMETER_RE.search(value)
    if parameter:
        raise TranslationReviewError(f"Paramètre français interdit dans {label} : {parameter.group(1)}")

TRANSLATED_CITATION_WARNING = "Citation traduite par IA"
FR_MONTHS = {
    "janvier": 1, "février": 2, "fevrier": 2, "mars": 3, "avril": 4, "mai": 5, "juin": 6,
    "juillet": 7, "août": 8, "aout": 8, "septembre": 9, "octobre": 10, "novembre": 11, "décembre": 12, "decembre": 12,
}
EN_MONTHS = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12,
}
CITATION_CONTROLLED_NAMES = {"citation", "date", "avertissements-citation", "avertissements citation", "avertissements"}
CITATION_PARAMETER_MAP = {
    "citation": "quote",
    "auteurs": "authors",
    "article": "article",
    "ouvrage": "work",
    "volume": "volume",
    "numéro": "issue",
    "numero": "issue",
    "page": "page",
    "localisation": "location",
    "édition": "publisher",
    "edition": "publisher",
    "lieu": "place",
    "date": "date",
    "lien": "link",
    "avertissements citation": "warnings",
    "avertissements": "warnings",
}


def _citation_warning(existing: Any) -> str:
    value = str(existing or "").strip().strip(",").strip()
    parts = [part.strip() for part in value.split(",") if part.strip()]
    if TRANSLATED_CITATION_WARNING not in parts:
        parts.append(TRANSLATED_CITATION_WARNING)
    return ", ".join(parts)


def _date_signature(value: Any, language: str) -> tuple[int, int | None, int | None] | None:
    text = re.sub(r"\s+", " ", str(value or "").strip())
    if not text:
        return None
    if re.fullmatch(r"\d{4}", text):
        return (int(text), None, None)
    months = FR_MONTHS if language == "fr" else EN_MONTHS
    match = re.fullmatch(r"(\d{1,2})\s+([A-Za-zÀ-ÿ]+)\s+(\d{4})", text, re.I)
    if match and match.group(2).casefold() in months:
        return (int(match.group(3)), months[match.group(2).casefold()], int(match.group(1)))
    match = re.fullmatch(r"([A-Za-zÀ-ÿ]+)\s+(\d{4})", text, re.I)
    if match and match.group(1).casefold() in months:
        return (int(match.group(2)), months[match.group(1).casefold()], None)
    return None


def _blank_citation(source: Mapping[str, Any]) -> dict[str, Any]:
    source_date = str(source.get("date") or "").strip()
    return {
        "id": source.get("id"),
        "source": copy.deepcopy(source),
        "status": "pending",
        "translated_citation": "",
        "translated_date": source_date if re.fullmatch(r"\d{4}", source_date) else "",
        "citation_translated": False,
        "date_translated_or_language_neutral": False,
        "preserved_parameters_unchanged": False,
        "translation_warning_appended": False,
        "reviewer": "",
        "reviewed_at": None,
        "note": "",
    }


def _validate_citations(rows: Any, french_rows: Sequence[Mapping[str, Any]], node_id: str) -> list[dict[str, Any]]:
    if not isinstance(rows, list):
        raise TranslationReviewError(f"Liste de citations anglaises absente pour {node_id}")
    expected = {str(row.get("id")): row for row in french_rows}
    if {str(row.get("id")) for row in rows if isinstance(row, dict)} != set(expected):
        raise TranslationReviewError(f"Les citations anglaises ne couvrent pas exactement les citations françaises de {node_id}")
    final: list[dict[str, Any]] = []
    by_id = {str(row.get("id")): row for row in rows}
    for citation_id, source in expected.items():
        row = by_id[citation_id]
        if row.get("source") != source:
            raise TranslationReviewError(f"Les paramètres source de la citation {citation_id} ont été modifiés")
        if row.get("status") != "approved":
            raise TranslationReviewError(f"Traduction de citation non approuvée : {citation_id}")
        translated = _text(row.get("translated_citation"), f"citation traduite {citation_id}", 2)
        source_date = str(source.get("date") or "").strip()
        translated_date = str(row.get("translated_date") or "").strip()
        if not source_date and translated_date:
            raise TranslationReviewError(f"Une date a été inventée pour la citation {citation_id}")
        if source_date:
            if not translated_date:
                raise TranslationReviewError(f"Date anglaise absente pour la citation {citation_id}")
            fr_sig = _date_signature(source_date, "fr")
            en_sig = _date_signature(translated_date, "en")
            if fr_sig is not None and en_sig != fr_sig:
                raise TranslationReviewError(f"La date traduite ne désigne pas la même date pour {citation_id}")
            if fr_sig is None and translated_date == source_date and re.search(r"[A-Za-zÀ-ÿ]", source_date):
                raise TranslationReviewError(f"La date textuelle de {citation_id} n’a pas été traduite")
        for field in ("citation_translated", "date_translated_or_language_neutral", "preserved_parameters_unchanged", "translation_warning_appended"):
            if row.get(field) is not True:
                raise TranslationReviewError(f"Attestation de citation manquante pour {citation_id} : {field}")
        _text(row.get("reviewer"), f"relecteur de citation {citation_id}", 3)
        _text(row.get("reviewed_at"), f"date de revue de citation {citation_id}", 10)
        _text(row.get("note"), f"note de revue de citation {citation_id}", 8)
        warning = _citation_warning(source.get("avertissements-citation"))
        output_parameters: list[dict[str, str]] = []
        warning_inserted = False
        for parameter in source.get("source_parameters") or []:
            source_name = str(parameter.get("name") or "").strip()
            normalized = re.sub(r"[ _-]+", " ", source_name.casefold())
            output_name = CITATION_PARAMETER_MAP.get(normalized)
            if output_name is None:
                raise TranslationReviewError(
                    f"Paramètre français de citation sans équivalent anglais déclaré pour {citation_id} : {source_name}"
                )
            if output_name == "quote":
                output_value = translated
            elif output_name == "date":
                output_value = translated_date
            elif output_name == "warnings":
                if warning_inserted:
                    continue
                output_value = warning
                warning_inserted = True
            else:
                output_value = str(parameter.get("value") or "")
            output_parameters.append({
                "name": output_name,
                "value": output_value,
                "source_name": source_name,
            })
        if not warning_inserted:
            output_parameters.append({
                "name": "warnings",
                "value": warning,
                "source_name": "avertissements-citation",
            })
        final.append({
            "id": citation_id,
            "source_template": source.get("source_template") or "Citation",
            "output_template": "Quote",
            "quote": translated,
            "date": translated_date,
            "warnings": warning,
            "parameter_name_mapping": copy.deepcopy(CITATION_PARAMETER_MAP),
            "preserved_parameters": copy.deepcopy(source.get("preserved_parameters") or []),
            "parameters": output_parameters,
            "source": copy.deepcopy(source),
            "reviewer": row.get("reviewer"),
            "reviewed_at": row.get("reviewed_at"),
            "note": row.get("note"),
        })
    return final


class TranslationReviewError(EditorialReviewError):
    pass


def translation_review_sha256(review: Mapping[str, Any]) -> str:
    body = copy.deepcopy(dict(review))
    body.pop("review_sha256", None)
    return sha256_bytes(canonical_json(body))


def _text(value: Any, label: str, minimum: int = 1) -> str:
    if not isinstance(value, str) or len(value.strip()) < minimum:
        raise TranslationReviewError(f"{label} est absent ou trop court")
    return value.strip()


def _strings(value: Any, label: str) -> list[str]:
    if not isinstance(value, list):
        raise TranslationReviewError(f"{label} doit être une liste")
    result: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise TranslationReviewError(f"{label} contient une valeur vide")
        clean = item.strip()
        if clean in result:
            raise TranslationReviewError(f"{label} contient un doublon : {clean}")
        result.append(clean)
    return result


def _plain(value: str) -> str:
    value = re.sub(r"<ref\b[^>]*>.*?</ref>|<ref\b[^>]*/>", " ", value or "", flags=re.I | re.S)
    value = re.sub(r"\{\{[^{}]*\}\}|\[\[[^\]]+\]\]", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def _assert_content_copy(workspace: Path, meta: Mapping[str, Any]) -> Path:
    source = workspace / "content-reviewed-copy"
    if not source.is_dir() or source.is_symlink():
        raise TranslationReviewError("content-reviewed-copy absent ou non sûr")
    expected = str((meta.get("content_reviewed_copy") or {}).get("tree_sha256") or "")
    actual = full_tree_sha256(source)
    if not expected or actual != expected:
        raise TranslationReviewError("content-reviewed-copy a changé depuis le verrouillage français")
    if (source / "output").exists():
        raise TranslationReviewError("Des pages finales existent déjà dans content-reviewed-copy")
    for required in ("data/fr_page_metadata_lock.json", "data/fr_content_lock.json", "data/keyword_vocabulary.json"):
        if not (source / required).is_file():
            raise TranslationReviewError(f"Verrou français requis absent : {required}")
    return source


def _source_snapshot(source: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    registry = load_json(source / "data/registre_debat.json", "registre du débat")
    metadata = load_json(source / "data/fr_page_metadata_lock.json", "verrou des métadonnées françaises")
    content = load_json(source / "data/fr_content_lock.json", "verrou du contenu français")
    vocabulary = load_json(source / "data/keyword_vocabulary.json", "vocabulaire français")
    return registry, metadata, content, vocabulary


def _blank_debate(fr_meta: Mapping[str, Any], fr_content: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "status": "pending",
        "page_origin": "new",
        "preserved_parameters": {},
        "canonical_title": "",
        "topic": "",
        "complete_topic": "",
        "sections": [],
        "keywords": [],
        "introduction": "",
        "subsections": [],
        "wikipedia_articles": [],
        "documentation": {bucket: [] for bucket in DEBATE_BUCKETS},
        "documentation_family_notes": {"bibliography": "", "webliography": "", "videography": ""},
        "topic_label_rationale": "",
        "complete_topic_initial_capital_justification": None,
        "metadata_equivalent_to_french": False,
        "content_equivalent_to_french": False,
        "sections_exactly_mapped": False,
        "keywords_exactly_mapped": False,
        "keywords_order_preserved_by_relevance": False,
        "introduction_functionally_equivalent": False,
        "wikipedia_articles_verified": False,
        "all_debate_sources_english": False,
        "reviewer": "",
        "reviewed_at": None,
        "note": "",
        **{field: False for field in INTRO_TRUE_FIELDS},
        "french": {"metadata": copy.deepcopy(fr_meta), "content": copy.deepcopy(fr_content)},
    }


def _blank_argument(fr_meta: Mapping[str, Any], fr_content: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "status": "pending",
        "page_origin": "new",
        "preserved_parameters": {},
        "canonical_title": "",
        "displayed_title": "",
        "sections": [],
        "keywords": [],
        "summary": "",
        "citations": [_blank_citation(row) for row in (fr_content.get("citations") or [])],
        "sources": {bucket: [] for bucket in ARGUMENT_BUCKETS},
        "metadata_equivalent_to_french": False,
        "summary_equivalent_to_french": False,
        "sections_exactly_mapped": False,
        "keywords_exactly_mapped": False,
        "keywords_order_preserved_by_relevance": False,
        "title_is_idiomatic": False,
        "displayed_title_is_complete_proposition": False,
        "displayed_title_concision_reviewed": False,
        "summary_ratio_reviewed": False,
        "forceful_expression": "",
        "quantitative_claims_verified": False,
        "quantitative_claims_note": "",
        "documentation_rationale": "",
        "reviewer": "",
        "reviewed_at": None,
        "note": "",
        **{field: False for field in SUMMARY_TRUE_FIELDS},
        "french": {"metadata": copy.deepcopy(fr_meta), "content": copy.deepcopy(fr_content)},
    }


def prepare_review(project_root: Path, debate_id: str, work_id: str, *, overwrite: bool = False) -> dict[str, Any]:
    workspace, meta = _load_workspace(project_root, debate_id, work_id)
    if meta.get("status") not in {"fr_content_applied", "en_translation_review_ready"}:
        raise TranslationReviewError(f"Statut incompatible avec la préparation anglaise : {meta.get('status')}")
    _assert_source_unchanged(project_root, debate_id, meta)
    source = _assert_content_copy(workspace, meta)
    readiness = load_json(workspace / "reviews/en/translation_readiness.json", "préparation anglaise")
    if readiness.get("status") != "ready_for_translation":
        raise TranslationReviewError("La préparation anglaise n’est pas ouverte")
    review_path = workspace / "reviews/en/translation_review.json"
    sources_path = workspace / "data/sources_en_working.json"
    if review_path.exists() and not overwrite:
        current = load_json(review_path, "revue anglaise")
        return {"status": "en_translation_review_ready", "debate_id": debate_id, "work_id": work_id, "arguments": len(current.get("arguments") or []), "idempotent": True}
    if overwrite and (workspace / "translated-copy").exists():
        raise TranslationReviewError("Impossible de régénérer une traduction déjà appliquée")
    registry, metadata_lock, content_lock, vocabulary = _source_snapshot(source)
    fr_meta_by_id = {str(row.get("entity_id")): row for row in metadata_lock.get("arguments") or []}
    fr_content_by_id = {str(row.get("id")): row for row in content_lock.get("arguments") or []}
    active_ids = [str(node.get("id")) for node in ((registry.get("graph") or {}).get("nodes") or []) if node.get("status") == "active"]
    if set(active_ids) != set(fr_meta_by_id) or set(active_ids) != set(fr_content_by_id):
        raise TranslationReviewError("Les verrous français ne couvrent pas exactement les arguments actifs")
    now = now_iso()
    review = {
        "schema": TRANSLATION_REVIEW_SCHEMA,
        "schema_version": "1.0",
        "normative_revision": NORM_VERSION,
        "kit_version": KIT_VERSION,
        "debate_id": debate_id,
        "work_id": work_id,
        "source_language": "fr",
        "target_language": "en",
        "status": "draft",
        "prepared_at": now,
        "prepared_content_reviewed_copy_sha256": full_tree_sha256(source),
        "french_metadata_review_sha256": metadata_lock.get("review_sha256"),
        "french_content_review_sha256": content_lock.get("review_sha256"),
        "section_mapping": copy.deepcopy(SECTION_MAP),
        "vocabulary": [
            {
                "fr": row.get("fr"), "en": row.get("en") or "", "definition_en": "",
                "kind": row.get("kind"), "capitalization_policy": row.get("capitalization_policy"),
                "capitalization_verified": False, "capitalization_rationale_en": "",
                "status": "pending", "idiomatic_equivalent": False, "same_concept": False,
                "reviewer": "", "reviewed_at": None, "note": "",
                "usages": copy.deepcopy(row.get("usages") or []),
            }
            for row in vocabulary.get("entries") or []
        ],
        "debate": _blank_debate(metadata_lock.get("debate") or {}, content_lock.get("debate") or {}),
        "arguments": [
            {"id": node_id, "translation": _blank_argument(fr_meta_by_id[node_id], fr_content_by_id[node_id])}
            for node_id in active_ids
        ],
        "global_review": {
            "reviewer": "", "reviewed_at": None,
            "all_entities_translated": False, "all_equivalences_reviewed": False,
            "all_selected_sources_verified": False, "relations_and_occurrences_unchanged": False,
            "no_final_pages_generated": True, "remote_access_not_used": True,
            "blocking_issues": [], "note": "",
        },
        "review_sha256": None,
    }
    write_json(review_path, review)
    write_json(sources_path, {
        "schema": EN_SOURCES_WORKING_SCHEMA,
        "source_registry_version": "1.0",
        "debate_id": debate_id,
        "work_id": work_id,
        "status": "draft",
        "prepared_at": now,
        "sources": [],
    })
    write_json(workspace / "audits/en_translation_inventory.json", {
        "schema": "wikidebia-en-translation-inventory-1.0",
        "debate_id": debate_id, "work_id": work_id, "generated_at": now,
        "arguments": len(active_ids), "vocabulary_entries": len(review["vocabulary"]),
        "french_sources": len((load_json(source / "data/sources.json", "sources françaises").get("sources") or [])),
        "boundaries": {"automatic_translation": False, "final_pages_generated": False, "remote_access": False},
    })
    (workspace / "audits/en_translation_inventory.md").write_text(
        "\n".join(["# English translation inventory", "", f"- Debate: `{debate_id}`", f"- Arguments: {len(active_ids)}", f"- Controlled terms: {len(review['vocabulary'])}", "", "No automatic translation or final page generation was performed.", ""]),
        encoding="utf-8", newline="\n",
    )
    meta = copy.deepcopy(meta)
    meta["kit_version"] = KIT_VERSION
    meta["status"] = "en_translation_review_ready"
    meta.setdefault("artifacts", {})["english_translation_review"] = "reviews/en/translation_review.json"
    meta["artifacts"]["english_sources_working"] = "data/sources_en_working.json"
    meta["artifacts"]["translated_copy"] = "translated-copy"
    meta["english_translation_review"] = {"status": "prepared", "prepared_at": now, "prepared_content_reviewed_copy_sha256": review["prepared_content_reviewed_copy_sha256"]}
    meta["boundaries"]["english_translation_started"] = True
    meta["boundaries"]["final_pages_generated"] = False
    meta["workspace_sha256"] = None
    meta["workspace_sha256"] = workspace_receipt_hash(meta)
    write_json(workspace / "workspace.json", meta)
    readiness["status"] = "translation_review_in_progress"
    for item in readiness.get("items") or []:
        item["translation_status"] = "translation_review_in_progress"
    write_json(workspace / "reviews/en/translation_readiness.json", readiness)
    return {"status": "en_translation_review_ready", "debate_id": debate_id, "work_id": work_id, "review_path": relative_to_project(review_path, project_root), "sources_path": relative_to_project(sources_path, project_root), "arguments": len(active_ids), "automatic_translation": False, "final_pages_generated": False}


def _validate_sources(data: Mapping[str, Any], debate_id: str, french_ids: set[str]) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    if data.get("schema") != EN_SOURCES_WORKING_SCHEMA or data.get("debate_id") != debate_id:
        raise TranslationReviewError("Schéma ou identité du registre documentaire anglais invalide")
    rows = data.get("sources")
    if not isinstance(rows, list):
        raise TranslationReviewError("Le registre documentaire anglais doit contenir une liste sources")
    result: list[dict[str, Any]] = []
    by_id: dict[str, dict[str, Any]] = {}
    dedup: set[str] = set()
    for index, row in enumerate(rows, 1):
        if not isinstance(row, dict):
            raise TranslationReviewError(f"Source anglaise #{index} invalide")
        sid = _text(row.get("id"), f"identifiant de source anglaise #{index}")
        if not SOURCE_ID.fullmatch(sid) or sid in by_id or sid in french_ids:
            raise TranslationReviewError(f"Identifiant documentaire anglais invalide, dupliqué ou déjà utilisé : {sid}")
        stype = row.get("type")
        if stype not in {"bibliography", "webliography", "videography"}:
            raise TranslationReviewError(f"Type documentaire anglais invalide pour {sid}")
        if row.get("language") != "en":
            raise TranslationReviewError(f"La langue réelle de {sid} doit être en")
        metadata = row.get("metadata")
        if not isinstance(metadata, dict) or set(metadata) != set(SOURCE_METADATA_FIELDS):
            raise TranslationReviewError(f"Métadonnées anglaises incomplètes pour {sid}")
        authors = metadata.get("authors")
        if not isinstance(authors, list) or any(not isinstance(a, str) or not a.strip() for a in authors):
            raise TranslationReviewError(f"Auteurs invalides pour {sid}")
        if stype == "bibliography" and (not authors or not (metadata.get("article") or metadata.get("work"))):
            raise TranslationReviewError(f"Référence bibliographique anglaise incomplète : {sid}")
        if stype in {"webliography", "videography"} and not HTTP_URL.match(str(metadata.get("link") or "")):
            raise TranslationReviewError(f"Lien HTTP(S) obligatoire pour {sid}")
        verification = row.get("verification")
        if not isinstance(verification, dict) or verification.get("status") != "verified" or verification.get("language_verified") is not True:
            raise TranslationReviewError(f"Source anglaise non vérifiée : {sid}")
        if stype in {"webliography", "videography"} and verification.get("authorship_checked") is not True:
            raise TranslationReviewError(f"Attribution anglaise non vérifiée : {sid}")
        usages = row.get("usage")
        if not isinstance(usages, list) or not usages:
            raise TranslationReviewError(f"Aucun usage documentaire anglais pour {sid}")
        for usage in usages:
            if not isinstance(usage, dict) or usage.get("language") != "en" or not usage.get("page_id") or not usage.get("role"):
                raise TranslationReviewError(f"Usage anglais invalide pour {sid}")
            if usage.get("role") == "supports_summary":
                if usage.get("argument_development_verified") is not True:
                    raise TranslationReviewError(f"Le développement de l’argument n’est pas vérifié pour {sid}")
                if not isinstance(usage.get("also_develops_objections"), bool):
                    raise TranslationReviewError(f"La couverture éventuelle d’objections doit être attestée pour {sid}")
            if len(str(usage.get("selection_reason") or "").strip()) < 12:
                raise TranslationReviewError(f"Justification de sélection anglaise insuffisante pour {sid}")
        key = _text(row.get("deduplication_key"), f"clé de dédoublonnage de {sid}")
        if key in dedup:
            raise TranslationReviewError(f"Clé documentaire anglaise dupliquée : {key}")
        dedup.add(key)
        by_id[sid] = copy.deepcopy(row)
        result.append(copy.deepcopy(row))
    return result, by_id


def _has_usage(source: Mapping[str, Any], page_id: str, roles: set[str]) -> bool:
    return any(u.get("page_id") == page_id and u.get("language") == "en" and u.get("role") in roles for u in source.get("usage") or [])


def _validate_title(value: Any, label: str, *, displayed: bool = False) -> str:
    text = _text(value, label, 8)
    if BAD_QUOTES.search(text) or BAD_ELLIPSIS.search(text) or text.endswith("."):
        raise TranslationReviewError(f"Titre anglais non conforme : {label}")
    if displayed and not VERB_HINT.search(text):
        raise TranslationReviewError(f"Le titre affiché anglais n’est pas une proposition complète : {label}")
    return text


def _first_alphabetic(value: str) -> str:
    return next((char for char in value if char.isalpha()), "")


def _english_capitalization_issues(value: str, kind: str) -> list[str]:
    first = _first_alphabetic(value)
    if kind in {"noun", "noun_phrase"} and first and first.isupper():
        return ["common_keyword_initial_uppercase"]
    if kind == "acronym":
        letters = [char for char in value if char.isalpha()]
        if not letters or any(char.islower() for char in letters):
            return ["acronym_not_uppercase"]
    return []


def _validate_vocabulary(rows: Any, french_entries: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, str]]:
    if not isinstance(rows, list) or len(rows) != len(french_entries):
        raise TranslationReviewError("Le vocabulaire anglais ne couvre pas exactement le vocabulaire français")
    expected = {str(row.get("fr")): row for row in french_entries}
    result: list[dict[str, Any]] = []
    mapping: dict[str, str] = {}
    english_seen: set[str] = set()
    for row in rows:
        if not isinstance(row, dict) or str(row.get("fr")) not in expected:
            raise TranslationReviewError("Entrée de vocabulaire anglaise inconnue")
        fr = str(row.get("fr"))
        en = _text(row.get("en"), f"équivalent anglais de {fr}", 2)
        if en.casefold() in english_seen:
            raise TranslationReviewError(f"Équivalent anglais dupliqué : {en}")
        english_seen.add(en.casefold())
        kind = str(expected[fr].get("kind") or "")
        if row.get("kind") != kind or row.get("capitalization_policy") != expected[fr].get("capitalization_policy"):
            raise TranslationReviewError(f"Nature ou politique de capitalisation divergente : {fr}")
        capitalization_issues = _english_capitalization_issues(en, kind)
        if capitalization_issues:
            raise TranslationReviewError(f"Capitalisation anglaise non canonique pour {fr} : {capitalization_issues}")
        if row.get("capitalization_verified") is not True:
            raise TranslationReviewError(f"Capitalisation anglaise non attestée : {fr}")
        if kind in {"proper_name", "acronym"} and len(str(row.get("capitalization_rationale_en") or "").strip()) < 12:
            raise TranslationReviewError(f"Justification de capitalisation anglaise insuffisante : {fr}")
        if kind in {"noun", "noun_phrase"} and str(row.get("capitalization_rationale_en") or "").strip():
            raise TranslationReviewError(f"Justification de majuscule anglaise inattendue pour le nom commun : {fr}")
        if row.get("status") != "approved" or row.get("idiomatic_equivalent") is not True or row.get("same_concept") is not True:
            raise TranslationReviewError(f"Équivalence lexicale non approuvée : {fr}")
        _text(row.get("definition_en"), f"définition anglaise de {fr}", 8)
        _text(row.get("reviewer"), f"relecteur lexical de {fr}", 3)
        _text(row.get("reviewed_at"), f"date de revue lexicale de {fr}", 10)
        _text(row.get("note"), f"note lexicale de {fr}", 8)
        mapping[fr] = en
        result.append(copy.deepcopy(row))
    if set(mapping) != set(expected):
        raise TranslationReviewError("Le vocabulaire anglais omet des termes français")
    return result, mapping


def _expected_sections(fr: Sequence[str]) -> list[str]:
    try:
        return sorted((SECTION_MAP[item] for item in fr), key=lambda x: x.casefold())
    except KeyError as exc:
        raise TranslationReviewError(f"Rubrique française sans section anglaise contrôlée : {exc.args[0]}") from exc


def _expected_keywords(fr: Sequence[str], mapping: Mapping[str, str]) -> list[str]:
    try:
        return [mapping[item] for item in fr]
    except KeyError as exc:
        raise TranslationReviewError(f"Mot-clé français sans équivalent anglais : {exc.args[0]}") from exc


def _validate_debate(row: Mapping[str, Any], mapping: Mapping[str, str], sources: Mapping[str, Mapping[str, Any]], debate_id: str) -> dict[str, Any]:
    if row.get("status") != "approved":
        raise TranslationReviewError("Traduction de la page Debate non approuvée")
    fr_meta = ((row.get("french") or {}).get("metadata") or {})
    fr_content = ((row.get("french") or {}).get("content") or {})
    title = _validate_title(row.get("canonical_title"), "titre canonique de Debate")
    topic = _text(row.get("topic"), "topic", 3)
    complete = _text(row.get("complete_topic"), "complete-topic", 3)
    if QUESTION_TOPIC.search(complete):
        raise TranslationReviewError("complete-topic doit être nominal et non interrogatif")
    if complete[0].isalpha() and complete[0].isupper() and not row.get("complete_topic_initial_capital_justification"):
        raise TranslationReviewError("La majuscule initiale de complete-topic doit être justifiée")
    sections = _strings(row.get("sections"), "sections de Debate")
    expected_sections = _expected_sections(fr_meta.get("rubriques") or [])
    if sections != expected_sections or row.get("sections_exactly_mapped") is not True:
        raise TranslationReviewError("Les sections anglaises de Debate ne correspondent pas aux rubriques françaises")
    keywords = _strings(row.get("keywords"), "keywords de Debate")
    expected_keywords = _expected_keywords(fr_meta.get("keywords") or [], mapping)
    if keywords != expected_keywords or row.get("keywords_exactly_mapped") is not True or not 5 <= len(keywords) <= 8:
        raise TranslationReviewError("Les keywords de Debate ne correspondent pas au vocabulaire contrôlé")
    if row.get("keywords_order_preserved_by_relevance") is not True:
        raise TranslationReviewError("L’ordre de pertinence des keywords de Debate n’est pas attesté")
    introduction = _text(row.get("introduction"), "introduction anglaise", 40)
    _assert_english_wikicode_localized(introduction, "l’introduction anglaise")
    subsections = row.get("subsections")
    if not isinstance(subsections, list) or not subsections:
        raise TranslationReviewError("L’introduction anglaise doit comporter des sous-parties")
    for sub in subsections:
        if not isinstance(sub, dict):
            raise TranslationReviewError("Sous-partie anglaise invalide")
        _text(sub.get("title"), "titre de sous-partie anglaise", 3)
        _text(sub.get("purpose"), "fonction de sous-partie anglaise", 12)
        if sub.get("necessary_for_understanding") is not True or sub.get("relevance_to_debate_explained") is not True:
            raise TranslationReviewError("Chaque sous-partie anglaise doit être nécessaire et contextualisée")
    wikipedia = _strings(row.get("wikipedia_articles"), "articles Wikipédia anglais")
    if not wikipedia or row.get("wikipedia_articles_verified") is not True:
        raise TranslationReviewError("Au moins un article Wikipédia anglais vérifié est obligatoire")
    documentation = row.get("documentation")
    if not isinstance(documentation, dict) or set(documentation) != set(DEBATE_BUCKETS):
        raise TranslationReviewError("Neuf paramètres documentaires anglais requis")
    final_doc: dict[str, list[str]] = {}
    for bucket, (stype, role) in DEBATE_BUCKETS.items():
        ids = _strings(documentation.get(bucket), bucket)
        if len(ids) < 2:
            raise TranslationReviewError(f"Le bucket anglais {bucket} doit contenir au moins deux références")
        for sid in ids:
            source = sources.get(sid)
            if not source or source.get("type") != stype or source.get("language") != "en" or not _has_usage(source, debate_id, {role}):
                raise TranslationReviewError(f"Source anglaise incompatible dans {bucket} : {sid}")
        final_doc[bucket] = ids
    for field in ("metadata_equivalent_to_french", "content_equivalent_to_french", "introduction_functionally_equivalent", "all_debate_sources_english", *INTRO_TRUE_FIELDS):
        if row.get(field) is not True:
            raise TranslationReviewError(f"Attestation anglaise manquante pour Debate : {field}")
    _text(row.get("topic_label_rationale"), "justification de topic", 12)
    _text(row.get("reviewer"), "relecteur de Debate", 3)
    _text(row.get("reviewed_at"), "date de revue de Debate", 10)
    _text(row.get("note"), "note de revue de Debate", 12)
    return {
        "canonical_title": title, "topic": topic, "complete_topic": complete,
        "sections": sections, "keywords": keywords, "introduction": introduction,
        "subsections": copy.deepcopy(subsections), "wikipedia_articles": wikipedia,
        "documentation": final_doc, "documentation_family_notes": copy.deepcopy(row.get("documentation_family_notes") or {}),
        "topic_label_rationale": row.get("topic_label_rationale"),
        "complete_topic_initial_capital_justification": row.get("complete_topic_initial_capital_justification"),
        "reviewer": row.get("reviewer"), "reviewed_at": row.get("reviewed_at"), "note": row.get("note"),
        "french_subject": fr_content.get("subject"), "french_complete_topic": fr_content.get("complete_topic"),
        **_validate_page_lifecycle(row, "debate", "Debate"),
    }


def _validate_argument(item: Mapping[str, Any], mapping: Mapping[str, str], sources: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    node_id = _text(item.get("id"), "identifiant d’argument")
    row = item.get("translation") or {}
    if row.get("status") != "approved":
        raise TranslationReviewError(f"Traduction anglaise non approuvée pour {node_id}")
    fr_meta = ((row.get("french") or {}).get("metadata") or {})
    fr_content = ((row.get("french") or {}).get("content") or {})
    canonical = _validate_title(row.get("canonical_title"), f"titre canonique anglais de {node_id}")
    displayed = _validate_title(row.get("displayed_title"), f"titre affiché anglais de {node_id}", displayed=True)
    sections = _strings(row.get("sections"), f"sections de {node_id}")
    if sections != _expected_sections(fr_meta.get("rubriques") or []) or row.get("sections_exactly_mapped") is not True:
        raise TranslationReviewError(f"Sections anglaises divergentes pour {node_id}")
    keywords = _strings(row.get("keywords"), f"keywords de {node_id}")
    if keywords != _expected_keywords(fr_meta.get("keywords") or [], mapping) or row.get("keywords_exactly_mapped") is not True or not 2 <= len(keywords) <= 4:
        raise TranslationReviewError(f"Keywords anglais divergents pour {node_id}")
    if row.get("keywords_order_preserved_by_relevance") is not True:
        raise TranslationReviewError(f"Ordre de pertinence des keywords non attesté pour {node_id}")
    summary = _text(row.get("summary"), f"summary de {node_id}", 40)
    _assert_english_wikicode_localized(summary, f"le summary de {node_id}")
    if META_DISCOURSE.search(_plain(summary)):
        raise TranslationReviewError(f"Métadiscours interdit dans le summary de {node_id}")
    fr_summary = _text(fr_content.get("summary"), f"résumé français verrouillé de {node_id}", 40)
    ratio = len(_plain(summary)) / max(1, len(_plain(fr_summary)))
    if not 0.60 <= ratio <= 1.45 or row.get("summary_ratio_reviewed") is not True:
        raise TranslationReviewError(f"Ratio anglais/français hors limites pour {node_id} : {ratio:.2f}")
    for field in ("metadata_equivalent_to_french", "summary_equivalent_to_french", "title_is_idiomatic", "displayed_title_is_complete_proposition", "displayed_title_concision_reviewed", *SUMMARY_TRUE_FIELDS):
        if row.get(field) is not True:
            raise TranslationReviewError(f"Attestation anglaise manquante pour {node_id} : {field}")
    expression = _text(row.get("forceful_expression"), f"expression de force anglaise de {node_id}", 8)
    if _plain(expression).casefold() not in _plain(summary).casefold():
        raise TranslationReviewError(f"L’expression de force anglaise est absente du summary de {node_id}")
    numbers = NUMBER.findall(_plain(summary))
    if numbers and (row.get("quantitative_claims_verified") is not True or len(str(row.get("quantitative_claims_note") or "").strip()) < 12):
        raise TranslationReviewError(f"Donnée chiffrée anglaise non vérifiée dans {node_id}")
    citations = _validate_citations(row.get("citations"), fr_content.get("citations") or [], node_id)
    selected = row.get("sources")
    if not isinstance(selected, dict) or set(selected) != set(ARGUMENT_BUCKETS):
        raise TranslationReviewError(f"Sélection documentaire anglaise absente pour {node_id}")
    final_sources: dict[str, list[str]] = {}
    for bucket, stype in ARGUMENT_BUCKETS.items():
        ids = _strings(selected.get(bucket), f"sources anglaises {bucket} de {node_id}")
        for sid in ids:
            source = sources.get(sid)
            if not source or source.get("type") != stype or not _has_usage(source, node_id, {"supports_summary"}):
                raise TranslationReviewError(f"Source anglaise incompatible pour {node_id} : {sid}")
        final_sources[bucket] = ids
    _text(row.get("documentation_rationale"), f"justification documentaire anglaise de {node_id}", 12)
    _text(row.get("reviewer"), f"relecteur anglais de {node_id}", 3)
    _text(row.get("reviewed_at"), f"date de revue anglaise de {node_id}", 10)
    _text(row.get("note"), f"note de revue anglaise de {node_id}", 12)
    return {
        "id": node_id, "canonical_title": canonical, "displayed_title": displayed,
        "sections": sections, "keywords": keywords, "summary": summary, "citations": citations, "sources": final_sources,
        "summary_length_ratio": round(ratio, 4), "forceful_expression": expression,
        "quantitative_claims": numbers, "quantitative_claims_verified": bool(row.get("quantitative_claims_verified")),
        "quantitative_claims_note": row.get("quantitative_claims_note"),
        "reviewer": row.get("reviewer"), "reviewed_at": row.get("reviewed_at"), "note": row.get("note"),
        **_validate_page_lifecycle(row, "argument", node_id),
    }


def finalize_review(project_root: Path, debate_id: str, work_id: str) -> dict[str, Any]:
    workspace, meta = _load_workspace(project_root, debate_id, work_id)
    if meta.get("status") not in {"en_translation_review_ready", "en_translation_review_finalized"}:
        raise TranslationReviewError(f"Statut incompatible avec la finalisation anglaise : {meta.get('status')}")
    _assert_source_unchanged(project_root, debate_id, meta)
    source = _assert_content_copy(workspace, meta)
    review_path = workspace / "reviews/en/translation_review.json"
    review = load_json(review_path, "revue anglaise")
    if review.get("status") == "approved" and review.get("review_sha256"):
        if review.get("review_sha256") != translation_review_sha256(review):
            raise TranslationReviewError("Empreinte de revue anglaise invalide")
        if review.get("prepared_content_reviewed_copy_sha256") != full_tree_sha256(source):
            raise TranslationReviewError("content-reviewed-copy a changé depuis la finalisation anglaise")
        return {"status": "en_translation_review_finalized", "debate_id": debate_id, "work_id": work_id, "review_sha256": review["review_sha256"], "idempotent": True}
    if review.get("schema") != TRANSLATION_REVIEW_SCHEMA or review.get("debate_id") != debate_id or review.get("work_id") != work_id:
        raise TranslationReviewError("Schéma ou identité de revue anglaise invalide")
    if review.get("normative_revision") != NORM_VERSION or review.get("prepared_content_reviewed_copy_sha256") != full_tree_sha256(source):
        raise TranslationReviewError("Base française ou norme divergente pour la revue anglaise")
    registry, metadata_lock, content_lock, vocabulary_fr = _source_snapshot(source)
    french_source_rows = load_json(source / "data/sources.json", "sources françaises").get("sources") or []
    french_ids = {str(row.get("id")) for row in french_source_rows}
    english_rows, by_source = _validate_sources(load_json(workspace / "data/sources_en_working.json", "sources anglaises"), debate_id, french_ids)
    vocabulary, keyword_map = _validate_vocabulary(review.get("vocabulary"), vocabulary_fr.get("entries") or [])
    final_debate = _validate_debate(review.get("debate") or {}, keyword_map, by_source, debate_id)
    items = review.get("arguments")
    if not isinstance(items, list):
        raise TranslationReviewError("Liste des arguments anglais absente")
    active_ids = {str(node.get("id")) for node in ((registry.get("graph") or {}).get("nodes") or []) if node.get("status") == "active"}
    if {str(item.get("id")) for item in items if isinstance(item, dict)} != active_ids:
        raise TranslationReviewError("La revue anglaise ne couvre pas exactement les arguments actifs")
    final_arguments = [_validate_argument(item, keyword_map, by_source) for item in items]
    canonical_titles = [row["canonical_title"].casefold() for row in final_arguments]
    if len(set(canonical_titles)) != len(canonical_titles) or final_debate["canonical_title"].casefold() in canonical_titles:
        raise TranslationReviewError("Collision de titres canoniques anglais")
    exact = sum(row["canonical_title"].casefold() == row["displayed_title"].casefold() for row in final_arguments)
    if final_arguments and exact / len(final_arguments) > 0.10:
        raise TranslationReviewError("Plus de 10 % des displayed titles anglais sont identiques aux titres canoniques")
    keyword_sets = collections.Counter(tuple(row["keywords"]) for row in final_arguments)
    if final_arguments and max(keyword_sets.values(), default=0) / len(final_arguments) > 0.25:
        raise TranslationReviewError("Un même jeu exact de keywords anglais domine plus de 25 % des arguments")
    global_review = review.get("global_review") or {}
    for field in ("all_entities_translated", "all_equivalences_reviewed", "all_selected_sources_verified", "relations_and_occurrences_unchanged", "no_final_pages_generated", "remote_access_not_used"):
        if global_review.get(field) is not True:
            raise TranslationReviewError(f"Attestation globale anglaise manquante : {field}")
    if global_review.get("blocking_issues") not in ([], None):
        raise TranslationReviewError("La revue anglaise contient encore des blocages")
    _text(global_review.get("reviewer"), "relecteur global anglais", 3)
    _text(global_review.get("reviewed_at"), "date de revue globale anglaise", 10)
    _text(global_review.get("note"), "note de revue globale anglaise", 12)
    selected_ids: set[str] = set()
    for ids in final_debate["documentation"].values(): selected_ids.update(ids)
    for arg in final_arguments:
        for ids in arg["sources"].values(): selected_ids.update(ids)
    if selected_ids != set(by_source):
        raise TranslationReviewError(f"Le registre anglais doit couvrir exactement les sources retenues; inutilisées={sorted(set(by_source)-selected_ids)}, absentes={sorted(selected_ids-set(by_source))}")
    finalized = copy.deepcopy(review)
    finalized.update({
        "kit_version": KIT_VERSION, "status": "approved", "finalized_at": now_iso(),
        "source_registry_sha256": sha256_bytes(canonical_json({"source_registry_version": "1.0", "debate_id": debate_id, "sources": english_rows})),
        "final_values": {"debate": final_debate, "arguments": final_arguments, "vocabulary": vocabulary, "sources": english_rows},
        "summary": {"arguments": len(final_arguments), "vocabulary_entries": len(vocabulary), "sources": len(english_rows), "debate_documentary_references": sum(len(v) for v in final_debate["documentation"].values()), "argument_documentary_references": sum(len(v) for arg in final_arguments for v in arg["sources"].values()), "citations": sum(len(arg.get("citations") or []) for arg in final_arguments)},
        "review_sha256": None,
    })
    finalized["review_sha256"] = translation_review_sha256(finalized)
    write_json(review_path, finalized)
    meta = copy.deepcopy(meta)
    meta["kit_version"] = KIT_VERSION
    meta["status"] = "en_translation_review_finalized"
    meta["english_translation_review"] = {"status": "finalized", "review_sha256": finalized["review_sha256"], "finalized_at": finalized["finalized_at"], "prepared_content_reviewed_copy_sha256": finalized["prepared_content_reviewed_copy_sha256"]}
    meta["workspace_sha256"] = None
    meta["workspace_sha256"] = workspace_receipt_hash(meta)
    write_json(workspace / "workspace.json", meta)
    return {"status": "en_translation_review_finalized", "debate_id": debate_id, "work_id": work_id, "review_sha256": finalized["review_sha256"], **finalized["summary"], "content_reviewed_copy_mutated": False, "final_pages_generated": False}


def _merge_introduction_review(path: Path, debate: Mapping[str, Any]) -> None:
    data = load_json(path, "revue des introductions") if path.is_file() else {"normative_revision": NORM_VERSION, "entries": []}
    entries = [row for row in data.get("entries") or [] if row.get("language") != "en"]
    entries.append({"language": "en", **{field: True for field in INTRO_TRUE_FIELDS}, "documentation_family_notes": copy.deepcopy(debate.get("documentation_family_notes") or {}), "common_acronym": None, "topic_label_rationale": debate.get("topic_label_rationale"), "complete_topic_initial_capital_justification": debate.get("complete_topic_initial_capital_justification"), "subsections": copy.deepcopy(debate.get("subsections") or [])})
    data["entries"] = entries
    write_json(path, data)


def _summary_mechanism_excerpt(summary: Any) -> str:
    text = str(summary or "").strip()
    if not text:
        return "The reviewed summary explicitly states the central mechanism supporting the claim."
    first = re.split(r"(?<=[.!?])\s+", text, maxsplit=1)[0].strip()
    return first if len(first) >= 30 else text


def _merge_summary_review(path: Path, arguments: Sequence[Mapping[str, Any]], debate_id: str) -> None:
    data = load_json(path, "revue des résumés") if path.is_file() else {"normative_revision": NORM_VERSION, "entries": []}
    by_id = {str(row.get("id")): row for row in data.get("entries") or []}
    for arg in arguments:
        entry = by_id.setdefault(arg["id"], {"id": arg["id"], "languages": {}})
        entry.setdefault("languages", {})["en"] = {
            "status": "translated_and_reviewed", "thesis_first": True, "general_public_style": True,
            "sentence_rhythm_reviewed": True, "technical_terms_reviewed": True,
            "opening_develops_title": True, "example_or_data_reviewed": True,
            "assertive_tone_reviewed": True, "no_artificial_example_or_number": True,
            "no_polemical_overstatement": True, "conviction_visible": True,
            "wikipedia_hover_links_reviewed": True, "specialized_terms_linked_or_explained": True,
            "forceful_expression": arg.get("forceful_expression"),
            "originality_reviewed": True,
            "mechanism_statement": _summary_mechanism_excerpt(arg.get("summary")),
            "quantitative_claims_verified": arg.get("quantitative_claims_verified"),
            "quantitative_claims_note": arg.get("quantitative_claims_note"), "note": arg.get("note"),
        }
    data["schema_version"] = "1.0"
    data["normative_revision"] = NORM_VERSION
    data["summary_policy_revision"] = "1.2.39"
    data.pop("quality_policy_revision", None)
    data["debate_id"] = debate_id
    data["entries"] = [by_id[key] for key in sorted(by_id)]
    write_json(path, data)


def _build_translated_copy(project_root: Path, source: Path, target: Path, review: Mapping[str, Any], debate_id: str, work_id: str) -> dict[str, Any]:
    shutil.copytree(source, target, symlinks=False, copy_function=shutil.copy2)
    final = review["final_values"]
    registry = load_json(target / "data/registre_debat.json", "registre du débat")
    old_structural = str((((registry.get("graph") or {}).get("lifecycle") or {}).get("structural_sha256") or ""))
    by_id = {row["id"]: row for row in final["arguments"]}
    debate_pages = (registry.setdefault("debate", {}).setdefault("pages", {}))
    en_debate = debate_pages.setdefault("en", {})
    en_debate["canonical_title"] = final["debate"]["canonical_title"]
    en_debate["title_status"] = "validated"
    fr_debate = debate_pages.setdefault("fr", {})
    fr_debate.setdefault("interlanguage", {})["target_title"] = final["debate"]["canonical_title"]
    fr_debate["interlanguage"]["status"] = "ready"
    operations: list[dict[str, Any]] = []
    for node in ((registry.get("graph") or {}).get("nodes") or []):
        if node.get("status") != "active": continue
        row = by_id[str(node.get("id"))]
        en = node.setdefault("en", {})
        before = copy.deepcopy(en)
        en.update({"canonical_title": row["canonical_title"], "displayed_title": row["displayed_title"], "sections": copy.deepcopy(row["sections"]), "keywords": copy.deepcopy(row["keywords"]), "title_status": "validated"})
        node.setdefault("sources", {}).setdefault("en", {}).update(copy.deepcopy(row["sources"]))
        pages = node.setdefault("pages", {})
        pages.setdefault("fr", {}).setdefault("interlanguage", {})["target_title"] = row["canonical_title"]
        pages["fr"]["interlanguage"]["status"] = "ready"
        operations.append({"entity_type": "argument", "entity_id": row["id"], "field": "english_projection", "before": before, "after": copy.deepcopy(en)})
    new_structural = structural_sha256(registry)
    lifecycle = (registry.get("graph") or {}).get("lifecycle") or {}
    lifecycle["structural_sha256"] = new_structural
    projection = load_json(target / "graph/graphe_argumentatif.json", "projection du graphe")
    projection["nodes"] = copy.deepcopy((registry.get("graph") or {}).get("nodes") or [])
    projection["lifecycle"] = copy.deepcopy(lifecycle)
    french_sources = load_json(target / "data/sources.json", "sources françaises")
    merged_sources = copy.deepcopy(french_sources.get("sources") or []) + copy.deepcopy(final["sources"])
    timestamp = now_iso()
    metadata_lock = {
        "schema": EN_METADATA_LOCK_SCHEMA, "schema_version": "1.0", "normative_revision": NORM_VERSION,
        "kit_version": KIT_VERSION, "debate_id": debate_id, "work_id": work_id, "language": "en",
        "status": "locked_for_generation", "review_sha256": review["review_sha256"], "applied_at": timestamp,
        "old_structural_sha256": old_structural, "new_structural_sha256": new_structural,
        "debate": {k: copy.deepcopy(final["debate"][k]) for k in ("canonical_title", "topic", "complete_topic", "sections", "keywords", "reviewer", "reviewed_at", "note")},
        "arguments": [{k: copy.deepcopy(row[k]) for k in ("id", "canonical_title", "displayed_title", "sections", "keywords", "reviewer", "reviewed_at", "note")} for row in final["arguments"]],
    }
    content_lock = {
        "schema": EN_CONTENT_LOCK_SCHEMA, "schema_version": "1.0", "normative_revision": NORM_VERSION,
        "kit_version": KIT_VERSION, "debate_id": debate_id, "work_id": work_id, "language": "en",
        "status": "locked_for_generation", "review_sha256": review["review_sha256"],
        "source_registry_sha256": review["source_registry_sha256"], "applied_at": timestamp,
        "debate": copy.deepcopy(final["debate"]), "arguments": copy.deepcopy(final["arguments"]),
    }
    translation_lock = {
        "schema": TRANSLATION_LOCK_SCHEMA, "schema_version": "1.0", "normative_revision": NORM_VERSION,
        "kit_version": KIT_VERSION, "debate_id": debate_id, "work_id": work_id,
        "source_language": "fr", "target_language": "en", "status": "locked_for_generation",
        "review_sha256": review["review_sha256"], "french_metadata_review_sha256": review["french_metadata_review_sha256"],
        "french_content_review_sha256": review["french_content_review_sha256"], "applied_at": timestamp,
        "relations_and_occurrences_unchanged": True, "argument_count": len(final["arguments"]),
        "vocabulary_count": len(final["vocabulary"]), "source_count": len(final["sources"]),
        "citation_count": sum(len(arg.get("citations") or []) for arg in final["arguments"]),
        "citation_translation_policy": {
            "translated_value_fields": ["citation->quote", "date->date"],
            "parameter_names": "all_french_parameter_names_are_mapped_to_declared_english_names",
            "preserved_values": "all_values_except_quote_and_date",
            "parameter_mapping": copy.deepcopy(CITATION_PARAMETER_MAP),
            "warning_parameter": "warnings",
            "warning_value": TRANSLATED_CITATION_WARNING,
            "warning_separator": ", ",
        },
    }
    vocabulary = load_json(target / "data/keyword_vocabulary.json", "vocabulaire français")
    by_fr = {row["fr"]: row for row in final["vocabulary"]}
    bilingual_entries = []
    for row in vocabulary.get("entries") or []:
        merged = copy.deepcopy(row)
        translated = by_fr[str(row.get("fr"))]
        merged.update({"en": translated["en"], "definition_en": translated["definition_en"], "capitalization_rationale_en": translated.get("capitalization_rationale_en", ""), "status": "approved_bilingual", "english_review": {"reviewer": translated["reviewer"], "reviewed_at": translated["reviewed_at"], "note": translated["note"]}})
        bilingual_entries.append(merged)
    changeset = {
        "schema": TRANSLATION_CHANGESET_SCHEMA, "schema_version": "1.0", "debate_id": debate_id,
        "work_id": work_id, "status": "applied", "review_sha256": review["review_sha256"],
        "applied_at": timestamp, "operation_count": len(operations) + 1,
        "operations": [{"entity_type": "debate", "entity_id": debate_id, "field": "english_projection", "before": None, "after": copy.deepcopy(final["debate"])}] + operations,
        "relations_mutated": False, "occurrences_mutated": False, "french_locks_mutated": False,
        "final_pages_generated": False, "remote_access": False,
    }
    write_json(target / "data/registre_debat.json", registry)
    write_json(target / "graph/graphe_argumentatif.json", projection)
    write_json(target / "data/sources.json", {"source_registry_version": "1.0", "debate_id": debate_id, "sources": merged_sources})
    write_json(target / "data/en_page_metadata_lock.json", metadata_lock)
    write_json(target / "data/en_content_lock.json", content_lock)
    write_json(target / "data/en_translation_lock.json", translation_lock)
    write_json(target / "data/keyword_vocabulary_bilingual.json", {"schema": "wikidebia-keyword-vocabulary-bilingual-1.0", "normative_revision": NORM_VERSION, "keyword_policy_revision": "1.2.39", "debate_id": debate_id, "status": "approved_bilingual", "language_status": "bilingual_locked", "review_sha256": review["review_sha256"], "entries": bilingual_entries})
    write_json(target / "changes/en_translation_changeset.json", changeset)
    write_json(target / "reviews/en/translation_review.json", copy.deepcopy(review))
    _merge_introduction_review(target / "reviews/introduction_review.json", final["debate"])
    _merge_summary_review(target / "reviews/summary_style_review.json", final["arguments"], debate_id)
    manifest = load_json(target / "manifest.json", "manifest.json")
    manifest.setdefault("translation_status", {})["en"] = "ready"
    controls = manifest.setdefault("editorial_controls", {})
    required_reports = controls.setdefault("required_reports", [])
    for rel in ("reports/en_translation_preflight.json", "reports/en_translation_validation.json"):
        if rel not in required_reports: required_reports.append(rel)
    manifest["updated_at"] = timestamp
    write_json(target / "manifest.json", manifest)
    preflight = _run_validator(project_root, target, scopes=("schema", "coherence", "graph", "files"), json_output=target / "reports/en_translation_preflight.json", text_output=target / "reports/en_translation_preflight.txt")
    validation = _run_validator(project_root, target, scopes=("schema", "coherence", "graph", "files", "bilingual", "workflow"), json_output=target / "reports/en_translation_validation.json", text_output=target / "reports/en_translation_validation.txt")
    return {"metadata_lock": metadata_lock, "content_lock": content_lock, "translation_lock": translation_lock, "changeset": changeset, "preflight_result": preflight.get("result"), "validator_result": validation.get("result")}


def apply_review(project_root: Path, debate_id: str, work_id: str, confirm_review_sha256: str) -> dict[str, Any]:
    workspace, meta = _load_workspace(project_root, debate_id, work_id)
    if meta.get("status") not in {"en_translation_review_finalized", "en_translation_applied"}:
        raise TranslationReviewError(f"Statut incompatible avec l’application anglaise : {meta.get('status')}")
    _assert_source_unchanged(project_root, debate_id, meta)
    source = _assert_content_copy(workspace, meta)
    review = load_json(workspace / "reviews/en/translation_review.json", "revue anglaise")
    if review.get("status") != "approved" or review.get("review_sha256") != translation_review_sha256(review):
        raise TranslationReviewError("La revue anglaise n’est pas finalisée ou son empreinte est invalide")
    if confirm_review_sha256 != review.get("review_sha256"):
        raise TranslationReviewError("L’empreinte confirmée ne correspond pas à la revue anglaise")
    if review.get("prepared_content_reviewed_copy_sha256") != full_tree_sha256(source):
        raise TranslationReviewError("content-reviewed-copy a changé depuis la finalisation anglaise")
    target = workspace / "translated-copy"
    if target.is_dir():
        if meta.get("status") != "en_translation_applied":
            raise TranslationReviewError("translated-copy existe sans état cohérent")
        expected = str((meta.get("translated_copy") or {}).get("tree_sha256") or "")
        actual = full_tree_sha256(target)
        if actual != expected: raise TranslationReviewError("Empreinte de translated-copy divergente")
        return {"status": "en_translation_applied", "debate_id": debate_id, "work_id": work_id, "review_sha256": review["review_sha256"], "translated_copy_tree_sha256": actual, "idempotent": True}
    if target.exists() or target.is_symlink():
        raise TranslationReviewError("Chemin translated-copy déjà occupé")
    temp = Path(tempfile.mkdtemp(prefix=".translated-copy.tmp-", dir=workspace))
    try:
        shutil.rmtree(temp)
        result = _build_translated_copy(project_root, source, temp, review, debate_id, work_id)
        for rel in ("imports",):
            if full_tree_sha256(temp / rel) != full_tree_sha256(source / rel):
                raise TranslationReviewError(f"La provenance {rel} a été modifiée pendant la traduction")
        for rel in ("data/fr_page_metadata_lock.json", "data/fr_content_lock.json"):
            if (temp / rel).read_bytes() != (source / rel).read_bytes():
                raise TranslationReviewError(f"Le verrou français {rel} a été modifié")
        tree_hash = full_tree_sha256(temp)
        os.replace(temp, target)
        fsync_directory(workspace)
    except Exception:
        shutil.rmtree(temp, ignore_errors=True)
        raise
    applied_at = result["translation_lock"]["applied_at"]
    readiness = load_json(workspace / "reviews/en/translation_readiness.json", "préparation anglaise")
    readiness["status"] = "translation_locked"
    readiness["english_translation_review_sha256"] = review["review_sha256"]
    readiness["english_translation_locked_at"] = applied_at
    for item in readiness.get("items") or []:
        item["translation_status"] = "translated_and_locked"
        item["equivalence_review_status"] = "approved"
    write_json(workspace / "reviews/en/translation_readiness.json", readiness)
    meta = copy.deepcopy(meta)
    meta["kit_version"] = KIT_VERSION
    meta["status"] = "en_translation_applied"
    meta["translated_copy"] = {"path": "translated-copy", "tree_sha256": tree_hash, "status": "bilingual_content_locked", "review_sha256": review["review_sha256"], "applied_at": applied_at}
    meta["english_translation_review"]["status"] = "applied"
    meta["english_translation_review"]["applied_at"] = applied_at
    meta["boundaries"]["english_translation_started"] = True
    meta["boundaries"]["final_pages_generated"] = False
    meta["boundaries"]["remote_access"] = False
    meta["workspace_sha256"] = None
    meta["workspace_sha256"] = workspace_receipt_hash(meta)
    write_json(workspace / "workspace.json", meta)
    return {"status": "en_translation_applied", "debate_id": debate_id, "work_id": work_id, "review_sha256": review["review_sha256"], "translated_copy": relative_to_project(target, project_root), "translated_copy_tree_sha256": tree_hash, "arguments": len(review["final_values"]["arguments"]), "sources": len(review["final_values"]["sources"]), "vocabulary_entries": len(review["final_values"]["vocabulary"]), "relations_mutated": False, "occurrences_mutated": False, "french_locks_mutated": False, "final_pages_generated": False, "remote_access": False, "validator_result": result["validator_result"]}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Préparer, finaliser ou appliquer la traduction anglaise contrôlée.")
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
        raise TranslationReviewError("--confirm-review-sha256 est obligatoire avec --apply")
    with exclusive_lock(project_root, args.debate_id, "editorial_translation_review"):
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
    except (TranslationReviewError, EditorialReviewError, WorkspaceError, CorpusBuildError) as exc:
        print(f"WIKIDEBIA BLOQUÉ : {exc}", file=__import__("sys").stderr)
        raise SystemExit(2)
