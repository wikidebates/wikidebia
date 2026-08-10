# Migration 0.4.64

Correctif d’intégration avec le kit 2.15.38 / norme 1.2.61.

- le schéma `debate_package` accepte les versions de revue sémantique 1.2 et de moteur de marqueurs 1.1 réellement émises par le kit ;
- le schéma `argument_name_discovery_review` accepte les champs de portée vides lorsque `outcome=none` et les exige strictement pour `known_name` ;
- la compatibilité 1.2.59 n’est plus omise des listes déclarées.
- la validation pré-rendu de `argument_name_discovery_review.json` reconnaît désormais les pages nouvelles déclarées dans les verrous de contenu lorsque `manifest.pages` n'est pas encore peuplé ; les entrées historiques restent lisibles sans être confondues avec les pages nouvelles soumises à la recherche obligatoire.
