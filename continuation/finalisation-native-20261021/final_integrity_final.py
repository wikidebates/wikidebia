"""Intégrité de la copie relue ; ce rapport ne remplace pas les verrous natifs."""
from pathlib import Path
import json,hashlib,collections,datetime,sys,re
import mwparserfromhell as mw
A=Path(__file__).parent;R=Path('/workspace/work/cannabis-translation-verification-20261021/relecture-approfondie');W=A/'working';V=Path('/workspace/output/cannabis_traduction_2026-10-21_verifiee')
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
def check(name,condition):
 checks.append(dict(check=name,passed=bool(condition)))
 assert condition,name
rows=load(W/'data/translation_pages.json');original=load(V/'data/translation_pages.json');notes=sum([load(p) for p in sorted(R.glob('notes-*.json'))],[])
check('153_individual_textual_review_notes',len(notes)==153 and {n['id'] for n in notes}=={r['id'] for r in rows})
check('153_pages_exactly',len(rows)==153 and {str(p.relative_to(W)) for p in (W/'pages').rglob('*.wiki')}=={r['target_relative_path'] for r in rows})
check('immutable_v2_manifest',all(sha(V/f['path'])==f['sha256'] for f in load(V/'MANIFEST_SHA256.json')['files']))
texts=load(W/'data/translation_texts.json');qs=load(W/'data/translation_quotes.json');orig_qs=load(V/'data/translation_quotes.json');rels=load(W/'data/relations_bilingual.json');labels={r['fr']:r['en'] for r in load(W/'data/labels_bilingual.json')};byid={r['id']:r for r in rows};edge_types={'pro':'Pro argument','con':'Con argument','objection':'Objection','justification':'Justification'}
summary_count=0;absent_count=0;quote_count=0;date_count=0;edges=[];ratios=[];templates=collections.defaultdict(set)
for row,old in zip(rows,original):
 pid=row['id'];check(pid+'_source_identity',all(row[k]==old[k] for k in ['source_title_fr','source_revision_id','source_sha256','source_snapshot_relative_path']))
 check(pid+'_source_hash',sha(V/row['source_snapshot_relative_path'])==row['source_sha256']);check(pid+'_target_hash',sha(W/row['target_relative_path'])==row['target_sha256'])
 f=mw.parse((V/row['source_snapshot_relative_path']).read_text());e=mw.parse((W/row['target_relative_path']).read_text());fp=next(t for t in f.filter_templates() if str(t.name).strip() in {'Débat','Argument'});ep=next(t for t in e.filter_templates() if str(t.name).strip() in {'Debate','Argument'})
 check(pid+'_canonical_data',texts['canonical_titles'][pid]==row['canonical_title_en'])
 if pid!='debate':
  fs=str(fp.get('résumé').value).strip() if fp.has('résumé') else '';es=str(ep.get('summary').value).strip() if ep.has('summary') else ''
  check(pid+'_summary_presence',bool(fs)==bool(es))
  if fs:
   summary_count+=1;check(pid+'_summary_data',texts['summaries'][pid]==es);ratio=len(es)/len(fs);ratios.append(dict(page=pid,ratio=ratio));check(pid+'_summary_length_risk',.60<=ratio<=1.45)
  else:absent_count+=1
 check(pid+'_no_french_lifecycle_copy',not any(ep.has(k) for k in ['creation-date','date-création','initialization','initialisation']))
 actual_q=[t for t in e.filter_templates() if str(t.name).strip()=='Quote'];data_q=[q for q in qs if q['page_id']==pid];check(pid+'_quote_coverage',len(actual_q)==len(data_q))
 for t,q in zip(actual_q,data_q):
  quote_count+=1;check(q['id']+'_quote_text_and_data',str(t.get('quote').value).strip()==q['target_text']==texts['quote_texts'][q['id']]);check(q['id']+'_all_target_params',[[str(p.name).strip(),str(p.value).strip()] for p in t.params]==q['target_parameters']);date_count+=int(t.has('date'))
 for t in e.filter_templates():
  name=str(t.name).strip();templates[name].update(str(p.name).strip() for p in t.params)
  if name in edge_types.values():edges.append((pid,name,str(t)))
 for rel in [r for r in rels if r['source_id']==pid]:
  check(pid+'_edge_'+str(rel['order_in_parameter'])+'_'+rel['relation'],rel['target_title_en']==byid[rel['target_id']]['canonical_title_en'] and rel['displayed_title_en']==labels[rel['displayed_title_fr']])
  tname=edge_types[rel['relation']];matches=[t for t in e.filter_templates() if str(t.name).strip()==tname];t=matches[rel['order_in_parameter']-1]
  values=[str(p.value).strip() for p in t.params];check(pid+'_rendered_edge_'+rel['relation']+'_'+str(rel['order_in_parameter']),rel['target_title_en'] in values and rel['displayed_title_en'] in values)
