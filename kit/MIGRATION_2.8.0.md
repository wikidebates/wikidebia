# Migration vers le kit 2.8.0

Le kit 2.8.0 ajoute la revue formelle du contenu français après l’application des métadonnées 2.7.0.

La nouvelle commande `corpus-workspace-content-review` prépare, finalise et applique les décisions relatives au sujet de la page Débat, à son introduction, aux articles Wikipédia, aux neuf paramètres documentaires, aux résumés d’arguments et à leurs références.

La phase conserve `working-copy/` et `reviewed-copy/` sans modification. Une application réussie crée `content-reviewed-copy/` et un verrou `data/fr_content_lock.json`. Aucune page finale, traduction anglaise ou écriture distante n’est effectuée.
