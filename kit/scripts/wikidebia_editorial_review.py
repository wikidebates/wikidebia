#!/usr/bin/env python3
"""Finalize and apply the French metadata review of an editorial workspace.

This phase consumes the human/AI-completed ledger created by
``corpus-workspace-init``.  Finalization is read-only with respect to corpus
and working-copy content.  Application creates a new, atomically visible
``reviewed-copy/`` while preserving ``working-copy/`` byte-for-byte.

Only French canonical/displayed titles, rubriques and keywords are handled.
No final MediaWiki page is rendered and no English translation is started.
"""

from __future__ import annotations

import argparse
import collections
import copy
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from wikidebia_corpus_build import (
    NORM_VERSION,
    VALIDATOR_VERSION,
    CorpusBuildError,
    assert_control_directory,
    assert_graph_validated_without_final_pages,
    assert_no_symlinks,
    canonical_json,
    exclusive_lock,
    full_tree_sha256,
    load_json,
    now_iso,
    relative_to_project,
    sha256_bytes,
    structural_sha256,
    validate_debate_id,
    write_json,
)
from wikidebia_corpus_init import RUBRIQUES, _markdown_graph
from wikidebia_editorial_workspace import (
    WorkspaceError,
    fsync_directory,
    keyword_diagnostics,
    capitalization_policy_for_kind,
    keyword_capitalization_issues,
    normalized_identity,
    normalized_text,
    rubrique_diagnostics,
    title_diagnostics,
    token_words,
    validate_work_id,
    workspace_receipt_hash,
)

KIT_VERSION = "2.15.52"
REVIEW_SCHEMA = "wikidebia-fr-page-metadata-review-1.1"
METADATA_LOCK_SCHEMA = "wikidebia-fr-page-metadata-lock-1.0"
CHANGESET_SCHEMA = "wikidebia-editorial-changeset-1.1"
ALLOWED_KEYWORD_KINDS = {"noun", "noun_phrase", "proper_name", "acronym"}
COMPOSITIONAL_KEYWORD_FR = re.compile(
    r"^(?:(?:psychologie|sociologie|histoire|géographie|généalogie)\s+religieuse?s?|science\s+et\s+religion)$",
    flags=re.IGNORECASE,
)


def _is_compositional_keyword_fr(term: str) -> bool:
    """Return True for a domain intersection that must be split into base keywords."""
    return bool(COMPOSITIONAL_KEYWORD_FR.fullmatch(normalized_text(term)))


class EditorialReviewError(WorkspaceError):
    pass


def review_sha256(review: Mapping[str, Any]) -> str:
    body = copy.deepcopy(dict(review))
    body.pop("review_sha256", None)
    return sha256_bytes(canonical_json(body))


def _text_ok(value: Any, minimum: int = 12) -> bool:
    return isinstance(value, str) and len(value.strip()) >= minimum


def _workspace_path(project_root: Path, debate_id: str, work_id: str) -> Path:
    debate_id = validate_debate_id(debate_id)
    work_id = validate_work_id(work_id)
    state = assert_control_directory(project_root / ".state", project_root)
    editorial = assert_control_directory(state / "editorial-workspaces", project_root)
    debate_root = assert_control_directory(editorial / debate_id, project_root)
    raw = debate_root / work_id
    if raw.is_symlink():
        raise EditorialReviewError(f"Lien symbolique interdit pour le workspace : {raw}")
    path = raw.resolve()
    if path.parent != debate_root or not path.is_dir():
        raise EditorialReviewError(f"Workspace introuvable : .state/editorial-workspaces/{debate_id}/{work_id}")
    assert_no_symlinks(path)
    return path


def _load_workspace(project_root: Path, debate_id: str, work_id: str) -> tuple[Path, dict[str, Any]]:
    path = _workspace_path(project_root, debate_id, work_id)
    meta = load_json(path / "workspace.json", "workspace.json")
    if meta.get("schema") != "wikidebia-editorial-workspace-1.0":
        raise EditorialReviewError("Schéma de workspace non pris en charge")
    if meta.get("debate_id") != debate_id or meta.get("work_id") != work_id:
        raise EditorialReviewError("Identité du workspace divergente")
    if meta.get("workspace_sha256") != workspace_receipt_hash(meta):
        raise EditorialReviewError("Empreinte de workspace.json invalide")
    return path, meta


def _assert_source_unchanged(project_root: Path, debate_id: str, meta: Mapping[str, Any]) -> None:
    source = project_root / "corpus" / debate_id
    if not source.is_dir() or source.is_symlink():
        raise EditorialReviewError(f"Corpus source introuvable ou non sûr : corpus/{debate_id}")
    assert_no_symlinks(source)
    expected = str((meta.get("source") or {}).get("tree_sha256") or "")
    actual = full_tree_sha256(source)
    if not expected or actual != expected:
        raise EditorialReviewError("Le corpus source a changé depuis l’ouverture du workspace")


def _assert_pristine_working_copy(path: Path, meta: Mapping[str, Any]) -> Path:
    working = path / "working-copy"
    if not working.is_dir() or working.is_symlink():
        raise EditorialReviewError("working-copy absent ou non sûr")
    assert_no_symlinks(working)
    expected = str((meta.get("working_copy") or {}).get("initial_tree_sha256") or "")
    actual = full_tree_sha256(working)
    if not expected or actual != expected:
        raise EditorialReviewError("working-copy a été modifié depuis son initialisation")
    assert_graph_validated_without_final_pages(working)
    return working


