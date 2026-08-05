# Guide de comparaison distante en lecture seule — Kit 2.15.11

## Commande

```bash
./wikidebia corpus-workspace-remote-compare <debate_id> \
  --work-id <work_id> \
  --confirm-release-sha256 <empreinte_de_release-copy> \
  --scope all
```

La commande ouvre les wikis uniquement en lecture. Elle ne vérifie pas les droits d’écriture, ne demande aucune confirmation d’exécution et n’appelle aucune méthode de création, modification, déplacement ou suppression.

## Base historique

Pour chaque langue, l’état publié signé est prioritaire. À défaut, le français est reconstruit depuis `data/import_provenance.json` et les fichiers `imports/fr/`; l’anglais reçoit une base vide explicite lorsqu’il s’agit d’une traduction nouvelle.

## Sorties

Les fichiers sont écrits sous `.state/remote-comparisons/<debate_id>/<work_id>/<comparison_id>/` :

- `baseline/fr.json` et `baseline/en.json` ;
- `remote-inventory.json` ;
- `read-only-events.jsonl` ;
- `update-plan.json` ;
- `plan-validation.json` et `plan-validation.txt` ;
- `comparison-receipt.json`.

Un plan contenant `manual_review` ou `blocked` reste un résultat de comparaison valable mais n’est pas exécutable.

## Portée française différée

La comparaison distante ignore les pages anglaises absentes lorsqu’un manifeste 1.2.x pris en charge déclare explicitement `translation_status.en=deferred`. Elle ne doit ni créer d'opération anglaise ni interpréter l'absence de lien français comme un retrait.

