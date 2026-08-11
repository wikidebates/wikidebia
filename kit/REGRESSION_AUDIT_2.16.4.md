# Audit de régression kit 2.16.4

- primitives détaillées de revue, correction, promotion et publication conservées ;
- `review-import` sans `--execute-graph-actions` conserve le comportement sûr non destructif ;
- actions structurées `remove`, `merge_redirect`, `move`, `relation_change` couvertes ;
- compatibilité étroite avec les décisions explicites des ZIP 2.16.2/2.16.3 couverte ;
- suppression d’un nœud multi-occurrence ou porteur d’enfants bloquée ;
- doublon : retrait du lien parent puis redirection `#REDIRECTION [[destination]]` ;
- retrait non doublon : retrait du lien parent puis suppression distante ;
- résumés de modification individualisés ; destination `[[...]]` obligatoire pour le résumé parent d’un doublon ;
- validation prospective locale avant toute écriture distante ;
- préflight distant global, garde de révision avant chaque mutation, relecture contenu/résumé/balise ;
- ordre d’écriture : pages mères, redirections, suppressions ;
- nouvelle revue complète obligatoire après application ; aucune promotion implicite.
