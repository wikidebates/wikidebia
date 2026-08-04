# Migration vers le kit 2.15.5

Le kit 2.15.5 corrige la compatibilité des sorties `graph-extract` sans retirer les métriques explicites introduites en 2.15.4.

Les champs explicites ont la sémantique non ambiguë suivante :

- `niveau_minimal` et `niveau_maximal_occurrences` comptent les niveaux à partir de 1 ;
- `profondeur_minimale_en_aretes` et `profondeur_maximale_en_aretes` comptent les arêtes à partir de 0 ;
- `pages_terminales_reelles` exclut les frontières et les pages manquantes ;
- `pages_sans_sortie_dans_graphe_extrait` inclut toute page sans relation conservée.

Pour éviter toute régression chez les consommateurs historiques, les anciens champs conservent exactement leur sémantique 1.0.0 :

- `profondeur_minimale` reste l’ancien niveau minimal commençant à 1 ;
- `occurrences_par_profondeur` reste indexé par les anciens niveaux commençant à 1 ;
- les profondeurs historiques des relations restent les anciens niveaux ;
- `profondeur_maximale` reste le niveau minimal maximal des pages uniques dans les métadonnées, et le niveau maximal des occurrences dans une branche ;
- `pages_terminales` reste le nombre de pages sans sortie dans le graphe extrait.

Les snapshots et rapports 1.0.0 ou 1.0.1 restent lisibles. Il n’est pas nécessaire de relire le wiki : relancer `graph-extract` sans `--force-refresh` régénère les rapports depuis le cache local.
