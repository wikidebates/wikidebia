# Migration vers la norme 1.2.39

Cette révision protège les contenus historiques contre les corrections hors périmètre. Les corpus anciens peuvent activer uniquement l'atomicité des mots-clés avec `keyword_policy_revision=1.2.39`. Les résumés ne sont alors ni réécrits ni soumis rétroactivement au contrôle d'originalité.

Le paramètre `initialisation` est conservé seulement lorsqu'un verrou historique atteste sa présence et sa valeur. Les pages nouvelles continuent de ne pas l'utiliser.
