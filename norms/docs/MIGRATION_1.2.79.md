# Migration 1.2.79 — résumés individualisés des reprises distantes

Cette révision remplace le résumé générique `Corrections` pour les **nouveaux** plans de reprise d’un corpus validé.

- `update --archive` produit un contrat `page_specific_v1` ;
- chaque création, mise à jour, renommage, redirection ou suppression reçoit un résumé MediaWiki propre à la mutation ;
- les mises à jour de contenu décrivent les familles de paramètres réellement modifiées ;
- la politique et le résumé sont signés dans le plan, recalculés avant écriture et relus après écriture ;
- les anciens plans déjà signés sans ce contrat restent lisibles ;
- `review-import` reste local tant qu’aucune page MediaWiki finale n’est disponible ; les actions structurelles explicitement exécutées conservent leur voie distante dédiée.

Aucune migration de corpus n’est requise.
