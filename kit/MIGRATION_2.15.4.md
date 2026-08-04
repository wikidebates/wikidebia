# Migration vers le kit 2.15.4

Le kit 2.15.4 corrige uniquement la présentation et l’audit des métriques de `graph-extract`, ainsi que la terminologie des occurrences affichée par `corpus-init-from-snapshot`.

Les snapshots et builds créés avec 2.15.3 restent lisibles. Pour régénérer les rapports d’un graphe déjà capturé sans relire le wiki, relancer la même commande `graph-extract` sans `--force-refresh` : le cache local est réutilisé.

Les nouveaux champs distinguent :

- `niveau_minimal_maximal_pages_uniques` ;
- `niveau_maximal_occurrences` ;
- `profondeur_maximale_en_aretes` ;
- `occurrences_argumentatives_depliees_par_chemins` ;
- `pages_sans_sortie_dans_graphe_extrait` ;
- `pages_terminales_reelles` ;
- `relations_locales_ignorees_aux_frontières`.

Les anciens alias `profondeur_maximale`, `occurrences_argumentatives` et `occurrences` restent présents pour compatibilité, mais les libellés explicites doivent être privilégiés.

## Correctif ultérieur

La version 2.15.4 a conservé les noms des anciens champs, mais a modifié par erreur la valeur de certains alias historiques. Cette régression de compatibilité est corrigée par le kit 2.15.5 et l’extracteur 1.0.2.
