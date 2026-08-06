# Migration vers le kit 2.15.16

Le kit 2.15.16 est aligné sur la norme 1.2.40 et exige le validateur 0.4.43. Lorsqu’un argument ne possédait aucun résumé dans sa source attestée, le workflow peut consigner `summary_decision=leave_absent` : aucun paramètre `résumé` n’est rendu et aucune prose de remplissage n’est générée. Un résumé existant ne peut pas être supprimé par cette décision.
