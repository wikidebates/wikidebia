# Migration 2.16.7

Correctif de reprise de provenance après plusieurs vagues de décisions structurelles du graphe.

- base : 1.2.77 / 0.4.80 / 2.16.6 ;
- norme et validateur inchangés ;
- les nouvelles actions restent protégées par la mise à jour immédiate de provenance introduite en 2.16.6 ;
- pour les états historiques 2.16.4/2.16.5 déjà affectés, la réparation ne dépend plus du seul `reviews/graph_action_decisions.json`, écrasé à chaque vague ;
- elle relit aussi les paires `plan.json` / `execution-receipt.json` sous `.state/graph-actions/<debate_id>/`, vérifie leurs empreintes internes et n’adopte que le contenu post-action exact avec la révision distante attestée ;
- aucune réécriture distante n’est effectuée ; une divergence non attestée reste bloquante.
