# Migration vers la norme 1.2.22

La norme 1.2.22 rend opposable la fonction de concision des titres affichés.

1. Revoir chaque titre affiché dans les deux langues sans modifier le titre canonique.
2. Conserver une proposition complète et intelligible, mais raccourcir le cadrage redondant.
3. Ajouter `displayed_title_concision_reviewed_fr=true` et `displayed_title_concision_reviewed_en=true` dans chaque entrée du registre individuel.
4. Pour toute identité exacte conservée, renseigner une justification spécifique dans `displayed_title_identity_justification_fr` ou `displayed_title_identity_justification_en`.
5. Vérifier que les identités exactes ne dépassent pas 10 % des arguments actifs par langue.
6. Régénérer projections, agrégats, inventaires et empreintes, puis valider avec le validateur 0.4.24.

Les corpus 1.2.21 restent compatibles sans activation rétroactive de ce seuil.
