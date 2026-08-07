# Audit de complétude — norme 1.2.54

## Objet

La révision 1.2.54 supprime l’usage des numéros de version comme interrupteurs des normes éditoriales et conserve les versions uniquement pour la compatibilité technique, les migrations, la provenance et l’identification des livraisons.

## Contrôles de refonte

- suppression des listes de versions servant à activer les règles courantes dans les modules éditoriaux, de workflow, de sources, de bilinguisme, de graphe et de cohérence ;
- suppression des conditions de schéma qui activaient une exigence selon `consolidated_norm` ou un champ de révision de politique ;
- maintien des versions de format propres aux artefacts et des contrôles de non-régression des sources normatives ;
- préservation de la protection générique des paramètres historiques `WDV-EDT-030`, désormais déclenchée par l’état de préservation et non par une version ;
- ajout de tests d’invariance : une variation isolée de `consolidated_norm` ou d’un champ de révision ne change pas le verdict éditorial ;
- maintien intégral des règles de traduction anglaise introduites en 1.2.53.

Les suites complètes du validateur et du kit doivent être rejouées sur l’archive finale reconstruite, avec auto-audit et vérification des manifestes SHA-256.
