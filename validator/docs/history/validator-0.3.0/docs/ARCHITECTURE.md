# Architecture du validateur

## Principes

Le validateur est une application locale sans état distant. La commande `validate` est strictement en lecture seule. Les écritures sont regroupées dans la commande distincte `recalc`, qui exige `--write`.

## Modules

| Module | Responsabilité |
|---|---|
| `schema_validation.py` | Chargement local des quatorze schémas, résolution des `$ref`, `FormatChecker` et validation JSON/JSONL |
| `coherence.py` | Identifiants du débat, cadrage, versions, projection, patch interlangue, journaux et manifeste de libération |
| `graph.py` | Identités, titres, relations, DAG, occurrences, profondeurs, compteurs et empreinte structurelle |
| `batches.py` | Lots, propriétaires, dépendances, couverture, chevauchements et instantanés d'entrée |
| `sources.py` | Registre documentaire, dédoublonnage et cohérence des usages |
| `files.py` | Présence, chemins, empreintes, manifestes individuels et inventaire de libération |
| `wikicode.py` | Analyse structurée des modèles MediaWiki, paramètres, sous-modèles, relations et agrégats |
| `bilingual.py` | Paires de pages, verrouillage anglais et correspondance rubriques-sections |
| `editorial.py` | Contrôles correctifs 1.1.0 : titres, classifications, résumés, documentation, dates et handoffs correctifs |
| `workflow.py` | États, validations préalables, Work, handoffs et transitions |
| `recalc.py` | Recalcul explicite des données dérivées, agrégats et empreintes |
| `report.py` | Sortie stable texte/JSON et niveaux `ERROR`, `WARNING`, `INFO` |

## Ordre d'exécution

1. JSON Schema ;
2. cohérence entre les fichiers ;
3. graphe ;
4. lots ;
5. sources ;
6. fichiers et empreintes ;
7. wikicode ;
8. bilingue ;
9. contrôles éditoriaux correctifs ;
10. workflow.

Chaque contrôle produit un code stable. Les erreurs d'un module n'empêchent pas volontairement les autres modules de rechercher des anomalies supplémentaires, sauf lorsqu'un document indispensable est illisible.

## Séparation des catégories de règles

### JSON Schema

Types, propriétés obligatoires, propriétés supplémentaires, formats, énumérations et cohérences locales exprimables sans contexte externe.

### Invariants sémantiques automatiques

DAG, références croisées, occurrence primaire, branches, profondeur, compteurs, couverture de lots, identité bilingue, hashes et états.

### Contrôles documentaires automatiques

Identifiants de sources, dédoublonnage par clé, état de vérification, usages, type et langue des références, paramètres documentaires MediaWiki.

### Contrôles éditoriaux humains

Force logique d'un argument, équilibre intellectuel, fidélité substantielle d'une source, qualité d'une traduction, quasi-doublons sémantiques non identifiables par clé et qualité rédactionnelle approfondie.

## Empreinte structurelle

L'empreinte est calculée sur un objet canonique contenant :

- les nœuds actifs triés par identifiant, avec titres canoniques et affichés français normalisés en NFC ;
- les relations actives triées par identifiant ;
- les occurrences actives triées par identifiant.

La sérialisation utilise `ensure_ascii=False`, `sort_keys=True`, `separators=(",", ":")`, `allow_nan=False`, puis UTF-8 sans BOM.

## Extension

Une nouvelle règle doit :

1. recevoir un code unique dans `codes.py` ;
2. être testée par au moins un cas négatif ;
3. ne pas modifier les fichiers en mode validation ;
4. conserver la compatibilité du format JSON de rapport ;
5. être ajoutée au catalogue documenté.

## Reprise corrective 1.1.0

Les handoffs W00–W10 restent des traces immuables de leurs états d’entrée. Pendant une reprise 1.1.0, leurs empreintes ne sont pas comparées aux fichiers actifs modifiés ; la nouvelle chaîne `handoff/corrective/` est contrôlée séparément. `validate` demeure sans écriture et `publication_gate` sépare la validité locale de l’autorisation distante.

## Lisibilité des résumés

Le module `editorial.py` calcule des métriques de longueur de phrases à partir du texte des résumés. Ces métriques produisent seulement un avertissement `WDV-EDT-013`. La conformité au style encyclopédique grand public et l'explication des termes techniques sont attestées par un registre de revue humaine couvrant chaque langue produite.
