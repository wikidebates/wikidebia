# Audit des noms internes après le renommage MediaWiki — kit 2.15.56

Recherche effectuée sur les trois composants pour `detailed_debate` et `complete_topic`.

## Conclusion

Les deux identifiants ne doivent pas faire l’objet d’un remplacement global : la migration 1.2.69 conserve explicitement `complete_topic` et `detailed_debate` comme clés techniques internes afin de préserver les registres, verrous et artefacts historiques.

La régression observée était différente : `argparse` créait `follow_local_relations_at_dedicated_debate`, tandis que deux chemins d’exécution lisaient encore `args.follow_local_relations_at_detailed_debate`. Ces accès ont été corrigés.

## Garde-fous

- zéro occurrence de `args.follow_local_relations_at_detailed_debate` dans `kit/scripts/` ;
- le gestionnaire utilise `follow_local_relations_at_dedicated_debate` ;
- l’extracteur utilise `args.follow_local_relations_at_dedicated_debate` ;
- l’alias CLI `--follow-local-relations-at-detailed-debate` reste accepté et converge vers le nouvel attribut ;
- les clés `complete_topic` / `detailed_debate` restent inchangées dans les structures internes ;
- les paramètres MediaWiki émis restent `sujet-développé` / `expanded-topic` et `débat-dédié` / `dedicated-debate`.

## Tests

La suite complète du kit passe avec 375 tests, dont des régressions nouvelles couvrant `argparse → main()` et les deux noms d’option CLI.
