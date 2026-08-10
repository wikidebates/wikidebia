import json
from pathlib import Path
from wikidebia_validator.schema_validation import SchemaStore


def base_entry():
    return {
      'language':'en','page_id':'A0001','title':'A page title','page_origin':'new','search_reviewed':True,
      'search_queries':['query one','query two'],'search_scope_note':'Exact English academic terminology was checked.',
      'search_provenance':'fresh_recheck','search_provenance_note':'A fresh search was performed for this page.',
      'outcome':'known_name','name':'Argument from example',
      'evidence':[{'source':'Academic source','label_as_used':'Argument from example','locator':'p. 12'}],
      'same_reasoning_confirmed':True,'non_invented_label_confirmed':True,'language_fit_confirmed':True,
      'rationale':'The label is attested for this exact reasoning.',
      'page_reasoning_scope_summary':'The page argues from the specific example to the stated conclusion.',
      'literature_name_scope_summary':'The literature uses this label for the same specific inference and no broader family.',
      'scope_relation':'exact_match','scope_identity_confirmed':True,
    }


def test_name_review_12_accepts_exact_scope_identity():
    store=SchemaStore()
    data={'version':'wikidebia-argument-name-discovery-review-1.2','debate_id':'d','entries':[base_entry()]}
    assert store.validate(data,'argument_name_discovery_review.schema.json') == []


def test_name_review_12_rejects_broader_or_narrower_scope_for_known_name():
    store=SchemaStore()
    row=base_entry(); row['scope_relation']='narrower_than_page'; row['scope_identity_confirmed']=False
    data={'version':'wikidebia-argument-name-discovery-review-1.2','debate_id':'d','entries':[row]}
    assert store.validate(data,'argument_name_discovery_review.schema.json')
