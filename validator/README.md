# Validateur stable Wikidéb’IA 0.4.17

Validateur local Python 3 aligné sur la norme 1.2.16 et compatible avec les paquets déclarant les normes 1.1.0 à 1.2.16. `validate` reste en lecture seule ; `recalc --write` est la seule écriture locale sur un corpus. Le validateur ne se connecte jamais à MediaWiki.

```bash
PYTHONPATH=src python scripts/wikidebia_validate.py validate /chemin/vers/corpus
```

## Plans de reprise distante

La commande suivante contrôle un plan déjà produit par le kit sans lire le wiki :

```bash
PYTHONPATH=src python scripts/wikidebia_validate.py validate-plan plans/debat/update-plan.json
```

Elle vérifie le JSON Schema, l’empreinte signée, les compteurs, les opérations mutantes contradictoires, les préconditions de mise à jour et de suppression, et la présence des comparaisons associées à `manual_review`. Les codes stables sont `WDV-RMT-001` à `WDV-RMT-006`.

Les schémas 0.4.17 couvrent :

- l’état publié signé ;
- les migrations de renommage et de fusion ;
- le plan de reprise distante ;
- le reçu final de reprise.

## Corpus historiques

Les versions inscrites dans `manifest.normative_versions` restent une provenance historique. La publication ou la reprise exécute le validateur courant et exige un rapport positif pour une norme listée dans `COMPATIBILITY.json`.

La source normative active embarquée est `normative_reference/01_normes/WIKIDEBIA_NORME_CONSOLIDEE_1.2.16.md`.
