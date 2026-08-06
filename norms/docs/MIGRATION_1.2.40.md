# Migration vers la norme 1.2.40

La migration ne réécrit aucun résumé historique. Elle classe chaque page Argument selon la provenance réelle du champ : `historical_existing`, `absent_at_import`, `new_page_unwritten` ou `authored_after_import`.

Pour `absent_at_import` et `new_page_unwritten`, le paramètre `résumé` / `summary` est supprimé. Il ne doit pas être conservé vide. Une rédaction ultérieure exige une revue individuelle et le passage explicite à `authored_after_import`.
