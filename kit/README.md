# Wikidéb’IA — Kit 2.2.13

Kit générique de publication et de reprise, aligné sur la norme 1.2.26 et le validateur 0.4.28. Les plans `manual_review` sont bloquants, les simulations ne modifient jamais le corpus actif et toute archive de reprise doit être sélectionnée explicitement avec `--archive`.

Un plan entièrement `skip` est relu à distance puis consigné par une attestation signée `no_changes`, sans écriture MediaWiki. Les zones de staging sont nettoyées sur toutes les sorties. Une reprise `--no-delete` conserve les pages différées sous le statut `pending_delete`, afin qu’une reprise ultérieure `--only-delete` puisse les traiter en sécurité.

La syntaxe des modèles `{{Lien Wikipédia}}` et `{{Wikipedia link}}` reste contrôlée par le validateur avant toute publication ou reprise ; le kit n’effectue aucune requête Wikipédia.
