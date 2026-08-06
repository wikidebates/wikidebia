# Wikidéb’IA Validator 0.4.43

Validateur local Python 3 aligné sur la norme 1.2.40 et rétrocompatible avec les révisions antérieures.

La version 0.4.43 ajoute `WDV-EDT-028` et contrôle l’état réel de rédaction des résumés. Lorsqu’un registre déclare `absent_at_import` ou `new_page_unwritten`, le paramètre `résumé` / `summary` doit être absent. Une paraphrase mécanique ne peut plus être utilisée pour satisfaire artificiellement la structure. Les résumés historiques et les paramètres `initialisation` restent protégés exactement par `WDV-EDT-027`.

La source normative active unique embarquée est `normative_reference/01_normes/WIKIDEBIA_NORME_CONSOLIDEE_1.2.40.md`.
