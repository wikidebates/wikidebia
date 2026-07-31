# Migration vers la norme 1.2.9

1. Convertir toute date documentaire `AAAA-MM-JJ` en date naturelle localisée ; ne pas modifier `date-création` ou `creation-date`.
2. Dans les introductions, remplacer les modèles documentaires spécialisés par `{{Référence}}` ou `{{Reference}}`.
3. Remplir chacun des neuf paramètres documentaires de Débat/Debate avec au moins deux références distinctes.
4. Ajouter à chaque entrée du registre de revue `common_acronym` (chaîne ou `null`) et `common_acronym_used_or_not_applicable: true`.
5. Pour une publication française seule, conserver les titres anglais verrouillés dans le registre maître ; les pages anglaises n’ont pas à figurer dans le manifeste de pages.
6. Déclarer les versions 1.2.9 / 0.4.9 / 2.1.9 et recalculer les empreintes.
