from pathlib import Path
import datetime, hashlib, json, shutil, subprocess, zipfile

O=Path(__file__).parent
R=Path('/workspace/work/cannabis-translation-verification-20261021/relecture-approfondie')
V=Path('/workspace/output/cannabis_traduction_2026-10-21_verifiee')
P=Path('/workspace/work/cannabis-interquotation-code')
B=Path('/workspace/work/cannabis-translation-en-backup-20261021')
NAME='cannabis_traduction_en_2026-10-21_documentation_et_revue_native'
D=Path('/workspace/output')/NAME
assert not D.exists(), 'Paquet existant à préserver.'
def load(p):return json.loads(p.read_text())
def save(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def cp(p,q):q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
shutil.copytree(O/'working-selected',D/'corpus')
shutil.copytree(V/'provenance/source',D/'provenance/source')
for filename in ['LIRE_D_ABORD.txt','RAPPORT_VERIFICATION.md','CONTINUER_AVEC_CODEX.txt','MANIFEST_SHA256.json']:
    if (V/filename).exists():cp(V/filename,D/'provenance/livraison-v2'/filename)
cp(O/'RAPPORT_REPRISE.md',D/'RAPPORT_REPRISE.md')
(D/'LIRE_D_ABORD.txt').write_text('WIKIDÉB’IA — TRADUCTION CANNABIS FR → EN\n\nCopie à reprendre : corpus/.\nLire RAPPORT_REPRISE.md puis CONTINUER_AVEC_CODEX.txt.\n153 pages relues, 149 citations et deux passages conservés, 40 références sélectionnées.\nÉtat : relecture textuelle et sélection documentaire effectuées ; validation documentaire complète et workflow natif non finalisés.\nAucune publication wiki. Aucune convergence officielle revendiquée.\nLe MANIFEST_SHA256.json à la racine est celui de ce nouveau paquet. Le manifeste sous provenance/livraison-v2 est uniquement historique.\n',encoding='utf-8')
(D/'CONTINUER_AVEC_CODEX.txt').write_text('Reprendre corpus/ de ce paquet, sans repartir de zéro et sans écraser les fichiers ou commits existants.\nTravailler en français. Lire les consignes actuelles du dépôt wikidebates/wikidebia.\n\nOrigine V2 : SHA-256 b317df79f35b047af2bdead55c5adbdb33c835fae528ed69f0de78e5d8332eda.\nLire RAPPORT_REPRISE.md et tous les blocages avant toute finalisation.\nLa branche de sauvegarde est translation/cannabis-en-20261021-verifiee ; le code du kit utilisé est fix/preserve-interquotation-prose, PR 9, commit 4b2abbe. Ne fusionner aucune de ces branches dans main.\n\nLe sous-projet natif est dans native/project/. Le code et les dépendances ne sont pas dupliqués : utiliser le commit complet indiqué dans native/code-provenance.json avec les dépendances du dépôt ; conserver corpus/ et .state/ du sous-projet. Adapter les chemins des scripts de recherche locaux, qui ne sont pas des commandes de publication.\nLe workspace reste fr_content_review_ready. reviews/en/translation_review.pending.json est une fiche préparatoire ; ne pas la renommer en revue officielle ni cocher les approbations restantes automatiquement. Aucun fr_content_lock ni en_translation_lock n’est fabriqué.\n\n149 traductions de citations et les deux passages passent les validateurs natifs. Q092/Q120 sont des cas de source déjà bilingue, relus explicitement. Ne pas supprimer les 149 citations, les deux passages, les 32 résumés ou les 120 absences de résumé. Ne pas copier les dates de création ou initialisations françaises en anglais.\nLes identifiants locaux de livraison doivent être raccordés au natif par titre français, révision et hash, pas par numéro seul.\n\nPoursuivre les points exacts du rapport : authenticité des citations, références historiques incertaines, découverte de noms, existence des liens/images cibles, préservation compatible des métadonnées/références françaises avant verrouillage natif, puis seulement revues de lots et convergence sémantique officielles. Ne jamais présenter les deux audits d’intégrité comme une validation documentaire complète.\nAucune page wiki à publier ; aucun relais de publication à utiliser ; aucun environnement à modifier ou republier.\n',encoding='utf-8')
for f in ['page-documentary-selection-final.json','documentary-changes-selected.json','sources_en_selected.json','source-topics-selected.json','final-integrity-audit.json','selected-integrity-audit.json','parameters-after.json','working-files-manifest.json','native-citation-validation.json','native-quotes-validated.json','native-classification-preservation-issues.json','native-integration-state.json','graph-placement-reading.json','native-title-issues.json','source-reading-notes.json','target-wiki-recheck-rev38.json']:
    cp(O/f,D/'reviews'/f)
for p in sorted(R.glob('notes-*.json')):cp(p,D/'reviews/textual'/p.name)
for f in ['RAPPORT_RELECTURE.md','corrections.json','supplemental-risk-review.json']:
    cp(R/f,D/'reviews/textual'/f)
cp(R.parent/'identity-map.json',D/'reviews/source-identity-map.json')
cp(R.parent/'documentary-research-by-page.json',D/'research/documentary-research-by-page.previous.json')
for f in ['research-results.json','exact-research-results.json','extra-fulltext-results.json','document-fulltext-results.json','specific-source-results.json','targeted-gap-results.json','institutional-term-results.json','residual-reference-results.json','media-link-results.json','name-search-results.json','uruguay-report-evidence.json','clinical-stigma-evidence.json','final-source-probes.json']:
    cp(O/f,D/'research'/f)
(D/'research/LIMITES.txt').write_text('Les résultats de recherche et codes HTTP sont des preuves de consultation, pas des attestations de pertinence. En particulier les résultats Bing par page sont hors sujet et non concluants. Les corps HTTP/PDF ne sont pas redistribués ; les notices retenues indiquent la portée réelle de lecture et leurs limites. Les chemins body_path sont des emplacements historiques locaux, pas des fichiers présents dans ce paquet.\n')
for f in ['curate_documentation.py','integrate_native_pending.py','parameters_selected.py','final_audit_selected.py','audit_selected.py','graph_review.py','package_review.py']:
    cp(O/f,D/'scripts'/f)
shutil.copytree(P/'corpus/cannabis',D/'native/project/corpus/cannabis',ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
for rel in ['.state/editorial-workspaces/cannabis/EN-CANNABIS-20261021','.state/corpus-promotions/cannabis']:
    shutil.copytree(P/rel,D/'native/project'/rel,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
save(D/'native/code-provenance.json',dict(repository='https://github.com/wikidebates/wikidebia',branch='fix/preserve-interquotation-prose',commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=P,text=True).strip(),pull_request='https://github.com/wikidebates/wikidebia/pull/9',merged_to_main=False))
save(D/'provenance/original-delivery.json',dict(filename='cannabis_traduction_en_2026-10-21_verifiee.zip',sha256='b317df79f35b047af2bdead55c5adbdb33c835fae528ed69f0de78e5d8332eda',source_snapshot='provenance/source/',delivery_local_ids=True))
save(D/'MANIFEST_SHA256.json',dict(schema='wikidebia-continuation-file-manifest-1.0',generated_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),publication_ready=False,files=[dict(path=str(p.relative_to(D)),sha256=sha(p),bytes=p.stat().st_size) for p in sorted(D.rglob('*')) if p.is_file()]))
manifest=load(D/'MANIFEST_SHA256.json')
assert all(sha(D/r['path'])==r['sha256'] for r in manifest['files'])
z=D.with_suffix('.zip');assert not z.exists()
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as out:
    for p in sorted(D.rglob('*')):
        if p.is_file():out.write(p,str(p.relative_to(D)))
# Vérification indépendante du contenu archivé, sans écraser la livraison.
verify=O/'archive-verification';assert not verify.exists()
with zipfile.ZipFile(z) as archive:
    assert all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in archive.namelist())
    archive.extractall(verify)
assert all(sha(verify/r['path'])==r['sha256'] for r in manifest['files'])
assert {str(p.relative_to(verify)) for p in verify.rglob('*') if p.is_file()}=={r['path'] for r in manifest['files']}|{'MANIFEST_SHA256.json'}
backup=B/'continuation/documentation-et-integration-native-20261021';assert not backup.exists()
shutil.copytree(D,backup)
receipt=dict(archive_path=str(z),sha256=sha(z),manifested_files=len(manifest['files']),archive_bytes=z.stat().st_size,fresh_extraction_verified=True,backup_relative_path=str(backup.relative_to(B)),publication_ready=False)
save(O/'delivery-receipt.json',receipt)
print(json.dumps(receipt,ensure_ascii=False,indent=2))