def _decision_value(review: Mapping[str, Any], source: Mapping[str, Any], field: str, entity_type: str) -> Any:
    if field == "canonical_title":
        if entity_type == "debate":
            return source.get("canonical_title")
        decision = review.get("canonical_title_decision")
        if decision == "keep":
            return source.get("canonical_title")
        if decision == "change":
            return review.get("proposed_canonical_title")
        raise EditorialReviewError("Décision de titre canonique absente ou invalide")
    if field == "displayed_title":
        if entity_type == "debate":
            return None
        decision = review.get("displayed_title_decision")
        if decision == "keep":
            return source.get("displayed_title")
        if decision == "change":
            return review.get("proposed_displayed_title")
        raise EditorialReviewError("Décision de titre affiché absente ou invalide")
    if field == "rubriques":
        decision = review.get("rubriques_decision")
        if decision == "keep":
            return source.get("rubriques") or []
        if decision == "change":
            return review.get("proposed_rubriques")
        raise EditorialReviewError("Décision de rubriques absente ou invalide")
    if field == "keywords":
        decision = review.get("keywords_decision")
        if decision == "keep":
            return source.get("keywords") or []
        if decision == "change":
            return review.get("proposed_keywords")
        raise EditorialReviewError("Décision de mots-clés absente ou invalide")
    raise EditorialReviewError(f"Champ éditorial inconnu : {field}")


def _clean_string_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list):
        raise EditorialReviewError(f"{label} doit être une liste")
    result: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise EditorialReviewError(f"{label} contient une valeur vide ou non textuelle")
        if item != normalized_text(item):
            raise EditorialReviewError(f"{label} contient une valeur non normalisée : {item!r}")
        result.append(item)
    return result


def _validate_item(item: Mapping[str, Any]) -> dict[str, Any]:
    entity_type = str(item.get("entity_type") or "")
    entity_id = str(item.get("entity_id") or "")
    if entity_type not in {"debate", "argument"} or not entity_id:
        raise EditorialReviewError("Entrée de revue sans identité valide")
    source = item.get("source")
    decision = item.get("review")
    if not isinstance(source, dict) or not isinstance(decision, dict):
        raise EditorialReviewError(f"Entrée de revue incomplète : {entity_id}")
    if decision.get("status") != "approved":
        raise EditorialReviewError(f"Entrée non approuvée : {entity_id}")
    if not _text_ok(decision.get("reviewer"), 2):
        raise EditorialReviewError(f"Relecteur absent : {entity_id}")
    if not _text_ok(decision.get("reviewed_at"), 10):
        raise EditorialReviewError(f"Date de revue absente : {entity_id}")

    canonical_raw = _decision_value(decision, source, "canonical_title", entity_type)
    if not isinstance(canonical_raw, str) or canonical_raw != normalized_text(canonical_raw):
        raise EditorialReviewError(f"Titre canonique non normalisé : {entity_id}")
    canonical = canonical_raw
    displayed_raw = _decision_value(decision, source, "displayed_title", entity_type)
    if displayed_raw is not None and (not isinstance(displayed_raw, str) or displayed_raw != normalized_text(displayed_raw)):
        raise EditorialReviewError(f"Titre affiché non normalisé : {entity_id}")
    displayed = displayed_raw
    rubriques = _clean_string_list(_decision_value(decision, source, "rubriques", entity_type), f"rubriques de {entity_id}")
    keywords = _clean_string_list(_decision_value(decision, source, "keywords", entity_type), f"mots-clés de {entity_id}")

    if not canonical:
        raise EditorialReviewError(f"Titre canonique vide : {entity_id}")
    if entity_type == "argument":
        if not displayed:
            raise EditorialReviewError(f"Titre affiché vide : {entity_id}")
        blocking_codes = {
            "TITLE_CANONICAL_MISSING", "TITLE_CANONICAL_SPACING", "TITLE_CANONICAL_TRAILING_PERIOD",
            "TITLE_CANONICAL_NON_ASCII_QUOTES", "TITLE_CANONICAL_ELLIPSIS", "TITLE_DISPLAYED_MISSING",
            "TITLE_DISPLAYED_SPACING", "TITLE_DISPLAYED_TRAILING_PERIOD", "TITLE_DISPLAYED_NON_ASCII_QUOTES",
            "TITLE_DISPLAYED_ELLIPSIS", "TITLE_DISPLAYED_TRAILING_CONNECTOR",
        }
        remaining = [row for row in title_diagnostics(canonical, displayed) if row.get("code") in blocking_codes]
        if remaining:
            raise EditorialReviewError(f"Titres non conformes pour {entity_id} : {[row.get('code') for row in remaining]}")
        if not _text_ok(decision.get("canonical_title_rationale"), 20):
            raise EditorialReviewError(f"Justification du titre canonique insuffisante : {entity_id}")
        if not _text_ok(decision.get("displayed_title_rationale"), 20):
            raise EditorialReviewError(f"Justification du titre affiché insuffisante : {entity_id}")
        for attestation in (
            "canonical_referents_explicit",
            "displayed_title_complete_proposition",
            "displayed_title_argument_intelligible",
            "displayed_title_concision_reviewed",
            "displayed_title_semantically_equivalent",
        ):
            if decision.get(attestation) is not True:
                raise EditorialReviewError(f"Attestation manquante ({attestation}) : {entity_id}")
        if normalized_identity(canonical) != normalized_identity(displayed):
            if decision.get("displayed_title_improves_readability_when_distinct") is not True:
                raise EditorialReviewError(f"Le titre affiché distinct n’améliore pas explicitement la lisibilité : {entity_id}")
            if not _text_ok(decision.get("displayed_title_rationale"), 40):
                raise EditorialReviewError(f"Le raccourcissement du titre affiché n’est pas suffisamment justifié : {entity_id}")

    rub_issues = rubrique_diagnostics(rubriques, False)
    if rub_issues:
        raise EditorialReviewError(f"Rubriques non conformes pour {entity_id} : {[row.get('code') for row in rub_issues]}")
    rub_rationales = decision.get("rubriques_rationales")
    if not isinstance(rub_rationales, dict) or set(rub_rationales) != set(rubriques):
        raise EditorialReviewError(f"Justifications de rubriques incomplètes : {entity_id}")
    for rubric, rationale in rub_rationales.items():
        if not _text_ok(rationale, 12):
            raise EditorialReviewError(f"Justification insuffisante pour la rubrique {rubric!r} : {entity_id}")
    if len(rubriques) == 4 and not _text_ok(decision.get("fourth_rubrique_exception_rationale"), 30):
        raise EditorialReviewError(f"Quatrième rubrique non exceptionnellement justifiée : {entity_id}")

    # Debate pages use five to eight broad keywords; Argument pages use two to four.
    minimum, maximum = (5, 8) if entity_type == "debate" else (2, 4)
    if not minimum <= len(keywords) <= maximum:
        raise EditorialReviewError(f"Nombre de mots-clés non conforme pour {entity_id}: {len(keywords)} (attendu {minimum}-{maximum})")
    generic_kw_issues = [row for row in keyword_diagnostics(keywords, False) if row.get("code") not in {"KEYWORDS_TOO_FEW", "KEYWORDS_TOO_MANY", "KEYWORDS_CAPITALIZATION_REVIEW"}]
    if generic_kw_issues:
        raise EditorialReviewError(f"Mots-clés non conformes pour {entity_id} : {[row.get('code') for row in generic_kw_issues]}")
    kw_rationales = decision.get("keywords_rationales")
    if not isinstance(kw_rationales, dict) or set(kw_rationales) != set(keywords):
        raise EditorialReviewError(f"Justifications de mots-clés incomplètes : {entity_id}")
    for keyword, rationale in kw_rationales.items():
        if not _text_ok(rationale, 12):
            raise EditorialReviewError(f"Justification insuffisante pour le mot-clé {keyword!r} : {entity_id}")
    if decision.get("keywords_ordered_by_relevance") is not True:
        raise EditorialReviewError(f"Classement des mots-clés par pertinence non attesté : {entity_id}")
    if not _text_ok(decision.get("keyword_order_rationale"), 20):
        raise EditorialReviewError(f"Justification de l’ordre des mots-clés insuffisante : {entity_id}")

    return {
        "entity_type": entity_type,
        "entity_id": entity_id,
        "canonical_title": canonical,
        "displayed_title": displayed,
        "rubriques": rubriques,
        "keywords": keywords,
        "reviewer": decision.get("reviewer"),
        "reviewed_at": decision.get("reviewed_at"),
        "notes": decision.get("notes") or "",
        "decisions": {
            "canonical_title": decision.get("canonical_title_decision"),
            "displayed_title": decision.get("displayed_title_decision"),
            "rubriques": decision.get("rubriques_decision"),
            "keywords": decision.get("keywords_decision"),
        },
        "rationales": {
            "canonical_title": decision.get("canonical_title_rationale") or "",
            "displayed_title": decision.get("displayed_title_rationale") or "",
            "rubriques": copy.deepcopy(rub_rationales),
            "keywords": copy.deepcopy(kw_rationales),
            "keyword_order": decision.get("keyword_order_rationale") or "",
            "displayed_title_identity": decision.get("displayed_title_identity_justification") or "",
            "fourth_rubrique_exception": decision.get("fourth_rubrique_exception_rationale") or "",
        },
        "attestations": {
            "canonical_referents_explicit": decision.get("canonical_referents_explicit") if entity_type == "argument" else None,
            "displayed_title_complete_proposition": decision.get("displayed_title_complete_proposition") if entity_type == "argument" else None,
            "displayed_title_argument_intelligible": decision.get("displayed_title_argument_intelligible") if entity_type == "argument" else None,
            "displayed_title_concision_reviewed": decision.get("displayed_title_concision_reviewed") if entity_type == "argument" else None,
            "displayed_title_semantically_equivalent": decision.get("displayed_title_semantically_equivalent") if entity_type == "argument" else None,
            "displayed_title_improves_readability_when_distinct": decision.get("displayed_title_improves_readability_when_distinct") if entity_type == "argument" else None,
            "keywords_ordered_by_relevance": True,
        },
    }


