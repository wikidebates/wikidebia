from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .graph import state_at_least
from .package import PackageContext
from .translation import english_translation_deferred


@dataclass
class Template:
    name: str
    params: list[tuple[str, str]]
    raw: str

    def values(self, name: str) -> list[str]:
        return [v for k, v in self.params if k == name]

    def one(self, name: str) -> str | None:
        vals = self.values(name)
        return vals[0] if vals else None


class WikiParseError(ValueError):
    pass


def _extract_outer(text: str) -> str:
    stripped = text.strip()
    if not stripped.startswith("{{"):
        raise WikiParseError("Le fichier ne commence pas par un modèle")
    depth = 0
    end = None
    i = 0
    while i < len(stripped) - 1:
        pair = stripped[i:i+2]
        if pair == "{{":
            depth += 1
            i += 2
            continue
        if pair == "}}":
            depth -= 1
            i += 2
            if depth == 0:
                end = i
                break
            if depth < 0:
                raise WikiParseError("Fermeture de modèle surnuméraire")
            continue
        i += 1
    if end is None or depth != 0:
        raise WikiParseError("Modèle non fermé")
    if stripped[end:].strip():
        raise WikiParseError("Texte extérieur au modèle principal")
    return stripped[:end]


def _split_top_level(content: str) -> list[str]:
    parts: list[str] = []
    start = 0
    brace_depth = 0
    link_depth = 0
    external_link_depth = 0
    i = 0
    while i < len(content):
        pair = content[i:i+2]
        if pair == "{{":
            brace_depth += 1; i += 2; continue
        if pair == "}}":
            brace_depth -= 1; i += 2; continue
        if pair == "[[":
            link_depth += 1; i += 2; continue
        if pair == "]]":
            link_depth = max(0, link_depth - 1); i += 2; continue
        if content[i] == "[" and link_depth == 0:
            external_link_depth += 1; i += 1; continue
        if content[i] == "]" and link_depth == 0 and external_link_depth:
            external_link_depth -= 1; i += 1; continue
        if content[i] == "|" and brace_depth == 0 and link_depth == 0 and external_link_depth == 0:
            # A parameter delimiter must be followed by a plausible name and '='.
            # This avoids treating ordinary pipes in prose, URLs or tables as parameters.
            tail = content[i + 1:]
            match = re.match(r"[ 	]*([^=|{}\n]+?)=", tail)
            if match:
                parts.append(content[start:i]); start = i + 1
        i += 1
    parts.append(content[start:])
    return parts


def parse_template(text: str) -> Template:
    raw = _extract_outer(text)
    inner = raw[2:-2]
    parts = _split_top_level(inner)
    name = parts[0].strip()
    if not name:
        raise WikiParseError("Nom de modèle vide")
    params: list[tuple[str, str]] = []
    for part in parts[1:]:
        if "=" not in part:
            raise WikiParseError(f"Paramètre sans signe égal : {part[:80]!r}")
        key, value = part.split("=", 1)
        key = key.strip()
        if not key:
            raise WikiParseError("Nom de paramètre vide")
        params.append((key, value.strip()))
    return Template(name, params, raw)


def parse_template_sequence(value: str) -> list[Template]:
    templates: list[Template] = []
    i = 0
    while i < len(value):
        while i < len(value) and value[i].isspace():
            i += 1
        if i >= len(value):
            break
        if value[i:i+2] != "{{":
            raise WikiParseError("Contenu non-modèle inattendu dans une séquence de sous-modèles")
        depth = 0
        start = i
        while i < len(value) - 1:
            pair = value[i:i+2]
            if pair == "{{": depth += 1; i += 2; continue
            if pair == "}}":
                depth -= 1; i += 2
                if depth == 0:
                    templates.append(parse_template(value[start:i]))
                    break
                continue
            i += 1
        else:
            raise WikiParseError("Sous-modèle non fermé")
    return templates


TOP_LEGACY = {
    ("fr", "debate"): {
        "model": "Débat",
        "order": ["sujet", "sujet-complet", "avancement", "avertissements-titre", "avertissements-débat", "introduction", "articles-Wikipédia", "arguments-pour", "arguments-contre", "avertissements-bibliographie", "bibliographie-pour", "bibliographie-contre", "bibliographie-ni-pour-ni-contre", "avertissements-sitographie", "sitographie-pour", "sitographie-contre", "sitographie-ni-pour-ni-contre", "avertissements-vidéographie", "vidéographie-pour", "vidéographie-contre", "vidéographie-ni-pour-ni-contre", "débats-connexes", "rubriques", "mots-clés", "interlangue", "date-création"],
        "required": ["sujet", "sujet-complet", "avancement", "avertissements-débat", "introduction", "arguments-pour", "arguments-contre", "rubriques", "mots-clés", "date-création"],
        "fixed": {"avancement": "Débat construit", "avertissements-débat": "Débat généré par IA"},
        "forbidden_generated": ["avertissements-titre", "avertissements-bibliographie", "avertissements-sitographie", "avertissements-vidéographie"],
    },
    ("en", "debate"): {
        "model": "Debate",
        "order": ["type", "topic", "progress", "title-warnings", "debate-warnings", "introduction", "wikipedia-articles", "pro-arguments", "con-arguments", "pro-bibliography", "con-bibliography", "bibliography", "pro-webliography", "con-webliography", "webliography", "pro-videography", "con-videography", "videography", "related-debates", "sections", "keywords", "creation-date"],
        "required": ["type", "topic", "progress", "debate-warnings", "introduction", "pro-arguments", "con-arguments", "sections", "keywords", "creation-date"],
        "fixed": {"progress": "Constructed debate", "debate-warnings": "Debate generated by AI"},
        "forbidden_generated": ["title-warnings"],
    },
    ("fr", "argument"): {
        "model": "Argument",
        "order": ["initialisation", "nom", "avertissements-titre", "avertissements-argument", "avertissements-résumé", "résumé", "citations", "avertissements-références", "références-bibliographiques", "références-sitographiques", "références-vidéographiques", "avertissements-justifications", "justifications", "avertissements-objections", "objections", "débat-détaillé", "rubriques", "mots-clés", "interlangue", "date-création"],
        "required": ["avertissements-argument", "résumé", "rubriques", "mots-clés", "date-création"],
        "fixed": {"avertissements-argument": "Argument généré par IA"},
        "forbidden_generated": ["initialisation", "nom", "avertissements-titre", "avertissements-résumé", "citations", "avertissements-références", "avertissements-justifications", "avertissements-objections", "débat-détaillé"],
    },
    ("en", "argument"): {
        "model": "Argument",
        "order": ["initialization", "name", "title-warnings", "argument-warnings", "summary-warnings", "summary", "quotes", "reference-warnings", "bibliography", "webliography", "videography", "justification-warnings", "justifications", "objection-warnings", "objections", "detailed-debate", "sections", "keywords", "creation-date"],
        "required": ["argument-warnings", "summary", "sections", "keywords", "creation-date"],
        "fixed": {"argument-warnings": "Argument generated by AI"},
        "forbidden_generated": ["initialization", "name", "title-warnings", "summary-warnings", "quotes", "reference-warnings", "justification-warnings", "objection-warnings", "detailed-debate"],
    },
}

TOP = {
    ("fr", "debate"): {
        "model": "Débat",
        "order": ["sujet", "sujet-complet", "avancement", "avertissements-titre", "avertissements-débat", "introduction", "articles-Wikipédia", "arguments-pour", "arguments-contre", "avertissements-bibliographie", "bibliographie-pour", "bibliographie-contre", "bibliographie-ni-pour-ni-contre", "avertissements-sitographie", "sitographie-pour", "sitographie-contre", "sitographie-ni-pour-ni-contre", "avertissements-vidéographie", "vidéographie-pour", "vidéographie-contre", "vidéographie-ni-pour-ni-contre", "débats-connexes", "rubriques", "mots-clés", "interlangue", "date-création"],
        "required": ["sujet", "sujet-complet", "avancement", "avertissements-débat", "introduction", "arguments-pour", "arguments-contre", "rubriques", "mots-clés", "date-création"],
        "fixed": {"avancement": "Débat construit", "avertissements-débat": "Débat généré par IA"},
        "forbidden_generated": ["avertissements-titre", "avertissements-bibliographie", "avertissements-sitographie", "avertissements-vidéographie"],
    },
    ("en", "debate"): {
        "model": "Debate",
        "order": ["topic", "complete-topic", "progress", "title-warnings", "debate-warnings", "introduction", "wikipedia-articles", "pro-arguments", "con-arguments", "pro-bibliography", "con-bibliography", "bibliography", "pro-webliography", "con-webliography", "webliography", "pro-videography", "con-videography", "videography", "related-debates", "sections", "keywords", "creation-date"],
        "required": ["topic", "complete-topic", "progress", "debate-warnings", "introduction", "pro-arguments", "con-arguments", "sections", "keywords", "creation-date"],
        "fixed": {"progress": "Constructed debate", "debate-warnings": "Debate generated by AI"},
        "forbidden_generated": ["title-warnings"],
    },
    ("fr", "argument"): {
        "model": "Argument",
        "order": ["initialisation", "nom", "avertissements-titre", "avertissements-argument", "avertissements-résumé", "résumé", "citations", "avertissements-références", "références-bibliographiques", "références-sitographiques", "références-vidéographiques", "avertissements-justifications", "justifications", "avertissements-objections", "objections", "débat-détaillé", "rubriques", "mots-clés", "interlangue", "date-création"],
        "required": ["avertissements-argument", "résumé", "rubriques", "mots-clés", "date-création"],
        "fixed": {"avertissements-argument": "Argument généré par IA"},
        "forbidden_generated": ["initialisation", "nom", "avertissements-titre", "avertissements-résumé", "citations", "avertissements-références", "avertissements-justifications", "avertissements-objections", "débat-détaillé"],
    },
    ("en", "argument"): {
        "model": "Argument",
        "order": ["initialization", "name", "title-warnings", "argument-warnings", "summary-warnings", "summary", "quotes", "reference-warnings", "bibliography", "webliography", "videography", "justification-warnings", "justifications", "objection-warnings", "objections", "detailed-debate", "sections", "keywords", "creation-date"],
        "required": ["argument-warnings", "summary", "sections", "keywords", "creation-date"],
        "fixed": {"argument-warnings": "Argument generated by AI"},
        "forbidden_generated": ["initialization", "name", "title-warnings", "summary-warnings", "quotes", "reference-warnings", "justification-warnings", "objection-warnings", "detailed-debate"],
    },
}

