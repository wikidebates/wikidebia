from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

NORM_VERSION = "1.2.23"
VALIDATOR_VERSION = "0.4.25"
KIT_VERSION = "2.2.10"
SCOPES = ("all", "fr", "en", "fr-debate", "en-debate")
COMPONENTS = {
    "wikidebia-normes": "norms",
    "wikidebia-validator": "validator",
    "wikidebia-kit": "kit",
}
TRACKED_ROOT_FILES = (
    "wikidebia",
    ".gitignore",
    "README.md",
    "WIKIDEBIA_NORMES_ACTIVES.md",
    "WIKIDEBIA_VALIDATEUR_ACTIF.md",
    "WIKIDEBIA_RECUS_ARCHIVES.json",
    "requirements-runtime.txt",
)

REQUIRED_GITIGNORE_RULES = (
    "/private/", "/corpus/", "/archives/", "/updates/", "/incoming/",
    "/logs/", "/plans/", "/.state/", "/.venv/",
    "/config/wikidebia.local.json", "/configs/", "/.gitconfig-wikidebia",
    "/user-config.py", "/user-password.cfg", "/apicache/",
    "*.lwp", "throttle.ctrl", "__pycache__/", ".pytest_cache/",
    "*.py[cod]", "*.egg-info/",
)
FORBIDDEN_GIT_PREFIXES = (
    "private/", "corpus/", "archives/", "updates/", "incoming/",
    "logs/", "plans/", ".state/", ".venv/", "configs/", "apicache/",
)
FORBIDDEN_GIT_EXACT = {
    "config/wikidebia.local.json", ".gitconfig-wikidebia",
    "user-config.py", "user-password.cfg", "throttle.ctrl",
}


class ManagementError(RuntimeError):
    pass


def timestamp() -> str:
    return dt.datetime.now().astimezone().strftime("%Y%m%d-%H%M%S")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_tree(path: Path) -> str:
    digest = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        relative = item.relative_to(path).as_posix().encode("utf-8")
        digest.update(len(relative).to_bytes(8, "big"))
        digest.update(relative)
        digest.update(bytes.fromhex(sha256_file(item)))
    return digest.hexdigest()


def json_load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ManagementError(f"JSON illisible : {path.name}") from exc
    if not isinstance(value, dict):
        raise ManagementError(f"Objet JSON attendu : {path.name}")
    return value


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def _safe_member(name: str) -> bool:
    pure = PurePosixPath(name)
    if pure.is_absolute() or ".." in pure.parts:
        return False
    if re.match(r"^[A-Za-z]:", name):
        return False
    return True


def safe_extract(archive: Path, destination: Path) -> None:
    try:
        with zipfile.ZipFile(archive) as bundle:
            seen: set[str] = set()
            for info in bundle.infolist():
                if not _safe_member(info.filename):
                    raise ManagementError(f"Chemin dangereux dans {archive.name} : {info.filename}")
                normalized = PurePosixPath(info.filename).as_posix()
                if normalized in seen:
                    raise ManagementError(f"Entrée ZIP dupliquée : {info.filename}")
                seen.add(normalized)
                mode = (info.external_attr >> 16) & 0o170000
                if mode == stat.S_IFLNK:
                    raise ManagementError(f"Lien symbolique interdit dans {archive.name}")
            bundle.extractall(destination)
    except zipfile.BadZipFile as exc:
        raise ManagementError(f"Archive ZIP invalide : {archive.name}") from exc


