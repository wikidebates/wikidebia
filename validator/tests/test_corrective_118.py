from pathlib import Path

from wikidebia_validator.editorial import summary_style_issues, validate_summary_style_review_data


def test_short_varied_sentences_do_not_trigger_style_warning():
    text = "Un essai randomisé répartit les participants par tirage au sort. Le contrôle en aveugle limite l’influence des attentes. Ces méthodes servent à distinguer un effet mesuré d’un biais d’observation."
    assert summary_style_issues(text)["issues"] == []


def test_accumulated_long_sentences_trigger_heuristic_warning():
    text = "Cette première phrase développe une explication particulièrement longue dans laquelle plusieurs propositions sont ajoutées successivement afin de retarder l'idée principale et de produire un rythme volontairement lourd pour le lecteur non spécialiste. Cette deuxième phrase poursuit la même construction avec de nombreuses précisions secondaires qui pourraient être séparées, définies plus simplement et placées après l'énoncé direct de la thèse centrale du raisonnement présenté. Cette troisième phrase ajoute encore des distinctions méthodologiques, des précautions et des enchaînements abstraits sans offrir au lecteur une pause suffisante ni une formulation immédiatement accessible du mécanisme concret concerné."
    assert "long_sentence_accumulation" in summary_style_issues(text)["issues"]


def test_summary_style_review_requires_all_human_attestations():
    nodes = [{"id": "A0001"}]
    pages = {"A0001": {"fr"}}
    review = {"entries": [{"id": "A0001", "languages": {"fr": {"status": "approved", "thesis_first": True, "general_public_style": True, "sentence_rhythm_reviewed": True, "technical_terms_reviewed": True, "note": "Résumé relu et accessible au grand public."}}}]}
    assert validate_summary_style_review_data(review, nodes, pages) == []
    review["entries"][0]["languages"]["fr"]["technical_terms_reviewed"] = False
    assert any(x["reason"] == "technical_terms_reviewed" for x in validate_summary_style_review_data(review, nodes, pages))


def test_active_norm_is_current():
    root = Path(__file__).parents[1] / "normative_reference" / "01_normes"
    assert sorted(p.name for p in root.glob("WIKIDEBIA_NORME_CONSOLIDEE_*.md")) == ["WIKIDEBIA_NORME_CONSOLIDEE_1.2.35.md"]
