"""Validate a date-only successor without changing publication permissions."""
from __future__ import annotations

import datetime as dt
import hashlib
from typing import Any, Mapping


class PublicationDateTransitionError(RuntimeError):
    pass


def sha_text(text: str) -> str:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n").rstrip("\n")
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def english_plan_rollover_transition(
    publisher: Any,
    old_plan: Mapping[str, Any],
    new_plan: Mapping[str, Any],
    current_date: str,
) -> dict[str, Any]:
    old_date = str(old_plan.get("publication_date") or "")
    try:
        dt.date.fromisoformat(old_date)
        dt.date.fromisoformat(current_date)
    except ValueError as exc:
        raise PublicationDateTransitionError("Date civile de publication invalide") from exc
    if not old_date or current_date <= old_date:
        raise PublicationDateTransitionError(
            f"Changement de jour de publication non croissant : {old_date!r} -> {current_date!r}",
        )
    if str(new_plan.get("publication_date") or "") != current_date:
        raise PublicationDateTransitionError("Le plan anglais successeur ne porte pas le jour de publication courant")

    def keyed(plan: Mapping[str, Any]) -> dict[tuple[str, str], Mapping[str, Any]]:
        rows = list(plan.get("actions") or [])
        result = {
            (str(row.get("language") or ""), str(row.get("page_id") or "")): row
            for row in rows
        }
        if len(result) != len(rows):
            raise PublicationDateTransitionError("Page dupliquée dans le plan de publication")
        return result

    old_actions = keyed(old_plan)
    new_actions = keyed(new_plan)
    if set(old_actions) != set(new_actions):
        raise PublicationDateTransitionError("Le plan anglais successeur ne couvre pas exactement les mêmes pages")

    invariant_fields = (
        "operation_id", "kind", "language", "page_id", "page_type", "title", "source_path",
        "parameter", "local_file_sha256", "local_target_sha256", "edit_summary", "change_tags",
    )
    completed: list[dict[str, Any]] = []
    remaining: list[dict[str, Any]] = []
    unchanged_skips: list[dict[str, Any]] = []

    for key in sorted(old_actions):
        old = old_actions[key]
        new = new_actions[key]
        for field in invariant_fields:
            if old.get(field) != new.get(field):
                raise PublicationDateTransitionError(
                    f"Le plan anglais successeur modifie {field} pour {old.get('page_id')}",
                )
        old_op = str(old.get("operation") or "")
        new_op = str(new.get("operation") or "")
        if old_op not in {"create", "skip"} or new_op not in {"create", "skip"}:
            raise PublicationDateTransitionError("Le plan anglais successeur contient une opération non autorisée")

        if old_op == "skip":
            if new_op != "skip" or old.get("desired_sha256") != new.get("desired_sha256"):
                raise PublicationDateTransitionError(
                    f"Une page déjà équivalente a changé pendant le basculement de date : {old.get('title')}",
                )
            unchanged_skips.append({"page_id": old.get("page_id"), "title": old.get("title")})
            continue

        old_creation_date = str(old.get("publication_creation_date") or "")
        if old_creation_date != old_date:
            raise PublicationDateTransitionError(
                f"Date de création de l'ancien plan incohérente : {old.get('page_id')}",
            )

        if new_op == "skip":
            # GenericPublisher only emits this skip after proving that the current
            # remote revision is the original AI translation creation (parent=0,
            # expected user, exact summary/tags/content).  Requiring the old
            # desired hash/date proves that this page was created under the old plan.
            if str(new.get("publication_creation_date") or "") != old_date:
                raise PublicationDateTransitionError(
                    f"Une page déjà créée a changé de date pendant la reprise : {old.get('title')}",
                )
            if new.get("desired_sha256") != old.get("desired_sha256"):
                raise PublicationDateTransitionError(
                    f"Une page déjà créée ne correspond plus exactement à l'ancien plan : {old.get('title')}",
                )
            completed.append({
                "page_id": old.get("page_id"), "title": old.get("title"),
                "creation_date": old_date, "desired_sha256": old.get("desired_sha256"),
                "remote_revision_id": new.get("remote_revision_id"),
            })
            continue

        if str(new.get("publication_creation_date") or "") != current_date:
            raise PublicationDateTransitionError(
                f"Une page restante ne porte pas la nouvelle date de publication : {old.get('title')}",
            )
        row = publisher._manifest_page("en", str(old.get("page_id") or ""))
        if row is None:
            raise PublicationDateTransitionError(f"Page anglaise absente du manifeste : {old.get('page_id')}")
        source = publisher.root / str(old.get("source_path") or "")
        source_text = source.read_text(encoding="utf-8")
        expected_old = publisher._english_translation_creation_text(row, source_text, old_date)
        expected_new = publisher._english_translation_creation_text(row, source_text, current_date)
        if sha_text(expected_old) != old.get("desired_sha256") or sha_text(expected_new) != new.get("desired_sha256"):
            raise PublicationDateTransitionError(
                f"Le plan successeur modifie autre chose que creation-date : {old.get('title')}",
            )
        remaining.append({
            "page_id": old.get("page_id"), "title": old.get("title"),
            "old_creation_date": old_date, "new_creation_date": current_date,
            "old_desired_sha256": old.get("desired_sha256"), "new_desired_sha256": new.get("desired_sha256"),
        })

    if not remaining and not completed:
        raise PublicationDateTransitionError("Aucune création anglaise n'est concernée par le changement de jour")
    return {
        "old_publication_date": old_date,
        "new_publication_date": current_date,
        "completed_before_rollover": completed,
        "remaining_after_rollover": remaining,
        "unchanged_skips": unchanged_skips,
    }


