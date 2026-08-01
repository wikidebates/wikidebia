# Architecture du validateur 0.4.22

Le validateur sépare schémas, cohérence, graphe, lots, sources, fichiers, wikicode, bilinguisme, éditorial et workflow. La commande `validate` demeure strictement en lecture seule ; `recalc --write` reste la seule commande d’écriture locale.

Sous la norme 1.2.20, le module éditorial charge le registre déclaré par `editorial_controls.graph_placement_review_path`. Il contrôle la couverture exacte des occurrences actives, la concordance des identifiants et profondeurs, la cible sémantique, la fonction `main_argument` / `justification` / `objection`, ainsi que les attestations propres aux niveaux 1 et aux niveaux subordonnés.

La qualité réelle du classement demeure une décision humaine, mais elle n’est plus implicite : les critères et décisions sont enregistrés et les incohérences déclaratives sont bloquantes par `WDV-EDT-022`. Tous les contrôles 0.4.21 sont conservés.
