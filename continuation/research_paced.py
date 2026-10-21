from pathlib import Path
import json,requests,datetime,time,hashlib,collections
ROOT=Path('/workspace/output/cannabis_traduction_2026-10-21_verifiee');OUT=Path(__file__).parent/'research';D=OUT/'responses'
old=json.loads((OUT/'batch-results.json').read_text());pages=json.loads((ROOT/'data/translation_pages.json').read_text())
jobs=[dict(id='retry-'+r['id'],page_id=r.get('page_id'),purpose=r['purpose'],url=r['url'],params=r.get('params')) for r in old if r.get('http_status')==429]
# A bibliographic search is evidence of a query, not an established-name decision.
for r in pages[1:]:
 q=r['canonical_title_en']+' argument reasoning'
 jobs.append(dict(id='name-'+r['id'],page_id=r['id'],purpose='established_name_candidate_discovery_not_outcome',url='https://api.crossref.org/works',params={'query':q,'rows':2}))
rows=[]
for j in jobs:
 time.sleep(1.1)
 row={**j,'accessed_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  r=requests.get(j['url'],params=j.get('params'),timeout=(7,18),headers={'User-Agent':'Wikidebia-documentary-review/1.0'})
  row.update(http_status=r.status_code,final_url=r.url,sha256=hashlib.sha256(r.content).hexdigest(),body_path='responses/'+j['id']+'.body')
  (OUT/row['body_path']).write_bytes(r.content)
  if r.status_code==200:
   data=r.json();row['candidates']=[{k:x.get(k) for k in ['title','DOI','author','URL','published','publisher','container-title','type','abstract']} for x in data['message']['items']]
  if r.status_code==429:
   row['rate_limit_remaining']=True
 except requests.RequestException as e:row.update(error=str(e)[:500])
 rows.append(row)
 (OUT/'paced-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
 if len(rows)%20==0:print('Paced discovery:',len(rows),'/',len(jobs),dict(collections.Counter(x.get('http_status','error') for x in rows)),flush=True)
print('Finished paced discovery',len(rows),flush=True)