def inspect_component_zip(archive: Path) -> dict[str, Any]:
    try:
        with zipfile.ZipFile(archive) as bundle:
            names = {PurePosixPath(info.filename).as_posix() for info in bundle.infolist() if not info.is_dir()}
            if "PACKAGE_MANIFEST_SHA256.json" not in names:
                raise ManagementError(f"Manifeste interne absent : {archive.name}")
            manifest = json.loads(bundle.read("PACKAGE_MANIFEST_SHA256.json").decode("utf-8"))
            artifact = str(manifest.get("artifact") or "")
            if artifact not in COMPONENTS:
                raise ManagementError(f"Type de composant inconnu dans {archive.name} : {artifact}")
            declared = {str(row["path"]): row for row in manifest.get("files", [])}
            metadata_names = {"PACKAGE_MANIFEST_SHA256.json"}
            if "PACKAGE_RECEIPT.json" in names:
                metadata_names.add("PACKAGE_RECEIPT.json")
            expected = set(declared) | metadata_names
            if names != expected:
                missing = sorted(expected - names)
                extra = sorted(names - expected)
                raise ManagementError(
                    f"Inventaire divergent dans {archive.name}; absents={missing[:3]}, supplémentaires={extra[:3]}"
                )
            if "PACKAGE_RECEIPT.json" in names:
                receipt = json.loads(bundle.read("PACKAGE_RECEIPT.json").decode("utf-8"))
                manifest_payload = bundle.read("PACKAGE_MANIFEST_SHA256.json")
                if str(receipt.get("artifact") or "") != artifact:
                    raise ManagementError(f"Reçu associé au mauvais composant : {archive.name}")
                if receipt.get("package_manifest_sha256") != hashlib.sha256(manifest_payload).hexdigest():
                    raise ManagementError(f"Reçu incohérent avec le manifeste : {archive.name}")
                if str(receipt.get("version") or "") != str(manifest.get("version") or ""):
                    raise ManagementError(f"Version du reçu incohérente : {archive.name}")
                if str(receipt.get("normative_revision") or "") != str(manifest.get("normative_revision") or ""):
                    raise ManagementError(f"Révision normative du reçu incohérente : {archive.name}")
                receipt_hash = str(receipt.get("receipt_sha256") or "")
                receipt_body = dict(receipt)
                receipt_body.pop("receipt_sha256", None)
                canonical = json.dumps(receipt_body, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
                if receipt_hash and receipt_hash != hashlib.sha256(canonical).hexdigest():
                    raise ManagementError(f"Empreinte du reçu incohérente : {archive.name}")
            for relative, row in declared.items():
                payload = bundle.read(relative)
                if len(payload) != int(row.get("size_bytes", -1)):
                    raise ManagementError(f"Taille divergente : {archive.name}:{relative}")
                if hashlib.sha256(payload).hexdigest() != row.get("sha256"):
                    raise ManagementError(f"SHA-256 divergent : {archive.name}:{relative}")
            versions = json.loads(bundle.read("VERSIONS.json").decode("utf-8"))
            return {"artifact": artifact, "manifest": manifest, "versions": versions}
    except (zipfile.BadZipFile, KeyError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ManagementError(f"Composant illisible : {archive.name}") from exc


def _iter_input_zips(updates: Path, explicit: Path | None) -> list[Path]:
    if explicit is not None:
        return [explicit.resolve()]
    return sorted(path for path in updates.iterdir() if path.is_file() and path.suffix.casefold() == ".zip")


def _discover_component_archives(workspace: Path, initial_archives: list[Path], max_depth: int = 2) -> list[Path]:
    """Discover component ZIPs directly or through a small number of safe wrapper ZIPs."""
    discovered: list[Path] = []
    pending: list[tuple[Path, int]] = [(path, 0) for path in initial_archives]
    seen: set[tuple[str, str]] = set()
    extracted_index = 0
    while pending:
        archive, depth = pending.pop(0)
        try:
            metadata = inspect_component_zip(archive)
        except ManagementError:
            metadata = None
        if metadata is not None:
            marker = (metadata["artifact"], hashlib.sha256(archive.read_bytes()).hexdigest())
            if marker not in seen:
                seen.add(marker)
                discovered.append(archive)
            continue
        if depth >= max_depth:
            continue
        try:
            with zipfile.ZipFile(archive) as bundle:
                nested_names = [PurePosixPath(info.filename).as_posix() for info in bundle.infolist() if not info.is_dir() and info.filename.casefold().endswith(".zip")]
        except zipfile.BadZipFile:
            continue
        if not nested_names:
            continue
        extracted_index += 1
        destination = workspace / f"wrapper-{extracted_index}"
        safe_extract(archive, destination)
        nested = sorted(path for path in destination.rglob("*.zip") if path.is_file())
        if len(nested) > 32:
            raise ManagementError(f"Archive enveloppante trop complexe : {archive.name}")

        # Prefer the shallowest directory that already contains a complete,
        # coherent set of the three component ZIPs. A project delivery may
        # also contain corpus archives with historical technical inputs; those
        # must never compete with the active root-level components.
        groups: dict[Path, dict[str, Path]] = {}
        divergent_groups: set[Path] = set()
        for nested_archive in nested:
            try:
                nested_metadata = inspect_component_zip(nested_archive)
            except ManagementError:
                continue
            parent = nested_archive.parent
            artifact = nested_metadata["artifact"]
            current = groups.setdefault(parent, {}).get(artifact)
            if current is not None and hashlib.sha256(current.read_bytes()).hexdigest() != hashlib.sha256(nested_archive.read_bytes()).hexdigest():
                divergent_groups.add(parent)
                continue
            groups[parent][artifact] = nested_archive
        complete_groups = [
            (parent, components)
            for parent, components in groups.items()
            if parent not in divergent_groups and set(components) == set(COMPONENTS)
        ]
        if complete_groups:
            parent, components = min(
                complete_groups,
                key=lambda item: (len(item[0].relative_to(destination).parts), item[0].as_posix()),
            )
            pending.extend((components[artifact], depth + 1) for artifact in sorted(COMPONENTS))
            continue
        pending.extend((path, depth + 1) for path in nested)
    return discovered


def collect_update_payload(root: Path, explicit: Path | None = None) -> tuple[dict[str, Path], list[Path], Path]:
    updates = root / "updates"
    updates.mkdir(parents=True, exist_ok=True)
    candidates = _iter_input_zips(updates, explicit)
    if not candidates:
        raise ManagementError("Aucune archive ZIP trouvée dans updates/")

    state_dir = root / ".state"
    state_dir.mkdir(parents=True, exist_ok=True)
    workspace = Path(tempfile.mkdtemp(prefix="wikidebia-update-", dir=state_dir))
    source_files = list(candidates)
    component_candidates = _discover_component_archives(workspace, candidates)

    components: dict[str, Path] = {}
    for candidate in component_candidates:
        metadata = inspect_component_zip(candidate)
        artifact = metadata["artifact"]
        if artifact in components:
            previous_hash = hashlib.sha256(components[artifact].read_bytes()).hexdigest()
            candidate_hash = hashlib.sha256(candidate.read_bytes()).hexdigest()
            if previous_hash != candidate_hash:
                raise ManagementError(f"Plusieurs archives candidates divergentes pour {artifact}")
            continue
        components[artifact] = candidate
    missing = sorted(set(COMPONENTS) - set(components))
    if missing:
        raise ManagementError("Composants de mise à jour absents : " + ", ".join(missing))
    return components, source_files, workspace


def _version_tuple(value: str) -> tuple[int, ...]:
    try:
        return tuple(int(part) for part in value.split("."))
    except ValueError as exc:
        raise ManagementError(f"Version invalide : {value}") from exc


def current_versions(root: Path) -> dict[str, str]:
    for component in ("norms", "validator", "kit"):
        path = root / component / "VERSIONS.json"
        if path.is_file():
            return {str(key): str(value) for key, value in json_load(path).items()}
    return {}


def verify_version_set(components: dict[str, Path], root: Path, allow_downgrade: bool) -> dict[str, str]:
    versions_by_artifact = {
        artifact: {str(key): str(value) for key, value in inspect_component_zip(path)["versions"].items()}
        for artifact, path in components.items()
    }
    unique = {json.dumps(value, sort_keys=True) for value in versions_by_artifact.values()}
    if len(unique) != 1:
        raise ManagementError("Les trois composants ne déclarent pas les mêmes versions")
    versions = next(iter(versions_by_artifact.values()))
    required = {"norm", "validator", "kit"}
    if set(versions) != required:
        raise ManagementError("VERSIONS.json doit contenir norm, validator et kit")
    previous = current_versions(root)
    if previous and not allow_downgrade:
        for key in required:
            if _version_tuple(versions[key]) < _version_tuple(previous.get(key, "0")):
                raise ManagementError(f"Rétrogradation refusée pour {key}: {previous[key]} -> {versions[key]}")
    return versions


def run(
    command: list[str],
    *,
    cwd: Path,
    capture: bool = False,
    check: bool = True,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    process_env = os.environ.copy()
    if env:
        process_env.update(env)
    result = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
        check=False,
        env=process_env,
    )
    if check and result.returncode != 0:
        detail = (result.stderr or result.stdout or "").strip()
        raise ManagementError(f"Commande échouée ({result.returncode}) : {' '.join(command)}\n{detail}")
    return result


def python_command(root: Path) -> str:
    candidate = root / ".venv" / "bin" / "python"
    return str(candidate) if candidate.is_file() else sys.executable


def runtime_requirements_sha(root: Path) -> str | None:
    path = root / "requirements-runtime.txt"
    return sha256_file(path) if path.is_file() else None


def runtime_environment_report(root: Path) -> dict[str, Any]:
    python = root / ".venv" / "bin" / "python"
    required = ("jsonschema", "referencing", "pytest", "pywikibot")
    report: dict[str, Any] = {
        "python": ".venv/bin/python",
        "python_available": False,
        "requirements_file": "requirements-runtime.txt",
        "requirements_sha256": runtime_requirements_sha(root),
        "modules": {},
        "missing_modules": list(required),
    }
    if not python.is_file():
        return report
    probe = r"""
import importlib.util
import json
import sys
from importlib.metadata import PackageNotFoundError, version
modules = ("jsonschema", "referencing", "pytest", "pywikibot")
packages = {}
missing = []
for name in modules:
    if importlib.util.find_spec(name) is None:
        missing.append(name)
        continue
    try:
        packages[name] = version(name)
    except PackageNotFoundError:
        packages[name] = "présent"
print(json.dumps({"python_version": sys.version.split()[0], "modules": packages, "missing_modules": missing}))
"""
    result = run([str(python), "-c", probe], cwd=root, capture=True, check=False)
    if result.returncode != 0:
        report["probe_error"] = (result.stderr or result.stdout or "échec inconnu").strip()
        return report
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        report["probe_error"] = "sortie de diagnostic Python illisible"
        return report
    report.update(payload)
    report["python_available"] = True
    return report


def write_runtime_marker_if_ready(root: Path) -> None:
    report = runtime_environment_report(root)
    expected = report.get("requirements_sha256")
    if not report.get("python_available") or report.get("missing_modules") or not expected:
        return
    marker = root / ".state" / "runtime-requirements.sha256"
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text(str(expected) + "\n", encoding="utf-8", newline="\n")


def extract_components(components: dict[str, Path], workspace: Path) -> dict[str, Path]:
    extracted: dict[str, Path] = {}
    for artifact, archive in components.items():
        destination = workspace / "staged" / COMPONENTS[artifact]
        destination.mkdir(parents=True, exist_ok=True)
        safe_extract(archive, destination)
        extracted[COMPONENTS[artifact]] = destination
    return extracted


def compare_normative_trees(norms: Path, validator: Path) -> None:
    source = norms / "normative_reference"
    embedded = validator / "normative_reference"
    if not source.is_dir() or not embedded.is_dir():
        raise ManagementError("Copie normative absente des composants")
    if sha256_tree(source) != sha256_tree(embedded):
        raise ManagementError("La copie normative du validateur diverge du paquet des normes")


def test_staged_components(root: Path, staged: dict[str, Path]) -> None:
    py = python_command(root)
    compare_normative_trees(staged["norms"], staged["validator"])
    run([py, "scripts/self_audit.py"], cwd=staged["validator"])
    run([py, "-m", "pytest", "-q"], cwd=staged["validator"], env={"PYTHONPATH": "src"})
    run([py, "-m", "pytest", "-q"], cwd=staged["kit"])


def aggregate_package(package: Path, title: str, versions: dict[str, str]) -> str:
    manifest = json_load(package / "PACKAGE_MANIFEST_SHA256.json")
    lines = [
        f"# {title}",
        "",
        f"**Norme active :** {versions['norm']}  ",
        f"**Validateur :** {versions['validator']}  ",
        f"**Kit :** {versions['kit']}",
        "",
    ]
    for row in manifest.get("files", []):
        relative = str(row["path"])
        path = package / relative
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        suffix = path.suffix.casefold()
        language = {".json": "json", ".py": "python", ".toml": "toml", ".sh": "bash"}.get(suffix, "")
        lines.extend(
            [
                f"# Source incorporée : `{relative}`",
                "",
                f"**SHA-256 :** `{row['sha256']}`",
                "",
                f"```{language}",
                text.rstrip("\n"),
                "```",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def generate_readable_sources(root: Path, staged: dict[str, Path], versions: dict[str, str], component_archives: dict[str, Path]) -> dict[str, Path]:
    output = root / ".state" / "generated-update"
    output.mkdir(parents=True, exist_ok=True)
    norms_md = output / "WIKIDEBIA_NORMES_ACTIVES.md"
    validator_md = output / "WIKIDEBIA_VALIDATEUR_ACTIF.md"
    norms_md.write_text(aggregate_package(staged["norms"], f"Wikidéb’IA — Normes actives {versions['norm']}", versions), encoding="utf-8", newline="\n")
    validator_md.write_text(aggregate_package(staged["validator"], f"Wikidéb’IA — Validateur actif {versions['validator']}", versions), encoding="utf-8", newline="\n")
    artifacts = []
    stable = {
        "wikidebia-normes": "wikidebia-normes.zip",
        "wikidebia-validator": "wikidebia-validator.zip",
        "wikidebia-kit": "wikidebia-kit.zip",
    }
    for artifact in ("wikidebia-normes", "wikidebia-validator", "wikidebia-kit"):
        path = component_archives[artifact]
        artifacts.append({"path": stable[artifact], "size_bytes": path.stat().st_size, "sha256": sha256_file(path)})
    for path in (norms_md, validator_md):
        artifacts.append({"path": path.name, "size_bytes": path.stat().st_size, "sha256": sha256_file(path)})
    receipt = output / "WIKIDEBIA_RECUS_ARCHIVES.json"
    write_json(
        receipt,
        {
            "release": f"WIKIDEBIA_{versions['norm']}",
            "generated_date": dt.date.today().isoformat(),
            "versions": versions,
            "artifacts": artifacts,
        },
    )
    return {path.name: path for path in (norms_md, validator_md, receipt)}


def migrate_private_files(root: Path, backup: Path) -> None:
    private = root / "private" / "pywikibot"
    private.mkdir(parents=True, exist_ok=True)
    for name in ("user-config.py", "user-password.cfg"):
        source = root / name
        target = private / name
        if not source.exists():
            continue
        if target.exists():
            destination = backup / "legacy-secrets" / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source), destination)
        else:
            shutil.move(str(source), target)
            target.chmod(0o600)


def migrate_legacy_debate_inbox(root: Path, backup: Path) -> None:
    legacy = root / "incoming" / "debates"
    if not legacy.exists():
        return
    if not legacy.is_dir():
        raise ManagementError("incoming/debates existe mais n’est pas un dossier")
    entries = sorted(legacy.iterdir())
    unsupported = [item.name for item in entries if not item.is_file() or item.suffix.casefold() != ".zip"]
    if unsupported:
        raise ManagementError(
            "Migration de incoming/debates bloquée par des entrées non ZIP : " + ", ".join(unsupported)
        )
    incoming = root / "incoming"
    incoming.mkdir(parents=True, exist_ok=True)
    for source in entries:
        target = incoming / source.name
        if target.exists() and sha256_file(target) != sha256_file(source):
            collision = backup / "legacy-incoming-collisions" / source.name
            collision.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, collision)
            raise ManagementError(
                f"Collision pendant la migration de {source.name}; copie conservée dans {collision.relative_to(root)}"
            )
    for source in entries:
        target = incoming / source.name
        if target.exists():
            source.unlink()
        else:
            shutil.move(str(source), target)
    legacy.rmdir()


def backup_root_template_files(root: Path, backup: Path) -> None:
    targets = [root / name for name in ("wikidebia", ".gitignore", "README.md", "requirements-runtime.txt")]
    targets.extend([root / "config" / "wikidebia.example.json", root / ".github"])
    for target in targets:
        if not target.exists() and not target.is_symlink():
            continue
        relative = target.relative_to(root)
        destination = backup / "previous-root" / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        if target.is_dir():
            shutil.copytree(target, destination, dirs_exist_ok=True)
        else:
            shutil.copy2(target, destination)


def install_root_template(root: Path, kit: Path) -> None:
    template = kit / "root_template"
    if not template.is_dir():
        raise ManagementError("Le nouveau kit ne contient pas root_template/")
    for source in sorted(template.rglob("*")):
        relative = source.relative_to(template)
        target = root / relative
        if source.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        if relative.as_posix() == "config/wikidebia.local.json":
            continue
        shutil.copy2(source, target)
    launcher = root / "wikidebia"
    if launcher.is_file():
        launcher.chmod(launcher.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP)


def _replace_path(source: Path, target: Path, backup_root: Path) -> None:
    if target.exists() or target.is_symlink():
        destination = backup_root / "previous" / target.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(target), destination)
    shutil.move(str(source), target)