def publication_plan_rollover_transition(
    publisher: Any, old_plan: Mapping[str, Any], new_plan: Mapping[str, Any], current_date: str,
) -> dict[str, Any]:
    """Also bind the full signed envelope and unchanged non-English operations."""
    changing = {"plan_sha256", "publication_date", "actions", "counts", "blockers", "validator_report_sha256"}
    for field in (set(old_plan) | set(new_plan)) - changing:
        if old_plan.get(field) != new_plan.get(field):
            raise PublicationDateTransitionError(f"Le plan successeur modifie {field}")
    if old_plan.get("blockers") or new_plan.get("blockers"):
        raise PublicationDateTransitionError("Un plan de changement de date contient des bloqueurs")
    old_actions = list(old_plan.get("actions") or [])
    new_actions = list(new_plan.get("actions") or [])

    def keys(rows: list[Mapping[str, Any]]) -> list[tuple[Any, Any]]:
        return [(row.get("language"), row.get("page_id")) for row in rows]

    if keys(old_actions) != keys(new_actions) or len(set(keys(old_actions))) != len(old_actions):
        raise PublicationDateTransitionError("Le plan successeur change l'ordre ou la couverture des pages")

    def translated(row: Mapping[str, Any]) -> bool:
        return row.get("language") == "en" and bool(row.get("publication_creation_date"))

    previous_english = {**old_plan, "actions": [row for row in old_actions if translated(row)]}
    next_english = {**new_plan, "actions": [row for row in new_actions if translated(row)]}
    result = english_plan_rollover_transition(publisher, previous_english, next_english, current_date)
    completed_other = []
    mutable = {
        "operation", "classification", "note", "remote_revision_id",
        "remote_sha256", "remote_target_sha256",
    }
    for old, new in zip(old_actions, new_actions):
        if translated(old):
            continue
        for field in (set(old) | set(new)) - mutable:
            if old.get(field) != new.get(field):
                raise PublicationDateTransitionError(f"Le plan successeur modifie {field} hors traduction anglaise")
        old_op, new_op = old.get("operation"), new.get("operation")
        if old_op not in {"create", "update", "skip"} or new_op not in {old_op, "skip"}:
            raise PublicationDateTransitionError("Opération non anglaise modifiée lors du changement de jour")
        if old_op != "skip" and new_op == "skip":
            if new.get("remote_sha256") != old.get("desired_sha256"):
                raise PublicationDateTransitionError("Une page terminée hors traduction anglaise a divergé")
            completed_other.append({"language": old.get("language"), "page_id": old.get("page_id")})
        elif any(
            old.get(field) != new.get(field)
            for field in ("remote_revision_id", "remote_sha256", "remote_target_sha256")
        ):
            raise PublicationDateTransitionError("Une révision distante hors traduction anglaise a changé")
    return {**result, "completed_other_operations": completed_other}

