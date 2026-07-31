from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any
from pathlib import Path


def portable_display_path(value: str | Path) -> str:
    """Retourne un chemin affichable sans enregistrer de chemin absolu local."""
    raw = Path(value).expanduser()
    if not raw.is_absolute():
        return raw.as_posix() or "."
    # Un chemin absolu local ne doit jamais dépendre du dossier courant :
    # conserver uniquement le nom final évite toute fuite partielle de chemin.
    return raw.name or "."


from .codes import CODES


@dataclass(frozen=True)
class Finding:
    code: str
    level: str
    message: str
    path: str | None = None
    pointer: str | None = None
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class Report:
    def __init__(self, validator_version: str, package_root: str, scopes: list[str]):
        self.validator_version = validator_version
        self.package_root = package_root
        self.scopes = scopes
        self.findings: list[Finding] = []
        self.metrics: dict[str, Any] = {}

    def add(self, code: str, level: str, message: str, *, path: str | None = None,
            pointer: str | None = None, details: dict[str, Any] | None = None) -> None:
        if code not in CODES:
            code = "WDV-INT-001"
        self.findings.append(Finding(code, level, message, path, pointer, details or {}))

    def error(self, code: str, message: str, **kwargs: Any) -> None:
        self.add(code, "ERROR", message, **kwargs)

    def warning(self, code: str, message: str, **kwargs: Any) -> None:
        self.add(code, "WARNING", message, **kwargs)

    def info(self, code: str, message: str, **kwargs: Any) -> None:
        self.add(code, "INFO", message, **kwargs)

    @property
    def errors(self) -> int:
        return sum(f.level == "ERROR" for f in self.findings)

    @property
    def warnings(self) -> int:
        return sum(f.level == "WARNING" for f in self.findings)

    @property
    def infos(self) -> int:
        return sum(f.level == "INFO" for f in self.findings)

    def to_dict(self) -> dict[str, Any]:
        return {
            "validator_version": self.validator_version,
            "package_root": self.package_root,
            "scopes": self.scopes,
            "result": "failed" if self.errors else ("passed_with_warnings" if self.warnings else "passed"),
            "summary": {"errors": self.errors, "warnings": self.warnings, "infos": self.infos},
            "metrics": self.metrics,
            "findings": [f.to_dict() for f in self.findings],
        }

    def to_text(self) -> str:
        lines = [
            "VALIDATEUR WIKIDÉB'IA",
            f"Version : {self.validator_version}",
            f"Paquet : {self.package_root}",
            f"Portées : {', '.join(self.scopes)}",
            "",
        ]
        for f in sorted(self.findings, key=lambda x: ({"ERROR": 0, "WARNING": 1, "INFO": 2}[x.level], x.code, x.path or "", x.pointer or "")):
            loc = ""
            if f.path:
                loc += f" [{f.path}]"
            if f.pointer:
                loc += f" {f.pointer}"
            lines.append(f"{f.level} {f.code}{loc} — {f.message}")
        if not self.findings:
            lines.append("Aucune anomalie détectée.")
        lines += ["", f"Erreurs : {self.errors} | Avertissements : {self.warnings} | Informations : {self.infos}"]
        lines.append("VALIDATION GLOBALE : " + ("ÉCHOUÉE" if self.errors else "RÉUSSIE"))
        return "\n".join(lines) + "\n"
