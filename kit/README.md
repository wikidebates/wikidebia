# Wikidéb’IA — Kit 2.15.29

Le kit 2.15.29 intègre la recherche des appellations consacrées pour les arguments nouveaux. Chaque argument généré doit être associé à une revue documentaire ; le résultat normal est l’absence de nom. `nom` / `name` n’est rendu que lorsque la revue conclut `known_name` et documente que la littérature emploie réellement cette appellation pour le même raisonnement.
La revue française de contenu d’un workspace reste une phase d’import et ne crée pas d’arguments français nouveaux ; pour un corpus généré qui en contient, la revue 1.2.52 est fournie avec le corpus et contrôlée par le validateur. La traduction anglaise du kit renseigne séparément la revue des pages anglaises nouvelles.

Le kit 2.15.28 ajoute la prise en charge de l’attribution éditoriale explicite de `nom` / `name` selon la politique 1.2.51. Un nom historiquement absent reste protégé par défaut ; il ne peut être ajouté que pour une page Argument inscrite dans un registre approuvé par le propriétaire, avec un titre et une valeur exacts.

La reprise distante applique cette exception uniquement à `nom` / `name`. Tous les autres paramètres historiques protégés conservent les garanties de la révision 2.15.27.

Kit aligné sur la norme 1.2.52 et le validateur 0.4.55.
