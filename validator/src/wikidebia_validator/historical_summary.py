from __future__ import annotations

from typing import Any

from .package import PackageContext

HISTORICAL_PRESENT = {
    "historical_existing",
    "historical_authorized_change",
    "historical_authorized_creation",
}


def _english_argument_ids(manifest: dict[str, Any]) -> set[str]:
    return {
        str(page.get("page_id"))
        for page in manifest.get("pages", [])
        if isinstance(page, dict)
        and page.get("language") == "en"
        and page.get("page_type") == "argument"
        and page.get("page_id")
    }


def _summary_provenance_sets(ctx: PackageContext) -> dict[str, frozenset[tuple[str, str]]]:
    """Return the authoritative summary provenance sets for this package.

    Wikicode and editorial validation must use exactly the same derivation.
    Older implementations kept separate helpers with the same cache attribute;
    when wikicode ran first it could cache an incomplete set that omitted
    ``historical_authorized_change`` and poison the later editorial scope.
    """
    cached = getattr(ctx, "_historical_summary_provenance_sets_v1_cache", None)
    if isinstance(cached, dict) and {"protected", "absent", "owner_removed"} <= set(cached):
        return cached

    protected: set[tuple[str, str]] = set()
    absent: set[tuple[str, str]] = set()
    owner_removed: set[tuple[str, str]] = set()
    manifest = ctx.manifest() or {}
    exists = getattr(ctx, "exists", lambda _path: False)
    load_json = getattr(ctx, "load_json", lambda _path: None)

    def classify(node_id: object, language: object, provenance: object) -> bool:
        if not isinstance(node_id, str) or language not in {"fr", "en"}:
            return False
        key = (node_id, str(language))
        value = str(provenance or "")
        if value in HISTORICAL_PRESENT:
            protected.add(key)
            return True
        if value == "historical_absent":
            absent.add(key)
            return True
        if value == "owner_removed":
            owner_removed.add(key)
            return True
        return False

    # Legacy aggregate lock, when a historical workspace still declares one.
    controls = manifest.get("editorial_controls") or {}
    cfg = controls.get("legacy_content_preservation") or {}
    rel = cfg.get("lock_path")
    if cfg.get("enabled") is True and isinstance(rel, str) and exists(rel):
        lock = load_json(rel)
        if isinstance(lock, dict):
            for entry in lock.get("arguments") or []:
                if isinstance(entry, dict):
                    classify(entry.get("id"), entry.get("language"), entry.get("summary_provenance"))

    # Current FR/EN content locks are authoritative.
    for language, lock_rel in (("fr", "data/fr_content_lock.json"), ("en", "data/en_content_lock.json")):
        if not exists(lock_rel):
            continue
        lock = load_json(lock_rel)
        if not isinstance(lock, dict):
            continue
        for entry in lock.get("arguments") or []:
            if not isinstance(entry, dict) or not isinstance(entry.get("id"), str):
                continue
            node_id = str(entry["id"])
            if classify(node_id, language, entry.get("summary_provenance")):
                continue

            # Compatibility with early provenance-aware locks that did not
            # yet expose summary_provenance explicitly.
            if language == "fr" and entry.get("page_origin") == "preexisting":
                if entry.get("summary") is None:
                    absent.add((node_id, language))
                elif entry.get("summary") not in {"", None}:
                    protected.add((node_id, language))
            elif language == "en" and entry.get("source_page_origin") == "preexisting":
                if entry.get("summary") is None:
                    absent.add((node_id, language))
                elif entry.get("summary") not in {"", None}:
                    protected.add((node_id, language))

        # Consent-era French locks also carry a separate historical decision
        # inventory. Keep it as a compatibility proof, but never let it
        # override the explicit per-argument provenance above.
        if language == "fr":
            decisions = lock.get("historical_text_decisions")
            if isinstance(decisions, dict):
                for entry in decisions.get("arguments") or []:
                    if not isinstance(entry, dict) or not isinstance(entry.get("id"), str):
                        continue
                    if entry.get("page_origin") != "preexisting":
                        continue
                    node_id = str(entry["id"])
                    historical_status = str(entry.get("historical_status") or "")
                    if historical_status == "historical_absent" and entry.get("decision") == "preserved":
                        absent.add((node_id, "fr"))
                    elif historical_status and historical_status != "historical_absent":
                        protected.add((node_id, "fr"))

    # A historical French source remains historical when translated. Limit
    # propagation to English argument pages that actually exist in manifest.
    en_ids = _english_argument_ids(manifest)
    protected.update(
        (node_id, "en")
        for node_id, language in list(protected)
        if language == "fr" and node_id in en_ids
    )
    absent.update(
        (node_id, "en")
        for node_id, language in list(absent)
        if language == "fr" and node_id in en_ids
    )
    owner_removed.update(
        (node_id, "en")
        for node_id, language in list(owner_removed)
        if language == "fr" and node_id in en_ids
    )

    result = {
        "protected": frozenset(protected),
        "absent": frozenset(absent),
        "owner_removed": frozenset(owner_removed),
    }
    setattr(ctx, "_historical_summary_provenance_sets_v1_cache", result)
    return result


def protected_historical_summary_keys(ctx: PackageContext) -> set[tuple[str, str]]:
    return set(_summary_provenance_sets(ctx)["protected"])


def historically_absent_summary_keys(ctx: PackageContext) -> set[tuple[str, str]]:
    return set(_summary_provenance_sets(ctx)["absent"])


def owner_removed_summary_keys(ctx: PackageContext) -> set[tuple[str, str]]:
    return set(_summary_provenance_sets(ctx)["owner_removed"])