def assert_portable_sources(root: Path) -> None:
    needle = str(root.resolve())
    candidates: list[Path] = []
    for dirname in ("norms", "validator", "kit"):
        base = root / dirname
        if base.is_dir():
            candidates.extend(path for path in base.rglob("*") if path.is_file())
    for name in TRACKED_ROOT_FILES:
        path = root / name
        if path.is_file():
            candidates.append(path)
    for base in (root / "config", root / ".github"):
        if base.is_dir():
            candidates.extend(path for path in base.rglob("*") if path.is_file())
    for path in candidates:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if needle in text:
            raise ManagementError(f"Chemin absolu du projet conservé dans {path.relative_to(root)}")


def _normalized_git_path(value: str) -> str:
    path = value.replace("\\", "/")
    while path.startswith("./"):
        path = path[2:]
    return PurePosixPath(path).as_posix()


def forbidden_git_path(value: str) -> bool:
    path = _normalized_git_path(value)
    return (
        path in FORBIDDEN_GIT_EXACT
        or path.casefold().endswith(".lwp")
        or any(path == prefix.rstrip("/") or path.startswith(prefix) for prefix in FORBIDDEN_GIT_PREFIXES)
    )


def gitignore_missing_rules(root: Path) -> list[str]:
    path = root / ".gitignore"
    if not path.is_file():
        return list(REQUIRED_GITIGNORE_RULES)
    active = {line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip() and not line.lstrip().startswith("#")}
    return [rule for rule in REQUIRED_GITIGNORE_RULES if rule not in active]


