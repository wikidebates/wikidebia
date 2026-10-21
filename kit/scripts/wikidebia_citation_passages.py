"""Preserve editorial prose before, between and after imported quotations."""

from __future__ import annotations

import copy
from typing import Any, Mapping, Sequence, Callable

from wikidebia_graph_extract import iter_templates, normalize_key


def inventory_passages(value: str, node_id: str) -> list[dict[str, Any]]:
    calls = [c for c in iter_templates(value or "") if normalize_key(c.name) == "citation"]
    result: list[dict[str, Any]] = []
    cursor = 0
    for index, call in enumerate(calls, 1):
        start = value.find(call.raw, cursor)
        if start < 0:
            raise ValueError(f"Citations imbriquées ou chevauchantes dans {node_id}")
        gap = value[cursor:start]
        if gap.strip():
            result.append({"id": f"{node_id}-P{len(result)+1:03d}",
                           "before_citation_id": f"{node_id}-C{index:03d}", "text": gap})
        cursor = start + len(call.raw)
    gap = (value or "")[cursor:]
    if gap.strip():
        result.append({"id": f"{node_id}-P{len(result)+1:03d}",
                       "before_citation_id": None, "text": gap})
    return result


def blank_translations(passages: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [{"id": p["id"], "before_citation_id": p["before_citation_id"],
             "source_text": p["text"], "text": "", "equivalent_to_french": False,
             "review_note": ""} for p in passages]


def validate_translations(rows: Any, sources: Sequence[Mapping[str, Any]], node_id: str) -> list[dict[str, Any]]:
    if not isinstance(rows, list) or len(rows) != len(sources):
        raise ValueError(f"Couverture des passages hors Citation incomplète dans {node_id}")
    result = []
    for row, source in zip(rows, sources):
        if not isinstance(row, dict) or any(row.get(k) != source.get(k) for k in ("id", "before_citation_id")):
            raise ValueError(f"Ordre ou ancrage des passages hors Citation modifié dans {node_id}")
        if row.get("source_text") != source.get("text"):
            raise ValueError(f"Source d'un passage hors Citation modifiée dans {node_id}")
        if not isinstance(row.get("text"), str) or not row["text"].strip():
            raise ValueError(f"Traduction d'un passage hors Citation absente dans {node_id}")
        if row.get("equivalent_to_french") is not True or len(str(row.get("review_note") or "").strip()) < 12:
            raise ValueError(f"Revue d'un passage hors Citation absente dans {node_id}")
        result.append(copy.deepcopy(row))
    return result


def render_sequence(citations: Sequence[Mapping[str, Any]], passages: Sequence[Mapping[str, Any]],
                    renderer: Callable[[Mapping[str, Any]], str]) -> str:
    ids = [c.get("id") for c in citations]
    if len(set(ids)) != len(ids):
        raise ValueError("Identifiants de citation dupliqués")
    positions = {value: i for i, value in enumerate(ids)}
    positions[None] = len(ids)
    previous = -1
    by_anchor: dict[Any, list[str]] = {}
    passage_ids = set()
    for passage in passages:
        anchor = passage.get("before_citation_id")
        if anchor not in positions or positions[anchor] < previous or passage.get("id") in passage_ids:
            raise ValueError("Ancrage, ordre ou identité des passages hors Citation invalide")
        text = passage.get("text")
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Passage hors Citation vide")
        previous = positions[anchor]
        passage_ids.add(passage.get("id"))
        by_anchor.setdefault(anchor, []).append(text)
    result = []
    for citation in citations:
        result.extend(by_anchor.get(citation.get("id"), []))
        result.append(renderer(citation))
    result.extend(by_anchor.get(None, []))
    return "".join(result)
