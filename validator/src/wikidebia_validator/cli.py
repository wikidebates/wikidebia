from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .codes import CODES
from .recalc import recalculate
from .validator import ALL_SCOPES, validate_package


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="wikidebia-validate", description="Valide un paquet de débat Wikidéb'IA sans le modifier.")
    sub = parser.add_subparsers(dest="command")
    validate = sub.add_parser("validate", help="Valider un paquet")
    validate.add_argument("package", type=Path)
    validate.add_argument("--scope", action="append", choices=["all", *ALL_SCOPES], help="Portée ciblée, répétable")
    validate.add_argument("--previous-status", help="État précédent à contrôler pour la transition")
    validate.add_argument("--format", choices=["text", "json", "both"], default="text")
    validate.add_argument("--text-output", type=Path)
    validate.add_argument("--json-output", type=Path)

    recalc = sub.add_parser("recalc", help="Recalcul explicite des données dérivées")
    recalc.add_argument("package", type=Path)
    recalc.add_argument("--graph", action="store_true", help="Recalculer compteurs, derived et empreinte structurelle")
    recalc.add_argument("--aggregates", action="store_true", help="Régénérer les agrégats depuis les pages individuelles")
    recalc.add_argument("--hashes", action="store_true", help="Recalculer les empreintes de pages et agrégats")
    recalc.add_argument("--write", action="store_true", help="Autoriser explicitement les écritures")

    catalog = sub.add_parser("codes", help="Afficher le catalogue stable des codes")
    catalog.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    command = args.command or "validate"
    if args.command is None:
        # Backward-compatible convenience: wikidebia-validate PACKAGE
        parser.print_help()
        return 2
    if command == "codes":
        if args.json:
            print(json.dumps(CODES, ensure_ascii=False, indent=2))
        else:
            for code, label in CODES.items():
                print(f"{code}\t{label}")
        return 0
    if command == "recalc":
        if not (args.graph or args.aggregates or args.hashes):
            parser.error("recalc exige au moins une option parmi --graph, --aggregates, --hashes")
        changed, report = recalculate(args.package, graph=args.graph, aggregates=args.aggregates, hashes=args.hashes, write=args.write)
        sys.stdout.write(report.to_text())
        if changed:
            print("Fichiers modifiés :")
            for rel in changed:
                print(f"- {rel}")
        return 1 if report.errors else 0
    report = validate_package(args.package, scopes=args.scope, previous_status=args.previous_status)
    text = report.to_text()
    data = json.dumps(report.to_dict(), ensure_ascii=False, indent=2) + "\n"
    if args.text_output:
        args.text_output.parent.mkdir(parents=True, exist_ok=True)
        args.text_output.write_text(text, encoding="utf-8", newline="\n")
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(data, encoding="utf-8", newline="\n")
    if args.format in {"text", "both"}:
        sys.stdout.write(text)
    if args.format in {"json", "both"}:
        sys.stdout.write(data)
    return 1 if report.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