def git_is_repo(root: Path) -> bool:
    return (root / ".git").is_dir()


def git_tracked_forbidden_paths(root: Path) -> list[str]:
    if not git_is_repo(root):
        return []
    result = run(["git", "ls-files", "-z"], cwd=root, capture=True, check=False)
    if result.returncode != 0:
        return []
    return sorted(path for path in result.stdout.split("\0") if path and forbidden_git_path(path))


def git_unignored_forbidden_paths(root: Path) -> list[str]:
    if not git_is_repo(root):
        return []
    result = run(
        ["git", "ls-files", "--others", "--exclude-standard", "-z"],
        cwd=root,
        capture=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return sorted(path for path in result.stdout.split("\0") if path and forbidden_git_path(path))


def git_security_issues(root: Path) -> list[str]:
    issues: list[str] = []
    missing = gitignore_missing_rules(root)
    if missing:
        issues.append("Règles .gitignore manquantes : " + ", ".join(missing))
    tracked = git_tracked_forbidden_paths(root)
    if tracked:
        issues.append("Fichiers locaux ou sensibles encore suivis par Git : " + ", ".join(tracked))
    unignored = git_unignored_forbidden_paths(root)
    if unignored:
        issues.append("Fichiers locaux ou sensibles non ignorés : " + ", ".join(unignored))
    return issues


def prepare_git_security(root: Path) -> None:
    missing = gitignore_missing_rules(root)
    if missing:
        raise ManagementError("Règles de sécurité absentes du .gitignore : " + ", ".join(missing))
    tracked = git_tracked_forbidden_paths(root)
    if tracked:
        for offset in range(0, len(tracked), 100):
            run(
                ["git", "rm", "-r", "--cached", "--ignore-unmatch", "--", *tracked[offset:offset + 100]],
                cwd=root,
            )
        print("Fichiers locaux retirés de l’index Git sans suppression locale : " + ", ".join(tracked), file=sys.stderr)
    remaining = git_security_issues(root)
    if remaining:
        raise ManagementError("Contrôle de sécurité Git échoué : " + " | ".join(remaining))


def git_has_origin(root: Path) -> bool:
    if not git_is_repo(root):
        return False
    result = run(["git", "remote", "get-url", "origin"], cwd=root, capture=True, check=False)
    return result.returncode == 0 and bool(result.stdout.strip())


def ensure_git_identity(root: Path) -> None:
    defaults = {
        "user.name": "Wikidéb’IA",
        "user.email": "wikidebia@localhost",
    }
    for key, default in defaults.items():
        result = run(["git", "config", "--get", key], cwd=root, capture=True, check=False)
        if result.returncode != 0 or not result.stdout.strip():
            run(["git", "config", "--local", key, default], cwd=root)


def git_push_current_branch(root: Path, *, strict: bool) -> bool:
    if not git_has_origin(root):
        message = (
            "Aucun remote origin n’est configuré. Utilisez ./wikidebia github-init URL_DU_DEPOT."
        )
        if strict:
            raise ManagementError(message)
        print("Dépôt Git mis à jour localement. " + message, file=sys.stderr)
        return False
    branch = run(["git", "branch", "--show-current"], cwd=root, capture=True).stdout.strip() or "main"
    result = run(
        ["git", "push", "-u", "origin", branch],
        cwd=root,
        capture=True,
        check=False,
        env={"GIT_TERMINAL_PROMPT": "0"},
    )
    if result.returncode == 0:
        return True
    detail = (result.stderr or result.stdout or "échec d’authentification inconnu").strip()
    message = (
        "Push GitHub non effectué. Le commit reste local. Authentifiez GitHub CLI avec "
        "`gh auth login -h github.com -p https`, puis exécutez `gh auth setup-git --hostname github.com` "
        "et `./wikidebia github-sync`. Détail Git : " + detail
    )
    if strict:
        raise ManagementError(message)
    print("AVERTISSEMENT : " + message, file=sys.stderr)
    return False


def git_commit_and_push(root: Path, message: str, *, push: bool) -> bool:
    if not git_is_repo(root):
        run(["git", "init", "-b", "main"], cwd=root)
    ensure_git_identity(root)
    prepare_git_security(root)
    run(["git", "add", "-A"], cwd=root)
    tracked_after_add = git_tracked_forbidden_paths(root)
    if tracked_after_add:
        raise ManagementError("git add a tenté de suivre des fichiers interdits : " + ", ".join(tracked_after_add))
    status = run(["git", "status", "--porcelain"], cwd=root, capture=True).stdout.strip()
    if status:
        run(["git", "commit", "-m", message], cwd=root)
    return git_push_current_branch(root, strict=False) if push else False


def update_sources(root: Path, archive: Path | None, *, allow_downgrade: bool, no_push: bool, no_git: bool) -> dict[str, str]:
    components, input_files, workspace = collect_update_payload(root, archive)
    try:
        versions = verify_version_set(components, root, allow_downgrade)
        staged = extract_components(components, workspace)
        test_staged_components(root, staged)
        generated = generate_readable_sources(root, staged, versions, components)

        backup = root / "archives" / "updates" / f"{timestamp()}-{versions['norm']}"
        backup.mkdir(parents=True, exist_ok=True)
        migrate_private_files(root, backup)
        migrate_legacy_debate_inbox(root, backup)
        backup_root_template_files(root, backup)

        installed: list[str] = []
        try:
            for name in ("norms", "validator", "kit"):
                _replace_path(staged[name], root / name, backup)
                installed.append(name)
        except Exception:
            for name in reversed(installed):
                current = root / name
                if current.exists():
                    shutil.rmtree(current)
                previous = backup / "previous" / name
                if previous.exists():
                    shutil.move(str(previous), current)
            raise
        install_root_template(root, root / "kit")
        write_runtime_marker_if_ready(root)
        for name, source in generated.items():
            target = root / name
            if target.exists():
                destination = backup / "previous" / name
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(target), destination)
            shutil.copy2(source, target)

        incoming_archive = backup / "incoming"
        incoming_archive.mkdir(parents=True, exist_ok=True)
        updates_dir = root / "updates"
        for item in list(updates_dir.iterdir()):
            shutil.move(str(item), incoming_archive / item.name)
        for item in input_files:
            if item.parent != updates_dir and item.exists():
                shutil.copy2(item, incoming_archive / item.name)

        assert_portable_sources(root)
        if not no_git:
            git_commit_and_push(
                root,
                f"Mise à jour Wikidéb’IA {versions['norm']} / {versions['validator']} / {versions['kit']}",
                push=not no_push,
            )
        return versions
    finally:
        shutil.rmtree(workspace, ignore_errors=True)


