# Orchestration des revues éditoriales ChatGPT — Kit 2.16.7

## Usage normal

Pour lancer ou reprendre la préparation bilingue d'un débat existant :

```bash
./wikidebia workflow "Un revenu de base doit-il être instauré ?"
```

La commande réutilise un snapshot `graph-extract` compatible déjà présent lorsque c'est possible ; sinon elle effectue l'extraction en lecture seule. Elle initialise le corpus, lance les validations mécaniques et s'arrête au premier point où une décision éditoriale externe est requise.

Exemple :

```text
Revue du graphe préparée.
191 placements doivent être analysés par ChatGPT.

Envoyez ce fichier à ChatGPT :
outgoing/revenu_de_base_graph_review.zip

Après correction, réimportez le ZIP rendu avec :
./wikidebia review-import revenu_de_base <fichier_corrige.zip>
```

Après le retour de ChatGPT :

```bash
./wikidebia review-import revenu_de_base fichier_corrige.zip
```

Le kit vérifie le paquet, installe uniquement les fichiers autorisés, finalise et applique la revue, puis poursuit automatiquement jusqu'au prochain point éditorial. Aucun SHA-256 n'est à recopier manuellement.

L'état courant est consultable avec :

```bash
./wikidebia workflow-status revenu_de_base
```

## Contrat des paquets

Un paquet de revue contient uniquement :

- `REVIEW_PACKAGE.json` : provenance et empreintes ;
- `INSTRUCTIONS.md` : consignes de la revue ;
- `editable/` : seuls fichiers que ChatGPT peut modifier ;
- `context/` : sources nécessaires en lecture seule.

Le retour doit conserver exactement cette structure. Les fichiers de contexte, le manifeste et les instructions ne peuvent pas être modifiés. Les fichiers supplémentaires sont refusés. Les chemins dangereux, liens symboliques et paquets provenant d'un autre débat, d'un autre Work ou d'une ancienne revue sont refusés.

`outgoing/` est une zone privée exclue de Git. Aucun secret, cookie, fichier Pywikibot privé, configuration locale ou état de publication n'est inclus par les listes blanches de revue.

## Points éditoriaux orchestrés

Le cycle courant couvre successivement :

1. graphe et placements ;
2. titres, rubriques et mots-clés français ;
3. introduction, résumés et documentation française ;
4. traduction et documentation anglaises, y compris la recherche d'`established-name=` lorsqu'elle s'applique ;
5. première passe de convergence sémantique ;
6. deuxième passe indépendante de convergence.

Si une passe sémantique trouve une erreur certaine, la traduction est rouverte, les constatations sont fournies comme contexte dans un paquet de correction, puis les deux passes de convergence recommencent sur la nouvelle empreinte.

Après deux passes propres et indépendantes, l'application, le rendu et la construction `release_ready` sont automatiques. Le workflow normal n'exécute aucune publication distante ; l'exception explicite `review-import ... --execute-graph-actions` ne concerne que les mutations structurelles déjà décidées pendant la revue du graphe.

## Commandes avancées

Toutes les primitives existantes restent disponibles (`corpus-review-graph --prepare/--finalize`, `corpus-promote`, `corpus-workspace-review`, `corpus-workspace-content-review`, `corpus-workspace-translation`, `corpus-workspace-semantic-convergence`, etc.). Elles constituent la couche d'audit/debug et restent autoritatives ; l'orchestrateur ne fait que les enchaîner et résoudre automatiquement leurs confirmations mécaniques.
## Blocage technique avant une revue

La validation initiale distingue désormais les anomalies éditoriales différables des erreurs structurelles. Un titre importé à reformuler n’empêche pas la création du paquet de revue des métadonnées. En revanche, un cycle, une relation invalide ou une incohérence d’occurrence reste bloquant.

Dans ce cas, l’utilisateur n’a pas à rechercher un rapport sous `.state/`. Le programme affiche les principaux diagnostics et crée automatiquement :

```text
outgoing/<debate_id>_initial_validation_diagnostic.zip
```

Ce fichier peut être envoyé tel quel à ChatGPT pour diagnostic. Après correction du kit ou des données, relancer exactement la même commande `./wikidebia workflow ...` : la validation bloquée est réessayée et le workflow reprend automatiquement.
## Appliquer une revue du graphe avec actions distantes

Lorsqu’un ZIP de revue rejetée contient des décisions structurelles explicites, utilisez :

```bash
./wikidebia review-import <debate_id> <zip_revu> --execute-graph-actions
```

Cette commande valide d’abord la projection locale complète, préflight toutes les pages distantes concernées, puis applique dans l’ordre les modifications des pages mères, les redirections des doublons et les suppressions non fusionnées. Les actions possibles sont `remove`, `merge_redirect`, `move` et `relation_change`. Un doublon est remplacé par `#REDIRECTION [[Destination]]` et le résumé de la page mère mentionne `[[Destination]]`. Les résumés génériques `Corrections` ne sont pas utilisés. Après succès, une nouvelle revue complète du graphe est automatiquement préparée.


## Transaction de réimport et reprise

À partir du kit 2.16.8, un `review-import` qui ne comporte pas d’écriture distante irréversible reste une transaction jusqu’au prochain arrêt éditorial. La revue n’est donc pas considérée comme définitivement consommée tant que l’avancement mécanique suivant n’a pas réussi. En cas d’échec, le workflow, la base revue et les artefacts mécaniques créés pendant la tentative sont restaurés ; le même ZIP peut être réimporté.

Les actions de graphe exécutées explicitement avec `--execute-graph-actions` constituent une frontière irréversible : si les écritures distantes ont réussi, leurs plans et reçus restent autoritatifs et le workflow reprend depuis l’état post-action au lieu de prétendre revenir avant les écritures.

## Compatibilité des composants lors de `upgrade`

À partir du gestionnaire 2.16.8, chaque composant est autoritatif pour sa propre version : `wikidebia-normes` pour `norm`, `wikidebia-validator` pour `validator`, et `wikidebia-kit` pour `kit`. Les autres numéros répétés dans leur `VERSIONS.json` sont des informations de provenance et ne doivent plus forcer le reconditionnement d’un composant inchangé. Les garde-fous portent sur la version propre du composant, l’anti-rétrogradation, la révision normative effectivement implémentée et les schémas/capacités déclarés.
