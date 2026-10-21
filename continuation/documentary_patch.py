from pathlib import Path
import json,hashlib,sys,datetime,copy
import mwparserfromhell as mw
ROOT=Path('/workspace/output/cannabis_traduction_2026-10-21_verifiee');OUT=Path(__file__).parent
sys.path.insert(0,'/workspace/work/cannabis-correction-relecture/kit/scripts')
from wikidebia_content_review import SOURCE_METADATA_FIELDS
from wikidebia_translation_review import _validate_sources
from wikidebia_render import _source_template
R=OUT/'research'; docs=[]
for f in ['initial-probes.json','batch-results.json','additional-results.json']:docs.extend(json.loads((R/f).read_text()))
byid={r['id']:r for r in docs};mapping=json.loads((OUT/'identity-map.json').read_text())['rows'];bylocal={x['delivery_id']:x for x in mapping}
sources=[]
def add(i,kind,origin,meta,primary,note,uses,document_kind=None):
 r=byid[origin];assert r.get('http_status')==200
 m={k:None for k in SOURCE_METADATA_FIELDS};m['authors']=[];m.update(meta)
 use=[]
 for pid,reason in uses:
  item=dict(page_id='cannabis' if pid=='debate' else bylocal[pid]['build_node_id'],language='en',role='neutral_reference' if pid=='debate' else 'context',selection_reason=reason)
  if pid=='debate' and kind=='bibliography':item['documentary_scope']='broad_synthesis'
  use.append(item)
 s=dict(id=i,type=kind,document_kind=document_kind,language='en',metadata=m,verification=dict(status='verified',verified_at=r['accessed_at'],primary_source=primary,notes=[note],language_verified=True,authorship_checked=True,authorship_verified=bool(m['authors'])),usage=use,deduplication_key=m['link'],evidence=dict(url=r['url'],response_sha256=r['sha256'],local_response_path=r.get('body_path',origin+'.body')))
 sources.append(s);return s
