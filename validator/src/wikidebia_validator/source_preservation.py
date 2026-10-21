"""Exact preservation checks; these never attest historical factual accuracy."""
from __future__ import annotations
import hashlib
from typing import Any
from .package import PackageContext
from .schema_validation import _valid_translation_source_preservation

def preserved_french_page(ctx: PackageContext, page: dict[str, Any], text: str) -> bool:
    if page.get('language') != 'fr' or not _valid_translation_source_preservation(ctx):
        return False
    receipt = ctx.load_json('data/source_preservation_receipt.json') or {}
    kind = page.get('page_type')
    row = next((r for r in receipt['pages'] if (r.get('page_id') == page.get('page_id') or kind == 'debate' and r.get('kind') == 'debate')), None)
    if not row:
        return False
    from .wikicode import _split_top_level, parse_template, WikiParseError
    try:
        original = ctx.safe_path(row['import_path']).read_text(encoding='utf-8')
        source = parse_template(original)
        target = parse_template(text)
        if source.name != target.name or source.values('interlangue'):
            return False
        parts = _split_top_level(target.raw[2:-2])
        links = [p for p in parts[1:] if p.split('=', 1)[0].strip() == 'interlangue']
        without = '{{' + '|'.join(p for p in parts if p not in links) + '}}'
        return len(links) == 1 and without == source.raw and text.strip() == target.raw
    except (OSError, ValueError, KeyError, WikiParseError):
        return False

def source_keywords(ctx: PackageContext) -> set[str]:
    if not _valid_translation_source_preservation(ctx):
        return set()
    lock = ctx.load_json('data/fr_page_metadata_lock.json') or {}
    return {term for row in [lock.get('debate') or {}, *lock.get('arguments', [])] for term in row.get('keywords', [])}