def load_local_settings(root: Path) -> dict[str, Any]:
    path = root / "config" / "wikidebia.local.json"
    if not path.is_file():
        return {}
    return json_load(path)


def ensure_credentials(root: Path) -> Path:
    private = root / "private" / "pywikibot"
    private.mkdir(parents=True, exist_ok=True)
    for name in ("user-config.py", "user-password.cfg"):
        legacy = root / name
        target = private / name
        if legacy.is_file() and not target.exists():
            shutil.move(str(legacy), target)
            target.chmod(0o600)
    if not (private / "user-config.py").is_file():
        raise ManagementError("private/pywikibot/user-config.py est absent")
    return private


def find_debate_archive(root: Path, debate_identifier: str | None) -> Path:
    incoming = root / "incoming"
    incoming.mkdir(parents=True, exist_ok=True)
    candidates = sorted(path for path in incoming.iterdir() if path.is_file() and path.suffix.casefold() == ".zip")

    if debate_identifier is not None:
        identifier = debate_identifier.strip()
        if identifier.casefold().endswith(".zip"):
            raise ManagementError("Indiquez l’identifiant du débat sans l’extension .zip")
        if not re.fullmatch(r"[A-Za-z0-9_.-]+", identifier):
            raise ManagementError("Identifiant de débat invalide; caractères admis : lettres, chiffres, _, - et .")
        archive = incoming / f"{identifier}.zip"
        if not archive.is_file():
            available = ", ".join(path.stem for path in candidates) or "aucun"
            raise ManagementError(f"Archive introuvable : incoming/{identifier}.zip; identifiants disponibles : {available}")
        return archive

    if len(candidates) == 1:
        return candidates[0]
    if not candidates:
        raise ManagementError("Aucune archive ZIP trouvée dans incoming/")
    available = ", ".join(path.stem for path in candidates)
    raise ManagementError(
        "Plusieurs archives ZIP sont présentes dans incoming/. "
        f"Relancez avec ./wikidebia publish IDENTIFIANT. Identifiants disponibles : {available}"
    )