SUB = {
    "Sous-partie": (["titre", "contenu", "avertissements"], ["titre", "contenu"]),
    "Subsection": (["title", "content", "warnings"], ["title", "content"]),
    "Article Wikipédia": (["page"], ["page"]), "Wikipedia article": (["page"], ["page"]),
    "Argument pour": (["page", "titre-affiché", "avertissements"], ["page", "titre-affiché"]),
    "Argument contre": (["page", "titre-affiché", "avertissements"], ["page", "titre-affiché"]),
    "Pro argument": (["page", "displayed-title", "warnings"], ["page", "displayed-title"]),
    "Con argument": (["page", "displayed-title", "warnings"], ["page", "displayed-title"]),
    "Justification": (["page", "titre-affiché", "displayed-title", "avertissements", "warnings"], ["page"]),
    "Objection": (["page", "titre-affiché", "displayed-title", "avertissements", "warnings"], ["page"]),
    "Interlangue": (["langue", "page"], ["langue", "page"]),
    "Lien interlangue": (["langue", "page"], ["langue", "page"]),
    "Débat connexe": (["page"], ["page"]), "Related debate": (["page"], ["page"]),
    "Référence bibliographique": (["auteurs", "article", "ouvrage", "volume", "numéro", "localisation", "page", "édition", "lieu", "date", "lien", "avertissements"], ["auteurs"]),
    "Référence bibliographique pour": (["auteurs", "article", "ouvrage", "volume", "numéro", "localisation", "page", "édition", "lieu", "date", "lien", "avertissements"], ["auteurs"]),
    "Référence bibliographique contre": (["auteurs", "article", "ouvrage", "volume", "numéro", "localisation", "page", "édition", "lieu", "date", "lien", "avertissements"], ["auteurs"]),
    "Bibliographical reference": (["authors", "article", "work", "volume", "issue", "location", "page", "publisher", "place", "date", "link", "warnings"], ["authors"]),
    "Pro bibliographical reference": (["authors", "article", "work", "volume", "issue", "location", "page", "publisher", "place", "date", "link", "warnings"], ["authors"]),
    "Con bibliographical reference": (["authors", "article", "work", "volume", "issue", "location", "page", "publisher", "place", "date", "link", "warnings"], ["authors"]),
    "Référence sitographique": (["lien", "page", "auteurs", "site", "date", "avertissements"], ["lien", "site"]),
    "Référence sitographique pour": (["lien", "page", "auteurs", "site", "date", "avertissements"], ["lien", "site"]),
    "Référence sitographique contre": (["lien", "page", "auteurs", "site", "date", "avertissements"], ["lien", "site"]),
    "Web reference": (["link", "page", "authors", "site", "date", "warnings"], ["link", "site"]),
    "Pro web reference": (["link", "page", "authors", "site", "date", "warnings"], ["link", "site"]),
    "Con web reference": (["link", "page", "authors", "site", "date", "warnings"], ["link", "site"]),
    "Référence vidéographique": (["titre", "auteurs", "lien", "avertissements"], ["titre", "lien"]),
    "Référence vidéographique pour": (["titre", "auteurs", "lien", "avertissements"], ["titre", "lien"]),
    "Référence vidéographique contre": (["titre", "auteurs", "lien", "avertissements"], ["titre", "lien"]),
    "Video reference": (["title", "authors", "link", "warnings"], ["title", "link"]),
    "Pro video reference": (["title", "authors", "link", "warnings"], ["title", "link"]),
    "Con video reference": (["title", "authors", "link", "warnings"], ["title", "link"]),
    # Citation parameters are checked against the sealed bilingual locks.  Quote
    # accepts the historical French aliases for backward validation only; from
    # norm 1.2.30 onward WDV-MWK-021 requires the English parameter contract.
    "Citation": ([], ["citation"]),
    "Quote": ([
        "quote", "authors", "article", "work", "volume", "issue", "page", "location", "publisher", "place", "date", "link", "warnings",
        "citation", "auteurs", "ouvrage", "numéro", "localisation", "édition", "lieu", "lien", "avertissements-citation", "avertissements",
    ], []),
}

SEQUENCE_PARAMS = {
    "introduction", "articles-Wikipédia", "arguments-pour", "arguments-contre", "bibliographie-pour", "bibliographie-contre", "bibliographie-ni-pour-ni-contre", "sitographie-pour", "sitographie-contre", "sitographie-ni-pour-ni-contre", "vidéographie-pour", "vidéographie-contre", "vidéographie-ni-pour-ni-contre", "débats-connexes",
    "wikipedia-articles", "pro-arguments", "con-arguments", "pro-bibliography", "con-bibliography", "bibliography", "pro-webliography", "con-webliography", "webliography", "pro-videography", "con-videography", "videography", "related-debates",
    "références-bibliographiques", "références-sitographiques", "références-vidéographiques", "justifications", "objections", "interlangue",
    "citations", "quotes",
}

PARAM_TEMPLATE_ALLOWED = {
    "introduction": {"Sous-partie", "Subsection"},
    "articles-Wikipédia": {"Article Wikipédia"}, "wikipedia-articles": {"Wikipedia article"},
    "arguments-pour": {"Argument pour"}, "arguments-contre": {"Argument contre"},
    "pro-arguments": {"Pro argument"}, "con-arguments": {"Con argument"},
    "bibliographie-pour": {"Référence bibliographique pour"}, "bibliographie-contre": {"Référence bibliographique contre"},
    "bibliographie-ni-pour-ni-contre": {"Référence bibliographique"},
    "pro-bibliography": {"Pro bibliographical reference"}, "con-bibliography": {"Con bibliographical reference"}, "bibliography": {"Bibliographical reference"},
    "sitographie-pour": {"Référence sitographique pour"}, "sitographie-contre": {"Référence sitographique contre"},
    "sitographie-ni-pour-ni-contre": {"Référence sitographique"},
    "pro-webliography": {"Pro web reference"}, "con-webliography": {"Con web reference"}, "webliography": {"Web reference"},
    "vidéographie-pour": {"Référence vidéographique pour"}, "vidéographie-contre": {"Référence vidéographique contre"},
    "vidéographie-ni-pour-ni-contre": {"Référence vidéographique"},
    "pro-videography": {"Pro video reference"}, "con-videography": {"Con video reference"}, "videography": {"Video reference"},
    "débats-connexes": {"Débat connexe"}, "related-debates": {"Related debate"},
    "références-bibliographiques": {"Référence bibliographique"},
    "références-sitographiques": {"Référence sitographique"},
    "références-vidéographiques": {"Référence vidéographique"},
    "justifications": {"Justification"}, "objections": {"Objection"},
    "citations": {"Citation"}, "quotes": {"Quote"},
    "interlangue": {"Interlangue", "Lien interlangue"},
}

FR_SECTIONS = ["Aménagement", "Culture", "Droit", "Écologie", "Économie", "Éducation", "Éthique", "Géopolitique", "Histoire", "Philosophie", "Politique", "Psychologie", "Religion et spiritualité", "Santé", "Science", "Société", "Sport et loisirs", "Technologie"]
EN_SECTIONS = ["Planning", "Culture", "Law", "Ecology", "Economy", "Education", "Ethics", "Geopolitics", "History", "Philosophy", "Politics", "Psychology", "Religion and spirituality", "Health", "Science", "Society", "Sport and leisure", "Technology"]


EN_MONTHS = {
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
}
FR_MONTHS = {
    "janvier", "février", "mars", "avril", "mai", "juin",
    "juillet", "août", "septembre", "octobre", "novembre", "décembre",
}
EN_PLACES_EXPECTED_FR = {
    "London": "Londres", "Brussels": "Bruxelles", "Geneva": "Genève",
    "Copenhagen": "Copenhague", "The Hague": "La Haye",
}
FR_PLACES_EXPECTED_EN = {value: key for key, value in EN_PLACES_EXPECTED_FR.items()}


MACHINE_DOCUMENTARY_DATE_RE = re.compile(r"^\d{4}-\d{2}(?:-\d{2})?(?:[T ]\d{2}:\d{2}(?::\d{2})?(?:Z|[+-]\d{2}:?\d{2})?)?$")


def documentary_date_is_machine(value: str) -> bool:
    """Return True for ISO-like documentary dates; bare years remain valid."""
    return bool(MACHINE_DOCUMENTARY_DATE_RE.fullmatch(value.strip()))


def explicit_parenthetical_acronym(value: str) -> str | None:
    match = re.search(r"\(([A-ZÀ-ÖØ-Þ][A-ZÀ-ÖØ-Þ0-9.-]{1,9})\)", value)
    return match.group(1) if match else None


def _check_reference_language_and_typography(ctx: PackageContext, tmpl: Template, rel: str, lang: str) -> None:
    """Apply active 1.0.6 language-sensitive documentary rules."""
    if lang == "fr":
        # A French reference call belongs before final punctuation: texte<ref>...</ref>.
        for match in re.finditer(r"[.!?;:]\s*<ref(?:\s|>)", tmpl.raw, flags=re.IGNORECASE):
            ctx.report.error(
                "WDV-MWK-014",
                "Dans le texte français, l'appel de référence doit précéder le signe de ponctuation final",
                path=rel,
                details={"offset": match.start()},
            )
    for key, value in tmpl.params:
        if key not in SEQUENCE_PARAMS:
            continue
        try:
            subs = parse_template_sequence(value)
        except WikiParseError:
            continue
        for sub in subs:
            date_value = sub.one("date") or ""
            place_value = sub.one("lieu" if lang == "fr" else "place") or ""
            if lang == "fr":
                foreign_months = sorted(month for month in EN_MONTHS if re.search(rf"\b{re.escape(month)}\b", date_value))
                if foreign_months:
                    ctx.report.error(
                        "WDV-MWK-014",
                        "Date descriptive anglaise dans une page française",
                        path=rel,
                        details={"template": sub.name, "date": date_value, "months": foreign_months},
                    )
                if place_value in EN_PLACES_EXPECTED_FR:
                    ctx.report.error(
                        "WDV-MWK-014",
                        "Nom de lieu non adapté au français",
                        path=rel,
                        details={"actual": place_value, "expected": EN_PLACES_EXPECTED_FR[place_value]},
                    )
            else:
                foreign_months = sorted(month for month in FR_MONTHS if re.search(rf"\b{re.escape(month)}\b", date_value, flags=re.IGNORECASE))
                if foreign_months:
                    ctx.report.error(
                        "WDV-MWK-014",
                        "Date descriptive française dans une page anglaise",
                        path=rel,
                        details={"template": sub.name, "date": date_value, "months": foreign_months},
                    )
                if place_value in FR_PLACES_EXPECTED_EN:
                    ctx.report.error(
                        "WDV-MWK-014",
                        "Nom de lieu non adapté à l'anglais",
                        path=rel,
                        details={"actual": place_value, "expected": FR_PLACES_EXPECTED_EN[place_value]},
                    )


