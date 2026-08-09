from pathlib import Path


def test_future_translation_convention_literals():
    root = Path(__file__).resolve().parents[1]
    publish = (root / "scripts" / "wikidebia_publish.py").read_text()
    update = (root / "scripts" / "wikidebia_update.py").read_text()
    review = (root / "scripts" / "wikidebia_translation_review.py").read_text()
    assert "Translation of the French page: [[:fr:{source_title}|{source_title}]]" in publish
    assert "Ajout du lien interlangue vers la page anglaise : [[:en:{title}|{title}]]" in update
    assert 'TRANSLATED_CITATION_WARNING = "AI-translated quote"' in review
    assert '"translation_change_tag": "translated-fr"' in (root / "KIT_MANIFEST.json").read_text()


def test_retro_tag_accepts_legacy_and_new_summary_forms():
    root = Path(__file__).resolve().parents[1]
    retro = (root / "scripts" / "wikidebia_retro_tag.py").read_text()
    assert "def legacy_expected_summary" in retro
    assert "accepted_summaries" in retro
