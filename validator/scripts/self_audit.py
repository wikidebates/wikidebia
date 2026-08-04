#!/usr/bin/env python3
from __future__ import annotations

import ast
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
errors = []

RUNTIME_DIRS = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
RUNTIME_SUFFIXES = {".pyc", ".pyo"}

def is_runtime_artifact(rel: Path) -> bool:
    return any(part in RUNTIME_DIRS for part in rel.parts) or rel.suffix in RUNTIME_SUFFIXES
text_suffixes = {".py", ".md", ".txt", ".json", ".toml", ".sh"}
for path in sorted(ROOT.rglob("*")):
    if not path.is_file() or path.suffix not in text_suffixes:
        continue
    raw = path.read_bytes()
    rel = path.relative_to(ROOT)
    if raw.startswith(b"\xef\xbb\xbf"):
        errors.append(f"BOM: {rel}")
    if b"\r" in raw:
        errors.append(f"CR/CRLF: {rel}")
    if raw and not raw.endswith(b"\n"):
        errors.append(f"fin de ligne absente: {rel}")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        errors.append(f"UTF-8 invalide: {rel}: {exc}")
        continue
    if path.suffix == ".py":
        try:
            ast.parse(text, filename=str(rel))
        except SyntaxError as exc:
            errors.append(f"Python invalide: {rel}: {exc}")
    if path.suffix == ".json":
        try:
            json.loads(text)
        except json.JSONDecodeError as exc:
            errors.append(f"JSON invalide: {rel}: {exc}")

# Verify that the common version table matches the component metadata.
versions_path = ROOT / "VERSIONS.json"
if not versions_path.is_file():
    errors.append("VERSIONS.json absent")
else:
    try:
        versions = json.loads(versions_path.read_text(encoding="utf-8"))
        expected_keys = {"norm", "validator", "kit"}
        if set(versions) != expected_keys:
            errors.append("clés inattendues dans VERSIONS.json")
        compatibility_path = ROOT / "COMPATIBILITY.json"
        if compatibility_path.is_file():
            compatibility = json.loads(compatibility_path.read_text(encoding="utf-8"))
            if compatibility.get("validator_version") != versions.get("validator"):
                errors.append("version du validateur divergente dans COMPATIBILITY.json")
            if compatibility.get("implemented_normative_revision") != versions.get("norm"):
                errors.append("révision normative divergente dans COMPATIBILITY.json")
        init_path = ROOT / "src/wikidebia_validator/__init__.py"
        if init_path.is_file():
            match = re.search(r'^__version__\s*=\s*["\']([^"\']+)["\']', init_path.read_text(encoding="utf-8"), re.M)
            if not match or match.group(1) != versions.get("validator"):
                errors.append("version du paquet Python divergente")
        pyproject_path = ROOT / "pyproject.toml"
        if pyproject_path.is_file():
            match = re.search(r'^version\s*=\s*"([^"]+)"', pyproject_path.read_text(encoding="utf-8"), re.M)
            if not match or match.group(1) != versions.get("validator"):
                errors.append("version du pyproject divergente")
    except Exception as exc:
        errors.append(f"VERSIONS.json illisible: {exc}")

# Verify the package manifest when present. This catches undeclared historical
# files as well as modified, missing or incorrectly sized artifacts.
manifest_path = ROOT / "PACKAGE_MANIFEST_SHA256.json"
receipt_path = ROOT / "PACKAGE_RECEIPT.json"
if manifest_path.is_file():
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        excluded = set(manifest.get("self_excluded") or [])
        declared = {row["path"]: row for row in manifest.get("files") or []}
        manifest_count = manifest.get("declared_file_count")
        if manifest_count is None or int(manifest_count) != len(declared):
            errors.append("nombre de fichiers déclaré divergent dans le manifeste")
        declared_test_count = manifest.get("declared_test_count")
        test_report_path = ROOT / "docs/TEST_REPORT.txt"
        if declared_test_count is None:
            errors.append("nombre de tests déclaré absent dans le manifeste")
        elif test_report_path.is_file():
            report_match = re.search(
                r"Tests pytest\s*:\s*(\d+)\s+réussis",
                test_report_path.read_text(encoding="utf-8"),
            )
            if not report_match or int(declared_test_count) != int(report_match.group(1)):
                errors.append("nombre de tests déclaré divergent dans le manifeste")
        actual = {
            path.relative_to(ROOT).as_posix()
            for path in ROOT.rglob("*")
            if path.is_file()
            and path.relative_to(ROOT).as_posix() not in excluded
            and not is_runtime_artifact(path.relative_to(ROOT))
        }
        for rel in sorted(set(declared) - actual):
            errors.append(f"fichier déclaré absent: {rel}")
        for rel in sorted(actual - set(declared)):
            errors.append(f"fichier livré non déclaré: {rel}")
        for rel, row in declared.items():
            path = ROOT / rel
            if not path.is_file():
                continue
            raw = path.read_bytes()
            digest = hashlib.sha256(raw).hexdigest()
            if len(raw) != row.get("size_bytes"):
                errors.append(f"taille divergente: {rel}")
            if digest != row.get("sha256"):
                errors.append(f"SHA-256 divergent: {rel}")
        if receipt_path.is_file():
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            digest = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
            if receipt.get("package_manifest_sha256") != digest:
                errors.append("empreinte du manifeste divergente dans le reçu")
            declared_count = receipt.get("declared_file_count")
            if declared_count is not None and int(declared_count) != len(declared):
                errors.append("nombre de fichiers déclaré divergent dans le reçu")
            receipt_test_count = receipt.get("declared_test_count")
            if receipt_test_count is not None and declared_test_count is not None and int(receipt_test_count) != int(declared_test_count):
                errors.append("nombre de tests déclaré divergent dans le reçu")
    except Exception as exc:
        errors.append(f"vérification du manifeste impossible: {exc}")

