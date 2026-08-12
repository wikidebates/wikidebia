# Audit kit 2.16.20 — paramètres facultatifs vides des citations historiques

## Anomalie reproduite

Le rendu du checkpoint français refusait une `Citation` importée dès qu'un sous-paramètre inventorié possédait une valeur vide. Ce comportement contredisait le profil actif, qui exige l'omission des sous-paramètres facultatifs vides dans le wikicode canonique.

## Correctif

`_citation_template()` bloque uniquement un **nom** de paramètre vide. Les valeurs vides restent dans l'inventaire/provenance puis sont transmises à `_template()`, qui les omet sans inventer de valeur.

Le trajet anglais conserve les lignes vides dans `source_parameters` puis dans `parameters` mappés ; le rendu `{{Quote}}` omet les équivalents vides.

## Régressions

- Citation historique avec valeurs facultatives vides : acceptée ;
- omission canonique des seules valeurs vides ;
- nom de paramètre vide : bloqué ;
- `citation` obligatoire vide : bloquée en amont ;
- formes A0055-C001 et A0056-C001 : acceptées ;
- Citation→Quote : paramètres vides conservés en provenance et omis du wikicode ;
- aucune valeur documentaire inventée ;
- intégration vote électronique : autorisation historique → checkpoint FR n°2 → préparation de la revue anglaise.
