from __future__ import annotations

import json
import re
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .graph import state_at_least
from .package import PackageContext


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
}

SEQUENCE_PARAMS = {
    "introduction", "articles-Wikipédia", "arguments-pour", "arguments-contre", "bibliographie-pour", "bibliographie-contre", "bibliographie-ni-pour-ni-contre", "sitographie-pour", "sitographie-contre", "sitographie-ni-pour-ni-contre", "vidéographie-pour", "vidéographie-contre", "vidéographie-ni-pour-ni-contre", "débats-connexes",
    "wikipedia-articles", "pro-arguments", "con-arguments", "pro-bibliography", "con-bibliography", "bibliography", "pro-webliography", "con-webliography", "webliography", "pro-videography", "con-videography", "videography", "related-debates",
    "références-bibliographiques", "références-sitographiques", "références-vidéographiques", "justifications", "objections", "interlangue",
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


def validate_template_shape(ctx: PackageContext, tmpl: Template, lang: str, page_type: str, rel: str) -> None:
    base_spec = TOP[(lang, page_type)] if _is_norm_120(ctx) else TOP_LEGACY[(lang, page_type)]
    spec = {**base_spec, "order": list(base_spec["order"]), "required": list(base_spec["required"]), "forbidden_generated": list(base_spec["forbidden_generated"])}
    if _is_norm_1217(ctx) and page_type == "debate":
        wikipedia_parameter = "articles-Wikipédia" if lang == "fr" else "wikipedia-articles"
        related_parameter = "débats-connexes" if lang == "fr" else "related-debates"
        if wikipedia_parameter not in spec["required"]:
            spec["required"].append(wikipedia_parameter)
        if related_parameter not in spec["forbidden_generated"]:
            spec["forbidden_generated"].append(related_parameter)
    if tmpl.name != spec["model"]:
        ctx.report.error("WDV-MWK-002", f"Modèle principal attendu {spec['model']}, trouvé {tmpl.name}", path=rel)
    keys = [k for k, _ in tmpl.params]
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
            order, required = SUB[sub.name]
            subkeys = [k for k, _ in sub.params]
            if len(subkeys) != len(set(subkeys)):
                ctx.report.error("WDV-MWK-012", f"Paramètre dupliqué dans {sub.name}", path=rel)
            for skey in subkeys:
                if skey not in order:
                    ctx.report.error("WDV-MWK-012", f"Paramètre inconnu {skey} dans {sub.name}", path=rel)
            indexes = [order.index(x) for x in subkeys if x in order]
            if indexes != sorted(indexes):
                ctx.report.error("WDV-MWK-006", f"Ordre incorrect dans {sub.name}", path=rel)
            for req in required:
                if req not in subkeys or not (sub.one(req) or "").strip():
                    ctx.report.error("WDV-MWK-012", f"Paramètre obligatoire {req} absent ou vide dans {sub.name}", path=rel)
            for skey, sval in sub.params:
                if not sval.strip():
                    ctx.report.error("WDV-MWK-005", f"Sous-paramètre vide interdit : {sub.name}.{skey}", path=rel)
                if skey in {"avertissements", "warnings"}:
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
                    ctx.report.error("WDV-DOC-004", "Le titre de page sitographique duplique le nom du site et doit être omis", path=rel, details={"template": sub.name, "value": sub.one("page")})
                if author_value and page_value and site_value and author_value == page_value == site_value:
                    ctx.report.error("WDV-DOC-004", "Les champs auteur, page et site sont remplis mécaniquement avec la même valeur", path=rel, details={"template": sub.name, "value": sub.one("site")})

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
    if lang == "en":
        if links or tmpl.one("interlangue"):
            ctx.report.error("WDV-MWK-011", "Une page anglaise ne doit jamais contenir de lien interlangue", path=rel)
        return

    norm_120 = _is_norm_120(ctx)
    expected_present = True if norm_120 else (staging or state_at_least(status, "interlanguage_applied"))
    if expected_present and len(links) != 1:
        message = "Un lien interlangue français unique est requis dès la création" if norm_120 else "Un lien interlangue français unique est requis à cette étape"
        ctx.report.error("WDV-MWK-011", message, path=rel)
    if not expected_present and links:
        ctx.report.error("WDV-MWK-011", "Lien interlangue français prématuré", path=rel)
    if links:
        link = links[0]
        expected_model = "Lien interlangue" if norm_120 or page_type == "argument" else "Interlangue"
        if link.name != expected_model:
            ctx.report.error("WDV-MWK-011", f"Sous-modèle interlangue attendu : {expected_model}", path=rel)
        if link.one("langue") != "en":
            ctx.report.error("WDV-MWK-011", "La langue cible doit être en", path=rel)
        if page_type == "debate":
            expected_title = (((registry.get("debate") or {}).get("pages") or {}).get("en") or {}).get("canonical_title")
        else:
            node = next((n for n in registry.get("graph", {}).get("nodes", []) if n.get("id") == page_id), {})
            expected_title = (node.get("en") or {}).get("canonical_title")
        if not expected_title and norm_120:
            ctx.report.error("WDV-MWK-011", "Le titre canonique anglais doit être verrouillé avant la création française", path=rel)
        if link.one("page") != expected_title:
            ctx.report.error("WDV-MWK-011", "Cible interlangue incorrecte", path=rel, details={"expected": expected_title, "actual": link.one("page")})



PAIRED_EM_DASH_RE = re.compile(r"\s—\s[^—\n]{1,500}?\s—(?=\s|[.,;:!?])")


def _validate_french_parenthetical_dashes(ctx: PackageContext, tmpl: Template, rel: str, page_type: str) -> None:
    if _consolidated_norm(ctx) not in {"1.2.1", "1.2.2", "1.2.3", "1.2.4", "1.2.5", "1.2.6", "1.2.7", "1.2.8", "1.2.9", "1.2.10", "1.2.11", "1.2.12", "1.2.13", "1.2.14", "1.2.15", "1.2.16", "1.2.17", "1.2.18", "1.2.19", "1.2.20", "1.2.21", "1.2.22"}:
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
    validate_template_shape(ctx, tmpl, lang, page_type, rel)
    _check_reference_language_and_typography(ctx, tmpl, rel, lang)
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