def split_list(value: str) -> list[str]:
    return [x.strip() for x in value.split(",") if x.strip()]


def _consolidated_norm(ctx: PackageContext) -> str | None:
    return ((ctx.manifest() or {}).get("normative_versions") or {}).get("consolidated_norm")


def _norm_tuple(value: str | None) -> tuple[int, ...]:
    try:
        return tuple(int(part) for part in str(value or "").split("."))
    except ValueError:
        return ()


def _norm_at_least(ctx: PackageContext, minimum: str) -> bool:
    current = _norm_tuple(_consolidated_norm(ctx))
    target = _norm_tuple(minimum)
    return bool(current and target and current >= target)


def _is_norm_120(ctx: PackageContext) -> bool:
    return _norm_at_least(ctx, "1.2.0")


def _is_norm_126(ctx: PackageContext) -> bool:
    return _norm_at_least(ctx, "1.2.6")


def _is_norm_1217(ctx: PackageContext) -> bool:
    return _norm_at_least(ctx, "1.2.17")


def _is_norm_1218(ctx: PackageContext) -> bool:
    return _norm_at_least(ctx, "1.2.18")


def _alphabetical_key(value: str) -> str:
    folded = unicodedata.normalize("NFKD", value.casefold())
    return "".join(c for c in folded if not unicodedata.combining(c))


def alphabetically_sorted(values: list[str]) -> list[str]:
    return sorted(values, key=_alphabetical_key)


def _first_alpha_is_upper(value: str) -> bool:
    first = next((c for c in value.strip() if c.isalpha()), "")
    return bool(first and first.isupper())


def _first_alpha_is_lower(value: str) -> bool:
    first = next((c for c in value.strip() if c.isalpha()), "")
    return bool(first and first.islower())


def _complete_topic_looks_interrogative(value: str, lang: str) -> bool:
    clean = value.strip()
    if not clean or "?" in clean:
        return True
    if lang == "fr":
        return bool(re.match(r"^(?:si\b|faut[- ]?il\b|est[- ]?ce\s+que\b|doit[- ]?on\b|peut[- ]?on\b)", clean, flags=re.I))
    return bool(re.match(r"^(?:whether\b|if\b|should\b|can\b|could\b|is\b|are\b|do\b|does\b|must\b)", clean, flags=re.I))


SPLIT_ADJACENT_TEMPLATES_RE = re.compile(r"}}[ \t\r\n]+\{\{")


def split_adjacent_templates(text: str) -> list[re.Match[str]]:
    """Return forbidden whitespace-separated adjacent template boundaries."""
    return list(SPLIT_ADJACENT_TEMPLATES_RE.finditer(text))


PROTECTED_PAGE_PARAMETERS = {
    ("fr", "debate"): ("avancement", "avertissements-débat", "débats-connexes"),
    ("en", "debate"): ("progress", "debate-warnings", "related-debates"),
    ("fr", "argument"): ("avertissements-argument",),
    ("en", "argument"): ("argument-warnings",),
}


def _summary_policy_1240(ctx: PackageContext) -> bool:
    manifest = ctx.manifest() or {}
    controls = manifest.get("editorial_controls") or {}
    norm = ((manifest.get("normative_versions") or {}).get("consolidated_norm"))
    return controls.get("summary_policy_revision") == "1.2.40" or norm == "1.2.40"


def _summary_provenance_map(ctx: PackageContext) -> dict[tuple[str, str], str]:
    cached = getattr(ctx, "_summary_provenance_map_cache", None)
    if isinstance(cached, dict):
        return cached
    result: dict[tuple[str, str], str] = {}
    manifest = ctx.manifest() or {}
    cfg = ((manifest.get("editorial_controls") or {}).get("legacy_content_preservation") or {})
    rel = cfg.get("lock_path")
    if isinstance(rel, str) and ctx.exists(rel):
        lock = ctx.load_json(rel)
        if isinstance(lock, dict):
            for entry in lock.get("arguments") or []:
                if not isinstance(entry, dict):
                    continue
                node_id, language = entry.get("id"), entry.get("language")
                provenance = entry.get("summary_provenance")
                if isinstance(node_id, str) and language in {"fr", "en"} and isinstance(provenance, str):
                    result[(node_id, language)] = provenance
    setattr(ctx, "_summary_provenance_map_cache", result)
    return result


def _apply_page_lifecycle_contract(ctx: PackageContext, spec: dict[str, Any], tmpl: Template, lang: str, page_type: str, rel: str, page_manifest: dict[str, Any] | None) -> None:
    if not _norm_at_least(ctx, "1.2.33"):
        return
    if not isinstance(page_manifest, dict):
        ctx.report.error("WDV-MWK-023", "Manifeste de page absent pour le contrôle création/modification", path=rel)
        return
    origin = page_manifest.get("page_origin")
    preserved = page_manifest.get("preserved_parameters")
    protected = PROTECTED_PAGE_PARAMETERS[(lang, page_type)]
    if origin not in {"new", "preexisting"} or not isinstance(preserved, dict):
        ctx.report.error("WDV-MWK-023", "Origine ou paramètres préservés absents du manifeste de page", path=rel)
        return
    if origin == "new":
        if preserved:
            ctx.report.error("WDV-MWK-023", "Une page nouvelle ne doit pas déclarer de paramètres préservés", path=rel)
        if page_type == "debate":
            related = "débats-connexes" if lang == "fr" else "related-debates"
            if related not in spec["forbidden_generated"]:
                spec["forbidden_generated"].append(related)
        return
    for name in protected:
        if name in spec["required"]:
            spec["required"].remove(name)
        spec["fixed"].pop(name, None)
        if name in spec["forbidden_generated"]:
            spec["forbidden_generated"].remove(name)
    if set(preserved) != set(protected):
        ctx.report.error("WDV-MWK-023", "L’état antérieur des paramètres protégés est incomplet", path=rel, details={"expected": list(protected), "actual": sorted(preserved)})
        return
    for name in protected:
        state = preserved.get(name)
        if not isinstance(state, dict) or not isinstance(state.get("present"), bool):
            ctx.report.error("WDV-MWK-023", f"État antérieur invalide pour {name}", path=rel)
            continue
        actual = tmpl.one(name)
        if state["present"]:
            expected = state.get("value")
            if not isinstance(expected, str) or not expected.strip() or actual != expected:
                ctx.report.error("WDV-MWK-023", f"Le paramètre existant {name} n’a pas été préservé exactement", path=rel, details={"expected": expected, "actual": actual})
        elif actual is not None:
            ctx.report.error("WDV-MWK-023", f"Le paramètre {name} a été ajouté à une page existante alors qu’il était absent", path=rel, details={"actual": actual})


