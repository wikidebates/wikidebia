from __future__ import annotations

import hashlib
import json
from pathlib import Path

from wikidebia_validator.editorial import (
    dominant_classification_ratio,
    summary_has_auto_objection,
    title_copy_ratio,
)
from wikidebia_validator.validator import validate_package
from .helpers import create_fr_package


def tree_hash(root: Path) -> str:
    h = hashlib.sha256()
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        h.update(path.relative_to(root).as_posix().encode())
        h.update(b"\0")
        h.update(path.read_bytes())
    return h.hexdigest()


def test_summary_auto_objection_positive_and_negative():
    assert summary_has_auto_objection(
        "Le protocole annonce un effet. Cependant, il pourrait être dû au hasard.", "fr"
    )
    assert not summary_has_auto_objection(
        "Le protocole annonce un effet. Ainsi, une réplication indépendante peut le mettre à l'épreuve.", "fr"
    )
    assert summary_has_auto_objection(
        "The protocol predicts an effect. However, ordinary error may explain it.", "en"
    )
    assert not summary_has_auto_objection(
        "The protocol predicts an effect. Accordingly, an independent replication can test it.", "en"
    )


def test_title_copy_ratio_detects_mechanical_copy():
    nodes = [
        {"fr": {"canonical_title": "Titre A", "displayed_title": "Titre A"}},
        {"fr": {"canonical_title": "Titre B", "displayed_title": "Titre B"}},
        {"fr": {"canonical_title": "Titre C", "displayed_title": "Titre court"}},
    ]
    assert title_copy_ratio(nodes, "fr") == 2 / 3


def test_classification_ratio_detects_uniformity():
    nodes = [
        {"fr": {"rubriques": ["Science"]}},
        {"fr": {"rubriques": ["Science"]}},
        {"fr": {"rubriques": ["Philosophie"]}},
    ]
    assert dominant_classification_ratio(nodes, "fr") == 2 / 3


def test_bibliographic_page_parameter_is_accepted(tmp_path: Path):
    root = create_fr_package(tmp_path)
    p = root / "output/fr/debate/debate.wiki"
    content = p.read_text(encoding="utf-8").replace(
        "|rubriques=",
        "|bibliographie-ni-pour-ni-contre={{Référence bibliographique\n"
        "|auteurs=Autrice Test\n"
        "|article=Article test\n"
        "|ouvrage=Revue test\n"
        "|page=12-18\n"
        "|date=2026\n"
        "}}\n|rubriques=",
    )
    p.write_text(content, encoding="utf-8")
    report = validate_package(root, scopes=["wikicode"])
    assert not any(f.code in {"WDV-MWK-012", "WDV-DOC-002"} for f in report.findings), report.to_text()


def test_pagination_in_location_is_rejected(tmp_path: Path):
    root = create_fr_package(tmp_path)
    p = root / "output/fr/debate/debate.wiki"
    content = p.read_text(encoding="utf-8").replace(
        "|rubriques=",
        "|bibliographie-ni-pour-ni-contre={{Référence bibliographique\n"
        "|auteurs=Autrice Test\n"
        "|article=Article test\n"
        "|ouvrage=Revue test\n"
        "|localisation=pages 12-18\n"
        "|date=2026\n"
        "}}\n|rubriques=",
    )
    p.write_text(content, encoding="utf-8")
    report = validate_package(root, scopes=["wikicode"])
    assert any(f.code == "WDV-DOC-002" for f in report.findings), report.to_text()


def test_access_date_is_rejected(tmp_path: Path):
    root = create_fr_package(tmp_path)
    p = root / "output/fr/debate/debate.wiki"
    content = p.read_text(encoding="utf-8").replace(
        "|rubriques=",
        "|sitographie-ni-pour-ni-contre={{Référence sitographique\n"
        "|lien=https://example.org/source\n"
        "|page=Source test\n"
        "|site=Example\n"
        "|date=consulté le 25 juillet 2026\n"
        "}}\n|rubriques=",
    )
    p.write_text(content, encoding="utf-8")
    report = validate_package(root, scopes=["wikicode"])
    assert any(f.code == "WDV-DOC-003" for f in report.findings), report.to_text()


def test_validate_is_read_only(tmp_path: Path):
    root = create_fr_package(tmp_path)
    before = tree_hash(root)
    validate_package(root)
    after = tree_hash(root)
    assert before == after