def locate_package_root(extracted: Path) -> Path:
    manifests = sorted(extracted.rglob("manifest.json"))
    if len(manifests) != 1:
        raise ManagementError(f"Le ZIP de débat doit contenir exactement un manifest.json; trouvé : {len(manifests)}")
    return manifests[0].parent


def install_debate_corpus(root: Path, archive: Path) -> tuple[str, Path]:
    stage = root / ".state" / "debates" / f"{timestamp()}-{sha256_file(archive)[:12]}"
    stage.mkdir(parents=True, exist_ok=True)
    safe_extract(archive, stage)
    package_root = locate_package_root(stage)
    manifest = json_load(package_root / "manifest.json")
    debate_id = str(manifest.get("debate_id") or "").strip()
    if not debate_id or not re.fullmatch(r"[A-Za-z0-9_.-]+", debate_id):
        raise ManagementError("debate_id absent ou impropre à un nom de dossier")
    # Le nom du ZIP sert uniquement à sélectionner l’archive. Le manifeste reste
    # l’autorité pour l’identité du débat, notamment pour les anciennes archives
    # dont le nom contient des suffixes descriptifs ou une date.
    target = root / "corpus" / debate_id
    if target.is_dir() and sha256_tree(target) == sha256_tree(package_root):
        shutil.rmtree(stage, ignore_errors=True)
        return debate_id, target
    if target.exists():
        backup = root / "archives" / "debates" / f"{timestamp()}-{debate_id}" / "previous-corpus"
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(target), backup)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(package_root, target)
    shutil.rmtree(stage, ignore_errors=True)
    return debate_id, target


def scope_values(scope: str) -> tuple[list[str], list[str]]:
    mapping = {
        "all": (["fr", "en"], []),
        "fr": (["fr"], []),
        "en": (["en"], []),
        "fr-debate": (["fr"], ["debate"]),
        "en-debate": (["en"], ["debate"]),
    }
    return mapping[scope]


def publication_config(root: Path, debate_id: str, scope: str, run_dir: Path) -> Path:
    settings = load_local_settings(root)
    languages, page_types = scope_values(scope)
    users = settings.get("expected_users") or {"fr": "ChatGPT", "en": "ChatGPT"}
    summaries = settings.get("edit_summaries") or {
        "fr": "Contenu généré par ChatGPT 5.6",
        "en": "Content generated by ChatGPT 5.6",
    }
    sites = {language: {"code": language, "expected_user": str(users.get(language) or "ChatGPT")} for language in languages}
    config = {
        "kit_version": KIT_VERSION,
        "project_root": ".",
        "family": str(settings.get("family") or "wikidebates"),
        "family_file": "kit/families/wikidebates_family.py",
        "pywikibot_dir": "private/pywikibot",
        "sites": sites,
        "change_tags": ["chatgpt"],
        "verification_attempts": int(settings.get("verification_attempts", 8)),
        "verification_delay_seconds": float(settings.get("verification_delay_seconds", 2)),
        "write_delay_seconds": float(settings.get("write_delay_seconds", 0.5)),
        "debate_id": debate_id,
        "corpus_root": f"corpus/{debate_id}",
        "logs_dir": f"logs/{debate_id}/{run_dir.name}",
        "validator": {
            "command": [".venv/bin/python", "validator/scripts/wikidebia_validate.py", "validate"],
            "required_version": VALIDATOR_VERSION,
            "scopes": ["schema", "coherence", "graph", "files", "batches", "sources", "wikicode", "bilingual", "editorial", "workflow"],
            "max_warnings": 0,
            "fingerprint_path": "validator",
        },
        # Les versions déclarées par le corpus sont une provenance historique.
        # La sécurité repose sur le validateur installé, sa version réelle et son
        # rapport positif, non sur une réécriture du manifeste au fil des mises à jour.
        "manifest_requirements": {},
        "operation": {
            "id": f"publish_{scope.replace('-', '_')}",
            "kind": "full_page",
            "languages": languages,
            "page_types": page_types,
            "language_order": languages,
            "page_type_order": ["debate", "argument"],
            "source_path_field": "file_path",
            "create_missing": True,
            "update_existing": False,
            "edit_summaries": {language: str(summaries[language]) for language in languages},
            "remote_title_overrides": {language: {} for language in languages},
        },
        "publication_profile": "norm_1_2_direct_interlanguage",
    }
    path = run_dir / "config.json"
    write_json(path, config)
    return path


def publisher_command(root: Path, config: Path, *args: str) -> list[str]:
    return [python_command(root), "kit/scripts/wikidebia_publish.py", "--config", str(config.relative_to(root)), *args]


def publish_debate(root: Path, debate_identifier: str | None, scope: str, assume_yes: bool, keep_zip: bool) -> dict[str, int]:
    ensure_credentials(root)
    archive = find_debate_archive(root, debate_identifier)
    debate_id, _ = install_debate_corpus(root, archive)
    try:
        archive_display = archive.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        archive_display = archive.name
    print(f"Archive sélectionnée : {archive_display}")
    print(f"Identifiant interne du débat : {debate_id}")
    run_dir = root / "plans" / debate_id / timestamp()
    run_dir.mkdir(parents=True, exist_ok=True)
    config = publication_config(root, debate_id, scope, run_dir)
    plan_path = run_dir / "plan.json"
    run(publisher_command(root, config, "--mode", "plan", "--plan-output", str(plan_path.relative_to(root))), cwd=root)
    plan = json_load(plan_path)
    if plan.get("blockers"):
        raise ManagementError(f"Le plan contient {len(plan['blockers'])} bloqueur(s); voir {plan_path.relative_to(root)}")
    counts = plan.get("counts") or {}
    print(json.dumps(counts, ensure_ascii=False, indent=2))
    # Le plan signé est transmis automatiquement au moteur ; aucune invite interactive n’est utilisée.

    receipt_path = run_dir / "debate-test-receipt.json"
    french_create = any(
        row.get("language") == "fr" and row.get("page_type") == "debate" and row.get("operation") == "create"
        for row in plan.get("actions", [])
    )
    if french_create:
        run(
            publisher_command(
                root,
                config,
                "--mode", "debate-test",
                "--execute",
                "--plan-input", str(plan_path.relative_to(root)),
                "--confirm-plan-sha256", str(plan["plan_sha256"]),
                "--debate-test-receipt-output", str(receipt_path.relative_to(root)),
            ),
            cwd=root,
        )

    publish_args = [
        "--mode", "publish",
        "--execute",
        "--plan-input", str(plan_path.relative_to(root)),
        "--confirm-plan-sha256", str(plan["plan_sha256"]),
    ]
    if french_create:
        publish_args.extend(["--debate-test-receipt", str(receipt_path.relative_to(root))])
    result = run(publisher_command(root, config, *publish_args), cwd=root, capture=True)
    output = (result.stdout or "").strip().splitlines()
    published = json.loads(output[-1]) if output else {}
    if french_create:
        published["created"] = int(published.get("created", 0)) + 1
        published["skipped"] = max(0, int(published.get("skipped", 0)) - 1)
    if not keep_zip:
        destination = root / "archives" / "debates" / f"{timestamp()}-{debate_id}" / archive.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        if archive.resolve().is_relative_to(root.resolve()):
            shutil.move(str(archive), destination)
        else:
            shutil.copy2(archive, destination)
    return {str(key): int(value) for key, value in published.items()}



