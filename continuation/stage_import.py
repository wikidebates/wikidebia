from pathlib import Path
import json,hashlib,collections,datetime,sys
import mwparserfromhell as mw
sys.path.insert(0,'/workspace/work/cannabis-correction-relecture/kit/scripts')
from wikidebia_content_review import _citation_records
OUT=Path(__file__).parent;V2=Path('/workspace/output/cannabis_traduction_2026-10-21_verifiee')
load=lambda p:json.loads(p.read_text())
ident=load(OUT/'identity-map.json')['rows'];mapid={r['delivery_id']:r for r in ident};qs=load(V2/'data/translation_quotes.json');byq=collections.defaultdict(list)
for q in qs:byq[q['page_id']].append(q)
frbyid={}
for r in ident:
 if r['delivery_id']=='debate':continue
 source=mw.parse((V2/r['source_relative_path']).read_text())
 page=next(t for t in source.filter_templates() if str(t.name).strip()=='Argument')
 frbyid[r['build_node_id']]={'citations':_citation_records(str(page.get('citations').value).strip() if page.has('citations') else '',r['build_node_id'])}
records=[];qcount=0
for r in ident:
 pid=r['delivery_id'];row=dict(r)
 row['working_target_relative_path']=r['target_relative_path'];row['working_target_sha256']=hashlib.sha256((OUT/'working'/r['target_relative_path']).read_bytes()).hexdigest()
 row['native_french_lock_sha256']=None;row['english_creation_date']=None
 matched=[]
 if pid!='debate':
  fq=frbyid[r['build_node_id']]['citations'];eq=byq[pid];assert len(fq)==len(eq)
  for old,new in zip(fq,eq):
   native_params=[[x['name'],x['value']] for x in old['source_parameters']]
   ignored=[x for x in new['source_parameters'] if x[0].isdigit() and not x[1].strip()]
   assert native_params==[x for x in new['source_parameters'] if x not in ignored],new['id']
   matched.append(dict(delivery_quote_id=new['id'],build_quote_id=old['id'],source_parameters=new['source_parameters'],target_parameters=new['target_parameters'],empty_positional_parameters_not_exposed_by_native_extractor=ignored))
  qcount+=len(matched)
 row['quotes']=matched;records.append(row)
assert len(records)==153 and qcount==149
(OUT/'native-import.pending.json').write_text(json.dumps(dict(schema='wikidebia-translation-external-delivery-intake-staging-1.0',status='pending_native_french_metadata_content_locks_and_documentary_review',official_kit_artifact=False,ready_for_native_application=False,source_delivery_sha256='b317df79f35b047af2bdead55c5adbdb33c835fae528ed69f0de78e5d8332eda',records=records),ensure_ascii=False,indent=2)+'\n')
old=load(OUT/'research/batch-results.json');paced=load(OUT/'research/paced-results.json');allrows=old+paced
search={};names={}
for r in allrows:
 if r['id'].startswith(('search-','retry-search-')):search[r['page_id']]=r
 if r['id'].startswith('name-'):names[r['page_id']]=r
registry=load(OUT/'sources_en_working.partial.json');report=[]
for r in ident:
 pid=r['delivery_id'];s=search[pid];n=names.get(pid)
 assert s.get('http_status')==200 and (n is None or n.get('http_status')==200)
 chosen=[x['id'] for x in registry['sources'] if any(u['page_id']==('cannabis' if pid=='debate' else r['build_node_id']) for u in x['usage'])]
 report.append(dict(page_id=pid,build_node_id=r['build_node_id'],source_title_fr=r['source_title_fr'],source_revision_id=r['source_revision_id'],documentation_search=dict(provenance='actual_log',query=s.get('params',{}).get('query',s.get('query')),accessed_at=s['accessed_at'],url=s['final_url'],response_sha256=s['sha256'],candidates=s.get('candidates',[])),established_name_search=None if n is None else dict(provenance='actual_log',query=n['params']['query'],accessed_at=n['accessed_at'],url=n['final_url'],response_sha256=n['sha256'],candidates=n.get('candidates',[]),outcome='pending_scope_identity_and_full_text_review'),selected_source_ids=chosen,page_documentary_review_closed=False,note='Une recherche bibliographique donne des candidats, pas une attestation de langue, de pertinence, de lecture intégrale, d’édition équivalente ou de nom consacré. Aucun nom ajouté automatiquement.'))
(OUT/'documentary-research-by-page.json').write_text(json.dumps(dict(schema='wikidebia-documentary-candidate-research-log-1.0',status='candidate_discovery_complete_editorial_selection_incomplete',page_count=153,independent_documentary_queries=153,established_name_queries=152,rows=report),ensure_ascii=False,indent=2)+'\n')
findings=load(OUT/'research/quotation-authenticity-inventory.json')
(OUT/'research/quotation-editorial-findings.json').write_text(json.dumps([r for r in findings['quotes'] if r.get('note') or r.get('priority_review')],ensure_ascii=False,indent=2)+'\n')
print('Staging:',len(records),'pages,',qcount,'citations raccordées ;',len(report),'recherches documentaires et',len(names),'recherches de noms tracées.')
