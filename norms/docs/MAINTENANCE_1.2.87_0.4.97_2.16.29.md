# Maintenance d’implémentation 1.2.87 / 0.4.97 / 2.16.29

Aucune règle normative 1.2.87 n’est modifiée. Cette maintenance réconcilie les deux variantes parallèles 0.4.96 / 2.16.28 :

- la branche documentaire conserve `en_documentation_correction`, la réutilisation de l’identité documentaire canonique FR→EN et l’alignement de `WDV-SRC-005` sur la portée fondatrice/synthétique plutôt que sur une liste fermée de `document_kind` ;
- la branche rendu conserve `historical_text_render_validation_mode=differential_preservation_v1`, afin de préserver les textes et absences historiques attestés sans réécriture rétroactive, tout en maintenant les contrôles stricts des contenus nouveaux.

Les deux jeux de régressions et d’audits sont conservés dans les composants alignés.
