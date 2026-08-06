# Migration 1.2.40 — résumés absents plutôt que mécaniques

Le registre de provenance couvre chaque page Argument. Les états `absent_at_import` et `new_page_unwritten` imposent l’absence du paramètre `résumé` / `summary`. `authored_after_import` exige un contenu non vide et une revue individuelle. Les résumés `historical_existing` restent verrouillés sur l’inventaire source.
