# Audit kit 2.16.21 — rollback transactionnel du checkpoint français

## Défaut reproduit

Dans 2.16.20, `review-import` sauvegardait le workspace et plusieurs artefacts mécaniques, mais pas `.state/fr-publication/<debate>/<work>/<stage>`. Un checkpoint `content` créé avant `RemoteUpdatePlanner.build_plan()` survivait donc à un échec local du validateur et bloquait la revue corrigée par divergence de `source_tree_sha256`.

## Correctif

La transaction capture désormais le stage français susceptible d’être touché par la revue courante. S’il existait avant la tentative, une copie transactionnelle exacte est conservée hors du stage ; s’il n’existait pas, son absence est enregistrée. Lors d’un échec **avant toute exécution distante**, le stage est restauré ou supprimé avec le reste de la transaction. Le work et le checkpoint `graph` déjà publiés ne sont jamais supprimés par un rollback du stage `content`.

La frontière distante reste prioritaire : lorsque `FrenchCheckpointError.remote_execution_started` est vrai, ou lorsqu’un reçu de publication vient d’être acquis, aucun rollback du stage français n’est exécuté. Les artefacts sont conservés pour reprise idempotente.

## Compatibilité 2.16.20

`build_checkpoint()` peut rencontrer un stage orphelin créé avant l’installation de 2.16.21. Il ne le reconstruit automatiquement que lorsque l’absence d’exécution distante est démontrée par le trajet local : `publish_checkpoint` écrit toujours `update-plan.json` avant de créer `PlanExecutor`; l’absence de plan prouve donc que l’exécuteur n’a pas pu commencer. Un plan explicitement `blocked`/`manual_review` est également non exécutable par contrat. Tout plan exécutable ou `publication-receipt.json` rend le nettoyage automatique interdit.

## Régressions

- checkpoint content provisoire puis échec local : stage supprimé ;
- deuxième échec local successif : aucun faux verrou ;
- checkpoint graph publié : identité byte-for-byte conservée ;
- erreur après début d’exécution distante : stage et plan conservés ;
- checkpoint 2.16.20 sans plan exécutable : reconstruction sûre sur une nouvelle source ;
- plan exécutable ou reçu de publication : aucune reconstruction automatique ;
- intégration vote électronique : v6 rejetée avant écriture, v7 corrigée, SHA source différent, checkpoint 2 reconstruit et handoff `en_translation_review` produit.

La norme 1.2.86 et le validateur 0.4.91 ne changent pas : le contrat transactionnel avant/après frontière distante était déjà normatif et ce défaut était une régression d’implémentation du kit.
