# Wikidéb’IA — Normes 1.2.80

La révision 1.2.80 fait de la validation complète du contenu français une frontière de publication : les corrections françaises scellées sont publiées avec des résumés MediaWiki individualisés avant la préparation de la traduction anglaise. Les ZIP de revue retournés sont désormais consommés depuis `incoming/` par `./wikidebia review-import` (sélection automatique s’il n’y en a qu’un, sinon par `debate_id`). `sources_working.json` valide aussi `document_kind` avant projection.

Elle conserve intégralement le contrat 1.2.79 de résumés individualisés et la politique différentielle 1.2.78 des métadonnées préexistantes.
