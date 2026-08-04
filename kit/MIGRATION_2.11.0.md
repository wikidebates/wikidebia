# Migration vers le kit 2.11.0

Le kit 2.11.0 ajoute `corpus-workspace-release`. La commande exige l’empreinte exacte de `rendered-copy/`, crée une `release-copy/` distincte, génère un ZIP autonome et un reçu externe sous `.state/corpus-releases/`, puis marque le corpus `release_ready` sans autoriser d’écriture distante.

Le ZIP contient un manifeste de libération exhaustif et une entrée préparatoire pour la future comparaison avec l’état publié. Aucun inventaire distant, plan de reprise ou appel MediaWiki n’est effectué dans cette phase.