def audit_normative_provenance(root: Path, errors: list[str]) -> None:
    catalog_path = root / "normative_reference/01_normes/requirements_catalog_wikidebia.json"
    if not catalog_path.is_file():
        return
    try:
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"catalogue d'exigences illisible: {exc}")
        return
    requirements = catalog.get("requirements") or []
    requirement_ids = [req.get("id") for req in requirements if isinstance(req, dict)]
    duplicate_ids = sorted({value for value in requirement_ids if value and requirement_ids.count(value) > 1})
    for requirement_id in duplicate_ids:
        errors.append(f"identifiant d'exigence dupliqué: {requirement_id}")
    aliases = catalog.get("source_aliases") or {}
    used = {label for req in requirements for label in (req.get("sources") or [])}
    missing_labels = sorted(used - set(aliases))
    for label in missing_labels:
        errors.append(f"étiquette de provenance sans alias: {label}")
    ref_root = root / "normative_reference"
    for label, paths in aliases.items():
        if not isinstance(paths, list) or not paths:
            errors.append(f"alias de provenance vide: {label}")
            continue
        for rel in paths:
            if not (ref_root / rel).is_file():
                errors.append(f"alias de provenance vers fichier absent: {label} -> {rel}")
    for req in catalog.get("requirements", []):
        for rel in req.get("normative_files") or []:
            if not (ref_root / rel).is_file():
                errors.append(f"chemin normatif absent: {req.get('id')} -> {rel}")
    compatibility_path = root / "COMPATIBILITY.json"
    if compatibility_path.is_file():
        implemented = json.loads(compatibility_path.read_text(encoding="utf-8")).get("implemented_normative_revision")
        active_norms = sorted((root / "normative_reference/01_normes").glob("WIKIDEBIA_NORME_CONSOLIDEE_*.md"))
        expected_active = f"WIKIDEBIA_NORME_CONSOLIDEE_{implemented}.md"
        if [path.name for path in active_norms] != [expected_active]:
            errors.append("source normative active absente, multiple ou sur une mauvaise révision")
        structures = root / "normative_reference/01_normes/structures_mediawiki_wikidebia.md"
        profiles = root / "normative_reference/01_normes/profils_rendu_wikidebia.md"
        cahier = root / "normative_reference/01_normes/cahier_des_charges_consolide_wikidebia.md"
        if implemented == "1.2.29":
            structures_text = structures.read_text(encoding="utf-8") if structures.is_file() else ""
            if "|quotes={{Quote" not in structures_text or "|quotes={{Citation" in structures_text:
                errors.append("structure anglaise des citations non conforme")
            if "|avertissements-citation=" not in structures_text:
                errors.append("paramètre avertissements-citation absent des structures")
            profiles_text = profiles.read_text(encoding="utf-8") if profiles.is_file() else ""
            if "Les citations textuelles ne sont jamais générées" in profiles_text or "Quotes are never generated" in profiles_text:
                errors.append("ancienne interdiction des citations encore active dans les profils")
            cahier_text = cahier.read_text(encoding="utf-8") if cahier.is_file() else ""
            if "MW-009 — ACTIVE" in cahier_text:
                errors.append("MW-009 reste active dans le cahier des charges")
            mw009 = next((req for req in requirements if req.get("id") == "MW-009"), {})
            if mw009.get("disposition") != "superseded":
                errors.append("MW-009 n'est pas classée comme remplacée dans le catalogue")
        for example in sorted((root / "examples").glob("*review.example.json")):
            try:
                data = json.loads(example.read_text(encoding="utf-8"))
            except Exception as exc:
                errors.append(f"exemple actif illisible: {example.name}: {exc}")
                continue
            if data.get("normative_revision") != implemented:
                errors.append(f"exemple actif sur une mauvaise révision: {example.name}")

audit_normative_provenance(ROOT, errors)

if errors:
    print("AUTO-AUDIT : ÉCHEC")
    for error in errors:
        print("-", error)
    raise SystemExit(1)
print("AUTO-AUDIT : RÉUSSI")
print("Encodage, fins de ligne, syntaxe Python, JSON, versions, provenance et chemins normatifs contrôlés.")
