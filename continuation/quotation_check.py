from pathlib import Path
import json,re,unicodedata,subprocess,collections
R=Path(__file__).parent/'research';V=Path('/workspace/output/cannabis_traduction_2026-10-21_verifiee')
qs=json.loads((V/'data/translation_quotes.json').read_text());rs=json.loads((R/'batch-results.json').read_text())
byq={q:r for r in rs for q in r.get('quote_ids',[])}
def norm(s):
 s=unicodedata.normalize('NFKD',s).casefold();return ''.join(c for c in s if c.isalnum())
rows=[]
for q in qs:
 r=byq.get(q['id']);row=dict(quote_id=q['id'],page_id=q['page_id'],quoted_text_preserved=True,online_authenticity_verified=False,english_edition_verified=False)
 if not r:row.update(status='no_direct_source_url_in_original_metadata')
 elif r.get('http_status')!=200:row.update(status='source_unavailable',http_status=r.get('http_status'),error=r.get('error'),url=r['url'])
 elif r.get('title')=='Client Challenge':row.update(status='challenge_page_not_article',url=r['url'])
 elif q['id']=='Q117':row.update(status='source_url_now_unrelated_gambling_page',url=r['url'],observed_title=r.get('title'))
 else:
  body=R/r['body_path'];txt=body.with_suffix('.txt')
  if body.read_bytes().startswith(b'%PDF') and not txt.exists():subprocess.run(['pdftotext','-layout',str(body),str(txt)],capture_output=True)
  text=txt.read_text() if txt.exists() else ''
  needle=q['target_text'] if q['translation_mode']=='supplied_english_preserved' else q['source_text']
  # The two originally bilingual quotes retain the supplied English verbatim.
  if q['id'] in ['Q092','Q120']:needle=q['target_text']
  match=bool(norm(needle)) and norm(needle) in norm(text)
  row.update(status='full_text_match_in_consulted_document' if match else 'full_text_not_matched_requires_editorial_authentication',url=r['url'],response_sha256=r['sha256'],full_quoted_text_match=match)
 rows.append(row)
(R/'quotation-authenticity-inventory.json').write_text(json.dumps(dict(status='incomplete_editorial_authentication',note='A match is a lexical observation, not verification of attribution, original edition, truth or contemporary applicability. No quotation altered or removed.',quotes=rows),ensure_ascii=False,indent=2)+'\n')
print(dict(collections.Counter(r['status'] for r in rows)))
for r in rows:
 if r.get('full_quoted_text_match'):print(r['quote_id'],r['status'])
