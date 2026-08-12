# Migration 2.16.12

Aucune migration de corpus n’est requise.

Les nouveaux plans de reprise distante produits par le kit portent `edit_summary_contract=page_specific_v1`. Chaque mutation possède un `edit_summary_policy` et un `edit_summary` signés. L’exécuteur recalcule le résumé à partir du contenu et de l’état distant avant écriture.

Les anciens plans déjà signés et dépourvus de ce contrat restent exécutables selon leur comportement historique, sous réserve de leurs autres garde-fous.
