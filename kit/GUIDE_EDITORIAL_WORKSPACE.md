# Workspace éditorial d’un corpus promu

Le kit 2.15.1 ouvre un espace de travail éditorial à partir d’un corpus déjà promu au statut `graph_validated`.

```bash
./wikidebia corpus-workspace-init dieu_existe
```

Un identifiant de Work est attribué automatiquement sous la forme `EDIT-AAAAMMJJ-NNN`. Il peut être fixé explicitement :

```bash
./wikidebia corpus-workspace-init dieu_existe --work-id EDIT-DIEU-001
```

## Séparation entre corpus et workspace

Le corpus source reste sous :

```text
corpus/<debate_id>/
```

Le workspace est créé sous :

```text
.state/editorial-workspaces/<debate_id>/<work_id>/
```

Il contient une copie complète et initialement identique du corpus dans `working-copy/`. Le kit calcule l’empreinte SHA-256 du corpus source avant et après l’opération et vérifie l’identité de la copie. Le workspace apparaît seulement après un renommage local de son dossier temporaire entièrement construit.

Le corpus source n’est jamais modifié. Un corpus au statut `graph_draft`, un lien symbolique, un corpus contenant déjà des pages finales ou un workspace préexistant sont refusés.

## Fichiers produits

- `workspace.json` : identité du Work, empreintes du corpus et limites de la phase ;
- `working-copy/` : copie éditoriale complète du corpus promu ;
- `audits/editorial_inventory.json` et `.md` : diagnostics initiaux ;
- `reviews/fr/page_metadata_review.json` : revue page par page des titres, rubriques et mots-clés ;
- `reviews/en/translation_readiness.json` : préparation de la future traduction anglaise ;
- `tasks/editorial_tasks.json` : tâches à traiter ;
- `data/keyword_vocabulary_working.json` : vocabulaire contrôlé de travail et usages observés ;
- `changes/changeset.json` : registre vide des futures modifications.

## Portée de l’audit initial

L’audit signale notamment :

- titres canoniques ou affichés manquants, tronqués, mal ponctués ou potentiellement dépendants du contexte ;
- titres affichés identiques au titre canonique ou ne semblant pas former une proposition complète ;
- rubriques absentes, invalides, dupliquées, non ordonnées ou issues d’un repli d’import ;
- mots-clés trop peu nombreux, trop nombreux, dupliqués, trop longs ou issus d’un repli d’import ;
- jeu exact de mots-clés dominant plus de 25 % des arguments ;
- proportion de titres affichés identiques supérieure à 10 % ;
- métadonnées anglaises encore absentes.

Les contrôles sémantiques sont nécessairement humains. Les signaux sur la propositionnalité ou l’autonomie des titres sont explicitement marqués comme heuristiques. Ils ouvrent une tâche mais ne valident ni ne corrigent une page.

## Limites de cette phase

Cette commande :

- n’applique aucune correction éditoriale ;
- ne modifie pas le registre du corpus source ;
- ne génère aucun fichier sous `output/` ;
- ne traduit aucune page ;
- ne contacte pas MediaWiki ;
- ne prépare pas encore un plan de reprise distante.

La traduction anglaise reste explicitement bloquée dans son registre tant que les métadonnées françaises ne sont pas revues et verrouillées.

## Étape suivante

Une fois les registres complétés, utiliser `corpus-workspace-review --finalize`, puis `--apply` avec l’empreinte renvoyée. Le guide détaillé est `GUIDE_EDITORIAL_REVIEW.md`. L’application crée `reviewed-copy/` et conserve `working-copy/` intact.