def validate_template_shape(ctx: PackageContext, tmpl: Template, lang: str, page_type: str, rel: str, page_manifest: dict[str, Any] | None = None) -> None:
    base_spec = TOP[(lang, page_type)] if _is_norm_120(ctx) else TOP_LEGACY[(lang, page_type)]
    spec = {**base_spec, "order": list(base_spec["order"]), "required": list(base_spec["required"]), "forbidden_generated": list(base_spec["forbidden_generated"])}
    spec["fixed"] = dict(base_spec["fixed"])
    if _norm_at_least(ctx, "1.2.27") and page_type == "argument":
        citation_parameter = "citations" if lang == "fr" else "quotes"
        if citation_parameter in spec["forbidden_generated"]:
            spec["forbidden_generated"].remove(citation_parameter)
    preservation = (((ctx.manifest() or {}).get("editorial_controls") or {}).get("legacy_content_preservation") or {})
    protected_fields = set(preservation.get("protected_fields") or [])
    if preservation.get("enabled") is True and page_type == "argument":
        init_parameter = "initialisation" if lang == "fr" else "initialization"
        if init_parameter in protected_fields and init_parameter in spec["forbidden_generated"]:
            spec["forbidden_generated"].remove(init_parameter)
    if _is_norm_1217(ctx) and not _norm_at_least(ctx, "1.2.33") and page_type == "debate":
        wikipedia_parameter = "articles-Wikipédia" if lang == "fr" else "wikipedia-articles"
        related_parameter = "débats-connexes" if lang == "fr" else "related-debates"
        if wikipedia_parameter not in spec["required"]:
            spec["required"].append(wikipedia_parameter)
        if related_parameter not in spec["forbidden_generated"]:
            spec["forbidden_generated"].append(related_parameter)
    _apply_page_lifecycle_contract(ctx, spec, tmpl, lang, page_type, rel, page_manifest)
    summary_provenance = None
    summary_parameter = "résumé" if lang == "fr" else "summary"
    if _summary_policy_1240(ctx) and page_type == "argument":
        page_id = page_manifest.get("page_id") if isinstance(page_manifest, dict) else None
        if isinstance(page_id, str):
            summary_provenance = _summary_provenance_map(ctx).get((page_id, lang))
        if summary_provenance in {"absent_at_import", "new_page_unwritten"}:
            if summary_parameter in spec["required"]:
                spec["required"].remove(summary_parameter)
        elif summary_provenance in {"historical_existing", "authored_after_import"}:
            if summary_parameter not in spec["required"]:
                spec["required"].append(summary_parameter)
        else:
            ctx.report.error(
                "WDV-EDT-028",
                "État de rédaction du résumé absent ou invalide pour la politique 1.2.40",
                path=rel,
                details={"page_id": page_id, "language": lang, "summary_provenance": summary_provenance},
            )
    if tmpl.name != spec["model"]:
        ctx.report.error("WDV-MWK-002", f"Modèle principal attendu {spec['model']}, trouvé {tmpl.name}", path=rel)
    keys = [k for k, _ in tmpl.params]
    if summary_provenance in {"absent_at_import", "new_page_unwritten"} and summary_parameter in keys:
        ctx.report.error(
            "WDV-EDT-028",
            "Un résumé non rédigé doit être absent, et non remplacé par un texte généré ou un paramètre vide",
            path=rel,
            details={"summary_provenance": summary_provenance},
        )
    for dup, n in Counter(keys).items():
        if n > 1:
            ctx.report.error("WDV-MWK-003", f"Paramètre dupliqué : {dup}", path=rel)
    allowed = spec["order"]
    for key in keys:
        if key not in allowed:
            ctx.report.error("WDV-MWK-003", f"Paramètre inconnu : {key}", path=rel)
    for key in spec["forbidden_generated"]:
        if key in keys:
            ctx.report.error("WDV-MWK-003", f"Paramètre autorisé par la structure mais interdit dans une sortie générée : {key}", path=rel)
    for key in spec["required"]:
        if key not in keys:
            ctx.report.error("WDV-MWK-004", f"Paramètre obligatoire absent : {key}", path=rel)
    for key, value in tmpl.params:
        if not value.strip():
            ctx.report.error("WDV-MWK-005", f"Paramètre vide interdit : {key}", path=rel)
    positions = [allowed.index(k) for k in keys if k in allowed]
    if positions != sorted(positions):
        ctx.report.error("WDV-MWK-006", "Ordre relatif des paramètres incorrect", path=rel, details={"parameters": keys})
    for key, expected in spec["fixed"].items():
        actual = tmpl.one(key)
        if actual is not None and actual != expected:
            ctx.report.error("WDV-MWK-007", f"Valeur fixe incorrecte pour {key}", path=rel, details={"expected": expected, "actual": actual})

    if _is_norm_126(ctx):
        section_param = "rubriques" if lang == "fr" else "sections"
        values = split_list(tmpl.one(section_param) or "")
        expected_values = alphabetically_sorted(values)
        if values and values != expected_values:
            ctx.report.error("WDV-MWK-016", f"{section_param} doit être rangé par ordre alphabétique", path=rel, details={"actual": values, "expected": expected_values})
        if page_type == "debate":
            topic_param = "sujet" if lang == "fr" else "topic"
            topic = tmpl.one(topic_param) or ""
            if not _first_alpha_is_upper(topic):
                ctx.report.error("WDV-MWK-017", f"{topic_param} doit commencer par une majuscule", path=rel, details={"actual": topic})
            complete_param = "sujet-complet" if lang == "fr" else "complete-topic"
            complete = tmpl.one(complete_param) or ""
            if _complete_topic_looks_interrogative(complete, lang):
                ctx.report.error("WDV-EDT-018", f"{complete_param} doit compléter l’en-tête de la page sous une forme non interrogative", path=rel, details={"actual": complete})
            if _norm_at_least(ctx, "1.2.23") and not _first_alpha_is_lower(complete):
                ctx.report.error(
                    "WDV-EDT-018",
                    f"{complete_param} doit normalement commencer par une minuscule dans les deux langues",
                    path=rel,
                    details={"actual": complete, "exception_policy": "reformuler avec un déterminant ou justifier un nom propre/acronyme inévitable dans la revue"},
                )
            declared_acronym = explicit_parenthetical_acronym(topic)
            if _norm_at_least(ctx, "1.2.9") and declared_acronym and not re.search(rf"(?<![\w.-]){re.escape(declared_acronym)}(?![\w.-])", complete):
                ctx.report.error("WDV-EDT-018", f"{complete_param} doit employer l’acronyme courant déclaré dans {topic_param}", path=rel, details={"acronym": declared_acronym, "actual": complete})

    if _norm_at_least(ctx, "1.2.11"):
        matches = split_adjacent_templates(tmpl.raw)
        if matches:
            first = matches[0]
            line = tmpl.raw.count("\n", 0, first.start()) + 1
            ctx.report.error(
                "WDV-MWK-018",
                "Deux modèles MediaWiki adjacents doivent être accolés sous la forme }}{{",
                path=rel,
                details={"occurrences": len(matches), "first_line": line, "replacement": "}}{{"},
            )

    if _is_norm_120(ctx) and re.search(r"<references\b[^>]*(?:/\s*)?>", tmpl.raw, flags=re.IGNORECASE):
        ctx.report.error("WDV-EDT-010", "La balise <references /> est interdite par les normes 1.2.x", path=rel)

    for key, value in tmpl.params:
        if key not in SEQUENCE_PARAMS:
            continue
        try:
            subs = parse_template_sequence(value)
        except WikiParseError as exc:
            ctx.report.error("WDV-MWK-001", f"Sous-modèles invalides dans {key} : {exc}", path=rel)
            continue
        for sub in subs:
            if sub.name not in SUB:
                ctx.report.error("WDV-MWK-012", f"Sous-modèle inconnu : {sub.name}", path=rel)
                continue
            expected_models = PARAM_TEMPLATE_ALLOWED.get(key)
            if expected_models and sub.name not in expected_models:
                ctx.report.error("WDV-MWK-012", f"Sous-modèle {sub.name} interdit dans le paramètre {key}", path=rel, details={"expected": sorted(expected_models)})
            if _norm_at_least(ctx, "1.2.30"):
                if key == "introduction":
                    localized_model = "Sous-partie" if lang == "fr" else "Subsection"
                    if sub.name != localized_model:
                        ctx.report.error(
                            "WDV-MWK-022",
                            f"Le modèle {sub.name} ne correspond pas à la langue de la page",
                            path=rel,
                            details={"expected": localized_model},
                        )
                if sub.name in {"Justification", "Objection"}:
                    wrong_names = ({"displayed-title", "warnings"} if lang == "fr" else {"titre-affiché", "avertissements"})
                    found_wrong = sorted({name for name, _value in sub.params} & wrong_names)
                    if found_wrong:
                        ctx.report.error(
                            "WDV-MWK-022",
                            f"Paramètres de l’autre langue interdits dans {sub.name}",
                            path=rel,
                            details={"forbidden": found_wrong},
                        )
            order, required = SUB[sub.name]
            subkeys = [k for k, _ in sub.params]
            if len(subkeys) != len(set(subkeys)):
                ctx.report.error("WDV-MWK-012", f"Paramètre dupliqué dans {sub.name}", path=rel)
            dynamic_citation = sub.name in {"Citation", "Quote"} and _norm_at_least(ctx, "1.2.27")
            if not dynamic_citation:
                for skey in subkeys:
                    if skey not in order:
                        ctx.report.error("WDV-MWK-012", f"Paramètre inconnu {skey} dans {sub.name}", path=rel)
                indexes = [order.index(x) for x in subkeys if x in order]
                if indexes != sorted(indexes):
                    ctx.report.error("WDV-MWK-006", f"Ordre incorrect dans {sub.name}", path=rel)
            for req in ([] if dynamic_citation else required):
                if req not in subkeys or not (sub.one(req) or "").strip():
                    ctx.report.error("WDV-MWK-012", f"Paramètre obligatoire {req} absent ou vide dans {sub.name}", path=rel)
            for skey, sval in sub.params:
                if not sval.strip():
                    ctx.report.error("WDV-MWK-005", f"Sous-paramètre vide interdit : {sub.name}.{skey}", path=rel)
                if skey in {"avertissements", "warnings"}:
                    allowed_quote_warning = sub.name == "Quote" and skey == "warnings" and _norm_at_least(ctx, "1.2.30")
                    if not allowed_quote_warning:
                        ctx.report.error("WDV-MWK-003", f"Sous-paramètre d'avertissement interdit dans une sortie générée : {sub.name}.{skey}", path=rel)
                if _is_norm_1217(ctx) and skey in {"auteurs", "authors"}:
                    candidate = sval.strip()
                    parsed_json = None
                    if candidate.startswith("["):
                        try:
                            parsed_json = json.loads(candidate)
                        except json.JSONDecodeError:
                            parsed_json = None
                    if isinstance(parsed_json, list) or (candidate.startswith("[") and candidate.endswith("]")):
                        ctx.report.error(
                            "WDV-DOC-006",
                            "Le champ auteur MediaWiki ne doit pas contenir une sérialisation de tableau JSON",
                            path=rel,
                            details={
                                "template": sub.name,
                                "parameter": skey,
                                "actual": sval,
                                "conversion": "un élément -> texte brut ; plusieurs éléments -> valeurs séparées par ', ' ; liste vide -> paramètre omis",
                            },
                        )
                    if _is_norm_1218(ctx):
                        malformed_separator = (
                            ";" in candidate
                            or "，" in candidate
                            or bool(re.search(r"\s+,|,(?! )|, {2,}|,$", candidate))
                        )
                        if malformed_separator:
                            ctx.report.error(
                                "WDV-DOC-007",
                                "Plusieurs auteurs doivent être séparés exactement par une virgule suivie d’une espace",
                                path=rel,
                                details={
                                    "template": sub.name,
                                    "parameter": skey,
                                    "actual": sval,
                                    "expected_separator": ", ",
                                },
                            )
                if skey in {"numéro", "issue"} and not sval.isdigit():
                    ctx.report.error("WDV-MWK-012", f"{sub.name}.{skey} doit contenir uniquement des chiffres", path=rel)
                if skey in {"lien", "link"} and not re.match(r"^https?://", sval):
                    ctx.report.error("WDV-MWK-012", f"URL HTTP/HTTPS attendue dans {sub.name}.{skey}", path=rel)
                if skey == "page" and ("bibliographique" in sub.name.lower() or "bibliographical" in sub.name.lower()):
                    if not re.fullmatch(r"[0-9]+(?:-[0-9]+)?", sval):
                        ctx.report.error("WDV-DOC-002", f"Pagination bibliographique non normalisée dans {sub.name}.page", path=rel, details={"value": sval})
                if skey in {"localisation", "location"} and re.search(r"^(?:pages?|pp?\.)\s*[0-9]", sval, flags=re.I):
                    ctx.report.error("WDV-DOC-002", f"Pagination bibliographique placée dans {sub.name}.{skey} au lieu de page", path=rel, details={"value": sval})
                if skey == "date" and re.search(r"\b(?:consulté(?:e)?|accessed|retrieved)\b", sval, flags=re.I):
                    ctx.report.error("WDV-DOC-003", f"Date de consultation utilisée comme date documentaire dans {sub.name}", path=rel, details={"value": sval})
                if _norm_at_least(ctx, "1.2.9") and skey == "date" and documentary_date_is_machine(sval):
                    ctx.report.error("WDV-DOC-005", f"Date documentaire au format machine dans {sub.name}; utiliser une date en langage naturel", path=rel, details={"value": sval, "creation_date_parameters_unchanged": ["date-création", "creation-date"]})
            if _is_norm_120(ctx) and sub.name in {
                "Référence sitographique", "Référence sitographique pour", "Référence sitographique contre",
                "Web reference", "Pro web reference", "Con web reference",
            }:
                page_value = (sub.one("page") or "").strip().casefold()
                site_value = (sub.one("site") or "").strip().casefold()
                author_value = (sub.one("auteurs") or sub.one("authors") or "").strip().casefold()
                if page_value and site_value and page_value == site_value:
                    ctx.report.error("WDV-DOC-004", "Le titre de page sitographique duplique le nom du site et doit être omis", path=rel, details={"template": sub.name, "value": sub.one("page"), "page_type": page_type})
                if _norm_at_least(ctx, "1.2.23") and author_value and site_value and author_value == site_value:
                    ctx.report.error(
                        "WDV-DOC-004",
                        "Le champ auteur reproduit le nom du site : rechercher de nouveau la signature ou les crédits, puis omettre l’auteur si aucune responsabilité distincte n’est trouvée",
                        path=rel,
                        details={"template": sub.name, "value": sub.one("site"), "page_type": page_type, "applies_to_argument_pages": True},
                    )
                if author_value and page_value and site_value and author_value == page_value == site_value:
                    ctx.report.error("WDV-DOC-004", "Les champs auteur, page et site sont remplis mécaniquement avec la même valeur", path=rel, details={"template": sub.name, "value": sub.one("site"), "page_type": page_type})

            if sub.name in {"Justification", "Objection"}:
                expected_display = "titre-affiché" if lang == "fr" else "displayed-title"
                wrong_display = "displayed-title" if lang == "fr" else "titre-affiché"
                if not sub.one(expected_display):
                    ctx.report.error("WDV-MWK-012", f"{sub.name} doit contenir {expected_display}", path=rel)
                if sub.one(wrong_display) is not None:
                    ctx.report.error("WDV-MWK-012", f"{sub.name} mélange les paramètres français et anglais", path=rel)
            if sub.name.startswith("Référence bibliographique") and not (sub.one("article") or sub.one("ouvrage")):
                ctx.report.error("WDV-MWK-012", f"{sub.name} doit contenir article ou ouvrage", path=rel)
            if sub.name.endswith("bibliographical reference") or sub.name == "Bibliographical reference":
                if not (sub.one("article") or sub.one("work")):
                    ctx.report.error("WDV-MWK-012", f"{sub.name} doit contenir article ou work", path=rel)