def _validate_corpus_rules(final_items: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    debates = [item for item in final_items if item.get("entity_type") == "debate"]
    arguments = [item for item in final_items if item.get("entity_type") == "argument"]
    if len(debates) != 1:
        raise EditorialReviewError(f"La revue doit couvrir exactement une page Débat, trouvé {len(debates)}")
    if not arguments:
        raise EditorialReviewError("La revue ne couvre aucun argument")
    ids = [str(item.get("entity_id")) for item in final_items]
    if len(ids) != len(set(ids)):
        raise EditorialReviewError("Identifiants dupliqués dans la revue")
    title_map: dict[str, str] = {}
    for item in final_items:
        title = str(item.get("canonical_title") or "")
        key = normalized_identity(title)
        if key in title_map:
            raise EditorialReviewError(f"Collision de titres canoniques : {title_map[key]!r} et {title!r}")
        title_map[key] = title
    identical = sum(normalized_identity(item.get("canonical_title")) == normalized_identity(item.get("displayed_title")) for item in arguments)
    identity_ratio = identical / len(arguments)
    sets = collections.Counter(tuple(item.get("keywords") or []) for item in arguments)
    dominant_count = sets.most_common(1)[0][1]
    dominant_ratio = dominant_count / len(arguments)
    if dominant_ratio > 0.25:
        raise EditorialReviewError(f"Un jeu exact de mots-clés domine le corpus : {dominant_ratio:.2%} > 25 %")
    return {
        "pages": len(final_items),
        "arguments": len(arguments),
        "displayed_title_identity_count": identical,
        "displayed_title_identity_ratio": round(identity_ratio, 6),
        "dominant_keyword_set_count": dominant_count,
        "dominant_keyword_set_ratio": round(dominant_ratio, 6),
    }


def _expected_keyword_usages(final_items: Sequence[Mapping[str, Any]]) -> dict[str, dict[str, Any]]:
    expected: dict[str, dict[str, Any]] = {}
    for item in final_items:
        for keyword in item.get("keywords") or []:
            row = expected.setdefault(keyword, {"usages": [], "argument_count": 0})
            row["usages"].append({"entity_type": item.get("entity_type"), "entity_id": item.get("entity_id")})
            if item.get("entity_type") == "argument":
                row["argument_count"] += 1
    return expected


def _validate_vocabulary(vocabulary: Mapping[str, Any], final_items: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    entries = vocabulary.get("entries")
    if not isinstance(entries, list):
        raise EditorialReviewError("Le vocabulaire de travail ne contient pas de liste entries")
    expected = _expected_keyword_usages(final_items)
    by_fr: dict[str, dict[str, Any]] = {}
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("fr"), str):
            raise EditorialReviewError("Entrée invalide dans le vocabulaire")
        term = entry["fr"]
        if term in by_fr:
            raise EditorialReviewError(f"Mot-clé dupliqué dans le vocabulaire : {term}")
        folded = term.casefold()
        prior = next((existing for existing in by_fr if existing.casefold() == folded), None)
        if prior is not None:
            raise EditorialReviewError(f"Mots-clés différant seulement par la casse : {prior} / {term}")
        by_fr[term] = entry
    missing = sorted(set(expected) - set(by_fr))
    extra = sorted(set(by_fr) - set(expected))
    if missing or extra:
        raise EditorialReviewError(f"Couverture du vocabulaire divergente; manquants={missing[:8]}, extra={extra[:8]}")
    if len(by_fr) < 8:
        raise EditorialReviewError("Le vocabulaire français doit contenir au moins huit termes réutilisables")
    finalized: list[dict[str, Any]] = []
    for term in sorted(by_fr, key=str.casefold):
        entry = by_fr[term]
        expected_row = expected[term]
        if entry.get("decision") != "approved" or entry.get("status") not in {"approved_fr", "approved"}:
            raise EditorialReviewError(f"Mot-clé non approuvé dans le vocabulaire : {term}")
        if not _text_ok(entry.get("definition"), 12):
            raise EditorialReviewError(f"Définition insuffisante pour le mot-clé : {term}")
        if not _text_ok(entry.get("rationale"), 12):
            raise EditorialReviewError(f"Justification insuffisante pour le mot-clé : {term}")
        kind = entry.get("kind")
        if kind not in ALLOWED_KEYWORD_KINDS:
            raise EditorialReviewError(f"Nature grammaticale invalide pour le mot-clé : {term}")
        expected_policy = capitalization_policy_for_kind(str(kind))
        if entry.get("capitalization_policy") != expected_policy:
            raise EditorialReviewError(f"Politique de capitalisation invalide pour le mot-clé : {term}")
        capitalization_issues = keyword_capitalization_issues(term, str(kind))
        if capitalization_issues:
            raise EditorialReviewError(f"Capitalisation non canonique pour le mot-clé {term} : {capitalization_issues}")
        if kind in {"proper_name", "acronym"} and not _text_ok(entry.get("capitalization_rationale"), 12):
            raise EditorialReviewError(f"Justification de capitalisation insuffisante pour le mot-clé : {term}")
        if kind in {"noun", "noun_phrase"} and str(entry.get("capitalization_rationale") or "").strip():
            raise EditorialReviewError(f"Justification de majuscule inattendue pour le nom commun : {term}")
        if _is_compositional_keyword_fr(term):
            raise EditorialReviewError(
                f"Mot-clé composé à décomposer en unités de base : {term}. "
                "Exemple : psychologie religieuse → psychologie + religion."
            )
        if entry.get("atomic_concept") is not True:
            raise EditorialReviewError(f"Atomicité sémantique non attestée pour le mot-clé : {term}")
        if entry.get("compositional_intersection") is not False:
            raise EditorialReviewError(f"Intersection compositionnelle non exclue pour le mot-clé : {term}")
        if not isinstance(entry.get("multiword_exception"), bool):
            raise EditorialReviewError(f"Décision sur la locution polylexicale absente pour le mot-clé : {term}")
        if entry.get("multiword_exception") is True and not _text_ok(entry.get("multiword_exception_rationale"), 20):
            raise EditorialReviewError(f"Justification d'atomicité insuffisante pour la locution : {term}")
        if entry.get("scope") != "site_navigation":
            raise EditorialReviewError(f"Portée incorrecte pour le mot-clé : {term}")
        if entry.get("cross_debate_reusable") is not True:
            raise EditorialReviewError(f"Réutilisabilité inter-débat non attestée : {term}")
        if entry.get("local_frequency_is_validity_criterion") is not False:
            raise EditorialReviewError(f"Fréquence locale utilisée à tort pour le mot-clé : {term}")
        actual_usages = entry.get("usages")
        if actual_usages != expected_row["usages"]:
            raise EditorialReviewError(f"Usages divergents pour le mot-clé : {term}")
        raw_concept_id = str(entry.get("concept_id") or "").strip()
        if raw_concept_id:
            if not re.fullmatch(r"KWD-[A-F0-9]{12,64}", raw_concept_id):
                raise EditorialReviewError(f"concept_id invalide pour le mot-clé : {term}")
            concept_id = raw_concept_id
        else:
            concept_id = "KWD-" + sha256_bytes(normalized_text(term).casefold().encode("utf-8"))[:16].upper()
        finalized.append({
            "concept_id": concept_id,
            "fr": term,
            "en": entry.get("en") if isinstance(entry.get("en"), str) and entry.get("en").strip() else None,
            "definition": entry.get("definition").strip(),
            "kind": entry.get("kind"),
            "capitalization_policy": entry.get("capitalization_policy"),
            "capitalization_rationale": str(entry.get("capitalization_rationale") or "").strip(),
            "atomic_concept": True,
            "compositional_intersection": False,
            "multiword_exception": entry.get("multiword_exception"),
            **({"multiword_exception_rationale": str(entry.get("multiword_exception_rationale") or "").strip()} if entry.get("multiword_exception") else {}),
            "scope": "site_navigation",
            "cross_debate_reusable": True,
            "local_frequency_is_validity_criterion": False,
            "usage_count_in_debate": expected_row["argument_count"],
            "usages": copy.deepcopy(expected_row["usages"]),
            "status": "approved_fr",
            "rationale": entry.get("rationale").strip(),
        })
    concept_ids = [row["concept_id"] for row in finalized]
    if len(concept_ids) != len(set(concept_ids)):
        raise EditorialReviewError("concept_id dupliqué dans le vocabulaire contrôlé")
    return finalized


def _coverage_against_registry(working: Path, final_items: Sequence[Mapping[str, Any]]) -> None:
    _, registry, _ = assert_graph_validated_without_final_pages(working)
    active_ids = {str(node.get("id")) for node in (registry.get("graph") or {}).get("nodes") or [] if node.get("status") == "active"}
    reviewed_ids = {str(item.get("entity_id")) for item in final_items if item.get("entity_type") == "argument"}
    if reviewed_ids != active_ids:
        raise EditorialReviewError(f"Couverture des arguments divergente; manquants={sorted(active_ids-reviewed_ids)}, extra={sorted(reviewed_ids-active_ids)}")


def finalize_review(project_root: Path, debate_id: str, work_id: str) -> dict[str, Any]:
    workspace_path, meta = _load_workspace(project_root, debate_id, work_id)
    if meta.get("status") not in {"audit_ready", "fr_review_finalized"}:
        raise EditorialReviewError(f"Statut de workspace incompatible avec la finalisation : {meta.get('status')}")
    _assert_source_unchanged(project_root, debate_id, meta)
    working = _assert_pristine_working_copy(workspace_path, meta)
    review_path = workspace_path / "reviews" / "fr" / "page_metadata_review.json"
    review = load_json(review_path, "revue française")

    if review.get("status") == "approved" and review.get("review_sha256"):
        if review.get("review_sha256") != review_sha256(review):
            raise EditorialReviewError("Empreinte de revue finalisée invalide")
        if review.get("prepared_working_copy_sha256") != full_tree_sha256(working):
            raise EditorialReviewError("La copie de travail a changé depuis la finalisation")
        return {
            "status": "fr_review_finalized",
            "debate_id": debate_id,
            "work_id": work_id,
            "review_sha256": review["review_sha256"],
            "pages": (review.get("summary") or {}).get("pages"),
            "arguments": (review.get("summary") or {}).get("arguments"),
            "idempotent": True,
        }

    if review.get("schema") not in {"wikidebia-fr-page-metadata-review-1.0", REVIEW_SCHEMA}:
        raise EditorialReviewError("Schéma de revue française non pris en charge")
    if review.get("debate_id") != debate_id or review.get("work_id") != work_id:
        raise EditorialReviewError("Identité de la revue française divergente")
    raw_items = review.get("items")
    if not isinstance(raw_items, list):
        raise EditorialReviewError("La revue française ne contient pas de liste items")
    final_items = [_validate_item(item) for item in raw_items]
    summary = _validate_corpus_rules(final_items)
    _coverage_against_registry(working, final_items)
    vocabulary_path = workspace_path / "data" / "keyword_vocabulary_working.json"
    vocabulary = load_json(vocabulary_path, "vocabulaire de travail")
    finalized_vocabulary = _validate_vocabulary(vocabulary, final_items)

    finalized = copy.deepcopy(review)
    finalized.update({
        "schema": REVIEW_SCHEMA,
        "schema_version": "1.1",
        "kit_version": KIT_VERSION,
        "status": "approved",
        "finalized_at": now_iso(),
        "prepared_working_copy_sha256": full_tree_sha256(working),
        "summary": summary,
        "final_values": final_items,
        "finalized_vocabulary": finalized_vocabulary,
        "review_sha256": None,
    })
    finalized["review_sha256"] = review_sha256(finalized)
    write_json(review_path, finalized)

    meta = copy.deepcopy(meta)
    meta["kit_version"] = KIT_VERSION
    meta["status"] = "fr_review_finalized"
    meta.setdefault("artifacts", {})["french_metadata_review"] = "reviews/fr/page_metadata_review.json"
    meta["artifacts"]["french_metadata_lock"] = "data/fr_page_metadata_lock.json"
    meta["artifacts"]["reviewed_copy"] = "reviewed-copy"
    meta["french_review"] = {
        "status": "finalized",
        "review_sha256": finalized["review_sha256"],
        "finalized_at": finalized["finalized_at"],
        "prepared_working_copy_sha256": finalized["prepared_working_copy_sha256"],
    }
    meta["workspace_sha256"] = None
    meta["workspace_sha256"] = workspace_receipt_hash(meta)
    write_json(workspace_path / "workspace.json", meta)

    return {
        "status": "fr_review_finalized",
        "debate_id": debate_id,
        "work_id": work_id,
        "review_sha256": finalized["review_sha256"],
        "pages": summary["pages"],
        "arguments": summary["arguments"],
        "working_copy_mutated": False,
        "english_translation_started": False,
        "final_pages_generated": False,
    }



def _next_validation_id(manifest: Mapping[str, Any]) -> str:
    date = now_iso()[:10].replace("-", "")
    prefix = f"V{date}-"
    numbers = []
    for row in manifest.get("validations") or []:
        value = str((row or {}).get("id") or "")
        if value.startswith(prefix):
            try:
                numbers.append(int(value.rsplit("-", 1)[1]))
            except (ValueError, IndexError):
                pass
    return f"{prefix}{max(numbers, default=0) + 1:03d}"


def _run_validator(
    project_root: Path, package: Path, *, scopes: Sequence[str], json_output: Path, text_output: Path,
) -> dict[str, Any]:
    validator_src = project_root / "validator" / "src"
    if not validator_src.is_dir():
        raise EditorialReviewError("validator/src absent; l’application de la revue ne peut pas être validée")
    python = project_root / ".venv" / "bin" / "python"
    if not python.is_file():
        python = Path(sys.executable)
    command = [str(python), "-m", "wikidebia_validator.cli", "validate", str(package)]
    for scope in scopes:
        command.extend(["--scope", scope])
    command.extend(["--format", "text", "--json-output", str(json_output), "--text-output", str(text_output)])
    env = dict(os.environ)
    env["PYTHONPATH"] = str(validator_src) + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    completed = subprocess.run(command, text=True, capture_output=True, env=env, check=False)
    if not json_output.is_file():
        raise EditorialReviewError(f"Le validateur n’a pas produit son rapport : {completed.stderr[-1000:]}")
    report = load_json(json_output, "rapport du validateur")
    if completed.returncode != 0 or report.get("result") == "failed":
        errors = [item for item in (report.get("findings") or report.get("issues") or []) if str(item.get("level") or item.get("severity") or "").upper() == "ERROR"]
        detail = "; ".join(f"{item.get('code')} [{item.get('path')} {item.get('pointer')}]: {item.get('message')}" for item in errors[:4])
        raise EditorialReviewError(
            f"Validation structurelle échouée; consulter {json_output.relative_to(package).as_posix()}"
            + (f"; {detail}" if detail else "")
        )
    if str(report.get("validator_version")) != VALIDATOR_VERSION:
        raise EditorialReviewError(f"Version du validateur inattendue : {report.get('validator_version')}")
    return report

def _changes(source: Mapping[str, Any], final: Mapping[str, Any]) -> list[dict[str, Any]]:
    operations: list[dict[str, Any]] = []
    for field, source_key in (("canonical_title", "canonical_title"), ("displayed_title", "displayed_title"), ("rubriques", "rubriques"), ("keywords", "keywords")):
        before = source.get(source_key)
        after = final.get(field)
        if before != after:
            operations.append({
                "entity_type": final.get("entity_type"),
                "entity_id": final.get("entity_id"),
                "field": field,
                "before": copy.deepcopy(before),
                "after": copy.deepcopy(after),
                "decision": (final.get("decisions") or {}).get(field),
                "rationale": copy.deepcopy((final.get("rationales") or {}).get(field)),
            })
    return operations


def _build_reviewed_copy(project_root: Path, source: Path, target: Path, review: Mapping[str, Any], debate_id: str, work_id: str) -> dict[str, Any]:
    shutil.copytree(source, target, symlinks=False, copy_function=shutil.copy2)
    assert_no_symlinks(target)
    manifest, registry, projection = assert_graph_validated_without_final_pages(target)
    old_structural = str((((registry.get("graph") or {}).get("lifecycle") or {}).get("structural_sha256") or ""))
    final_items = review.get("final_values") or []
    by_id = {str(item.get("entity_id")): item for item in final_items if item.get("entity_type") == "argument"}
    debate_final = next(item for item in final_items if item.get("entity_type") == "debate")
    review_source_by_id = {str(item.get("entity_id")): item.get("source") or {} for item in review.get("items") or []}
    operations: list[dict[str, Any]] = []
    for node in (registry.get("graph") or {}).get("nodes") or []:
        if node.get("status") != "active":
            continue
        node_id = str(node.get("id"))
        final = by_id[node_id]
        fr = node.setdefault("fr", {})
        fr["canonical_title"] = final["canonical_title"]
        fr["displayed_title"] = final["displayed_title"]
        fr["rubriques"] = copy.deepcopy(final["rubriques"])
        fr["keywords"] = copy.deepcopy(final["keywords"])
        fr["title_status"] = "validated"
        operations.extend(_changes(review_source_by_id[node_id], final))

    new_structural = structural_sha256(registry)
    lifecycle = (registry.get("graph") or {}).get("lifecycle") or {}
    lifecycle["structural_sha256"] = new_structural
    projection["nodes"] = copy.deepcopy((registry.get("graph") or {}).get("nodes") or [])
    projection["edges"] = copy.deepcopy((registry.get("graph") or {}).get("edges") or [])
    projection["occurrences"] = copy.deepcopy((registry.get("graph") or {}).get("occurrences") or [])
    projection["derived_counts"] = copy.deepcopy((registry.get("graph") or {}).get("derived_counts") or {})
    projection["depth_policy"] = copy.deepcopy((registry.get("graph") or {}).get("depth_policy") or {})
    projection["lifecycle"] = copy.deepcopy(lifecycle)

    timestamp = now_iso()
    metadata_lock = {
        "schema": METADATA_LOCK_SCHEMA,
        "schema_version": "1.0",
        "normative_revision": NORM_VERSION,
        "kit_version": KIT_VERSION,
        "debate_id": debate_id,
        "work_id": work_id,
        "language": "fr",
        "status": "locked_for_generation",
        "review_sha256": review.get("review_sha256"),
        "applied_at": timestamp,
        "old_structural_sha256": old_structural,
        "new_structural_sha256": new_structural,
        "debate": debate_final,
        "arguments": [by_id[key] for key in sorted(by_id)],
    }
    vocabulary = {
        "schema": "wikidebia-keyword-vocabulary-1.0",
        "normative_revision": NORM_VERSION,
        "debate_id": debate_id,
        "status": "approved_fr",
        "language_status": "fr_locked_en_pending",
        "review_sha256": review.get("review_sha256"),
        "entries": copy.deepcopy(review.get("finalized_vocabulary") or []),
    }
    operations.extend(_changes(review_source_by_id["debate"], debate_final))
    changeset = {
        "schema": CHANGESET_SCHEMA,
        "schema_version": "1.1",
        "debate_id": debate_id,
        "work_id": work_id,
        "status": "applied",
        "review_sha256": review.get("review_sha256"),
        "applied_at": timestamp,
        "old_structural_sha256": old_structural,
        "new_structural_sha256": new_structural,
        "operation_count": len(operations),
        "operations": operations,
        "source_imports_mutated": False,
        "final_pages_generated": False,
        "english_translation_started": False,
    }
    write_json(target / "data" / "registre_debat.json", registry)
    write_json(target / "graph" / "graphe_argumentatif.json", projection)
    title = str((((registry.get("debate") or {}).get("pages") or {}).get("fr") or {}).get("canonical_title") or debate_final["canonical_title"])
    graph = registry.get("graph") or {}
    (target / "graph" / "graphe_argumentatif.md").write_text(
        _markdown_graph(title, graph.get("nodes") or [], graph.get("edges") or [], graph.get("occurrences") or [], graph.get("derived_counts") or {}),
        encoding="utf-8", newline="\n",
    )
    write_json(target / "data" / "fr_page_metadata_lock.json", metadata_lock)
    write_json(target / "data" / "keyword_vocabulary.json", vocabulary)
    write_json(target / "changes" / "changeset.json", changeset)
    manifest["updated_at"] = timestamp
    write_json(target / "manifest.json", manifest)
    assert_graph_validated_without_final_pages(target)
    if structural_sha256(load_json(target / "data" / "registre_debat.json")) != new_structural:
        raise EditorialReviewError("L’empreinte structurelle recalculée n’est pas reproductible")

    preflight_json = target / "reports" / "fr_metadata_preflight.json"
    preflight_txt = target / "reports" / "fr_metadata_preflight.txt"
    preflight = _run_validator(
        project_root, target, scopes=("schema", "coherence", "graph", "files"),
        json_output=preflight_json, text_output=preflight_txt,
    )
    manifest = load_json(target / "manifest.json", "manifest.json")
    manifest.setdefault("validations", []).append({
        "id": _next_validation_id(manifest),
        "scope": "graph",
        "language": None,
        "validator_version": VALIDATOR_VERSION,
        "executed_at": timestamp,
        "input_sha256": new_structural,
        "result": preflight.get("result"),
        "blocking_errors": int((preflight.get("summary") or {}).get("errors") or 0),
        "warnings": int((preflight.get("summary") or {}).get("warnings") or 0),
        "report_path": "reports/fr_metadata_preflight.json",
    })
    write_json(target / "manifest.json", manifest)
    final_json = target / "reports" / "fr_metadata_validation.json"
    final_txt = target / "reports" / "fr_metadata_validation.txt"
    final_validation = _run_validator(
        project_root, target, scopes=("schema", "coherence", "graph", "files", "workflow"),
        json_output=final_json, text_output=final_txt,
    )
    return {
        "old_structural_sha256": old_structural,
        "new_structural_sha256": new_structural,
        "operation_count": len(operations),
        "changeset": changeset,
        "metadata_lock": metadata_lock,
        "validator_result": final_validation.get("result"),
        "validator_report_path": "reports/fr_metadata_validation.json",
    }


def _update_tasks_after_apply(workspace_path: Path, applied_at: str) -> None:
    path = workspace_path / "tasks" / "editorial_tasks.json"
    data = load_json(path, "registre des tâches")
    for task in data.get("tasks") or []:
        area = task.get("area")
        if area in {"titles", "rubriques", "keywords", "keyword_vocabulary"}:
            task["status"] = "completed"
            task["completed_at"] = applied_at
        elif area == "english_translation_readiness":
            task["status"] = "ready"
            task["completed_at"] = None
    data["counts"] = dict(sorted(collections.Counter(task.get("status") for task in data.get("tasks") or []).items()))
    data["updated_at"] = applied_at
    write_json(path, data)


def _unlock_translation_registry(workspace_path: Path, applied_at: str) -> None:
    path = workspace_path / "reviews" / "en" / "translation_readiness.json"
    data = load_json(path, "préparation de la traduction")
    for item in data.get("items") or []:
        item["french_metadata_review_status"] = "locked"
        item["translation_status"] = "ready_for_translation"
    data["status"] = "ready_for_translation"
    data["french_metadata_locked_at"] = applied_at
    write_json(path, data)


def apply_review(project_root: Path, debate_id: str, work_id: str, confirm_review_sha256: str) -> dict[str, Any]:
    workspace_path, meta = _load_workspace(project_root, debate_id, work_id)
    if meta.get("status") not in {"fr_review_finalized", "fr_metadata_applied"}:
        raise EditorialReviewError(f"Statut de workspace incompatible avec l’application : {meta.get('status')}")
    _assert_source_unchanged(project_root, debate_id, meta)
    working = _assert_pristine_working_copy(workspace_path, meta)
    review = load_json(workspace_path / "reviews" / "fr" / "page_metadata_review.json", "revue française")
    if review.get("status") != "approved" or not review.get("review_sha256"):
        raise EditorialReviewError("La revue française n’est pas finalisée")
    if review.get("review_sha256") != review_sha256(review):
        raise EditorialReviewError("Empreinte de revue française invalide")
    if confirm_review_sha256 != review.get("review_sha256"):
        raise EditorialReviewError("L’empreinte confirmée ne correspond pas à la revue approuvée")
    if review.get("prepared_working_copy_sha256") != full_tree_sha256(working):
        raise EditorialReviewError("working-copy a changé depuis la finalisation")

    reviewed = workspace_path / "reviewed-copy"
    if reviewed.is_dir():
        if meta.get("status") != "fr_metadata_applied":
            raise EditorialReviewError("reviewed-copy existe sans état d’application cohérent")
        expected = str((meta.get("reviewed_copy") or {}).get("tree_sha256") or "")
        actual = full_tree_sha256(reviewed)
        if not expected or actual != expected:
            raise EditorialReviewError("Empreinte de reviewed-copy divergente")
        return {
            "status": "fr_metadata_applied",
            "debate_id": debate_id,
            "work_id": work_id,
            "review_sha256": review["review_sha256"],
            "reviewed_copy": relative_to_project(reviewed, project_root),
            "reviewed_copy_tree_sha256": actual,
            "idempotent": True,
        }
    if reviewed.exists() or reviewed.is_symlink():
        raise EditorialReviewError("Chemin reviewed-copy déjà occupé")

    temp = Path(tempfile.mkdtemp(prefix=".reviewed-copy.tmp-", dir=workspace_path))
    try:
        # tempfile created a directory; copytree requires a non-existing destination.
        shutil.rmtree(temp)
        result = _build_reviewed_copy(project_root, working, temp, review, debate_id, work_id)
        assert_no_symlinks(temp)
        reviewed_hash = full_tree_sha256(temp)
        # Provenance imports must remain exactly identical to the pristine source copy.
        if full_tree_sha256(temp / "imports") != full_tree_sha256(working / "imports"):
            raise EditorialReviewError("Les imports de provenance ont été modifiés pendant l’application")
        os.replace(temp, reviewed)
        fsync_directory(workspace_path)
    except Exception:
        shutil.rmtree(temp, ignore_errors=True)
        raise

    applied_at = result["metadata_lock"]["applied_at"]
    _update_tasks_after_apply(workspace_path, applied_at)
    _unlock_translation_registry(workspace_path, applied_at)
    meta = copy.deepcopy(meta)
    meta["kit_version"] = KIT_VERSION
    meta["status"] = "fr_metadata_applied"
    meta["working_copy"]["current_status"] = "preserved_pristine"
    meta["reviewed_copy"] = {
        "path": "reviewed-copy",
        "tree_sha256": reviewed_hash,
        "status": "fr_metadata_locked",
        "review_sha256": review["review_sha256"],
        "old_structural_sha256": result["old_structural_sha256"],
        "new_structural_sha256": result["new_structural_sha256"],
        "applied_at": applied_at,
    }
    meta["boundaries"]["automatic_editorial_corrections_applied"] = False
    meta["boundaries"]["final_pages_generated"] = False
    meta["boundaries"]["english_translation_started"] = False
    meta["french_review"]["status"] = "applied"
    meta["french_review"]["applied_at"] = applied_at
    meta["workspace_sha256"] = None
    meta["workspace_sha256"] = workspace_receipt_hash(meta)
    write_json(workspace_path / "workspace.json", meta)

    if full_tree_sha256(working) != review.get("prepared_working_copy_sha256"):
        raise EditorialReviewError("working-copy a changé pendant l’application")
    _assert_source_unchanged(project_root, debate_id, meta)

    return {
        "status": "fr_metadata_applied",
        "debate_id": debate_id,
        "work_id": work_id,
        "review_sha256": review["review_sha256"],
        "reviewed_copy": relative_to_project(reviewed, project_root),
        "reviewed_copy_tree_sha256": reviewed_hash,
        "old_structural_sha256": result["old_structural_sha256"],
        "new_structural_sha256": result["new_structural_sha256"],
        "operations": result["operation_count"],
        "source_corpus_mutated": False,
        "working_copy_mutated": False,
        "imports_mutated": False,
        "final_pages_generated": False,
        "english_translation_started": False,
        "translation_readiness": "ready_for_translation",
        "validator_result": result["validator_result"],
        "validator_report_path": result["validator_report_path"],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Finaliser ou appliquer la revue française des métadonnées éditoriales.")
    parser.add_argument("debate_id")
    parser.add_argument("--work-id", required=True)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--finalize", action="store_true", help="Valider et sceller la revue sans modifier la copie de travail")
    action.add_argument("--apply", action="store_true", help="Créer reviewed-copy à partir de la revue scellée")
    parser.add_argument("--confirm-review-sha256", help="Empreinte obligatoire avec --apply")
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--machine-readable", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    project_root = args.project_root.expanduser().resolve()
    debate_id = validate_debate_id(args.debate_id)
    work_id = validate_work_id(args.work_id)
    if args.apply and not args.confirm_review_sha256:
        raise EditorialReviewError("--confirm-review-sha256 est obligatoire avec --apply")
    with exclusive_lock(project_root, debate_id, "editorial_metadata_review"):
        if args.finalize:
            result = finalize_review(project_root, debate_id, work_id)
        else:
            result = apply_review(project_root, debate_id, work_id, str(args.confirm_review_sha256))
    print(json.dumps(result, ensure_ascii=False, sort_keys=True) if args.machine_readable else json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (EditorialReviewError, CorpusBuildError) as exc:
        print(f"WIKIDEBIA BLOQUÉ : {exc}", file=__import__("sys").stderr)
        raise SystemExit(2)
