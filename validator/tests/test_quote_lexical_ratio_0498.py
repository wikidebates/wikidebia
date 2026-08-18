from wikidebia_validator.wikicode import _lexical_word_count


def test_quote_lexical_count_matches_translation_review_typographic_apostrophes():
    source = "Ces expériences sont intéressantes à plus d’un titre. D’abord, elles montrent à quel point le mode de scrutin peut influer sur le résultat des élections. Ensuite, elles font connaître des alternatives au scrutin uninominal à deux tours dont les déficiences ne sont plus à démontrer."
    translated = "These experiments are interesting in more than one respect. First, they show how much the voting system can influence election results. Second, they bring attention to alternatives to the two-round single-member system, whose shortcomings no longer need to be demonstrated."
    assert _lexical_word_count(source) == 45
    assert _lexical_word_count(translated) == 40
    assert _lexical_word_count(translated) / _lexical_word_count(source) == 40 / 45


def test_quote_lexical_count_strips_same_markup_as_translation_review():
    value = "Un mot <ref>note ignorée</ref> et {{Modèle|contenu ignoré}} puis [[Lien|texte ignoré]] d’un autre mot."
    # Un, mot, et, puis, d’un, autre, mot
    assert _lexical_word_count(value) == 7

import json
from pathlib import Path
from wikidebia_validator.package import PackageContext
from wikidebia_validator.report import Report
from wikidebia_validator.wikicode import _validate_citations_against_locks, parse_template


def _quote_context(tmp_path: Path, source: str, translated: str, ratio: float) -> PackageContext:
    (tmp_path / "data").mkdir(parents=True, exist_ok=True)
    expected = {
        "id": "A0005-C001",
        "parameters": [
            {"name": "quote", "value": translated, "source_name": "citation"},
            {"name": "authors", "value": "Eric Lombard", "source_name": "auteurs"},
            {"name": "warnings", "value": "AI-translated quote", "source_name": "avertissements-citation"},
        ],
        "warnings": "AI-translated quote",
        "source": {"source_parameters": [
            {"name": "citation", "value": source},
            {"name": "auteurs", "value": "Eric Lombard"},
        ]},
        "lexical_ratio": ratio,
        "quote_completeness_reviewed": True,
        "quote_completeness_note": "The complete quotation was reviewed from beginning to end.",
        "quote_low_ratio_reviewed": True,
        "quote_low_ratio_note": "The lexical ratio was reviewed and no content was omitted.",
    }
    (tmp_path / "data/en_content_lock.json").write_text(
        json.dumps({"arguments": [{"id": "A0005", "citations": [expected]}]}, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return PackageContext(root=tmp_path, report=Report("0.4.98", tmp_path.name, ["wikicode"]), cache={})


def test_quote_ratio_validation_uses_same_tokenizer_as_translation_review(tmp_path: Path):
    source = "Ces expériences sont intéressantes à plus d’un titre. D’abord, elles montrent à quel point le mode de scrutin peut influer sur le résultat des élections. Ensuite, elles font connaître des alternatives au scrutin uninominal à deux tours dont les déficiences ne sont plus à démontrer."
    translated = "These experiments are interesting in more than one respect. First, they show how much the voting system can influence election results. Second, they bring attention to alternatives to the two-round single-member system, whose shortcomings no longer need to be demonstrated."
    ratio = _lexical_word_count(translated) / _lexical_word_count(source)
    ctx = _quote_context(tmp_path, source, translated, ratio)
    tmpl = parse_template("""{{Argument
|quotes={{Quote
|quote=%s
|authors=Eric Lombard
|warnings=AI-translated quote
}}
}}""" % translated)
    _validate_citations_against_locks(ctx, tmpl, "output/en/arguments/A0005.wiki", "en", "A0005")
    assert not any(f.code == "WDV-MWK-024" for f in ctx.report.findings), ctx.report.to_text()


def test_quote_ratio_validation_still_detects_rendered_quote_change(tmp_path: Path):
    source = "Ces expériences sont intéressantes à plus d’un titre. D’abord, elles montrent à quel point le mode de scrutin peut influer sur le résultat des élections. Ensuite, elles font connaître des alternatives au scrutin uninominal à deux tours dont les déficiences ne sont plus à démontrer."
    translated = "These experiments are interesting in more than one respect. First, they show how much the voting system can influence election results. Second, they bring attention to alternatives to the two-round single-member system, whose shortcomings no longer need to be demonstrated."
    ratio = _lexical_word_count(translated) / _lexical_word_count(source)
    ctx = _quote_context(tmp_path, source, translated, ratio)
    altered = translated + " Additional words change the rendered quotation materially."
    tmpl = parse_template("""{{Argument
|quotes={{Quote
|quote=%s
|authors=Eric Lombard
|warnings=AI-translated quote
}}
}}""" % altered)
    _validate_citations_against_locks(ctx, tmpl, "output/en/arguments/A0005.wiki", "en", "A0005")
    assert any(f.code in {"WDV-MWK-021", "WDV-MWK-024"} for f in ctx.report.findings), ctx.report.to_text()
