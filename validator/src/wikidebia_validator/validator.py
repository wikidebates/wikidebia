from __future__ import annotations

from pathlib import Path

from . import __version__
from .batches import validate_batches
from .bilingual import validate_bilingual
from .coherence import validate_coherence
from .files import validate_files
from .editorial import validate_editorial
from .graph import validate_graph
from .package import PackageContext
from .report import Report, portable_display_path
from .schema_validation import SchemaStore, validate_all_schemas
from .sources import validate_sources
from .wikicode import validate_wikicode
from .workflow import validate_workflow

ALL_SCOPES = ["schema", "coherence", "graph", "batches", "sources", "files", "wikicode", "bilingual", "editorial", "workflow"]


def validate_package(root: str | Path, scopes: list[str] | None = None, previous_status: str | None = None) -> Report:
    root_path = Path(root).resolve()
    selected = ALL_SCOPES if not scopes or "all" in scopes else scopes
    report = Report(__version__, portable_display_path(root), selected)
    if not root_path.is_dir():
        report.error("WDV-FS-001", "Le chemin du paquet n'est pas un dossier", path=portable_display_path(root))
        return report
    ctx = PackageContext(root_path, report)
    try:
        if "schema" in selected:
            validate_all_schemas(ctx, SchemaStore())
        if "coherence" in selected:
            validate_coherence(ctx)
        if "graph" in selected:
            validate_graph(ctx)
        if "batches" in selected:
            validate_batches(ctx)
        if "sources" in selected:
            validate_sources(ctx)
        if "files" in selected:
            validate_files(ctx)
        if "wikicode" in selected:
            validate_wikicode(ctx)
        if "bilingual" in selected:
            validate_bilingual(ctx)
        if "editorial" in selected:
            validate_editorial(ctx)
        if "workflow" in selected:
            validate_workflow(ctx, previous_status=previous_status)
        consolidated = ((ctx.manifest() or {}).get("normative_versions") or {}).get("consolidated_norm")
        if consolidated not in {"1.1.0", "1.1.1", "1.1.2", "1.1.3", "1.1.4", "1.1.5", "1.1.6", "1.1.7", "1.1.8", "1.1.9", "1.2.0", "1.2.1", "1.2.2", "1.2.3", "1.2.4", "1.2.5", "1.2.6", "1.2.7", "1.2.8", "1.2.9", "1.2.10", "1.2.11", "1.2.12", "1.2.13", "1.2.14", "1.2.15", "1.2.16", "1.2.17", "1.2.18", "1.2.19", "1.2.20", "1.2.21", "1.2.22", "1.2.23", "1.2.24", "1.2.25", "1.2.26", "1.2.27", "1.2.28", "1.2.29", "1.2.30"} or "editorial" not in selected:
            report.info("WDV-DOC-001", "Les contrôles de qualité argumentative, d'équilibre, de quasi-doublons sémantiques et de fidélité documentaire restent soumis à une revue humaine.")
    except Exception as exc:  # defensive boundary: stable report instead of traceback by default
        report.error("WDV-INT-001", f"Erreur interne : {type(exc).__name__}: {exc}")
    return report
