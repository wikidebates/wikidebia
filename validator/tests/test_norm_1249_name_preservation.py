from pathlib import Path
import hashlib, json
from wikidebia_validator.validator import validate_package
from .helpers import create_fr_package, dump


def _package(root: Path, source_has_name: bool = True):
    create_fr_package(root)
    manifest=json.loads((root/'manifest.json').read_text())
    manifest['translation_status']={'en':'deferred'}
    page=manifest['pages'][1]
    path=root/page['file_path']
    text=path.read_text()
    if source_has_name:
        text=text.replace('{{Argument\n','{{Argument\n|nom=Argument historique\n',1)
    path.write_text(text)
    inventory_path=root/'data/initial_remote_inventory_fr.json'
    inventory={'inventory_version':'1.0','inventory_mode':'explicit_debate_pages_read_only','debate_id':manifest['debate_id'],'language':'fr','generated_at':'2026-08-07T00:00:00+00:00','pages':[{'page_id':page['page_id'],'page_type':'argument','canonical_title':page['canonical_title'],'content_sha256':hashlib.sha256(text.encode()).hexdigest(),'revision_id':42,'status':'published','content':text}],'inventory_sha256':'0'*64}
    dump(inventory_path,inventory)
    manifest['editorial_controls']={'legacy_content_preservation':{'enabled':True,'lock_path':'data/historical_content_lock.json','protected_fields':['nom'],'source_archive_sha256':'a'*64,'verification_revision':'0.4.52','source_inventory_path':'data/initial_remote_inventory_fr.json','source_inventory_sha256':hashlib.sha256(inventory_path.read_bytes()).hexdigest()}}
    # lifecycle state: nom is protected for preexisting arguments
    page['page_origin']='preexisting'
    page['preserved_parameters']={'avertissements-argument':{'present':True,'value':'Argument généré par IA'},'nom':{'present':source_has_name,'value':'Argument historique' if source_has_name else None}}
    dump(root/'manifest.json',manifest)
    dump(root/'data/historical_content_lock.json',{'schema_version':'1.2','debate_id':manifest['debate_id'],'source_archive':'source.zip','source_archive_sha256':'a'*64,'protected_fields':['nom'],'arguments':[{'id':page['page_id'],'language':'fr','summary_provenance':'generated_after_import','initialisation':{'present':False},'nom':{'present':source_has_name,**({'value':'Argument historique'} if source_has_name else {})}}]})
    return page,path


def test_historical_name_is_allowed_and_preserved(tmp_path: Path):
    page,path=_package(tmp_path,True)
    report=validate_package(tmp_path,scopes=['schema','wikicode'])
    assert not any(f.code in {'WDV-MWK-003','WDV-EDT-027','WDV-MWK-023'} and f.path==page['file_path'] for f in report.findings)


def test_historical_name_removal_is_blocked(tmp_path: Path):
    page,path=_package(tmp_path,True)
    path.write_text(path.read_text().replace('|nom=Argument historique\n',''))
    report=validate_package(tmp_path,scopes=['wikicode'])
    assert any(f.code=='WDV-EDT-027' and 'nom historique' in f.message for f in report.findings)


def test_historical_name_change_is_blocked(tmp_path: Path):
    page,path=_package(tmp_path,True)
    path.write_text(path.read_text().replace('|nom=Argument historique','|nom=Argument modifié'))
    report=validate_package(tmp_path,scopes=['wikicode'])
    assert any(f.code=='WDV-EDT-027' and 'nom historique' in f.message for f in report.findings)


def test_name_cannot_be_invented_when_historically_absent(tmp_path: Path):
    page,path=_package(tmp_path,False)
    path.write_text(path.read_text().replace('{{Argument\n','{{Argument\n|nom=Nom inventé\n',1))
    report=validate_package(tmp_path,scopes=['wikicode'])
    assert any(f.code=='WDV-EDT-027' and 'ajouté sans provenance' in f.message for f in report.findings)
