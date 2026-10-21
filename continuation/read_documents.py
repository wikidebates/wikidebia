from html.parser import HTMLParser
from pathlib import Path
import subprocess,re,json
class Plain(HTMLParser):
 def __init__(self): super().__init__(); self.skip=0;self.out=[]
 def handle_starttag(self,t,a):
  if t in ('script','style','noscript'): self.skip+=1
  if t in ('p','div','section','h1','h2','h3','h4','li','br','tr'):self.out.append('\n')
 def handle_endtag(self,t):
  if t in ('script','style','noscript'): self.skip=max(0,self.skip-1)
 def handle_data(self,d):
  if not self.skip:self.out.append(d)
def plain(s):
 p=Plain();p.feed(s);return re.sub(r'\n[ \t]*\n+', '\n\n',''.join(p.out))
if __name__=='__main__':
 root=Path(__file__).parent/'research'
 for name in ['canada-panel','service-public-en','guardian-jenkins']:
  (root/(name+'.txt')).write_text(plain((root/(name+'.body')).read_text()))
 subprocess.run(['pdftotext','-layout',str(root/'euda-portugal.body'),str(root/'euda-portugal.txt')],check=True)
 for n in ['service-public-en','euda-portugal','canada-panel']:
  print('\nDOCUMENT',n)
  s=(root/(n+'.txt')).read_text()
  if n=='service-public-en':
   for pat in ['Verified','500','3,750','400','1,000']:
    i=s.find(pat);print(pat,repr(s[max(0,i-180):i+450]))
  else:
   for pat in (['National drug laws','decriminal','trafficking'] if n=='euda-portugal' else ['young people','illicit market','high-potency','2024','Expert Panel']):
    m=re.search(pat,s,re.I);i=m.start() if m else 0;print(pat,s[max(0,i-150):i+700])
