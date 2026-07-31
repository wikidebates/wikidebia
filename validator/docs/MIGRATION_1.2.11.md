# Migration vers la norme 1.2.11

1. Rechercher dans toutes les pages `.wiki` la séquence formée par `}}`, un ou plusieurs retours à la ligne éventuellement entourés d’espaces ou de tabulations, puis `{{`.
2. Remplacer chaque occurrence par la jonction exacte `}}{{` sans modifier le contenu des deux modèles.
3. Appliquer la même correction aux agrégats régénérés depuis les pages individuelles.
4. Conserver toutes les règles 1.2.10 sur les références directes, les dates documentaires, la pluralité documentaire, les acronymes et la publication française indépendante.
5. Déclarer `consolidated_norm` à `1.2.11`, utiliser le validateur 0.4.11 et le kit 2.1.11, puis recalculer les empreintes.
