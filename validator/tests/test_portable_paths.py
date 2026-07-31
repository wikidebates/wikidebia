from __future__ import annotations

from pathlib import Path

from wikidebia_validator.report import portable_display_path
from wikidebia_validator.validator import validate_package


def test_absolute_package_path_is_not_persisted(tmp_path: Path):
    missing = tmp_path / "missing-package"
    report = validate_package(missing)
    assert report.package_root == "missing-package"
    payload = report.to_dict()
    assert str(tmp_path) not in str(payload)
    assert str(tmp_path) not in report.to_text()


def test_relative_package_path_is_preserved():
    assert portable_display_path("corpus/demo") == "corpus/demo"


def test_absolute_package_path_is_stable_from_an_unrelated_cwd(tmp_path: Path, monkeypatch):
    package = tmp_path / "packages" / "missing-package"
    unrelated = tmp_path / "elsewhere"
    unrelated.mkdir()
    monkeypatch.chdir(unrelated)
    assert portable_display_path(package) == "missing-package"
