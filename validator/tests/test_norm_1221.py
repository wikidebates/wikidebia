from __future__ import annotations

import json
from pathlib import Path


def test_1221_graph_placement_requirement_ids_are_unique_and_correct():
    root = Path(__file__).resolve().parents[1]
    catalog = json.loads((root / "normative_reference/01_normes/requirements_catalog_wikidebia.json").read_text(encoding="utf-8"))
    rows = catalog["requirements"]
    ids = [row["id"] for row in rows]
    assert len(ids) == len(set(ids))
    by_id = {row["id"]: row for row in rows}
    for requirement_id in ("GR-048", "GR-049", "GR-050", "VAL-029"):
        assert requirement_id in by_id
    assert "Research sources" in by_id["GR-045"]["statement"]
    assert "rendered tree" in by_id["GR-046"]["statement"]
    assert "descendant subgraph" in by_id["GR-047"]["statement"]
