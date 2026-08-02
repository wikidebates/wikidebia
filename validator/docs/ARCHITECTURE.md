# Architecture du validateur 0.4.24

Le validateur sépare schémas, cohérence, graphe, lots, sources, fichiers, wikicode, bilinguisme, éditorial et workflow. La commande `validate` demeure strictement en lecture seule ; `recalc --write` reste la seule commande d’écriture locale.

Sous la norme 1.2.22, le module éditorial calcule le taux d’identité exacte entre titre canonique et titre affiché pour chaque langue. `WDV-EDT-001` bloque au-delà de 10 %. Le registre individuel atteste la recherche de concision et fournit une justification spécifique pour chaque identité conservée. Les contrôles propositionnels et de placement restent respectivement assurés par `WDV-EDT-021` et `WDV-EDT-022`.
