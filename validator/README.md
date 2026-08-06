# Wikidéb’IA Validator 0.4.44

Validateur local Python 3 aligné sur la norme 1.2.41 et rétrocompatible avec les révisions antérieures, notamment 1.2.36. La validation ordinaire reste strictement en lecture seule.

La version 0.4.44 distingue désormais trois provenances de résumé : `historical_existing`, `historical_absent` et `generated_after_import`. Lorsqu’un corpus active `historical_summary_absence_revision=1.2.40`, l’omission du paramètre est autorisée seulement si l’inventaire source attesté prouve son absence. Les pages nouvelles et les contenus réellement ajoutés après import conservent un résumé obligatoire. Les paramètres `initialisation` historiques restent également confrontés à l’inventaire source.

Les contrôles éditoriaux 0.4.41 (`WDV-EDT-024` à `WDV-EDT-027`) et toutes les protections antérieures sont conservés.

La source normative active unique embarquée est `normative_reference/01_normes/WIKIDEBIA_NORME_CONSOLIDEE_1.2.41.md`.
