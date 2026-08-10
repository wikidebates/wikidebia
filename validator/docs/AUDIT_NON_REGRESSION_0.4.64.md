# Audit de non-régression 0.4.64

Base : validateur 0.4.58 / norme 1.2.55 du début de la conversation.

- 313 fonctions de test historiques sur 313 toujours présentes ;
- aucune exigence initiale supprimée ou modifiée dans son énoncé/disposition/enforcement ;
- schéma de revue sémantique 1.2 et moteur 1.1 réellement acceptés ;
- `name=` 1.2 accepte les champs de portée vides uniquement pour `outcome=none` ;
- validation pré-rendu d’un translated-copy produit par le kit courant : 0 erreur, 0 avertissement ;
- test croisé exécutable isolément.
