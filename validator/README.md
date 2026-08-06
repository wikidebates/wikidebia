# Wikidéb’IA Validator 0.4.42

Validateur local Python 3 aligné sur la norme 1.2.39 et rétrocompatible avec les révisions antérieures, notamment 1.2.36. La validation ordinaire reste strictement en lecture seule.

La version 0.4.42 corrige le verrou des contenus historiques. Lorsqu’un corpus déclare `verification_revision=0.4.42`, les résumés et les paramètres `initialisation` protégés sont confrontés directement à l’inventaire source attesté par SHA-256. Un résumé absent de la source ne peut plus être déclaré historique, un résumé présent ne peut plus être classé comme généré, et une valeur `initialisation` ne peut plus être omise du verrou.

Les contrôles éditoriaux 0.4.41 (`WDV-EDT-024` à `WDV-EDT-027`) et toutes les protections antérieures sont conservés.

La source normative active unique embarquée est `normative_reference/01_normes/WIKIDEBIA_NORME_CONSOLIDEE_1.2.39.md`.