def remote_update_config(root: Path, debate_id: str, scope: str, run_dir: Path) -> Path:
    settings = load_local_settings(root)
    languages = ["fr", "en"] if scope == "all" else [scope]
    users = settings.get("expected_users") or {"fr": "ChatGPT", "en": "ChatGPT"}
    sites = {language: {"code": language, "expected_user": str(users.get(language) or "ChatGPT")} for language in languages}
    config = {
        "kit_version": KIT_VERSION,
        "project_root": ".",
        "family": str(settings.get("family") or "wikidebates"),
        "family_file": "kit/families/wikidebates_family.py",
        "pywikibot_dir": "private/pywikibot",
        "sites": sites,
        "languages": languages,
        "debate_id": debate_id,
        "corpus_root": f"corpus/{debate_id}",
        "logs_dir": f"logs/{debate_id}/{run_dir.name}",
        "published_state_dir": ".state/published",
        "receipts_dir": ".state/receipts",
        "validator": {
            "command": [".venv/bin/python", "validator/scripts/wikidebia_validate.py", "validate"],
            "required_version": VALIDATOR_VERSION,
            "scopes": ["schema", "coherence", "graph", "files", "batches", "sources", "wikicode", "bilingual", "editorial", "workflow"],
        },
        "edit_summaries": {
            "fr": "Corrections",
            "en": "Corrections",
        },
    }
    path = run_dir / "config.json"
    write_json(path, config)
    return path


def remote_update_command(root: Path, config: Path, *args: str) -> list[str]:
    return [python_command(root), "kit/scripts/wikidebia_update.py", "--config", str(config.relative_to(root)), *args]


def _prepare_update_corpus(root: Path, debate_identifier: str | None) -> tuple[str, Path | None]:
    incoming = root / "incoming"
    archive: Path | None = None
    if debate_identifier:
        exact = incoming / f"{debate_identifier}.zip"
        if exact.is_file():
            archive = exact
        elif (root / "corpus" / debate_identifier / "manifest.json").is_file():
            return debate_identifier, None
        else:
            try:
                archive = find_debate_archive(root, debate_identifier)
            except ManagementError:
                raise ManagementError(f"Corpus installé ou archive introuvable pour {debate_identifier}")
    else:
        zips = sorted(incoming.glob("*.zip")) if incoming.is_dir() else []
        if len(zips) == 1:
            archive = zips[0]
        else:
            raise ManagementError("Indiquez l’identifiant du débat à reprendre")
    debate_id, _ = install_debate_corpus(root, archive)
    return debate_id, archive


def update_debate(root: Path, debate_identifier: str | None, scope: str, assume_yes: bool, no_delete: bool, only_delete: bool, dry_run: bool, keep_zip: bool) -> dict[str, Any]:
    ensure_credentials(root)
    if no_delete and only_delete:
        raise ManagementError("--no-delete et --only-delete sont incompatibles")
    debate_id, archive = _prepare_update_corpus(root, debate_identifier)
    run_dir = root / "plans" / debate_id / timestamp()
    run_dir.mkdir(parents=True, exist_ok=True)
    config = remote_update_config(root, debate_id, scope, run_dir)
    plan_path = run_dir / "update-plan.json"
    flags: list[str] = []
    if no_delete:
        flags.append("--no-delete")
    if only_delete:
        flags.append("--only-delete")
    result = run(remote_update_command(root, config, "--mode", "plan", "--plan-output", str(plan_path.relative_to(root)), *flags), cwd=root, capture=True, check=False)
    if result.returncode not in {0, 3}:
        raise ManagementError((result.stderr or result.stdout or "Plan de reprise impossible").strip())
    plan = json_load(plan_path)
    print(json.dumps(plan.get("counts") or {}, ensure_ascii=False, indent=2))
    if dry_run:
        return {"status": "dry_run", "plan": str(plan_path.relative_to(root)), "plan_sha256": plan["plan_sha256"], "counts": plan.get("counts") or {}}
    if (plan.get("operations") or {}).get("blocked"):
        raise ManagementError(f"Le plan contient {len(plan['operations']['blocked'])} opération(s) bloquée(s); voir {plan_path.relative_to(root)}")
    # The signed plan hash is transmitted directly to the executor.  The legacy
    # --yes option remains accepted as a no-op, but update is deliberately
    # non-interactive so unattended and ordinary runs behave identically.
    _ = assume_yes
    execute = run(remote_update_command(root, config, "--mode", "execute", "--plan-input", str(plan_path.relative_to(root)), "--confirm-plan-sha256", str(plan["plan_sha256"]), *flags), cwd=root, capture=True)
    lines = (execute.stdout or "").strip().splitlines()
    counts = json.loads(lines[-1]) if lines else {}
    if archive is not None and not keep_zip:
        destination = root / "archives" / "debates" / f"{timestamp()}-{debate_id}" / archive.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(archive), destination)
    return {"status": "executed", "plan": str(plan_path.relative_to(root)), "plan_sha256": plan["plan_sha256"], "counts": counts}