def get_subs(tmpl: Template, param: str) -> list[Template]:
    value = tmpl.one(param)
    if not value:
        return []
    try:
        return parse_template_sequence(value)
    except WikiParseError:
        return []


def expected_relations(registry: dict[str, Any], node_id: str, lang: str, relation: str) -> list[tuple[str, str]]:
    nodes = {n.get("id"): n for n in registry.get("graph", {}).get("nodes", []) if n.get("status") == "active"}
    edges = [e for e in registry.get("graph", {}).get("edges", []) if e.get("status") == "active" and e.get("parent_node_id") == node_id and e.get("relation") == relation]
    edges.sort(key=lambda e: (e.get("order", 0), e.get("id", "")))
    out = []
    for e in edges:
        child = nodes.get(e.get("child_node_id"))
        if child:
            data = child.get(lang) or {}
            out.append((data.get("canonical_title"), data.get("displayed_title")))
    return out


def relation_pairs(subs: list[Template], lang: str) -> list[tuple[str | None, str | None]]:
    display = "titre-affiché" if lang == "fr" else "displayed-title"
    return [(s.one("page"), s.one(display)) for s in subs]


QUOTE_PARAMETER_MAP = {
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


def _quote_parameter_name(name: str) -> str | None:
    normalized = re.sub(r"[ _-]+", " ", str(name).strip().casefold())
    return QUOTE_PARAMETER_MAP.get(normalized)


def _parameter_pairs(rows: Any) -> list[tuple[str, str]]:
    if not isinstance(rows, list):
        return []
    out: list[tuple[str, str]] = []
    for row in rows:
        if not isinstance(row, dict):
            return []
        name = str(row.get("name") or "").strip()
        value = str(row.get("value") or "").strip()
        if not name or not value:
            return []
        out.append((name, value))
    return out


def _validate_citations_against_locks(
    ctx: PackageContext, tmpl: Template, rel: str, lang: str, page_id: str,
) -> None:
    if not _norm_at_least(ctx, "1.2.27"):
        return
    lock_path = "data/fr_content_lock.json" if lang == "fr" else "data/en_content_lock.json"
    lock = ctx.load_json(lock_path, required=True)
    if not isinstance(lock, dict):
        return
    argument = next((row for row in lock.get("arguments", []) if isinstance(row, dict) and row.get("id") == page_id), None)
    if argument is None:
        ctx.report.error("WDV-MWK-021", "Le verrou de contenu ne couvre pas cette page Argument", path=rel, details={"page_id": page_id, "lock": lock_path})
        return
    expected_rows = argument.get("citations") or []
    parameter = "citations" if lang == "fr" else "quotes"
    actual_templates = get_subs(tmpl, parameter)
    if len(actual_templates) != len(expected_rows):
        ctx.report.error("WDV-MWK-021", "Nombre de citations divergent du verrou éditorial", path=rel, details={"expected": len(expected_rows), "actual": len(actual_templates), "parameter": parameter})
        return
    for index, (actual, expected) in enumerate(zip(actual_templates, expected_rows), start=1):
        expected_model = "Citation" if lang == "fr" else "Quote"
        if actual.name != expected_model:
            ctx.report.error("WDV-MWK-021", f"Le modèle {expected_model} est obligatoire dans {parameter}", path=rel, pointer=f"{parameter}/{index}")
            continue
        expected_params = _parameter_pairs(expected.get("source_parameters") if lang == "fr" else expected.get("parameters"))
        actual_params = [(str(name).strip(), str(value).strip()) for name, value in actual.params]
        if actual_params != expected_params:
            ctx.report.error(
                "WDV-MWK-021",
                "Les paramètres de la citation divergent du verrou bilingue ; les noms doivent être anglais et seules les valeurs de quote et date peuvent être traduites",
                path=rel, pointer=f"{parameter}/{index}",
                details={"expected": expected_params, "actual": actual_params, "citation_id": expected.get("id")},
            )
        if lang == "en":
            current_contract = _norm_at_least(ctx, "1.2.30")
            warning_name = "warnings" if current_contract else "avertissements-citation"
            warning_values = [value for name, value in actual_params if name == warning_name]
            expected_warning = str(expected.get(warning_name) or "").strip()
            if warning_values != [expected_warning] or expected_warning.count("Citation traduite par IA") != 1:
                ctx.report.error(
                    "WDV-MWK-021",
                    "La citation anglaise doit contenir une unique mention 'Citation traduite par IA', ajoutée avec le séparateur ', ' après tout avertissement existant",
                    path=rel, pointer=f"{parameter}/{index}",
                    details={"expected": expected_warning, "actual": warning_values, "parameter": warning_name},
                )
            source = expected.get("source") or {}
            source_params = _parameter_pairs(source.get("source_parameters"))
            if current_contract:
                mapped_source: list[tuple[str, str]] = []
                unmapped: list[str] = []
                for source_name, source_value in source_params:
                    mapped_name = _quote_parameter_name(source_name)
                    if mapped_name is None:
                        unmapped.append(source_name)
                        continue
                    if mapped_name not in {"quote", "date", "warnings"}:
                        mapped_source.append((mapped_name, source_value))
                if unmapped:
                    ctx.report.error(
                        "WDV-MWK-021",
                        "Un paramètre français de Citation ne possède pas d’équivalent anglais déclaré",
                        path=rel, pointer=f"{parameter}/{index}", details={"unmapped": unmapped},
                    )
                preserved_actual = [(name, value) for name, value in actual_params if name not in {"quote", "date", "warnings"}]
                if preserved_actual != mapped_source:
                    ctx.report.error(
                        "WDV-MWK-021",
                        "La valeur d’un paramètre documentaire de Quote a été modifiée ou son nom n’a pas été traduit en anglais",
                        path=rel, pointer=f"{parameter}/{index}",
                        details={"expected_preserved": mapped_source, "actual_preserved": preserved_actual},
                    )
            else:
                preserved_source = [(name, value) for name, value in source_params if name not in {"citation", "date", "avertissements-citation"}]
                preserved_actual = [(name, value) for name, value in actual_params if name not in {"citation", "date", "avertissements-citation"}]
                if preserved_actual != preserved_source:
                    ctx.report.error(
                        "WDV-MWK-021",
                        "Un paramètre documentaire de la citation a été traduit ou modifié",
                        path=rel, pointer=f"{parameter}/{index}",
                        details={"expected_preserved": preserved_source, "actual_preserved": preserved_actual},
                    )


def _validate_argument_content(ctx: PackageContext, tmpl: Template, rel: str, lang: str, page_id: str, registry: dict[str, Any], page_manifest: dict[str, Any]) -> None:
    node = next((n for n in registry.get("graph", {}).get("nodes", []) if n.get("id") == page_id), None)
    if not node:
        ctx.report.error("WDV-GRA-003", f"Fichier de page pour un nœud inexistant : {page_id}", path=rel)
        return
    just_param = "justifications"
    obj_param = "objections"
    actual_just = relation_pairs(get_subs(tmpl, just_param), lang)
    actual_obj = relation_pairs(get_subs(tmpl, obj_param), lang)
    expected_just = expected_relations(registry, page_id, lang, "justification")
    expected_obj = expected_relations(registry, page_id, lang, "objection")
    if actual_just != expected_just:
        ctx.report.error("WDV-MWK-008", "Justifications MediaWiki divergentes du registre", path=rel, details={"expected": expected_just, "actual": actual_just})
    if actual_obj != expected_obj:
        ctx.report.error("WDV-MWK-008", "Objections MediaWiki divergentes du registre", path=rel, details={"expected": expected_obj, "actual": actual_obj})
    section_param = "rubriques" if lang == "fr" else "sections"
    expected_sections = (node.get(lang) or {}).get("rubriques" if lang == "fr" else "sections", [])
    actual_sections = split_list(tmpl.one(section_param) or "")
    if actual_sections != expected_sections:
        ctx.report.error("WDV-MWK-009", f"{section_param} divergent du registre", path=rel, details={"expected": expected_sections, "actual": actual_sections})
    allowed = FR_SECTIONS if lang == "fr" else EN_SECTIONS
    for value in actual_sections:
        if value not in allowed:
            ctx.report.error("WDV-MWK-009", f"{section_param} non autorisée : {value}", path=rel)
    kw_param = "mots-clés" if lang == "fr" else "keywords"
    expected_kw = (node.get(lang) or {}).get("keywords", [])
    actual_kw = split_list(tmpl.one(kw_param) or "")
    if actual_kw != expected_kw:
        ctx.report.error("WDV-MWK-009", f"{kw_param} divergents du registre", path=rel, details={"expected": expected_kw, "actual": actual_kw})
    _validate_citations_against_locks(ctx, tmpl, rel, lang, page_id)
    date_param = "date-création" if lang == "fr" else "creation-date"
    expected_date = page_manifest.get("creation_date") or (((node.get("pages") or {}).get(lang) or {}).get("generation") or {}).get("creation_date")
    actual_date = tmpl.one(date_param)
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", actual_date or "") or (expected_date and actual_date != expected_date):
        ctx.report.error("WDV-MWK-010", "Date de création absente, invalide ou divergente", path=rel, details={"expected": expected_date, "actual": actual_date})


def _validate_debate_content(ctx: PackageContext, tmpl: Template, rel: str, lang: str, registry: dict[str, Any], page_manifest: dict[str, Any]) -> None:
    if _is_norm_1217(ctx):
        wikipedia_parameter = "articles-Wikipédia" if lang == "fr" else "wikipedia-articles"
        wikipedia_model = "Article Wikipédia" if lang == "fr" else "Wikipedia article"
        articles = get_subs(tmpl, wikipedia_parameter)
        if not articles or any(article.name != wikipedia_model or not (article.one("page") or "").strip() for article in articles):
            ctx.report.error(
                "WDV-MWK-019",
                f"{wikipedia_parameter} doit contenir au moins un article Wikipédia vérifié",
                path=rel,
            )
    occs = [o for o in registry.get("graph", {}).get("occurrences", []) if o.get("depth") == 1]
    nodes = {n.get("id"): n for n in registry.get("graph", {}).get("nodes", [])}
    for branch, param in (("pro", "arguments-pour" if lang == "fr" else "pro-arguments"), ("con", "arguments-contre" if lang == "fr" else "con-arguments")):
        expected = []
        for occ in sorted((o for o in occs if o.get("branch") == branch), key=lambda o: (o.get("order", 0), o.get("id", ""))):
            data = (nodes.get(occ.get("node_id")) or {}).get(lang) or {}
            expected.append((data.get("canonical_title"), data.get("displayed_title")))
        actual = relation_pairs(get_subs(tmpl, param), lang)
        if actual != expected:
            ctx.report.error("WDV-MWK-008", f"Liste {param} divergente du registre", path=rel, details={"expected": expected, "actual": actual})
    date_param = "date-création" if lang == "fr" else "creation-date"
    expected_date = page_manifest.get("creation_date")
    actual_date = tmpl.one(date_param)
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", actual_date or "") or (expected_date and actual_date != expected_date):
        ctx.report.error("WDV-MWK-010", "Date de création du débat invalide ou divergente", path=rel, details={"expected": expected_date, "actual": actual_date})


def _validate_interlanguage(ctx: PackageContext, tmpl: Template, rel: str, lang: str, page_type: str, page_id: str, registry: dict[str, Any], staging: bool) -> None:
    manifest = ctx.manifest() or {}
    status = manifest.get("global_status")
    links = get_subs(tmpl, "interlangue")
    raw_parameter_present = tmpl.one("interlangue") is not None
    if lang == "en":
        if links or raw_parameter_present:
            ctx.report.error("WDV-MWK-011", "Une page anglaise ne doit jamais contenir de lien interlangue", path=rel)
        return

    norm_120 = _is_norm_120(ctx)
    deferred = english_translation_deferred(manifest)
    expected_present = False if deferred else (True if norm_120 else (staging or state_at_least(status, "interlanguage_applied")))
    if expected_present and len(links) != 1:
        message = "Un lien interlangue français unique est requis dès la création" if norm_120 else "Un lien interlangue français unique est requis à cette étape"
        ctx.report.error("WDV-MWK-011", message, path=rel)
    if deferred and raw_parameter_present and not links:
        ctx.report.error("WDV-MWK-011", "Le paramètre interlangue doit être absent, et non vide, tant que la traduction anglaise est différée", path=rel)
    if not expected_present and not deferred and links:
        ctx.report.error("WDV-MWK-011", "Lien interlangue français prématuré", path=rel)
    if deferred and len(links) > 1:
        ctx.report.error("WDV-MWK-011", "Une page française ne peut contenir qu'un seul lien interlangue", path=rel)

    if links:
        link = links[0]
        expected_model = "Lien interlangue" if norm_120 or page_type == "argument" else "Interlangue"
        if link.name != expected_model:
            ctx.report.error("WDV-MWK-011", f"Sous-modèle interlangue attendu : {expected_model}", path=rel)
        if link.one("langue") != "en":
            ctx.report.error("WDV-MWK-011", "La langue cible doit être en", path=rel)
        if page_type == "debate":
            english_record = (((registry.get("debate") or {}).get("pages") or {}).get("en") or {})
        else:
            node = next((n for n in registry.get("graph", {}).get("nodes", []) if n.get("id") == page_id), {})
            english_record = node.get("en") or {}
        expected_title = english_record.get("canonical_title")
        if english_record.get("title_status") != "locked" or not expected_title:
            ctx.report.error("WDV-MWK-011", "Un lien interlangue exige un titre canonique anglais verrouillé", path=rel)
        actual_title = link.one("page")
        if not actual_title:
            ctx.report.error("WDV-MWK-011", "La cible du lien interlangue ne peut pas être vide", path=rel)
        elif actual_title != expected_title:
            ctx.report.error("WDV-MWK-011", "Cible interlangue incorrecte", path=rel, details={"expected": expected_title, "actual": actual_title})



PAIRED_EM_DASH_RE = re.compile(r"\s—\s[^—\n]{1,500}?\s—(?=\s|[.,;:!?])")


def _validate_french_parenthetical_dashes(ctx: PackageContext, tmpl: Template, rel: str, page_type: str) -> None:
    if _consolidated_norm(ctx) not in {"1.2.1", "1.2.2", "1.2.3", "1.2.4", "1.2.5", "1.2.6", "1.2.7", "1.2.8", "1.2.9", "1.2.10", "1.2.11", "1.2.12", "1.2.13", "1.2.14", "1.2.15", "1.2.16", "1.2.17", "1.2.18", "1.2.19", "1.2.20", "1.2.21", "1.2.22", "1.2.23", "1.2.24", "1.2.25", "1.2.26", "1.2.27", "1.2.28", "1.2.29", "1.2.30", "1.2.31", "1.2.32", "1.2.33", "1.2.34", "1.2.35", "1.2.36", "1.2.37", "1.2.38", "1.2.39", "1.2.40"}:
        return
    values: list[tuple[str, str]] = []
    if page_type == "argument":
        values.append(("résumé", tmpl.one("résumé") or ""))
    elif page_type == "debate":
        try:
            for index, subsection in enumerate(get_subs(tmpl, "introduction"), start=1):
                values.append((f"introduction/{index}/contenu", subsection.one("contenu") or ""))
        except WikiParseError:
            return
    for field, value in values:
        prose = re.sub(r"<ref\b[^>]*>.*?</ref>", "", value, flags=re.IGNORECASE | re.DOTALL)
        match = PAIRED_EM_DASH_RE.search(prose)
        if match:
            excerpt = " ".join(match.group(0).split())[:220]
            ctx.report.error(
                "WDV-MWK-015",
                "Une incise française doit employer des parenthèses, non une paire de tirets cadratins",
                path=rel,
                pointer=field,
                details={"excerpt": excerpt},
            )


REF_BLOCK_RE = re.compile(r"<ref\b[^>]*>.*?</ref>", flags=re.IGNORECASE | re.DOTALL)
SELF_CLOSING_REF_RE = re.compile(r"<ref\b[^>]*/\s*>", flags=re.IGNORECASE)


def _inline_template_spans(text: str) -> list[str]:
    """Extract balanced top-level inline templates from free prose."""
    out: list[str] = []
    i = 0
    while i < len(text) - 1:
        if text[i:i+2] != "{{":
            i += 1
            continue
        start = i
        depth = 0
        while i < len(text) - 1:
            pair = text[i:i+2]
            if pair == "{{":
                depth += 1
                i += 2
                continue
            if pair == "}}":
                depth -= 1
                i += 2
                if depth == 0:
                    out.append(text[start:i])
                    break
                continue
            i += 1
        else:
            break
    return out


def _display_parameter_redundant(article: str, displayed: str) -> bool:
    def norm(value: str) -> str:
        return " ".join(value.replace("_", " ").split()).casefold()
    return norm(article) == norm(displayed)



def _protected_historical_summary_keys(ctx: PackageContext) -> set[tuple[str, str]]:
    cached = getattr(ctx, "_protected_historical_summary_keys_cache", None)
    if isinstance(cached, set):
        return cached
    result: set[tuple[str, str]] = set()
    manifest = ctx.manifest() or {}
    cfg = ((manifest.get("editorial_controls") or {}).get("legacy_content_preservation") or {})
    rel = cfg.get("lock_path")
    if cfg.get("enabled") is True and isinstance(rel, str) and ctx.exists(rel):
        lock = ctx.load_json(rel)
        if isinstance(lock, dict):
            for entry in lock.get("arguments") or []:
                if isinstance(entry, dict) and entry.get("summary_provenance") == "historical_existing":
                    node_id, language = entry.get("id"), entry.get("language")
                    if isinstance(node_id, str) and language in {"fr", "en"}:
                        result.add((node_id, language))
    setattr(ctx, "_protected_historical_summary_keys_cache", result)
    return result

def _validate_wikipedia_hover_links(ctx: PackageContext, tmpl: Template, rel: str, lang: str, page_type: str, *, skip_summary: bool = False) -> None:
    if not _norm_at_least(ctx, "1.2.24"):
        return
    if page_type == "argument" and skip_summary:
        return
    fields: list[tuple[str, str]] = []
    if page_type == "argument":
        key = "résumé" if lang == "fr" else "summary"
        fields.append((key, tmpl.one(key) or ""))
    else:
        content_key = "contenu" if lang == "fr" else "content"
        for index, subsection in enumerate(get_subs(tmpl, "introduction"), start=1):
            fields.append((f"introduction/{index}/{content_key}", subsection.one(content_key) or ""))

    expected_name = "Lien Wikipédia" if lang == "fr" else "Wikipedia link"
    other_name = "Wikipedia link" if lang == "fr" else "Lien Wikipédia"
    display_param = "texte-affiché" if lang == "fr" else "displayed-text"
    wrong_display_param = "displayed-text" if lang == "fr" else "texte-affiché"
    allowed = {"article", display_param}

    for pointer, value in fields:
        for ref_body in REF_BLOCK_RE.findall(value):
            if "{{Lien Wikipédia" in ref_body or "{{Wikipedia link" in ref_body:
                ctx.report.error("WDV-MWK-020", "Un lien Wikipédia explicatif est interdit dans le corps d’une note <ref>", path=rel, pointer=pointer)
        prose = REF_BLOCK_RE.sub("", value)
        prose = SELF_CLOSING_REF_RE.sub("", prose)
        for raw in _inline_template_spans(prose):
            try:
                sub = parse_template(raw)
            except WikiParseError as exc:
                ctx.report.error("WDV-MWK-020", f"Modèle inline mal formé : {exc}", path=rel, pointer=pointer)
                continue
            if sub.name == other_name:
                ctx.report.error("WDV-MWK-020", f"Le modèle {sub.name} ne correspond pas à la langue de la page", path=rel, pointer=pointer, details={"expected": expected_name})
                continue
            if sub.name != expected_name:
                ctx.report.error("WDV-MWK-020", f"Modèle inline non autorisé dans ce champ : {sub.name}", path=rel, pointer=pointer, details={"allowed": expected_name})
                continue
            keys = [key for key, _ in sub.params]
            if len(keys) != len(set(keys)):
                ctx.report.error("WDV-MWK-020", f"Paramètre dupliqué dans {expected_name}", path=rel, pointer=pointer)
            unknown = [key for key in keys if key not in allowed]
            if unknown:
                ctx.report.error("WDV-MWK-020", f"Paramètre inconnu dans {expected_name}", path=rel, pointer=pointer, details={"unknown": unknown, "allowed": sorted(allowed)})
            if wrong_display_param in keys:
                ctx.report.error("WDV-MWK-020", f"Paramètre d’affichage de l’autre langue interdit : {wrong_display_param}", path=rel, pointer=pointer)
            article = (sub.one("article") or "").strip()
            if not article:
                ctx.report.error("WDV-MWK-020", f"{expected_name} exige un paramètre article non vide", path=rel, pointer=pointer)
            elif re.match(r"https?://", article, flags=re.I):
                ctx.report.error("WDV-MWK-020", "Le paramètre article doit contenir un titre de page, non une URL", path=rel, pointer=pointer, details={"article": article})
            displayed = sub.one(display_param)
            if displayed is not None:
                if not displayed.strip():
                    ctx.report.error("WDV-MWK-020", f"Le paramètre {display_param} ne peut pas être vide", path=rel, pointer=pointer)
                elif article and _display_parameter_redundant(article, displayed):
                    ctx.report.error("WDV-MWK-020", f"Le paramètre {display_param} est redondant ; adapter simplement la casse dans article", path=rel, pointer=pointer, details={"article": article, "displayed": displayed})

def validate_page(ctx: PackageContext, page_manifest: dict[str, Any], *, override_path: str | None = None, staging: bool = False) -> Template | None:
    rel = override_path or page_manifest.get("file_path")
    if not rel:
        return None
    text = ctx.read_text(rel, required=page_manifest.get("status") in {"generated", "validated", "published"})
    if text is None:
        return None
    try:
        tmpl = parse_template(text)
    except WikiParseError as exc:
        ctx.report.error("WDV-MWK-001", str(exc), path=rel)
        return None
    lang = page_manifest.get("language")
    page_type = page_manifest.get("page_type")
    if (lang, page_type) not in TOP:
        return tmpl
    validate_template_shape(ctx, tmpl, lang, page_type, rel, page_manifest)
    _check_reference_language_and_typography(ctx, tmpl, rel, lang)
    page_key = (page_manifest.get("page_id"), lang)
    _validate_wikipedia_hover_links(ctx, tmpl, rel, lang, page_type, skip_summary=page_key in _protected_historical_summary_keys(ctx))
    if lang == "fr":
        _validate_french_parenthetical_dashes(ctx, tmpl, rel, page_type)
    registry = ctx.registry() or {}
    page_id = page_manifest.get("page_id")
    if page_type == "argument":
        _validate_argument_content(ctx, tmpl, rel, lang, page_id, registry, page_manifest)
    else:
        _validate_debate_content(ctx, tmpl, rel, lang, registry, page_manifest)
    _validate_interlanguage(ctx, tmpl, rel, lang, page_type, page_id, registry, staging)
    return tmpl


def _validate_legacy_content_preservation(ctx: PackageContext, parsed_by_key: dict[tuple[str, str], Template]) -> None:
    manifest = ctx.manifest() or {}
    controls = manifest.get("editorial_controls") or {}
    cfg = controls.get("legacy_content_preservation") or {}
    if cfg.get("enabled") is not True:
        return
    lock_rel = cfg.get("lock_path")
    if not isinstance(lock_rel, str) or not ctx.exists(lock_rel):
        ctx.report.error("WDV-EDT-027", "Verrou des contenus historiques absent", path=lock_rel or "manifest.json")
        return
    lock = ctx.load_json(lock_rel)
    if not isinstance(lock, dict):
        ctx.report.error("WDV-EDT-027", "Verrou des contenus historiques invalide", path=lock_rel)
        return
    if lock.get("debate_id") != manifest.get("debate_id"):
        ctx.report.error("WDV-EDT-027", "Le verrou historique ne correspond pas au débat", path=lock_rel)
    expected_source_sha = cfg.get("source_archive_sha256")
    if expected_source_sha and lock.get("source_archive_sha256") != expected_source_sha:
        ctx.report.error("WDV-EDT-027", "Empreinte de la source historique divergente", path=lock_rel, details={"expected": expected_source_sha, "actual": lock.get("source_archive_sha256")})

    source_templates: dict[tuple[str, str], Template] = {}
    verification_revision = cfg.get("verification_revision")
    if verification_revision in {"0.4.42", "0.4.43"}:
        inventory_rel = cfg.get("source_inventory_path")
        inventory_sha = cfg.get("source_inventory_sha256")
        if not isinstance(inventory_rel, str) or not ctx.exists(inventory_rel):
            ctx.report.error("WDV-EDT-027", "Inventaire source historique absent", path=inventory_rel or "manifest.json")
        else:
            raw_inventory = ctx.root.joinpath(inventory_rel).read_bytes()
            actual_inventory_sha = hashlib.sha256(raw_inventory).hexdigest()
            if inventory_sha != actual_inventory_sha:
                ctx.report.error("WDV-EDT-027", "Empreinte de l’inventaire source historique divergente", path=inventory_rel, details={"expected": inventory_sha, "actual": actual_inventory_sha})
            inventory = ctx.load_json(inventory_rel)
            if not isinstance(inventory, dict) or inventory.get("debate_id") != manifest.get("debate_id") or inventory.get("language") != "fr":
                ctx.report.error("WDV-EDT-027", "Inventaire source historique invalide", path=inventory_rel)
            else:
                for source_page in inventory.get("pages") or []:
                    if not isinstance(source_page, dict) or source_page.get("page_type") != "argument":
                        continue
                    page_id = source_page.get("page_id")
                    content = source_page.get("content")
                    if not isinstance(page_id, str) or not isinstance(content, str):
                        continue
                    # L’empreinte du fichier d’inventaire complet est autoritative. Les champs
                    # content_sha256 historiques peuvent provenir d’une sérialisation antérieure
                    # et ne doivent pas empêcher la lecture du contenu embarqué attesté.
                    try:
                        source_templates[(page_id, "fr")] = parse_template(content)
                    except WikiParseError as exc:
                        ctx.report.error("WDV-EDT-027", f"Page source historique illisible : {exc}", path=inventory_rel, details={"page_id": page_id})

    protected_fields = set(cfg.get("protected_fields") or [])
    entries = lock.get("arguments")
    if not isinstance(entries, list):
        ctx.report.error("WDV-EDT-027", "Liste des pages historiques absente", path=lock_rel)
        return
    by_key: dict[tuple[str, str], dict[str, Any]] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        key=(entry.get("id"),entry.get("language"))
        if not all(isinstance(v,str) for v in key) or key in by_key:
            ctx.report.error("WDV-EDT-027", "Entrée historique invalide ou dupliquée", path=lock_rel, details={"key": list(key)})
            continue
        by_key[key]=entry
    for key, entry in by_key.items():
        tmpl=parsed_by_key.get(key)
        if tmpl is None:
            ctx.report.error("WDV-EDT-027", "Page historique protégée absente du manifeste", path=lock_rel, details={"page_id": key[0], "language": key[1]})
            continue
        lang=key[1]
        if ("résumé" if lang=="fr" else "summary") in protected_fields:
            provenance = entry.get("summary_provenance")
            field="résumé" if lang=="fr" else "summary"
            source_tmpl = source_templates.get(key)
            source_summary = source_tmpl.one(field) if source_tmpl is not None else None
            valid_provenance = {"historical_existing", "generated_after_import"}
            if verification_revision == "0.4.43":
                valid_provenance |= {"absent_at_import", "new_page_unwritten", "authored_after_import"}
            if provenance not in valid_provenance:
                ctx.report.error("WDV-EDT-027", "Provenance du résumé historique invalide", path=lock_rel, details={"page_id":key[0],"provenance":provenance})
            elif verification_revision == "0.4.42" and source_tmpl is None:
                ctx.report.error("WDV-EDT-027", "Page historique absente de l’inventaire source", path=lock_rel, details={"page_id": key[0], "language": lang})
            elif verification_revision == "0.4.43" and source_tmpl is not None and source_summary is not None and provenance != "historical_existing":
                ctx.report.error("WDV-EDT-027", "Résumé historique présent dans l’inventaire mais mal classé", path=lock_rel, details={"page_id": key[0], "provenance": provenance})
            elif verification_revision == "0.4.43" and source_tmpl is not None and source_summary is None and provenance != "absent_at_import":
                ctx.report.error("WDV-EDT-027", "Absence historique du résumé mal classée", path=lock_rel, details={"page_id": key[0], "provenance": provenance})
            elif verification_revision == "0.4.43" and source_tmpl is None and provenance not in {"new_page_unwritten", "authored_after_import"}:
                ctx.report.error("WDV-EDT-027", "Page nouvelle ou hors inventaire mal classée", path=lock_rel, details={"page_id": key[0], "provenance": provenance})
            elif verification_revision == "0.4.42" and provenance == "historical_existing" and source_summary is None:
                ctx.report.error("WDV-EDT-027", "Résumé déclaré historique mais absent de l’inventaire source", path=lock_rel, details={"page_id": key[0]})
            elif verification_revision == "0.4.42" and provenance == "generated_after_import" and source_summary is not None:
                ctx.report.error("WDV-EDT-027", "Résumé historique présent dans l’inventaire mais classé comme généré", path=lock_rel, details={"page_id": key[0]})
            elif provenance == "historical_existing":
                actual=tmpl.one(field)
                actual_sha=hashlib.sha256((actual or "").encode("utf-8")).hexdigest()
                expected_sha = entry.get("summary_sha256")
                expected_length = entry.get("summary_length")
                if verification_revision in {"0.4.42", "0.4.43"} and source_summary is not None:
                    source_sha = hashlib.sha256(source_summary.encode("utf-8")).hexdigest()
                    if expected_sha != source_sha or expected_length != len(source_summary):
                        ctx.report.error("WDV-EDT-027", "Verrou du résumé historique incohérent avec l’inventaire source", path=lock_rel, details={"page_id": key[0], "expected_sha256": source_sha, "lock_sha256": expected_sha})
                if actual is None or actual_sha != expected_sha or len(actual) != expected_length:
                    ctx.report.error("WDV-EDT-027", "Résumé historique modifié", path=next((p.get("file_path") for p in manifest.get("pages",[]) if p.get("page_id")==key[0] and p.get("language")==lang), lock_rel), details={"page_id":key[0],"expected_sha256":expected_sha,"actual_sha256":actual_sha})
            elif verification_revision == "0.4.43" and provenance in {"absent_at_import", "new_page_unwritten"}:
                if tmpl.one(field) is not None:
                    ctx.report.error("WDV-EDT-028", "Un résumé déclaré non rédigé est présent dans la page", path=next((p.get("file_path") for p in manifest.get("pages",[]) if p.get("page_id")==key[0] and p.get("language")==lang), lock_rel), details={"page_id": key[0], "provenance": provenance})
            elif verification_revision == "0.4.43" and provenance == "authored_after_import":
                actual = tmpl.one(field)
                if actual is None or not actual.strip():
                    ctx.report.error("WDV-EDT-028", "Un résumé déclaré rédigé après import est absent ou vide", path=next((p.get("file_path") for p in manifest.get("pages",[]) if p.get("page_id")==key[0] and p.get("language")==lang), lock_rel), details={"page_id": key[0]})
        init_field="initialisation" if lang=="fr" else "initialization"
        if init_field in protected_fields:
            state=entry.get("initialisation") if lang=="fr" else entry.get("initialization")
            actual=tmpl.one(init_field)
            source_tmpl = source_templates.get(key)
            source_initialisation = source_tmpl.one(init_field) if source_tmpl is not None else None
            if verification_revision in {"0.4.42", "0.4.43"} and source_tmpl is not None:
                expected_present = source_initialisation is not None
                lock_present = isinstance(state, dict) and state.get("present") is True
                lock_value = state.get("value") if isinstance(state, dict) else None
                if lock_present != expected_present or (expected_present and lock_value != source_initialisation):
                    ctx.report.error("WDV-EDT-027", "Verrou d’initialisation incohérent avec l’inventaire source", path=lock_rel, details={"page_id": key[0], "expected": source_initialisation, "lock": lock_value if lock_present else None})
            if not isinstance(state,dict) or not isinstance(state.get("present"),bool):
                ctx.report.error("WDV-EDT-027", "État historique d'initialisation invalide", path=lock_rel, details={"page_id":key[0]})
            elif state.get("present"):
                if actual != state.get("value"):
                    ctx.report.error("WDV-EDT-027", "Paramètre initialisation historique modifié ou supprimé", path=next((p.get("file_path") for p in manifest.get("pages",[]) if p.get("page_id")==key[0] and p.get("language")==lang), lock_rel), details={"page_id":key[0],"expected":state.get("value"),"actual":actual})
            elif actual is not None:
                ctx.report.error("WDV-EDT-027", "Paramètre initialisation ajouté sans provenance historique", path=next((p.get("file_path") for p in manifest.get("pages",[]) if p.get("page_id")==key[0] and p.get("language")==lang), lock_rel), details={"page_id":key[0],"actual":actual})
    if verification_revision == "0.4.42":
        for key in parsed_by_key:
            if key in source_templates and key not in by_key:
                ctx.report.error("WDV-EDT-027", "Page importée active absente du verrou historique", path=lock_rel, details={"page_id": key[0], "language": key[1]})
    elif verification_revision == "0.4.43":
        for key in parsed_by_key:
            if not re.fullmatch(r"A[0-9]{4}", key[0]):
                continue
            if key not in by_key:
                ctx.report.error("WDV-EDT-027", "Page Argument active absente du registre de provenance des résumés", path=lock_rel, details={"page_id": key[0], "language": key[1]})
    for key, tmpl in parsed_by_key.items():
        if key in by_key:
            continue
        init_field="initialisation" if key[1]=="fr" else "initialization"
        if init_field in protected_fields and tmpl.one(init_field) is not None:
            ctx.report.error("WDV-EDT-027", "Paramètre initialisation présent sur une page non attestée par le verrou historique", path=next((p.get("file_path") for p in manifest.get("pages",[]) if p.get("page_id")==key[0] and p.get("language")==key[1]), lock_rel), details={"page_id":key[0],"language":key[1]})


def validate_wikicode(ctx: PackageContext) -> None:
    manifest = ctx.manifest()
    registry = ctx.registry()
    if not manifest or not registry:
        return
    pages = manifest.get("pages", [])
    declared_paths: set[str] = set()
    parsed_by_key: dict[tuple[str, str], Template] = {}
    for page in pages:
        path = page.get("file_path")
        if path:
            declared_paths.add(path)
        tmpl = validate_page(ctx, page)
        if tmpl:
            parsed_by_key[(page.get("page_id"), page.get("language"))] = tmpl
    _validate_legacy_content_preservation(ctx, parsed_by_key)
    # Staging copies are validated after normal interlanguage preparation and also
    # in migration packages that carry an explicit validated/partial patch.
    patch = ctx.load_json("patches/interlanguage_fr.validated.json")
    validate_staging = state_at_least(manifest.get("global_status"), "interlanguage_prepared") or (
        isinstance(patch, dict) and patch.get("status") in {"validated", "partially_applied", "applied"}
    )
    if validate_staging and not _is_norm_120(ctx):
        for page in pages:
            if page.get("language") != "fr":
                continue
            canonical = Path(page.get("file_path", ""))
            try:
                suffix = canonical.relative_to(Path("output/fr"))
            except ValueError:
                continue
            staging_path = (Path("staging/interlanguage/fr") / suffix).as_posix()
            validate_page(ctx, page, override_path=staging_path, staging=True)
    # Detect orphan individual page files.
    for path in ctx.iter_files("output/*/arguments/*.wiki"):
        rel = ctx.relative(path)
        if rel not in declared_paths:
            ctx.report.error("WDV-FS-006", "Fichier de page Argument non déclaré dans le manifeste", path=rel)
    validate_aggregates(ctx, pages)
    ctx.report.metrics["wikicode"] = {"declared_pages": len(pages), "parsed_pages": len(parsed_by_key)}


def validate_aggregates(ctx: PackageContext, pages: list[dict[str, Any]]) -> None:
    pages_by_batch: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for p in pages:
        if p.get("page_type") == "argument" and p.get("batch_id"):
            pages_by_batch[p["batch_id"]].append(p)
    manifest = ctx.manifest() or {}
    batches = {b.get("id"): b for b in manifest.get("batches", [])}
    for bid, batch_pages in pages_by_batch.items():
        batch = batches.get(bid)
        if not batch:
            continue
        aggregate = (batch.get("outputs") or {}).get("aggregate_path")
        if not aggregate or not ctx.exists(aggregate):
            continue
        text = ctx.read_text(aggregate)
        if text is None:
            continue
        pattern = re.compile(r"^===== PAGE : (.+?) =====\n", re.MULTILINE)
        matches = list(pattern.finditer(text))
        titles = [m.group(1) for m in matches]
        expected_pages = sorted(batch_pages, key=lambda p: ((batch.get("node_ids") or []).index(p.get("page_id")) if p.get("page_id") in (batch.get("node_ids") or []) else 10**9))
        expected_titles = [p.get("canonical_title") for p in expected_pages]
        if titles != expected_titles:
            ctx.report.error("WDV-MWK-013", f"Séparateurs de l'agrégat {bid} divergents", path=aggregate, details={"expected": expected_titles, "actual": titles})
        for i, page in enumerate(expected_pages):
            start = matches[i].end() if i < len(matches) else None
            end = matches[i+1].start() if i + 1 < len(matches) else len(text)
            if start is None:
                break
            aggregate_content = text[start:end].strip("\n") + "\n"
            individual = ctx.read_text(page.get("file_path"))
            if individual is not None and aggregate_content != individual:
                ctx.report.error("WDV-MWK-013", f"Contenu agrégé différent du fichier individuel {page.get('page_id')}", path=aggregate)
