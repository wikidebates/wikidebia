from pathlib import Path
import json,sys,collections,hashlib,re
import mwparserfromhell as mw
V=Path('/workspace/output/cannabis_traduction_2026-10-21_verifiee');W=Path('/workspace/work/cannabis-translation-verification-20261021/working');O=Path(__file__).parent
sys.path.insert(0,'/workspace/work/cannabis-interquotation-code/kit/scripts')
from wikidebia_translation_review import _date_signature,SECTION_MAP
from datetime import date as calendar_date
def date_key(value,lang):
 s=str(value or "").strip()
 if lang=="fr":
  m=re.fullmatch(r"(\d{1,2})[/.](\d{1,2})[/.](\d{4})",s)
  if m:
   d,month,y=map(int,m.groups());calendar_date(y,month,d);return(y,month,d)
  m=re.fullmatch(r"(\d{1,2})/(\d{4})",s)
  if m:return(int(m[2]),int(m[1]),None)
  if s=="17 nov 2021":return(2021,11,17)
 return _date_signature(s,lang)
if len(sys.argv)>1:W=Path(sys.argv[1])
rows=json.loads((W/'data/translation_pages.json').read_text());vocab=json.loads((W/'data/vocabulary_bilingual.json').read_text());terms={r['fr']:r['keyword_en'] for r in vocab}
MAP={'sujet':'topic','sujet-développé':'expanded-topic','avancement':'progress','avertissements-débat':'debate-warnings','avertissements-titre':'title-warnings','avertissements-argument':'argument-warnings','avertissements-résumé':'summary-warnings','introduction':'introduction','arguments-pour':'pro-arguments','arguments-contre':'con-arguments','rubriques':'sections','mots-clés':'keywords','résumé':'summary','citations':'quotes','objections':'objections','justifications':'justifications'}
DOC={'articles-Wikipédia':'wikipedia-articles','bibliographie-pour':'pro-bibliography','bibliographie-contre':'con-bibliography','bibliographie-ni-pour-ni-contre':'bibliography','sitographie-pour':'pro-webliography','sitographie-contre':'con-webliography','sitographie-ni-pour-ni-contre':'webliography','vidéographie-pour':'pro-videography','vidéographie-contre':'con-videography','vidéographie-ni-pour-ni-contre':'videography','références-bibliographiques':'bibliography','références-sitographiques':'webliography','références-vidéographiques':'videography','débats-connexes':'related-debates'}
CMAP={'citation':'quote','auteurs':'authors','ouvrage':'work','article':'article','page':'page','édition':'publisher','lieu':'place','lien':'link','volume':'volume','numéro':'issue','localisation':'location','date':'date','avertissements':'warnings','avertissements-citation':'warnings'}
CHECKS=[];gaps=[];inventory=[];qcount=0;duplicates=[];historical_duplicates=[]
def get(t,k):return str(t.get(k).value).strip() if t.has(k) else None
for row in rows:
 fr=mw.parse((V/row['source_snapshot_relative_path']).read_text());en=mw.parse((W/row['target_relative_path']).read_text());fp=next(t for t in fr.filter_templates() if str(t.name).strip() in {'Débat','Argument'});ep=next(t for t in en.filter_templates() if str(t.name).strip() in {'Debate','Argument'})
 for code,lang in [(fr,'fr'),(en,'en')]:
  for t in code.filter_templates():
   names=[str(p.name).strip() for p in t.params]
   if len(set(names))!=len(names):duplicates.append(dict(page=row['id'],language=lang,template=str(t.name),names=names))
 decisions=[]
 for p in fp.params:
  k=str(p.name).strip();val=str(p.value).strip()
  if k in MAP:state='translated_field_present' if ep.has(MAP[k]) else 'empty_parameter_omitted' if not val else 'MISSING';dest=MAP[k]
  elif k in DOC:state='documentary_reselection_or_target_check_still_open';dest=DOC[k]
  elif k in {'date-création','initialisation'}:state='omitted_by_explicit_english_lifecycle_rule';dest=None
  else:state='UNCLASSIFIED';dest=None
  decisions.append(dict(source_parameter=k,target_parameter=dest,source_nonempty=bool(val),disposition=state))
  if state in ['MISSING','UNCLASSIFIED']:gaps.append(dict(page=row['id'],parameter=k,issue=state))
 for frkey,enkey,mapping in [('rubriques','sections',SECTION_MAP),('mots-clés','keywords',terms)]:
  a=get(fp,frkey);b=get(ep,enkey)
  if a:
   expected=[mapping[t.strip()] for t in a.split(',') if t.strip()]
   if frkey=='rubriques':expected=sorted(expected,key=str.casefold)
   actual=[t.strip() for t in (b or '').split(',') if t.strip()]
   if len({x.casefold() for x in actual})!=len(actual):
    source_terms=[t.strip() for t in a.split(',') if t.strip()]
    if len({x.casefold() for x in source_terms})!=len(source_terms) and actual==expected:historical_duplicates.append(dict(page=row['id'],parameter=enkey,source=source_terms,target=actual,disposition='preserved_source_duplicate_not_silently_cleaned'))
    else:gaps.append(dict(page=row['id'],parameter=enkey,issue='duplicate_values',actual=actual))
   if expected!=actual:gaps.append(dict(page=row['id'],parameter=frkey,expected=expected,actual=actual))
  elif b:gaps.append(dict(page=row['id'],parameter=enkey,issue='value_added_to_absent_source'))
 if get(fp,'avancement'):
  expected={'Ébauche':'Draft','Débat en construction':'Debate under construction','Débat construit':'Constructed debate'}[get(fp,'avancement')]
  if get(ep,'progress')!=expected:gaps.append(dict(page=row['id'],parameter='progress',expected=expected))
 # Exact source-warning translation, including historical summary warnings.
 for a,b in [('avertissements-débat','debate-warnings'),('avertissements-titre','title-warnings'),('avertissements-argument','argument-warnings')]:
  if not fp.has(a) and ep.has(b):gaps.append(dict(page=row['id'],parameter=b,issue='default_added'))
 if get(fp,'avertissements-résumé') and not (get(fp,'avertissements-résumé')=='Résumé désavantageux' and get(ep,'summary-warnings')=='Biased summary'):gaps.append(dict(page=row['id'],parameter='summary-warnings',issue='warning_value_review',source=get(fp,'avertissements-résumé'),target=get(ep,'summary-warnings')))
 fquotes=[t for t in fr.filter_templates() if str(t.name).strip()=='Citation'];equotes=[t for t in en.filter_templates() if str(t.name).strip()=='Quote'];assert len(fquotes)==len(equotes)
 for index,(a,b) in enumerate(zip(fquotes,equotes),1):
  qcount+=1;allowed=set();warning=''
  for p in a.params:
   k=str(p.name).strip();val=str(p.value).strip()
   if k.isdigit() and not val:continue
   if k not in CMAP:gaps.append(dict(page=row['id'],quote=index,parameter=k,issue='unmapped_quote_parameter'));continue
   target=CMAP[k];allowed.add(target);translated=get(b,target)
   if k=='citation':continue
   if target=='warnings':warning=val;continue
   if target=='date':
    if date_key(val,'fr')!=date_key(translated,'en'):gaps.append(dict(page=row['id'],quote=index,parameter='date',source=val,target=translated))
   elif translated!=val:gaps.append(dict(page=row['id'],quote=index,parameter=target,source=val,target=translated))
  allowed.add('warnings')
  if set(str(p.name).strip() for p in b.params)!=allowed:gaps.append(dict(page=row['id'],quote=index,issue='quote_parameters_differ',expected=sorted(allowed),actual=[str(p.name).strip() for p in b.params]))
  if get(b,'warnings')!=((warning+', ') if warning else '')+'AI-translated quote':gaps.append(dict(page=row['id'],quote=index,issue='warnings_contract'))
 fsubs=[t for t in fr.filter_templates() if str(t.name).strip()=='Sous-partie'];esubs=[t for t in en.filter_templates() if str(t.name).strip()=='Subsection'];assert len(fsubs)==len(esubs)
 for i,(a,b) in enumerate(zip(fsubs,esubs)):
  if a.has('titre')!=b.has('title'):gaps.append(dict(page=row['id'],subsection=i+1,issue='subsection_title_presence_changed',source=get(a,'titre'),target=get(b,'title')))
 for p in ep.params:
  k=str(p.name).strip()
  if k not in set(MAP.values())|set(DOC.values()):gaps.append(dict(page=row['id'],parameter=k,issue='unexpected_english_parameter'))
 inventory.append(dict(page_id=row['id'],source_parameters=[str(p.name).strip() for p in fp.params],english_parameters=[str(p.name).strip() for p in ep.params],dispositions=decisions))
report=dict(schema='wikidebia-exhaustive-template-parameter-review-1.0',source_page_count=153,quoted_models_compared=qcount,source_parameter_dispositions=inventory,duplicate_parameters=duplicates,historical_duplicate_values_preserved=historical_duplicates,findings=gaps,official_kit_finalization=False)
(O/('parameters-after.json' if len(sys.argv)>1 else 'parameters-before.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('Pages',len(rows),'Quote comparées',qcount,'Doublons',len(duplicates));print(json.dumps(gaps,ensure_ascii=False,indent=2))