def github_init(root: Path, remote: str, private: bool) -> None:
    if not git_is_repo(root):
        run(["git", "init", "-b", "main"], cwd=root)
    if git_has_origin(root):
        current = run(["git", "remote", "get-url", "origin"], cwd=root, capture=True).stdout.strip()
        if current != remote:
            raise ManagementError(f"origin existe déjà et pointe vers {current}")
    else:
        run(["git", "remote", "add", "origin", remote], cwd=root)
    # Le caractère privé/public est défini lors de la création du dépôt distant.
    _ = private
    assert_portable_sources(root)
    git_commit_and_push(root, "Initialisation du dépôt Wikidéb’IA", push=False)
    git_push_current_branch(root, strict=True)


def github_sync(root: Path) -> None:
    if not git_is_repo(root):
        raise ManagementError("Le dossier n’est pas un dépôt Git")
    assert_portable_sources(root)
    # Cette commande sert aussi à terminer une mise à jour installée avec --no-git :
    # elle nettoie l’index, ajoute les sources sûres et crée le commit avant le push.
    git_commit_and_push(root, "Synchronisation sécurisée Wikidéb’IA", push=False)
    git_push_current_branch(root, strict=True)


def doctor(root: Path) -> dict[str, Any]:
    issues: list[str] = []
    versions = current_versions(root)
    if not versions:
        issues.append("VERSIONS.json introuvable")
    if (root / "user-config.py").exists() or (root / "user-password.cfg").exists():
        issues.append("Secrets Pywikibot encore présents à la racine")
    if not (root / "private" / "pywikibot" / "user-config.py").is_file():
        issues.append("private/pywikibot/user-config.py absent")
    runtime = runtime_environment_report(root)
    if not runtime.get("requirements_sha256"):
        issues.append("requirements-runtime.txt absent")
    if not runtime.get("python_available"):
        issues.append(".venv/bin/python absent ou inutilisable")
    missing = runtime.get("missing_modules") or []
    if missing:
        issues.append("Modules Python manquants dans .venv : " + ", ".join(str(item) for item in missing))
    if runtime.get("probe_error"):
        issues.append("Diagnostic de .venv impossible : " + str(runtime["probe_error"]))
    try:
        assert_portable_sources(root)
    except ManagementError as exc:
        issues.append(str(exc))
    issues.extend(git_security_issues(root))
    updates = root / "updates"
    update_count = len(list(updates.iterdir())) if updates.is_dir() else 0
    return {
        "versions": versions,
        "runtime_environment": runtime,
        "git_repository": git_is_repo(root),
        "git_origin": git_has_origin(root),
        "updates_entries": update_count,
        "issues": issues,
        "status": "passed" if not issues else "failed",
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="wikidebia", description="Gestion portable de Wikidéb’IA")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help=argparse.SUPPRESS)
    sub = parser.add_subparsers(dest="command", required=True)

    publish = sub.add_parser("publish", help="Valider, planifier et publier un ZIP de débat")
    publish.add_argument("debate_identifier", nargs="?", help="Nom du ZIP sans .zip; facultatif si incoming/ contient un seul ZIP. Le debate_id interne peut être différent.")
    publish.add_argument("--scope", choices=SCOPES, default="all")
    publish.add_argument("--yes", action="store_true", help=argparse.SUPPRESS)
    publish.add_argument("--keep-zip", action="store_true", help="Ne pas archiver le ZIP après succès")

    update = sub.add_parser("update", help="Reprendre un débat déjà publié avec créations, mises à jour et retraits contrôlés")
    update.add_argument("debate_identifier", nargs="?", help="Identifiant du débat installé ou nom du ZIP sans .zip")
    update.add_argument("--scope", choices=("all", "fr", "en"), default="all")
    update.add_argument("--yes", action="store_true", help=argparse.SUPPRESS)
    update.add_argument("--no-delete", action="store_true", help="Exécuter la reprise sans suppressions finales")
    update.add_argument("--only-delete", action="store_true", help="N’exécuter que les retraits sûrs et redirections de fusion")
    update.add_argument("--dry-run", action="store_true", help="Produire seulement le plan signé")
    update.add_argument("--keep-zip", action="store_true", help="Ne pas archiver le ZIP après succès")

    upgrade = sub.add_parser("upgrade", help="Installer les composants déposés dans updates/")
    upgrade.add_argument("archive", nargs="?", type=Path, help="Archive complète facultative")
    upgrade.add_argument("--allow-downgrade", action="store_true")
    upgrade.add_argument("--no-push", action="store_true", help="Créer le commit sans pousser vers origin")
    upgrade.add_argument("--no-git", action="store_true", help="Ne pas créer de commit Git")

    github = sub.add_parser("github-init", help="Initialiser le dépôt et pousser vers GitHub")
    github.add_argument("remote", help="URL Git du dépôt, par exemple git@github.com:COMPTE/wikidebia.git")
    github.add_argument("--private", action="store_true", help="Documentation uniquement; la visibilité se règle sur GitHub")
    sub.add_parser("github-sync", help="Pousser les commits locaux vers origin après authentification")

    sub.add_parser("doctor", help="Contrôler l'installation portable")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = args.root.expanduser().resolve()
    if args.command == "publish":
        result = publish_debate(root, args.debate_identifier, args.scope, args.yes, args.keep_zip)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    if args.command == "update":
        result = update_debate(root, args.debate_identifier, args.scope, args.yes, args.no_delete, args.only_delete, args.dry_run, args.keep_zip)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    if args.command == "upgrade":
        versions = update_sources(
            root,
            args.archive,
            allow_downgrade=args.allow_downgrade,
            no_push=args.no_push,
            no_git=args.no_git,
        )
        print(json.dumps(versions, ensure_ascii=False, sort_keys=True))
        return 0
    if args.command == "github-init":
        github_init(root, args.remote, args.private)
        print("Dépôt GitHub initialisé et synchronisé.")
        return 0
    if args.command == "github-sync":
        github_sync(root)
        print("Dépôt GitHub synchronisé.")
        return 0
    report = doctor(root)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "passed" else 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ManagementError as exc:
        print(f"WIKIDEBIA BLOQUÉ : {exc}", file=sys.stderr)
        raise SystemExit(2)
