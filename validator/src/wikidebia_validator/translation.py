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
    if not isinstance(manifest, dict):
        return False
    norm = ((manifest.get("normative_versions") or {}).get("consolidated_norm"))
    return _version_tuple(norm) >= (1, 2, 34) and english_translation_status(manifest) == "deferred"
