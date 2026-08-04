# Migration vers le kit 2.15.1

Le kit 2.15.1 est une correction de non-régression de 2.15.0. Les fonctions et formats distants restent inchangés. La mise à niveau aligne les composants sur 1.2.28 / 0.4.30, complète `doctor` et restaure deux modes exécutables historiques. Le test de staging répare aussi les extractions réalisées par un gestionnaire antérieur à 2.15.1, puis le nouveau gestionnaire réapplique désormais les permissions Unix déclarées dans les ZIP.

Les workspaces 1.2.27 sont acceptés par le rendu comme révision précédente migrable. Les preuves qui engagent explicitement la version du kit doivent être reconstruites avec 2.15.1 avant exécution.
