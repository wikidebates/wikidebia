# Migration 1.2.58 / validateur 0.4.61

La révision 1.2.58 ajoute trois artefacts/contrats sans transformer le numéro de norme en feature flag éditorial :

1. `data/documentary_resources.json` est un registre global dérivé de `data/sources.json`, avec identité DOI, URL canonique ou empreinte bibliographique ;
2. les rapports exposent `validation_layers.structural`, `documentary`, `semantic_review` et `fresh_archive` ; `fresh_archive` reste `not_run` dans une validation de dossier et n’est scellé qu’après création puis réextraction de l’archive exacte ;
3. `semantic_marker_engine_version=1.0` active un inventaire bilingue différentiel plus systématique sur titres canoniques, titres affichés et résumés.

Les anciens artefacts restent lisibles. Les nouvelles productions doivent générer le registre documentaire et conserver les attestations sémantiques ; les pertes de marqueurs sont des signaux de revue, jamais des réécritures automatiques.
