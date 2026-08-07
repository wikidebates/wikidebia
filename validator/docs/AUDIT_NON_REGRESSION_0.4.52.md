# Audit de non-régression — validateur 0.4.52

Le contrôle 0.4.52 protège `nom` / `name` comme donnée historique indépendante des titres canoniques et affichés. Les tests couvrent la conservation exacte d’une valeur existante, le refus de sa suppression, le refus de sa modification et le refus d’inventer le paramètre lorsqu’il était historiquement absent. Les protections antérieures de contenu historique, de frontières `débat-détaillé` et d’adoption distante restent actives.

La suite livrée contient 302 tests et passe sans échec.
