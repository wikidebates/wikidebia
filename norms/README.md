# Wikidéb’IA — Normes 1.2.83

La révision 1.2.83 corrige une régression critique de reprise : sur une page française préexistante, `fr_content_review` ne peut plus réécrire l’introduction historique ni les résumés historiques. Une absence historique de résumé reste une absence. Toute réécriture volontaire de ces champs exige une opération corrective distincte explicitement autorisée par le propriétaire.

Le verrou français porte les empreintes des textes historiques et le validateur bloque toute divergence au rendu. Le second checkpoint français conserve donc un delta nul sur introduction/résumés lors d’une reprise ordinaire, tout en restant capable de publier classifications, documentation et autres champs effectivement ouverts.

La révision conserve les deux checkpoints français de 1.2.81 et toutes les protections de reprise déjà actives.
