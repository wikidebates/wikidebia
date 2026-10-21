"""French numeric dates must not bypass translation equivalence checks."""
from pathlib import Path
import sys
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from wikidebia_content_review import _citation_records
import wikidebia_translation_review as translation


def validate(source_date, target_date):
    original=_citation_records('{{Citation|citation=Une citation de test complète.|date='+source_date+'}}','A0001')[0]
    row=translation._blank_citation(original)
    row.update(status='approved', translated_citation='A complete test quotation.', translated_date=target_date,
        citation_translated=True, date_translated_or_language_neutral=True, preserved_parameters_unchanged=True,
        translation_warning_appended=True, quote_completeness_reviewed=True,
        quote_completeness_note='The complete source text and its historical date were compared.',
        reviewer='Reviewer', reviewed_at='2026-10-21',note='Historical date equivalence reviewed.')
    return translation._validate_citations([row],[original],'A0001')


@pytest.mark.parametrize('fr,en',[
 ('15/06/2011','15 June 2011'),('15/6/2011','15 June 2011'),
 ('24.08.2018','24 August 2018'),('11/2020','November 2020'),
 ('17 nov 2021','17 November 2021'),('17 nov. 2021','17 November 2021'),
 ('29/02/2024','29 February 2024'),('2013','2013'),
 ('15/06/2011','15/06/2011'),('June 2011','June 2011')])
def test_accepts_equivalent_historical_date_at_same_precision(fr,en):
    assert validate(fr,en)[0]['date']==en


@pytest.mark.parametrize('fr,en',[
 ('15/06/2011','16 June 2011'),('15/06/2011','15 July 2011'),
 ('15/06/2011','15 June 2012'),('11/2020','12 November 2020'),
 ('17 nov 2021','17 October 2021'),('24.08.2018','24 August 2019')])
def test_rejects_different_date_or_invented_precision(fr,en):
    with pytest.raises(translation.TranslationReviewError,match='même date'):
        validate(fr,en)


@pytest.mark.parametrize('fr',['31/02/2011','13/2020','31 février 2011','0000','été 2011','unknown'])
def test_unrecognized_date_cannot_silently_validate_a_translation(fr):
    with pytest.raises(translation.TranslationReviewError,match='Format de date source'):
        validate(fr,'15 June 2011')
