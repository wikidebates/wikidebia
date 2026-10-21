"""Raccord au kit réel sans fabriquer de verrou FR ni d'approbation globale."""
from pathlib import Path
import copy, datetime, hashlib, json, sys
import mwparserfromhell as mw

O=Path(__file__).parent;W=O/'working-selected'
P=Path('/workspace/work/cannabis-interquotation-code')
R=Path('/workspace/work/cannabis-translation-verification-20261021/relecture-approfondie')
N=P/'.state/editorial-workspaces/cannabis/EN-CANNABIS-20261021'
sys.path.insert(0,str(P/'kit/scripts'))
import wikidebia_translation_review as tr
from wikidebia_content_review import _source_imports
from wikidebia_citation_passages import validate_translations

def load(p):return json.loads(p.read_text())
def save(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
LOW_RATIO_NOTES={
 'Q092':'Seconde comparaison effectuée : la source donne une phrase anglaise puis sa traduction française entre parenthèses. La cible conserve la phrase anglaise entière, state subsidy et organised crime compris ; elle ne répète pas son doublon français. Le rapport lexical de 0,55 ne signale donc pas une omission de proposition.',
 'Q120':'Seconde comparaison effectuée phrase par phrase : la source donne le paragraphe anglais puis sa traduction française entre crochets. La cible reprend intégralement le paragraphe anglais, réserves estimates vary, adultes et comparaisons 9–10 %, 20 %, 25 % et près de 30 % comprises. Seul le doublon français est omis ; pas de moitié de citation perdue.'
}
dest=N/'reviews/en/translation_review.pending.json'
assert not dest.exists(), 'Revue existante à préserver.'
reg,debate_source,arguments_source=_source_imports(N/'reviewed-copy')
provenance={r.get('page_id'):r for r in load(N/'reviewed-copy/data/import_provenance.json')['pages'] if r['kind']=='argument'}
meta=load(N/'reviewed-copy/data/fr_page_metadata_lock.json')
metadata={r['entity_id']:r for r in meta['arguments']}
sources={r['id']:r for r in arguments_source}
identity=load(R.parent/'identity-map.json')['rows']
native_by_delivery={r['delivery_id']:r['build_node_id'] for r in identity}
delivery_by_native={v:k for k,v in native_by_delivery.items()}
rows=load(W/'data/translation_pages.json');pages={r['id']:r for r in rows}
qdata=load(W/'data/translation_quotes.json')
notes={n['id']:n['note'] for p in sorted(R.glob('notes-*.json')) for n in load(p)}
passages=load(W/'data/translation_editorial_notes.json')
selections={r['delivery_id']:r for r in load(O/'page-documentary-selection-final.json')['rows']}
registry=load(O/'sources_en_selected.json');by_source={s['id']:s for s in registry['sources']}
native_quote_final=[];native_passage_final=[];coverage=[];classification=[]
out=dict(schema=tr.TRANSLATION_REVIEW_SCHEMA,schema_version='1.1',debate_id='cannabis',work_id='EN-CANNABIS-20261021',source_language='fr',target_language='en',status='draft',prepared_at=now,
    staging_only=True,preparation_method='Native review constructors and validators, source import and actual title lock; official prepare withheld because FR content lock is absent.',
    french_metadata_review_sha256=meta['review_sha256'],french_content_review_sha256=None,
    section_mapping=copy.deepcopy(tr.SECTION_MAP),vocabulary=load(W/'data/vocabulary_bilingual.json'),
    debate=tr._blank_debate(meta['debate'],debate_source),arguments=[],review_units=[],global_review=dict(all_entities_translated=False,all_equivalences_reviewed=False,all_selected_sources_verified=False,relations_and_occurrences_unchanged=True,no_final_pages_generated=False,remote_access_not_used=False,note='Pages de travail déjà présentes dans la livraison reprise ; recherches HTTP documentaires sans lecture éditoriale des pages anglaises cibles. Aucun rendu officiel et aucune publication.'),review_sha256=None)

def fields(pid):
    code=mw.parse((W/pages[pid]['target_relative_path']).read_text())
    t=next(t for t in code.filter_templates() if str(t.name).strip() in {'Argument','Debate'})
    def get(k):return str(t.get(k).value).strip() if t.has(k) else ''
    return code,t,get

_,dt,dget=fields('debate');dr=out['debate'];dr.update(canonical_title=pages['debate']['canonical_title_en'],topic=dget('topic'),complete_topic=dget('expanded-topic'),sections=[s.strip() for s in dget('sections').split(',') if s.strip()],keywords=[s.strip() for s in dget('keywords').split(',') if s.strip()],introduction=dget('introduction'),reviewer='Codex',reviewed_at=now,note=notes['debate'],content_equivalent_to_french=True)
for sid in selections['debate']['selected_source_ids']:
    dr['documentation'][by_source[sid]['type']].append(sid)
for node in [n for n in reg['graph']['nodes'] if n.get('status')=='active']:
    native=node['id'];pid=delivery_by_native[native];src=sources[native];frmeta=metadata[native]
    ident=next(r for r in identity if r['delivery_id']==pid)
    assert src['canonical_title'].replace('’',"'")==pages[pid]['source_title_fr'].replace('’',"'")
    assert src['import_sha256']==pages[pid]['source_sha256']
    assert provenance[native]['revision_id']==pages[pid]['source_revision_id']
    r=tr._blank_argument(frmeta,src);code,t,get=fields(pid)
    r.update(canonical_title=pages[pid]['canonical_title_en'],summary=get('summary'),sections=[s.strip() for s in get('sections').split(',') if s.strip()],keywords=[s.strip() for s in get('keywords').split(',') if s.strip()],reviewer='Codex — relecture textuelle complète',reviewed_at=now,note=notes[pid],canonical_title_semantic_inventory_note=notes[pid],documentation_rationale=selections[pid]['selection_note'])
    # Le libellé principal vient du vrai verrou de titres ; les 170 occurrences
    # complètes conservent leurs formes contextuelles dans relations_bilingual.
    frdisplay=src['displayed_title'];labels=load(W/'data/labels_bilingual.json')
    def norm(s):return ' '.join(s.replace('’',"'").replace('\u00a0',' ').strip().rstrip('.').split()).casefold()
    candidates={x['en'] for x in labels if norm(x['fr'])==norm(frdisplay)}
    assert len(candidates)==1,(pid,frdisplay,candidates)
    r['displayed_title']=next(iter(candidates));r['displayed_title_source_form']=frdisplay;r['displayed_title_target_form']=r['displayed_title']
    for sid in selections[pid]['selected_source_ids']:r['sources'][by_source[sid]['type']].append(sid)
    expected=[q for q in qdata if q['page_id']==pid]
    assert len(expected)==len(src['citations'])
    r['citations']=[]
    for sq,q in zip(src['citations'],expected):
        assert tr._citation_source_text(sq).strip()==q['source_text'].strip(),(pid,q['id'])
        cr=tr._blank_citation(sq)
        cr.update(status='approved',translated_citation=q['target_text'],translated_date=q['target_date'] or '',citation_translated=True,date_translated_or_language_neutral=True,preserved_parameters_unchanged=True,translation_warning_appended=True,quote_completeness_reviewed=True,quote_completeness_note=f"{q['id']} — {notes[pid]}",reviewer='Codex — comparaison bilingue de la livraison',reviewed_at=now,note='Fidélité de traduction et paramètres comparés ; authenticité externe de la citation non attestée.',quotation_authenticity_verified=False)
        if q['id'] in LOW_RATIO_NOTES:cr.update(quote_low_ratio_reviewed=True,quote_low_ratio_note=LOW_RATIO_NOTES[q['id']])
        r['citations'].append(cr)
    finals=tr._validate_citations(r['citations'],src['citations'],native)
    for f,q in zip(finals,expected):
        assert [(x['name'],x['value'].strip()) for x in f['parameters']]==[tuple(x) for x in q['target_parameters']],(pid,q['id'])
        coverage.append(dict(delivery_page_id=pid,native_page_id=native,delivery_quote_id=q['id'],native_quote_id=f['id'],parameter_contract='passed',external_authenticity_verified=False))
    native_quote_final.extend(finals)
    assert len(r['citation_passages'])==len([p for p in passages if p['page_id']==pid])
    for pr,p in zip(r['citation_passages'],[p for p in passages if p['page_id']==pid]):
        assert pr['source_text'].strip()==p['source_text'].strip()
        position=next(i for i,q in enumerate(expected) if q['id']==p['before_quote_id'])
        assert pr['before_citation_id']==src['citations'][position]['id']
        pr.update(text=p['target_text'],equivalent_to_french=True,review_note=notes[pid])
    native_passage_final.extend(validate_translations(r['citation_passages'],src['citation_passages'],native))
    raw_presence=src['source_parameter_presence'];fallback_fields=[k for k in ['rubriques','mots-clés'] if not raw_presence[k]['present']]
    if fallback_fields:classification.append(dict(delivery_id=pid,native_id=native,source_absent_parameters=fallback_fields,native_import_fallbacks=dict(rubriques=frmeta['rubriques'],keywords=frmeta['keywords']),disposition='English source absence retained; FR classification must not silently project import defaults.'))
    # Estimation native provisoire : compter les notices réellement présentes,
    # sans les faire passer pour des identifiants de sources FR verrouillées.
    risk_src=copy.deepcopy(src);risk_src['sources']={b:[f'raw-{b}-{i}' for i,_ in enumerate(mw.parse(v).filter_templates(),1)] for b,v in src['documentation_raw'].items()}
    risk=tr._translation_risk_profile(frmeta,risk_src)
    out['arguments'].append(dict(id=native,delivery_id=pid,review_risk=risk,review_risk_provisional=True,translation=r))
out['review_units']=tr._build_translation_review_units(out['arguments'])
for u in out['review_units']:u['note']='Plan calculé à la reprise ; aucune clôture rétrospective du protocole de lots n’est revendiquée. Verrous FR et revue documentaire globale encore ouverts.'
unit_by_page={pid:u['id'] for u in out['review_units'] for pid in u['page_ids']}
for r in out['arguments']:r['review_unit_id']=unit_by_page[r['id']]
out['blocking_issues']=[
    'FR content lock absent: original documentation and classification must not be silently replaced to open EN review.',
    'Historical quantitative claims and quotation authenticity are not all verified; no fabricated approval.',
    'Independent argument-name discovery is not closed: Bing results irrelevant; topic/principle labels are not argument names.',
    'Target wiki existence checks returned 403; related-debate/logo verification incomplete.',
    'Official lot closures and semantic convergence absent; pending file is not the official prepared review.'
]
save(dest,out);save(N/'data/sources_en_selected.pending.json',registry)
save(O/'native-citation-validation.json',dict(status='passed_translation_and_parameter_subset_only',native_code_commit='4b2abbe',quotes=len(native_quote_final),passages=len(native_passage_final),rows=coverage,official_translation_finalized=False,external_authenticity_verified=False))
save(O/'native-quotes-validated.json',dict(citations=native_quote_final,citation_passages=native_passage_final))
save(O/'native-classification-preservation-issues.json',classification)
save(O/'native-integration-state.json',dict(workspace=str(N),state=load(N/'workspace.json')['status'],pending_review_relative_path=str(dest.relative_to(P)),pending_review_sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),coverage=dict(arguments=len(out['arguments']),quotes=len(native_quote_final),passages=len(native_passage_final),review_units=len(out['review_units'])),classification_source_absence_pages=len(classification),french_content_lock_present=(N/'content-reviewed-copy/data/fr_content_lock.json').exists(),official_translation_prepared=False,official_translation_finalized=False,wiki_writes=False))
print('Revue native en attente :',len(out['arguments']),'arguments ; contrôle natif réussi pour',len(native_quote_final),'citations et',len(native_passage_final),'passages ;',len(out['review_units']),'unités non closes.')
