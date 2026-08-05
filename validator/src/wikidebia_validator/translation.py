from __future__ import annotations

from typing import Any


def _version_tuple(value: Any) -> tuple[int, ...]:
    try:
        return tuple(int(part) for part in str(value or "").split("."))
    except ValueError:
        return ()


def english_translation_status(manifest: dict[str, Any] | None) -> str:
    """Return the explicit English translation state.

    Packages predating norm 1.2.34 remain strict by default.  The relaxed
    behaviour is enabled only by an explicit ``translation_status.en`` value.
    """
    if not isinstance(manifest, dict):
        return "pending"
    status = ((manifest.get("translation_status") or {}).get("en"))
    return str(status or "pending")


def english_translation_deferred(manifest: dict[str, Any] | None) -> bool:
    """Return whether English production is explicitly deferred.

    The status is an operational workflow declaration, not a migration of the
    corpus' editorial norm.  It therefore applies to legacy 1.2.x corpora when
    explicitly present; absence of the field remains strict for backwards
    compatibility.
    """
    if not isinstance(manifest, dict):
        return False
    return english_translation_status(manifest) == "deferred"
