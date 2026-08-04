# Migration vers le kit 2.13.0

Le kit 2.13.0 ajoute `corpus-workspace-plan-review`. Les comparaisons produites par une version antérieure doivent être relancées avec 2.13.0 avant approbation, car le plan signé engage la version exacte du kit et du validateur.

La revue reste locale : elle ne vérifie pas les droits d'écriture, ne relit pas le wiki et n'exécute aucune opération. Un plan approuvé reçoit un handoff signé distinct; `remote_write_authorized` demeure faux jusqu'à la phase d'exécution explicite.
