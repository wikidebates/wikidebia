# Initialisation d’un corpus depuis un snapshot

Le kit 2.15.17 transforme un paquet produit par `graph-extract` en corpus local au statut `graph_draft`.

```bash
./wikidebia corpus-init-from-snapshot \
  .state/graph-extract/dieu_existe \
  --debate-id dieu_existe \
  --short-code DIEU
```

Le résultat est écrit par défaut dans :

```text
.state/corpus-builds/<debate_id>/
```

## Séparation entre import et sortie normative

Les wikicodes récupérés sont conservés sous :

```text
imports/fr/debate/debate.wiki
imports/fr/arguments/A0001.wiki
```

Ils constituent une provenance historique. Ils ne sont pas copiés dans `output/fr/` et ne sont pas déclarés comme pages générées ou validées. Les fichiers de sortie restent `pending` jusqu’au Work éditorial.

## Fichiers construits

- `manifest.json` au statut `graph_draft` ;
- `scope.json` provisoire ;
- `data/registre_debat.json` ;
- `data/import_provenance.json` ;
- `data/sources.json` ;
- `graph/graphe_argumentatif.json` ;
- `graph/graphe_argumentatif.md` ;
- registres de revue initialisés à `pending` ;
- rapport d’import ;
- rapports de validation structurelle initiale.

## Identifiants et occurrences

Les identifiants sont déterministes pour un même snapshot :

- nœuds : `A0001`, `A0002`, etc. ;
- relations : `E00001`, `E00002`, etc. ;
- occurrences : `O00001`, `O00002`, etc.

Une occurrence principale est créée pour chaque nœud. Une réutilisation crée une occurrence secondaire sans redéploiement de ses enfants, conformément au modèle normatif du registre. Le nombre d’occurrences normatives peut donc être inférieur au nombre de chemins du graphe entièrement déplié indiqué par l’extracteur. La sortie machine distingue désormais `source_unfolded_occurrences` et `normative_occurrences`; l’ancien champ `occurrences` reste un alias des occurrences normatives.

## Validation initiale

La commande lance automatiquement les portées suivantes du validateur local :

- `schema` ;
- `coherence` ;
- `graph` ;
- `files` ;
- `workflow`.

Elle n’exécute pas encore les contrôles `wikicode` ou `editorial`, car les pages importées ne sont pas des sorties normatives.

## Options utiles

```bash
--output-dir CHEMIN
--scope-summary TEXTE
--overwrite
--skip-validation
```

`--output-dir`, lorsqu’il est utilisé, doit rester sous `.state/corpus-builds/`. `--overwrite` ne concerne que le build local sélectionné dans cette zone. L’argument positionnel doit désigner la racine complète du paquet `graph-extract` ou son ZIP audité, et non le seul sous-dossier `snapshot/`, car le graphe JSON et le manifeste SHA-256 sont également requis. Le manifeste complet du paquet d’extraction, le graphe, le snapshot et chaque page importée sont revérifiés avant toute écriture locale. Aucune écriture MediaWiki et aucune promotion vers `corpus/` ne sont effectuées.
## Étape suivante

Le build reste volontairement sous `.state/corpus-builds/`. Sa revue et sa promotion utilisent ensuite :

```bash
./wikidebia corpus-review-graph <debate_id> --prepare
./wikidebia corpus-review-graph <debate_id> --finalize
./wikidebia corpus-promote <debate_id> --confirm-review-sha256 <empreinte>
```

Ces commandes ne génèrent pas encore de pages. Voir `GUIDE_CORPUS_REVIEW.md`.


## Profondeur

Sous les normes 1.2.31 et suivantes, le build utilise `depth_policy.limit_policy=unbounded`. La profondeur maximale observée est descriptive ; aucune limite, cible normale, justification d’exception ou alerte numérique n’est générée.
