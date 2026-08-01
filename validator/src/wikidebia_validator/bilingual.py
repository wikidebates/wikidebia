from __future__ import annotations

from typing import Any

from .graph import state_at_least
from .package import PackageContext
from .wikicode import alphabetically_sorted


SECTION_MAP = {
    "Aménagement": "Planning", "Culture": "Culture", "Droit": "Law", "Écologie": "Ecology",
    "Économie": "Economy", "Éducation": "Education", "Éthique": "Ethics", "Géopolitique": "Geopolitics",
    "Histoire": "History", "Philosophie": "Philosophy", "Politique": "Politics", "Psychologie": "Psychology",
    "Religion et spiritualité": "Religion and spirituality", "Santé": "Health", "Science": "Science",
    "Société": "Society", "Sport et loisirs": "Sport and leisure", "Technologie": "Technology",
}


def validate_bilingual(ctx: PackageContext) -> None:
    registry = ctx.registry()
    manifest = ctx.manifest()
    if not registry or not manifest:
        return
    strict = state_at_least(manifest.get("global_status"), "bilingual_validated")
    nodes = [n for n in registry.get("graph", {}).get("nodes", []) if n.get("status") == "active"]
    pages = {(p.get("page_id"), p.get("language")): p for p in manifest.get("pages", [])}
    for node in nodes:
        nid = node.get("id")
        fr = node.get("fr") or {}
        en = node.get("en") or {}
        if strict:
            if en.get("title_status") != "locked" or not en.get("canonical_title"):
                ctx.report.error("WDV-BIL-001", f"Titre anglais non verrouillé pour {nid}", path=ctx.core_paths()["registry"])
            if (nid, "fr") not in pages or (nid, "en") not in pages:
                ctx.report.error("WDV-BIL-001", f"Paire de pages bilingues incomplète pour {nid}", path="manifest.json")
        expected_sections = [SECTION_MAP[x] for x in fr.get("rubriques", []) if x in SECTION_MAP]
        norm = ((ctx.manifest().get("normative_versions") or {}).get("consolidated_norm"))
        if norm in {"1.2.6", "1.2.7", "1.2.8", "1.2.9", "1.2.10", "1.2.11", "1.2.12", "1.2.13", "1.2.14", "1.2.15", "1.2.16", "1.2.17", "1.2.18", "1.2.19", "1.2.20"}:
            expected_sections = alphabetically_sorted(expected_sections)
        if en.get("sections") and en.get("sections") != expected_sections:
            ctx.report.warning("WDV-BIL-004", f"Sections anglaises divergentes pour {nid}; une justification éditoriale est requise", path=ctx.core_paths()["registry"], details={"expected": expected_sections, "actual": en.get("sections")})
        fr_primary = (node.get("derived") or {}).get("primary_occurrence_id")
        # Same registry means relations/occurrences are language-neutral; still check page records exist symmetrically.
        if strict:
            fr_rec = ((node.get("pages") or {}).get("fr") or {})
            en_rec = ((node.get("pages") or {}).get("en") or {})
            if (fr_rec.get("generation") or {}).get("status") != "validated" or (en_rec.get("generation") or {}).get("status") != "validated":
                ctx.report.error("WDV-BIL-001", f"Pages bilingues non validées dans le registre pour {nid}")
            if not fr_primary:
                ctx.report.error("WDV-BIL-003", f"Occurrence primaire dérivée absente pour {nid}")
    # Debate pair.
    debate = registry.get("debate") or {}
    if strict:
        en_debate = ((debate.get("pages") or {}).get("en") or {})
        if en_debate.get("title_status") != "locked" or not en_debate.get("canonical_title"):
            ctx.report.error("WDV-BIL-001", "Titre canonique anglais de la page Debate non verrouillé")
    ctx.report.metrics["bilingual"] = {"active_nodes": len(nodes), "strict": strict}
