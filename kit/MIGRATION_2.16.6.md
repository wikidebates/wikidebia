# Migration 2.16.6

Correctif de cohérence de provenance après exécution des décisions structurelles du graphe.

- base autoritative : commit GitHub `5eca765` (1.2.77 / 0.4.80 / 2.16.5) ;
- aucune modification des schémas, de la norme éditoriale ou des décisions de revue ;
- les futures actions `update`/`redirect` actualisent immédiatement `sha256` et `size_bytes` dans `data/import_provenance.json` ;
- une reprise d’un état 2.16.4/2.16.5 répare seulement un fichier explicitement attesté par `reviews/graph_action_decisions.json`, avec contenu post-action exact et révision distante avancée ;
- aucune réécriture distante n’est effectuée par cette réparation ;
- toute divergence extérieure ou non attestée reste bloquante.
