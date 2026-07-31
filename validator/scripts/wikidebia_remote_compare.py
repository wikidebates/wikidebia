#!/usr/bin/env python3
"""Compare a Wikidéb'IA package with remote MediaWiki pages.

This utility is deliberately read-only. It never calls Page.save(), Page.put(),
Site.editpage(), or any write API. Existing Pywikibot configuration, cookies and
credentials may be used for authentication, but only GET/query operations are
performed by this program.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def sha256_text(text: str) -> str:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    if not normalized.endswith("\n"):
        normalized += "\n"
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def compact_wikitext(text: str) -> str:
    """A conservative comparison form; it does not parse or rewrite templates."""
    return "\n".join(line.rstrip() for line in text.replace("\r\n", "\n").replace("\r", "\n").strip().splitlines()) + "\n"


@dataclass
class Result:
    page_id: str
    language: str
    page_type: str
    local_title: str
    remote_title: str | None
    status: str
    remote_revision_id: int | None = None
    local_sha256: str | None = None
    remote_sha256: str | None = None
    exact_match: bool | None = None
    normalized_match: bool | None = None
    redirect_target: str | None = None
    error: str | None = None


def load_manifest(package: Path) -> dict[str, Any]:
    p = package / "manifest.json"
    if not p.is_file():
        raise SystemExit(f"manifest.json absent: {p}")
    return json.loads(p.read_text(encoding="utf-8"))


def load_fixture(fixture_dir: Path, lang: str, page_id: str) -> tuple[bool, bool, str | None, int | None, str | None]:
    p = fixture_dir / lang / f"{page_id}.wiki"
    if not p.is_file():
        return False, False, None, None, None
    return True, False, p.read_text(encoding="utf-8"), 1, None


def remote_fetch(site: Any, title: str) -> tuple[bool, bool, str | None, int | None, str | None]:
    import pywikibot  # imported only when remote mode is actually used

    page = pywikibot.Page(site, title)
    if not page.exists():
        return False, False, None, None, None
    is_redirect = page.isRedirectPage()
    target = None
    if is_redirect:
        try:
            target = page.getRedirectTarget().title()
        except Exception:
            target = None
    text = page.get(get_redirect=True)
    return True, is_redirect, text, page.latest_revision_id, target


def compare(args: argparse.Namespace) -> tuple[list[Result], dict[str, Any]]:
    package = Path(args.package).resolve()
    manifest = load_manifest(package)
    pages = manifest.get("pages", [])
    selected = []
    for page in pages:
        if args.language and page.get("language") != args.language:
            continue
        if args.page_type and page.get("page_type") != args.page_type:
            continue
        selected.append(page)
    if args.limit:
        selected = selected[: args.limit]

    sites: dict[str, Any] = {}
    if not args.fixture_dir:
        import pywikibot
        for lang in sorted({p.get("language") for p in selected}):
            sites[lang] = pywikibot.Site(lang, args.family)
            if args.login:
                sites[lang].login()

    results: list[Result] = []
    for page in selected:
        page_id = str(page.get("page_id"))
        lang = str(page.get("language"))
        local_title = str(page.get("canonical_title"))
        local_path = package / str(page.get("file_path"))
        local_text = local_path.read_text(encoding="utf-8")
        local_sha = sha256_text(local_text)
        try:
            if args.fixture_dir:
                exists, redirect, remote_text, revid, target = load_fixture(Path(args.fixture_dir), lang, page_id)
            else:
                exists, redirect, remote_text, revid, target = remote_fetch(sites[lang], local_title)
            if not exists:
                results.append(Result(page_id, lang, page.get("page_type"), local_title, None, "missing", local_sha256=local_sha))
                continue
            assert remote_text is not None
            remote_sha = sha256_text(remote_text)
            exact = local_sha == remote_sha
            normalized = compact_wikitext(local_text) == compact_wikitext(remote_text)
            status = "redirect" if redirect else ("identical" if exact else ("normalized_match" if normalized else "different"))
            results.append(Result(page_id, lang, page.get("page_type"), local_title, local_title, status, revid, local_sha, remote_sha, exact, normalized, target))
        except Exception as exc:  # report per page; never attempt a fallback write
            results.append(Result(page_id, lang, page.get("page_type"), local_title, None, "error", local_sha256=local_sha, error=f"{type(exc).__name__}: {exc}"))

    counts: dict[str, int] = {}
    for r in results:
        counts[r.status] = counts.get(r.status, 0) + 1
    summary = {
        "report_version": "1.0",
        "validator_version": "0.3.0",
        "mode": "fixture" if args.fixture_dir else "remote_read_only",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "package": str(package),
        "family": args.family,
        "selected_pages": len(selected),
        "counts": counts,
        "write_operations": 0,
        "publication_attempted": False,
    }
    return results, summary


def write_reports(results: list[Result], summary: dict[str, Any], text_path: Path | None, json_path: Path | None) -> None:
    payload = {"summary": summary, "results": [asdict(r) for r in results]}
    if json_path:
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    lines = [
        "COMPARAISON DISTANTE WIKIDÉB'IA — LECTURE SEULE",
        f"Mode : {summary['mode']}",
        f"Pages sélectionnées : {summary['selected_pages']}",
        "Publication tentée : NON",
        "Opérations d'écriture : 0",
        "",
        "Comptages :",
    ]
    for key in sorted(summary["counts"]):
        lines.append(f"- {key}: {summary['counts'][key]}")
    differences = [r for r in results if r.status not in {"identical", "normalized_match"}]
    if differences:
        lines += ["", "Anomalies ou différences :"]
        for r in differences:
            suffix = f" -> {r.redirect_target}" if r.redirect_target else ""
            err = f" ({r.error})" if r.error else ""
            lines.append(f"- [{r.language}] {r.page_id} {r.status}: {r.local_title}{suffix}{err}")
    text = "\n".join(lines) + "\n"
    if text_path:
        text_path.parent.mkdir(parents=True, exist_ok=True)
        text_path.write_text(text, encoding="utf-8", newline="\n")
    else:
        sys.stdout.write(text)


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Comparer un paquet Wikidéb'IA au wiki sans aucune publication.")
    p.add_argument("package", help="Dossier racine du paquet")
    p.add_argument("--family", default="wikidebia", help="Famille Pywikibot")
    p.add_argument("--language", choices=["fr", "en"])
    p.add_argument("--page-type", choices=["debate", "argument"])
    p.add_argument("--limit", type=int)
    p.add_argument("--login", action="store_true", help="Réutiliser explicitement la connexion configurée; lecture seule")
    p.add_argument("--fixture-dir", help="Mode de test hors ligne: snapshots <dir>/<lang>/<page_id>.wiki")
    p.add_argument("--text-output")
    p.add_argument("--json-output")
    return p


def main() -> int:
    args = parser().parse_args()
    results, summary = compare(args)
    write_reports(
        results,
        summary,
        Path(args.text_output) if args.text_output else None,
        Path(args.json_output) if args.json_output else None,
    )
    return 2 if summary["counts"].get("error", 0) else 0


if __name__ == "__main__":
    raise SystemExit(main())
