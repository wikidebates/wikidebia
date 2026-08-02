# Architecture du validateur 0.4.28

Le validateur sépare schémas, cohérence, graphe, sources, wikicode, bilinguisme, éditorial, workflow et plans distants. Pour la norme 1.2.26, il conserve tous les contrôles de contenu antérieurs et valide localement les plans, états et reçus sans les exécuter. L’attestation distante `no_changes`, la sélection stricte des archives, le nettoyage du staging et la conservation des suppressions différées relèvent du kit 2.2.13 et sont couverts par ses tests d’intégration.
