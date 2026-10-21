from pathlib import Path
import requests,json,datetime,hashlib,concurrent.futures,re
from read_documents import plain
O=Path(__file__).parent/'research';(O/'responses').mkdir(exist_ok=True)
jobs={
'wiki-drug-prohibition-full':'https://en.wikipedia.org/w/api.php?action=parse&page=Drug_prohibition&prop=text%7Csections&format=json',
'wiki-drug-liberalization-full':'https://en.wikipedia.org/w/api.php?action=parse&page=Drug_liberalization&prop=text&format=json',
'publisher-muscadier-search':'https://www.muscadier.fr/?s=Faut-il+d%C3%A9p%C3%A9naliser+le+cannabis',
'bing-kilmer-global':'https://www.bing.com/search?format=rss&q=%22Global+Perspectives+on+Cannabis+Legalization%22+Kilmer',
'bing-barry-commercialization':'https://www.bing.com/search?format=rss&q=%22Cannabis+Commercialization%22+%22Barry%22',
'bing-kilmer-safer':'https://www.bing.com/search?format=rss&q=%22The+Path+to+Safer+Consumption%22+Kilmer',
'quote117-archive-index':'https://web.archive.org/cdx/search/cdx?url=jeanyvesnau.com/2014/03/27/cannabis-non-lacademie-nationale-de-medecine-ne-remplit-pas-sa-mission/&output=json&filter=statuscode:200&filter=mimetype:text/html&collapse=digest&limit=4',
'pubmed-driving':'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3277079/',
'pubmed-opioid':'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6595272/',
'book-drug-war-heresies':'https://www.cambridge.org/core/books/drug-war-heresies/62BB70CFE3DECE875A31E474F73B1D32',
'book-habermas-search':'https://openlibrary.org/search.json?title=Postmetaphysical+Thinking&author=Habermas&limit=3',
'new-ccs-2024':'https://www.canada.ca/en/health-canada/services/drugs-medication/cannabis/research-data/canadian-cannabis-survey-2024-summary.html',
'who-cannabis-pdf':'https://iris.who.int/bitstream/handle/10665/251056/9789241510240-eng.pdf',
'rand-report-pdf':'https://www.rand.org/content/dam/rand/pubs/research_reports/RR800/RR864/RAND_RR864.pdf',
'stanford-fallacy':'https://plato.stanford.edu/entries/fallacies/',
'peertube-video':'https://tube.blueben.net/api/v1/videos/7d5b4c7a-5c1f-44f6-9603-6dfadd444040'}
def f(x):
 k,u=x;row=dict(id=k,url=u,accessed_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
 try:
  r=requests.get(u,timeout=(7,22));row.update(http_status=r.status_code,final_url=r.url,sha256=hashlib.sha256(r.content).hexdigest(),body_path='responses/'+k+'.body',content_type=r.headers.get('Content-Type'))
  (O/row['body_path']).write_bytes(r.content)
  if r.status_code==200 and 'html' in row['content_type']:
   (O/'responses'/ (k+'.txt')).write_text(plain(r.text))
 except requests.RequestException as e:row['error']=str(e)[:500]
 return row
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:rows=list(ex.map(f,jobs.items()))
(O/'additional-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
for r in rows:print(r['id'],r.get('http_status'),r.get('error',''))
