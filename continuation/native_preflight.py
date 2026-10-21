from pathlib import Path
import json,subprocess,datetime
ROOT=Path('/workspace/work/cannabis-correction-relecture');OUT=Path(__file__).parent
cmd=['/workspace/wikidebia/.venv/bin/python',str(ROOT/'kit/scripts/wikidebia_translation_review.py'),'--project-root',str(ROOT),'cannabis','--work-id','W001','--prepare']
# The native preflight must report missing state. Do not invent lock files or attestations.
r=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True)
report=dict(schema='wikidebia-translation-native-integration-preflight-1.0',checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),command=cmd,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,source_build_status='graph_draft',source_reviews_preserved=True,english_translation_applied=False,official_semantic_convergence_performed=False)
(OUT/'native-integration-preflight.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(r.returncode,r.stdout,r.stderr)
