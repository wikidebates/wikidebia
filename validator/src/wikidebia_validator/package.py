from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

from .report import Report


@dataclass
class PackageContext:
    root: Path
    report: Report
    cache: dict[str, Any] = field(default_factory=dict)

    def safe_path(self, rel: str) -> Path | None:
        try:
            posix = PurePosixPath(rel)
        except Exception:
            self.report.error("WDV-FS-002", f"Chemin invalide : {rel!r}", path=rel)
            return None
        if posix.is_absolute() or ".." in posix.parts or "\\" in rel:
            self.report.error("WDV-FS-002", f"Chemin extérieur ou non portable : {rel}", path=rel)
            return None
        candidate = (self.root / Path(*posix.parts)).resolve()
        try:
            candidate.relative_to(self.root.resolve())
        except ValueError:
            self.report.error("WDV-FS-002", f"Chemin extérieur au paquet : {rel}", path=rel)
            return None
        return candidate

    def exists(self, rel: str) -> bool:
        p = self.safe_path(rel)
        return bool(p and p.exists())

    def read_bytes(self, rel: str, required: bool = False) -> bytes | None:
        p = self.safe_path(rel)
        if not p:
            return None
        if not p.is_file():
            if required:
                self.report.error("WDV-FS-001", "Fichier obligatoire manquant", path=rel)
            return None
        try:
            return p.read_bytes()
        except OSError as exc:
            self.report.error("WDV-FS-001", f"Lecture impossible : {exc}", path=rel)
            return None

    def read_text(self, rel: str, required: bool = False) -> str | None:
        raw = self.read_bytes(rel, required=required)
        if raw is None:
            return None
        if raw.startswith(b"\xef\xbb\xbf"):
            self.report.error("WDV-FS-005", "BOM UTF-8 interdit", path=rel)
        try:
            text = raw.decode("utf-8-sig")
        except UnicodeDecodeError as exc:
            self.report.error("WDV-FS-005", f"Encodage UTF-8 invalide : {exc}", path=rel)
            return None
        if b"\r" in raw:
            self.report.error("WDV-FS-005", "Fins de ligne CR/CRLF interdites ; LF requis", path=rel)
        if raw and not raw.endswith(b"\n"):
            self.report.error("WDV-FS-005", "Fin de ligne finale absente", path=rel)
        if raw.endswith(b"\n\n"):
            self.report.error("WDV-FS-005", "Plus d'une fin de ligne finale", path=rel)
        return text

    def load_json(self, rel: str, required: bool = False) -> Any | None:
        if rel in self.cache:
            return self.cache[rel]
        text = self.read_text(rel, required=required)
        if text is None:
            return None
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            self.report.error("WDV-SCH-001", f"JSON invalide : {exc.msg}", path=rel, pointer=f"ligne {exc.lineno}, colonne {exc.colno}")
            return None
        self.cache[rel] = data
        return data

    def load_jsonl(self, rel: str) -> list[tuple[int, Any]]:
        text = self.read_text(rel)
        if text is None:
            return []
        out = []
        for no, line in enumerate(text.splitlines(), 1):
            if not line.strip():
                continue
            try:
                out.append((no, json.loads(line)))
            except json.JSONDecodeError as exc:
                self.report.error("WDV-SCH-001", f"Ligne JSONL invalide : {exc.msg}", path=rel, pointer=f"ligne {no}")
        return out

    def sha256(self, rel: str) -> str | None:
        raw = self.read_bytes(rel)
        return hashlib.sha256(raw).hexdigest() if raw is not None else None

    def iter_files(self, pattern: str) -> Iterable[Path]:
        return self.root.glob(pattern)

    def relative(self, path: Path) -> str:
        return path.resolve().relative_to(self.root.resolve()).as_posix()

    def manifest(self) -> dict[str, Any] | None:
        data = self.load_json("manifest.json", required=True)
        return data if isinstance(data, dict) else None

    def core_paths(self) -> dict[str, str]:
        manifest = self.manifest() or {}
        core = manifest.get("core_files") or {}
        defaults = {
            "scope": "scope.json",
            "registry": "data/registre_debat.json",
            "graph_json": "graph/graphe_argumentatif.json",
            "graph_markdown": "graph/graphe_argumentatif.md",
            "sources": "data/sources.json",
        }
        return {k: core.get(k, v) for k, v in defaults.items()}

    def registry(self) -> dict[str, Any] | None:
        data = self.load_json(self.core_paths()["registry"], required=True)
        return data if isinstance(data, dict) else None

    def graph_projection(self) -> dict[str, Any] | None:
        data = self.load_json(self.core_paths()["graph_json"])
        return data if isinstance(data, dict) else None

    def sources(self) -> dict[str, Any] | None:
        data = self.load_json(self.core_paths()["sources"])
        return data if isinstance(data, dict) else None
