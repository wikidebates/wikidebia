from __future__ import annotations

import json
from pathlib import Path

from wikidebia_validator.editorial import _validate_dates
from wikidebia_validator.package import PackageContext
from wikidebia_validator.report import Report
from wikidebia_validator.graph import validate_graph


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def test_per_page_preserved_dates_accept_historical_and_new_pages(tmp_path: Path) -> None:
    registry = {
        "debate": {"id": "demo", "pages": {"fr": {"generation": {"creation_date": "2026-08-04"}}}},
        "graph": {"nodes": [{"id": "A0001", "pages": {"fr": {"generation": {"creation_date": "2026-08-05"}}}}]},
    }
    dump(tmp_path / "data/registre_debat.json", registry)
    (tmp_path / "output/fr/arguments").mkdir(parents=True)
    (tmp_path / "output/fr/debat.wiki").write_text("{{Débat\n|date-création=2026-08-04\n}}\n", encoding="utf-8")
    (tmp_path / "output/fr/arguments/A0001.wiki").write_text("{{Argument\n|date-création=2026-08-05\n}}\n", encoding="utf-8")
    manifest = {
        "core_files": {"registry": "data/registre_debat.json"},
        "pages": [
            {"page_id": "demo", "language": "fr", "file_path": "output/fr/debat.wiki", "creation_date": "2026-08-04"},
            {"page_id": "A0001", "language": "fr", "file_path": "output/fr/arguments/A0001.wiki", "creation_date": "2026-08-05"},
        ],
    }
    report = Report("0.4.39", str(tmp_path), ["editorial"])
    ctx = PackageContext(tmp_path, report)
    assert _validate_dates(ctx, manifest, None, "per_page_preserved") == 0
    assert not any(f.code == "WDV-EDT-005" for f in report.findings)


def test_per_page_preserved_is_the_default_policy(tmp_path: Path) -> None:
    registry = {
        "debate": {"id": "demo", "pages": {"fr": {"generation": {"creation_date": "2018-02-03"}}}},
        "graph": {"nodes": [{"id": "A0001", "pages": {"fr": {"generation": {"creation_date": "2026-08-05"}}}}]},
    }
    dump(tmp_path / "data/registre_debat.json", registry)
    (tmp_path / "output/fr/arguments").mkdir(parents=True)
    (tmp_path / "output/fr/debat.wiki").write_text("{{Débat\n|date-création=2018-02-03\n}}\n", encoding="utf-8")
    (tmp_path / "output/fr/arguments/A0001.wiki").write_text("{{Argument\n|date-création=2026-08-05\n}}\n", encoding="utf-8")
    manifest = {
        "core_files": {"registry": "data/registre_debat.json"},
        "pages": [
            {"page_id": "demo", "language": "fr", "file_path": "output/fr/debat.wiki", "creation_date": "2018-02-03"},
            {"page_id": "A0001", "language": "fr", "file_path": "output/fr/arguments/A0001.wiki", "creation_date": "2026-08-05"},
        ],
    }
    report = Report("0.4.39", str(tmp_path), ["editorial"])
    ctx = PackageContext(tmp_path, report)
    assert _validate_dates(ctx, manifest, None) == 0


def test_per_page_preserved_dates_still_reject_registry_divergence(tmp_path: Path) -> None:
    registry = {"debate": {"id": "demo", "pages": {"fr": {"generation": {"creation_date": "2026-08-03"}}}}, "graph": {"nodes": []}}
    dump(tmp_path / "data/registre_debat.json", registry)
    (tmp_path / "output/fr").mkdir(parents=True)
    (tmp_path / "output/fr/debat.wiki").write_text("{{Débat\n|date-création=2026-08-04\n}}\n", encoding="utf-8")
    manifest = {"core_files": {"registry": "data/registre_debat.json"}, "pages": [{"page_id": "demo", "language": "fr", "file_path": "output/fr/debat.wiki", "creation_date": "2026-08-04"}]}
    report = Report("0.4.39", str(tmp_path), ["editorial"])
    ctx = PackageContext(tmp_path, report)
    assert _validate_dates(ctx, manifest, None, "per_page_preserved") == 1
    assert any(f.code == "WDV-EDT-005" for f in report.findings)
