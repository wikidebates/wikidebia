from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any
from pathlib import Path


def portable_display_path(value: str | Path) -> str:
    """Retourne un chemin affichable sans enregistrer de chemin absolu local."""
    raw = Path(value).expanduser()
    if not raw.is_absolute():
        return raw.as_posix() or "."
    return raw.name or "."


from .codes import ACTIVE_CODES as CODES


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


LAYER_SCOPES = {
    "structural": {"schema", "coherence", "graph", "batches", "files", "wikicode", "bilingual", "workflow"},
    "documentary": {"sources", "wikicode", "editorial"},
    "semantic_review": {"bilingual", "editorial"},
}


def finding_layer(code: str) -> str:
    if code.startswith("WDV-SRC-") or code.startswith("WDV-DOC-") or code in {"WDV-MWK-012", "WDV-MWK-014", "WDV-MWK-021", "WDV-MWK-024"}:
        return "documentary"
    if code.startswith("WDV-EDT-") or code in {"WDV-BIL-006", "WDV-BIL-007", "WDV-BIL-008", "WDV-BIL-009"}:
        return "semantic_review"
    return "structural"


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

    def _layer_status(self, layer: str) -> dict[str, Any]:
        selected = set(self.scopes)
        if "all" in selected:
            selected = set().union(*LAYER_SCOPES.values())
        if layer == "fresh_archive":
            return {
                "status": "not_run",
                "errors": 0,
                "warnings": 0,
                "infos": 0,
                "meaning": "Ce statut ne peut être établi qu'après création puis réextraction de l'archive exacte; il est scellé par le workflow de release.",
            }
        if not (selected & LAYER_SCOPES[layer]):
            return {"status": "not_run", "errors": 0, "warnings": 0, "infos": 0, "meaning": "Les portées nécessaires n'ont pas été exécutées."}
        findings = [f for f in self.findings if finding_layer(f.code) == layer]
        errors = sum(f.level == "ERROR" for f in findings)
        warnings = sum(f.level == "WARNING" for f in findings)
        infos = sum(f.level == "INFO" for f in findings)
        status = "failed" if errors else ("passed_with_warnings" if warnings else "passed")
        meanings = {
            "structural": "Schémas, fichiers, graphe, wikicode, cohérence et workflow automatisables.",
            "documentary": "Identité, langue, usages, métadonnées et cohérence normalisée des ressources documentaires.",
            "semantic_review": "Heuristiques bilingues et présence/cohérence des attestations humaines encodées; ce statut ne remplace pas la lecture humaine elle-même.",
        }
        return {"status": status, "errors": errors, "warnings": warnings, "infos": infos, "meaning": meanings[layer]}

    def validation_layers(self) -> dict[str, Any]:
        return {layer: self._layer_status(layer) for layer in ("structural", "documentary", "semantic_review", "fresh_archive")}

    def to_dict(self) -> dict[str, Any]:
        return {
            "validator_version": self.validator_version,
            "package_root": self.package_root,
            "scopes": self.scopes,
            "result": "failed" if self.errors else ("passed_with_warnings" if self.warnings else "passed"),
            "result_scope": "automated_validation",
            "result_meaning": "Automated structural, documentary and encoded editorial checks only; bilingual semantic fidelity still depends on the required human review attestations.",
            "validation_layers": self.validation_layers(),
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
        lines.append("VALIDATION AUTOMATISÉE GLOBALE : " + ("ÉCHOUÉE" if self.errors else "RÉUSSIE"))
        lines.append("Statuts par couche :")
        for name, row in self.validation_layers().items():
            lines.append(f"- {name}: {row['status']} (erreurs={row['errors']}, avertissements={row['warnings']})")
        lines.append("Portée du verdict : contrôles automatisés et attestations encodées ; la fidélité sémantique bilingue requiert la revue humaine prévue par la norme.")
        return "\n".join(lines) + "\n"
