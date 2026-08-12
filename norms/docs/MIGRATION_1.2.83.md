# Migration 1.2.83 — préservation des textes historiques

Cette révision corrige une régression de reprise : une revue française de contenu pouvait proposer, accepter puis publier une nouvelle introduction et de nouveaux résumés sur des pages déjà existantes.

Pour toute page `preexisting`, `fr_content_review` conserve désormais exactement l’introduction et les résumés importés. Une absence historique de résumé reste une absence. Les règles de style de création ne s’appliquent pas rétroactivement. Toute réécriture volontaire doit passer par une opération corrective distincte explicitement autorisée par le propriétaire.

Le verrou français enregistre des empreintes source et le validateur les compare au rendu.