rand=add('S90001','bibliography','rand-vermont',dict(authors=['Jonathan P. Caulkins','Beau Kilmer','Mark A. R. Kleiman','Robert J. MacCoun','Gregory Midgette','Pat Oglesby','Rosalie Liccardo Pacula','Peter Reuter'],work='Considering Marijuana Legalization: Insights for Vermont and Other Jurisdictions',publisher='RAND Corporation',place='Santa Monica, CA',date='2015',link=byid['rand-vermont']['url']),False,'Titre, huit auteurs, année et éditeur contrôlés sur la notice RAND. Rapport de synthèse des options, avantages, coûts et incertitudes ; pas une recommandation de légaliser. Les projections Vermont 2015 ne sont pas des observations France 2026.',[('debate','Synthèse générale des régimes possibles et de leurs effets sanitaires, économiques et sociaux, avec limites et incertitudes.'),('A0008','Analyse le rôle des taxes, prix et marchés parallèles, sans démontrer une persistance inconditionnelle.'),('A0056','Examine le commerce transfrontalier, le tourisme et les interactions entre politiques de juridictions voisines.'),('A0119','Étudie explicitement le prix comme dimension structurante de la politique du cannabis.'),('A0151','Fournit le contexte des prix, taxes et marchés illégaux dans différents modèles de régulation.')],'synthesis_report')
can=add('S90002','webliography','canada-panel',dict(authors=['Morris Rosenberg','Oyedeji Ayonrinde','Patricia J. Conrod','Lynda L. Levesque','Peter Selby'],page='Legislative Review of the Cannabis Act: Final Report of the Expert Panel',site='Health Canada',date='March 2024',link=byid['canada-panel']['url']),True,'Version anglaise officielle. Les cinq membres sont explicitement crédités sous Prepared by. Source primaire pour les conclusions de ce comité ; celles-ci ne valident pas chaque résultat scientifique sous-jacent. Résumé exécutif et passages sur jeunesse, produits puissants et déplacement du marché illicite lus.',[('debate','Documente la présentation nuancée de l’expérience canadienne dans l’introduction.'),('A0054','Permet de confronter les bénéfices et difficultés du modèle canadien ; ne valide pas toutes les affirmations du résumé historique.'),('A0057','Documente les préoccupations du comité sur les intérêts du marché et les produits puissants sans authentifier Q064.'),('A0063','Contexte vérifié du contrôle réglementaire de l’offre canadienne, sans authentifier Q069.'),('A0071','Évalue les tendances d’usage selon l’âge et les risques de produits puissants, sans conclure à une causalité générale.')])
euda=add('S90003','webliography','euda-portugal',dict(page='Portugal — Country Drug Report 2019',site='European Monitoring Centre for Drugs and Drug Addiction',date='2019',link=byid['euda-portugal']['url']),False,'PDF officiel anglais réellement consulté, section National drug laws (p. 5 du fichier) : loi 30/2000 appliquée depuis juillet 2001, consommation/acquisition/détention personnelles dépénalisées sous conditions ; trafic toujours distinct. Rapport de synthèse, pas texte législatif original ni bilan actuel de 2026.',[('debate','Vérifie la distinction entre la dépénalisation portugaise et la légalisation commerciale.'),('A0115','Documente le cadre juridique et les commissions de dissuasion ; ne prouve pas une réussite générale et inconditionnelle du modèle.'),('A0142','Documente un exemple effectif de dépénalisation de l’usage de plusieurs drogues sous conditions.')])
sp=add('S90004','webliography','service-public-en',dict(page='What is the risk for drug use?',site='Service Public',date='21 August 2026',link=byid['service-public-en']['url']),False,'Version anglaise effectivement publiée par Service Public ; traduction automatique signalée par le site. Fiche datée vérifiée, pas une édition inventée ni une lecture du texte législatif. Montants et maximum reproduits selon la fiche du 21 août 2026 ; ils ne s’appliquent pas indistinctement à tous les délits liés aux drogues.',[('debate','Référence anglaise de la fiche française utilisée dans l’introduction, même identifiant F33341 et date indiquée.')])
nida=add('S90005','webliography','new-nida',dict(page='Cannabis (Marijuana)',site='National Institute on Drug Abuse',link=byid['new-nida']['url']),False,'Page institutionnelle anglaise lue, notamment définition, modes d’usage, THC, effets indésirables et usages thérapeutiques. Aucun auteur individuel distinct n’est crédité : liste d’auteurs vide ; NIDA conservé comme site, pas inventé comme auteur.',[('A0106','Synthèse de santé sur les risques physiques et mentaux, permettant d’évaluer l’argument sans généraliser un risque à tous les usages.'),('A0134','Présente les risques liés au développement et à la santé mentale ; source de contexte, pas authentification des citations françaises.'),('A0117','Information sur le trouble de l’usage et les facteurs de risque ; ne transforme pas les pourcentages historiques en statistiques actuelles.'),('A0141','Décrit les modes d’usage et certains risques, sans prétendre qu’un mode serait sans danger.')])
registry=dict(schema='wikidebia-en-source-registry-working-1.0',debate_id='cannabis',work_id=None,status='partial_documentary_registry_not_applied_to_native_workspace',sources=sources)
_validate_sources(registry,'cannabis',set())
(OUT/'sources_en_working.partial.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n')
# Only reference localisation and explicitly reviewed documentary additions. The original delivery is immutable.
working=OUT/'working';(working/'pages/en/arguments').mkdir(parents=True,exist_ok=True)
rows=json.loads((ROOT/'data/translation_pages.json').read_text());changes=[]
replacements={
 'debate':[
 ('https://www.service-public.gouv.fr/particuliers/vosdroits/F33341 Que risque-t-on pour usage de drogues ?', 'https://www.service-public.gouv.fr/particuliers/vosdroits/F33341?lang=en What is the risk for drug use?'),
 ('https://www.canada.ca/fr/sante-canada/services/publications/drogues-medicaments/examen-legislatif-loi-cannabis-rapport-final-comite-experts.html Examen législatif de la Loi sur le cannabis : Rapport final du Comité d’experts', 'https://www.canada.ca/en/health-canada/services/publications/drugs-medication/legislative-review-cannabis-act-final-report-expert-panel.html Legislative Review of the Cannabis Act: Final Report of the Expert Panel')],
 'A0058':[('https://fr.wikipedia.org/wiki/L%C3%A9gislation_sur_le_cannabis French Wikipedia: Législation sur le cannabis','https://en.wikipedia.org/wiki/Legality_of_cannabis English Wikipedia: Legality of cannabis')],
 'A0073':[('https://fr.wikipedia.org/wiki/Prohibition_des_drogues#Mise_en_place_d.27une_r.C3.A9glementation_internationale','https://en.wikipedia.org/wiki/Drug_prohibition')],
 'A0125':[('https://fr.wikipedia.org/wiki/Prohibition_des_drogues#Mise_en_place_d.27une_r.C3.A9glementation_internationale','https://en.wikipedia.org/wiki/Drug_prohibition')],
 'A0143':[('https://fr.wikipedia.org/wiki/Libéralisation_des_drogues French Wikipedia: Libéralisation des drogues','https://en.wikipedia.org/wiki/Drug_liberalization English Wikipedia: Drug liberalization')]
}
added={}
for row in rows:
 old=(ROOT/row['target_relative_path']).read_text();new=old
 for a,b in replacements.get(row['id'],[]):
  assert new.count(a)==1,(row['id'],a);new=new.replace(a,b)
 code=mw.parse(new);page=next(t for t in code.filter_templates() if str(t.name).strip() in ['Argument','Debate'])
 pid='cannabis' if row['id']=='debate' else bylocal[row['id']]['build_node_id']
 selected=[s for s in sources if any(u['page_id']==pid for u in s['usage'])]
 for kind,param in [('bibliography','bibliography'),('webliography','webliography')]:
  vals=[_source_template(s,lang='en') for s in selected if s['type']==kind]
  if vals:page.add(param,''.join(vals)+'\n')
 if row['id']=='debate':page.add('wikipedia-articles','{{Wikipedia article\n|page=Legality of cannabis\n}}\n')
 new=str(code)
 dest=working/row['target_relative_path'];dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(new)
 if new!=old:
  changes.append(dict(page_id=row['id'],source_title_fr=row['source_title_fr'],relative_path=row['target_relative_path'],before_sha256=hashlib.sha256(old.encode()).hexdigest(),after_sha256=hashlib.sha256(new.encode()).hexdigest(),reference_replacements=len(replacements.get(row['id'],[])),added_sources=[s['id'] for s in selected],summary_prose_changed=False,quote_changes=False))
 # Preserve all quotes, relations, metadata and summaries other than the recorded link substitutions.
 ot=mw.parse(old);a=[str(t) for t in ot.filter_templates() if str(t.name).strip()=='Quote'];b=[str(t) for t in code.filter_templates() if str(t.name).strip()=='Quote'];assert a==b
 op=next(t for t in ot.filter_templates() if str(t.name).strip() in ['Argument','Debate'])
 for name in ['summary','pro-arguments','con-arguments','justifications','objections','sections','keywords']:
  ov=str(op.get(name).value) if op.has(name) else None;nv=str(page.get(name).value) if page.has(name) else None
  if name=='summary' and ov is not None:
   for x,y in replacements.get(row['id'],[]):ov=ov.replace(x,y)
  assert ov==nv,(row['id'],name)
(OUT/'documentary-changes.json').write_text(json.dumps(dict(status='working_draft_not_officially_finalized',publication_ready=False,registry_subset_validation_passed=True,official_workflow_validation=False,changes=changes),ensure_ascii=False,indent=2)+'\n')
print('Sources réellement vérifiées:',len(sources),'pages de travail modifiées documentairement:',len(changes),'(non finalisées)')
