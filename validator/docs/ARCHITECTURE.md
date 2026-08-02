# Architecture du validateur 0.4.26

Le validateur sépare schémas, cohérence, graphe, sources, wikicode, bilinguisme, éditorial et workflow. Pour la norme 1.2.24, le module wikicode inspecte localement les modèles Wikipédia explicatifs dans les introductions et résumés. Il vérifie leur syntaxe sans accéder au réseau ; l’existence et la pertinence de l’article restent attestées par la revue humaine.
