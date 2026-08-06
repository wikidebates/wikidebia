# Revue française des titres, rubriques et mots-clés

Le kit 2.15.19 transforme les décisions consignées dans un workspace éditorial en métadonnées françaises validées et verrouillées pour la future génération des pages.

## 1. Compléter les registres

Après :

```bash
./wikidebia corpus-workspace-init <debate_id> --work-id <work_id>
```

compléter :

```text
.state/editorial-workspaces/<debate_id>/<work_id>/reviews/fr/page_metadata_review.json
.state/editorial-workspaces/<debate_id>/<work_id>/data/keyword_vocabulary_working.json
```

Chaque page reçoit une décision explicite sur :

- le titre canonique et le titre affiché, pour les arguments ;
- les rubriques ;
- les mots-clés ;
- les attestations de propositionnalité, d’intelligibilité, d’autonomie et d’équivalence sémantique ;
- lorsque le titre affiché diffère, l’attestation que cette différence améliore réellement la lisibilité ;
- les justifications propres à chaque rubrique et à chaque mot-clé.

Le vocabulaire de travail couvre exactement les mots-clés finalement retenus. Chaque terme français possède une définition, une nature grammaticale, une justification de portée inter-débat et la liste exacte de ses usages. La traduction anglaise peut rester vide à ce stade.

## 2. Finaliser sans modifier le corpus

```bash
./wikidebia corpus-workspace-review <debate_id> \
  --work-id <work_id> \
  --finalize
```

La commande vérifie notamment :

- la couverture de la page Débat et de tous les nœuds actifs ;
- l’absence de collision entre titres canoniques ;
- la conformité formelle et l’intelligibilité des titres affichés ;
- l’acceptation sans quota du titre canonique comme titre affiché lorsqu’il est déjà le plus clair ;
- la justification d’un titre distinct par un gain réel de lisibilité et une équivalence sémantique stricte ;
- une à quatre rubriques, avec justification individuelle ;
- cinq à huit mots-clés pour la page Débat et deux à quatre pour chaque argument ;
- le maximum de 25 % pour un même jeu exact de mots-clés parmi les arguments ;
- la couverture et la qualité du vocabulaire contrôlé ;
- l’intégrité du corpus source et de `working-copy/`.

La revue est ensuite scellée par `review_sha256`. Cette opération ne modifie ni `corpus/`, ni `working-copy/`, ni les imports de provenance.

## 3. Appliquer la revue scellée

```bash
./wikidebia corpus-workspace-review <debate_id> \
  --work-id <work_id> \
  --apply \
  --confirm-review-sha256 <empreinte>
```

L’application crée :

```text
.state/editorial-workspaces/<debate_id>/<work_id>/reviewed-copy/
```

`working-copy/` reste l’instantané initial intact. `reviewed-copy/` contient :

- le registre maître mis à jour ;
- la projection du graphe et son rapport Markdown recalculés ;
- une nouvelle empreinte structurelle lorsque les titres ont changé ;
- `data/fr_page_metadata_lock.json` ;
- le vocabulaire français contrôlé dans `data/keyword_vocabulary.json` ;
- le changeset exhaustif dans `changes/changeset.json`.

Les fichiers de `imports/fr/` restent octet pour octet identiques. Aucun fichier final n’est créé sous `output/`.

Après application, le registre de préparation anglaise passe de `blocked_by_french_review` à `ready_for_translation`. Cela autorise seulement la phase suivante ; aucune traduction n’est encore produite.

## Ordre des mots-clés

Chaque liste `proposed_keywords` est classée du mot-clé le plus directement pertinent au moins direct. La chronologie de création, l’ordre d’import et l’ordre alphabétique ne sont pas utilisés. La revue exige `keywords_ordered_by_relevance=true` et une `keyword_order_rationale` propre à la page.
