# Audit de régression kit 2.16.1

Le correctif conserve l’orchestration 2.16.0, toutes les commandes détaillées et les protections de publication. Il corrige le premier passage du workflow : les anomalies éditoriales de titres importés sont différées jusqu’à leur revue ; une vraie erreur structurelle produit un diagnostic exploitable au lieu d’un message opaque. La reprise se fait par simple relance de `workflow`. Suite complète : 391/391 tests réussis avant scellement ; une nouvelle passe est exécutée sur l’archive fraîche exacte.
