# Wikidéb’IA — Kit 2.15.5

Kit générique complet aligné sur la norme 1.2.30 et le validateur 0.4.32. La projection anglaise localise désormais tous les modèles et tous les paramètres. Pour les citations, `{{Citation}}` devient `{{Quote}}`; les noms deviennent `quote`, `authors`, `work`, `issue`, `location`, `publisher`, `place`, `link` et `warnings`, tandis que seules les valeurs de `quote` et de `date` sont traduites.

Toutes les commandes, protections distantes et fonctionnalités du bundle source 2.4.0 restent conservées.

## Correctif 2.15.5 — métriques du graphe

`graph-extract` 1.0.2 sépare désormais les niveaux (racine = 1), les profondeurs en nombre d’arêtes (racine = 0), les occurrences dépliées par chemins, les pages uniques, les feuilles réelles et les frontières vers un débat détaillé. `corpus-init-from-snapshot` distingue également les occurrences dépliées de l’extracteur des occurrences normatives du registre.
