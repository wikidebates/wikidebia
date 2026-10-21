from pathlib import Path
import requests,json,datetime,hashlib,concurrent.futures
OUT=Path(__file__).parent/'research';OUT.mkdir(exist_ok=True)
urls={
'euda-portugal':'https://www.euda.europa.eu/system/files/media/publications/documents/11331/portugal-cdr-2019.pdf',
'canada-panel':'https://www.canada.ca/en/health-canada/services/publications/drugs-medication/legislative-review-cannabis-act-final-report-expert-panel.html',
'service-public-en':'https://www.service-public.gouv.fr/particuliers/vosdroits/F33341?lang=en',
'bing-test':'https://www.bing.com/search?format=rss&q=cannabis+legalisation+independent+review+health',
'crossref-test':'https://api.crossref.org/works?query.title=Cannabis%20Commercialization%20Lessons%20from%20Big%20Tobacco&rows=3',
'guardian-jenkins':'https://www.theguardian.com/commentisfree/2013/dec/12/heroic-uruguay-deserves-nobel-prize-cannabis'}
def fetch(item):
 name,url=item; row=dict(id=name,url=url,accessed_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
 try:
  r=requests.get(url,timeout=25,headers={'User-Agent':'Wikidebia-documentary-review/1.0'});row.update(http_status=r.status_code,final_url=r.url,content_type=r.headers.get('Content-Type'),sha256=hashlib.sha256(r.content).hexdigest(),bytes=len(r.content));(OUT/(name+'.body')).write_bytes(r.content)
 except requests.RequestException as e: row.update(error=str(e)[:550])
 return row
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex: rows=list(ex.map(fetch,urls.items()))
(OUT/'initial-probes.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n');print(json.dumps(rows,ensure_ascii=False,indent=2))
