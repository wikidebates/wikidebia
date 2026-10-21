from pathlib import Path
import json,requests,datetime,hashlib,concurrent.futures,xml.etree.ElementTree as ET,re
from read_documents import plain
ROOT=Path('/workspace/output/cannabis_traduction_2026-10-21_verifiee');OUT=Path(__file__).parent/'research';(OUT/'responses').mkdir(exist_ok=True)
pages=json.loads((ROOT/'data/translation_pages.json').read_text());quotes=json.loads((ROOT/'data/translation_quotes.json').read_text())
jobs=[]
def job(k,url,**x):jobs.append(dict(id=k,url=url,**x))
# Candidate discovery is logged separately from editorial verification.
for r in pages:
 query=r['canonical_title_en']+' cannabis policy evidence research'
 job('search-'+r['id'],'https://api.crossref.org/works',params={'query':query,'rows':3},purpose='independent_english_documentary_candidate_search',page_id=r['id'],query=query)
seen={}
for q in quotes:
 p=dict(q['source_parameters']);url=p.get('lien')
 if url: seen.setdefault(url,[]).append(q['id'])
for i,(url,ids) in enumerate(seen.items(),1):job('quote-source-%03d'%i,url,purpose='quotation_authenticity_source_access',quote_ids=ids)
for name,url in {
'rand-vermont':'https://www.rand.org/pubs/research_reports/RR864.html',
'wikipedia-links':'https://fr.wikipedia.org/w/api.php?action=query&prop=langlinks&lllang=en&lllimit=max&titles=Lib%C3%A9ralisation_du_cannabis%7CProhibition_des_drogues%7CLib%C3%A9ralisation_des_drogues%7CL%C3%A9gislation_sur_le_cannabis&format=json',
'wikipedia-legality':'https://en.wikipedia.org/api/rest_v1/page/summary/Legality_of_cannabis',
'wikipedia-drug-liberalization':'https://en.wikipedia.org/api/rest_v1/page/summary/Drug_liberalization',
'wikipedia-drug-prohibition':'https://en.wikipedia.org/api/rest_v1/page/summary/Prohibition_of_drugs',
'commons-image':'https://commons.wikimedia.org/w/api.php?action=query&titles=File:World-cannabis-laws.png&prop=imageinfo&iiprop=url%7Cextmetadata&format=json',
'english-related':'https://en.wikidebates.org/w/api.php?action=query&titles=Should%20all%20drugs%20be%20decriminalized%3F&format=json',
'crossref-kilmer-global':'https://api.crossref.org/works?query.title=Global%20Perspectives%20on%20Cannabis%20Legalization&query.author=Kilmer&rows=4',
'crossref-barry':'https://api.crossref.org/works?query.title=Cannabis%20Commercialization%20Lessons%20from%20Big%20Tobacco&query.author=Barry&rows=4',
'crossref-kilmer-regulating':'https://api.crossref.org/works?query.title=Regulating%20Cannabis%20The%20Path%20to%20Safer%20Consumption&query.author=Kilmer&rows=4',
'crossref-habermas':'https://api.crossref.org/works?query.title=Postmetaphysical%20Thinking&query.author=Habermas&rows=3',
'new-nejm-big-marijuana':'https://www.nejm.org/doi/full/10.1056/NEJMp1406074',
'new-pnas-opioid':'https://www.pnas.org/doi/10.1073/pnas.1903434116',
'new-nida':'https://nida.nih.gov/research-topics/cannabis-marijuana',
'new-who-cannabis':'https://www.who.int/publications/i/item/9789241510240',
'new-nasem':'https://nap.nationalacademies.org/catalog/24625/the-health-effects-of-cannabis-and-cannabinoids-the-current-state',
'new-inbc2013':'https://www.incb.org/documents/Publications/AnnualReports/AR2013/English/AR_2013_E.pdf',
'new-harm-principle':'https://plato.stanford.edu/entries/mill-moral-political/',
'new-slippery-slope':'https://plato.stanford.edu/entries/fallacies/'
}.items():job(name,url,purpose='targeted_documentary_or_navigation_verification')
def fetch(j):
 row={**j,'accessed_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  r=requests.get(j['url'],params=j.get('params'),timeout=(8,22),headers={'User-Agent':'Wikidebia-documentary-review/1.0'});body=r.content
  row.update(http_status=r.status_code,final_url=r.url,content_type=r.headers.get('Content-Type',''),sha256=hashlib.sha256(body).hexdigest(),bytes=len(body),body_path='responses/'+j['id']+'.body')
  (OUT/row['body_path']).write_bytes(body)
  if r.status_code==200:
   if body.startswith(b'%PDF'):pass
   elif 'json' in row['content_type']:
    data=r.json()
    if isinstance(data.get('message'),dict) and 'items' in data['message']:
     row['candidates']=[{k:x.get(k) for k in ['title','DOI','author','URL','published','publisher','container-title','type','abstract']} for x in data['message']['items']]
    elif 'extract' in data:row['extract']=data['extract']
   elif 'html' in row['content_type']:
    text=plain(r.text);(OUT/('responses/'+j['id']+'.txt')).write_text(text)
    title=re.search(r'<title[^>]*>(.*?)</title>',r.text,re.I|re.S);row['title']=re.sub(r'\s+',' ',title.group(1)).strip() if title else None
 except requests.RequestException as e:row.update(error=str(e)[:600])
 return row
rows=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
 for row in ex.map(fetch,jobs):
  rows.append(row)
  if len(rows)%25==0:
   (OUT/'batch-results.partial.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n');print('Fetched',len(rows),'/',len(jobs),flush=True)
(OUT/'batch-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
print('Finished',len(rows),'responses; HTTP200',sum(x.get('http_status')==200 for x in rows),flush=True)
