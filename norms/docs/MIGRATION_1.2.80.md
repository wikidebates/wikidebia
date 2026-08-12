# Migration 1.2.80

- `fr_content_review` devient un point de publication française automatique avant `en_translation_review`.
- le checkpoint est rendu sans lien interlangue tant que l’anglais n’est pas verrouillé et utilise le moteur de reprise signé avec résumés individualisés ;
- les ZIP de revue retournés se déposent dans `incoming/` puis se réimportent avec `./wikidebia review-import` ou, en cas de pluralité, `./wikidebia review-import <debate_id>` ;
- `sources_working.json` refuse immédiatement les valeurs `document_kind` hors enum ;
- un workflow 2.16.12 déjà arrêté sur une revue anglaise publie le checkpoint français manquant lors de sa reprise avant de continuer.