check('149_quotes_145_dates',quote_count==149 and date_count==145);check('32_summaries_120_absences',summary_count==32 and absent_count==120);check('170_relation_occurrences',len(edges)==len(rels)==170)
check('source_quote_data_immutable',all(q['source_text']==o['source_text'] and q['source_parameters']==o['source_parameters'] for q,o in zip(qs,orig_qs)))
for n in load(W/'data/translation_editorial_notes.json'):
 r=byid[n['page_id']];body=(W/r['target_relative_path']).read_text();q=next(q for q in qs if q['id']==n['before_quote_id']);check(n['id']+'_prose_preserved_and_anchored',n['target_text'] in body and body.index(n['target_text'])<body.index(q['target_text']))
parameters=load(A/'parameters-after.json');check('no_unresolved_structural_parameter_findings',not parameters['findings'] and not parameters['duplicate_parameters'])
allowed={'Debate','Argument','Subsection','Quote','Wikipedia article','Pro argument','Con argument','Justification','Objection','Bibliographical reference','Web reference'}
check('only_known_english_templates',not set(templates)-allowed)
allowed_parameters={
 'Debate':{'topic','expanded-topic','progress','debate-warnings','title-warnings','introduction','pro-arguments','con-arguments','sections','keywords','wikipedia-articles','related-debates','pro-bibliography','con-bibliography','bibliography','pro-webliography','con-webliography','webliography','pro-videography','con-videography','videography'},
 'Argument':{'title-warnings','argument-warnings','summary-warnings','summary','quotes','sections','keywords','justifications','objections','bibliography','webliography','videography','established-name'},
 'Quote':{'quote','authors','article','work','volume','issue','page','location','publisher','place','date','link','warnings'},
 'Subsection':{'title','content'},'Wikipedia article':{'page'},
 'Pro argument':{'page','displayed-title'},'Con argument':{'page','displayed-title'},'Justification':{'page','displayed-title'},'Objection':{'page','displayed-title'},
 'Bibliographical reference':{'authors','work','article','publisher','place','date','page','link','volume','issue'},
 'Web reference':{'authors','page','site','date','link'}}
for name,params in templates.items():check('allowed_parameter_names_'+name,not params-allowed_parameters[name])
report=dict(status='independent_textual_integrity_passed',checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),checks_passed=len(checks),checks=checks,counts=dict(pages=153,quotes=quote_count,quote_dates=date_count,summaries=summary_count,absent_summaries=absent_count,relation_occurrences=len(edges),distinct_displayed_labels=len(labels)),template_parameter_inventory={k:sorted(v) for k,v in sorted(templates.items())},summary_ratios=ratios,historical_keyword_duplicates_preserved=parameters['historical_duplicate_values_preserved'],scope='Text and parameter parity only; native release completion is attested separately by release-receipt.json and native-delivery-parity.json',wiki_writes=False)
(A/'final-integrity-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
(A/'working-files-manifest.json').write_text(json.dumps(dict(files=[dict(path=str(p.relative_to(W)),sha256=sha(p)) for p in sorted(W.rglob('*')) if p.is_file()]),ensure_ascii=False,indent=2)+'\n')
print('Contrôles réussis :',len(checks));print(report['counts']);print(report['template_parameter_inventory'])
