# Migration vers la norme 1.2.20

1. Déverrouiller explicitement le graphe dans le cadre d’une migration structurelle documentée.
2. Examiner chaque occurrence de profondeur 1 avec les tests de réponse directe, autonomie, tête de famille et absence de parent général préférable.
3. Déplacer sous leur cible les objections visant une preuve déterminée, les exemples historiques ou scientifiques, les interprétations particulières, doctrines instanciées, mécanismes techniques et applications sectorielles qui ne constituent pas une famille autonome.
4. Vérifier ensuite chaque occurrence subordonnée : le parent doit être sa meilleure cible immédiate et la relation doit être explicitement une justification ou une objection.
5. Créer `reports/graph_placement_review.json`, le déclarer dans `editorial_controls.graph_placement_review_path` et couvrir exactement toutes les occurrences actives.
6. Régénérer relations, occurrences, profondeurs, branches, lots, projections Markdown/JSON, pages Débat/Debate, pages Argument concernées, agrégats, manifestes et empreinte structurelle.
7. Déclarer 1.2.20, utiliser le validateur 0.4.22 et le kit 2.2.6, puis exécuter toutes les portées.

Le déplacement d’un argument de niveau 1 vers un niveau supérieur n’est pas une simple correction éditoriale : il modifie le graphe verrouillé et exige une migration explicite. Les corpus historiques restent publiables sous leur norme d’origine.
