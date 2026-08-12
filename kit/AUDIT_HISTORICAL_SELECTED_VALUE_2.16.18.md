# Audit — valeur finale sélectionnée des textes historiques — Kit 2.16.18

Statut : **PASSED**.

## Régression reproduite

Le cas réel du vote électronique part d’une introduction historique à quatre sous-parties et d’une introduction finale explicitement autorisée à cinq sous-parties, la cinquième étant `Enjeux du débat`. La revue `subsections` contient exactement les cinq titres finaux.

## Correction

- `preserved` sélectionne strictement le texte historique ;
- `authorized_change` sélectionne strictement le texte final autorisé ;
- l’historique reste la provenance et conserve son SHA-256 ;
- la valeur finale autorisée possède son propre SHA-256 ;
- les contrôles structurels, `review.subsections`, le verrou, le changeset, le rendu, le checkpoint français n°2 et la traduction utilisent la valeur sélectionnée ;
- une portée structurée d’introduction décrit `added`, `modified`, `removed`, `reordered` ;
- une autorisation ciblée bloque toute modification parasite hors portée ;
- les contrôles de création ne s’appliquent qu’aux sous-parties ajoutées ou substantiellement réécrites.

## Tests

Le test d’intégration `test_historical_selected_value_21618.py` vérifie : 4→5 sous-parties autorisé, verrou historique/final, changeset d’introduction, rendu du checkpoint 2 à cinq sous-parties, blocage sans consentement et blocage d’une modification parasite. Les suites complètes du kit passent 456/456.
