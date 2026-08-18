# Audit — garde des titres anglais — kit 2.16.26

Le Work `revenu_de_base` avait terminé deux passes propres de convergence avant que le préflight de `translated-copy` ne révèle des apostrophes typographiques dans des titres anglais. La cause était double : `_validate_title()` ne rejetait pas l’apostrophe courbe et le verrou anglais strict n’existait qu’au moment de l’application.

Le correctif ajoute un contrôle intrinsèque à la finalisation de la traduction, donc avant `semantic_convergence_1`. Pour les revues déjà finalisées/convergées sous une ancienne version, une garde de compatibilité inspecte les valeurs scellées avant application. En présence d’un défaut, elle ne modifie aucun titre : elle rouvre `en_translation_correction`, enregistre la liste exhaustive des champs, supprime le reçu de convergence et force deux nouvelles passes sur l’empreinte recalculée après correction.

Ce comportement respecte l’interdiction de normalisation silencieuse et le contrat selon lequel toute mutation postérieure à la convergence invalide la chaîne précédente.
