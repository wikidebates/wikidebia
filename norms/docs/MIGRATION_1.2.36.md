# Migration Wikidéb’IA 1.2.36

La révision 1.2.36 corrige les reprises de corpus contenant des pages déjà présentes sur le wiki.

- Les dates de création sont contrôlées page par page par défaut. Une page existante conserve sa date historique et n’adopte jamais automatiquement la date du corpus ou la date du jour.
- Lorsqu’une page distante est exactement celle attestée par l’état publié, le kit préserve automatiquement ses paramètres historiques protégés dans un fichier effectif dérivé : avertissements, avancement, débats connexes historiques admis et date de création.
- Une page historique sans avertissement IA n’est pas réétiquetée comme générée par IA.
- Une suppression sans marqueur IA reste interdite, sauf lorsqu’une migration explicite documente le retrait et que l’état distant correspond exactement à l’état attesté.
- Les modifications humaines ou les provenances indéterminées restent en `manual_review`.

Aucune modification du corpus source n’est effectuée par cette réconciliation ; seul le fichier effectif signé dans le plan est publié.
