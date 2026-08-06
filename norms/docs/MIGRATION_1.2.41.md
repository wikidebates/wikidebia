# Migration vers la norme 1.2.41

La révision 1.2.41 simplifie les mots-clés contextuels des pages nouvelles et restaure la sélection automatique de l’unique archive de `incoming/` pour `./wikidebia update`. Un sélecteur n’est demandé que lorsque plusieurs ZIP ou plusieurs corpus installés rendent le choix ambigu.

Lorsque `--scope` est omis, la commande choisit automatiquement les langues validées et non différées : `fr` pour un corpus français dont l’anglais est différé, `all` pour un corpus bilingue prêt.
