# Guide de publication et de reprise Wikidéb’IA 2.2.1

## Nouveau débat

1. Déposer l’archive dans `incoming/`.
2. Exécuter `./wikidebia publish [SÉLECTEUR] --scope all`.
3. Conserver les reçus et états écrits sous `.state/`.

## Débat déjà publié

1. Installer le nouveau corpus sous `corpus/<debate_id>` ou déposer son ZIP dans `incoming/`.
2. Exécuter `./wikidebia update <debate_id> --dry-run`.
3. Examiner `manual_review` et `blocked`; aucune opération distante n’est faite en mode sec.
4. Vérifier l’empreinte du plan.
5. Exécuter `./wikidebia update <debate_id>` et confirmer exactement cette empreinte.
6. Contrôler le reçu final et les nouveaux états publiés signés.

Pour publier d’abord les créations et mises à jour : `--no-delete`. Pour retirer ensuite seulement les pages attestées et sûres : `--only-delete`.

## Conflits

Une révision ou une empreinte distante différente de l’état attendu produit `manual_review` lors de la planification ou un conflit bloquant lors de l’exécution. Il faut alors intégrer, adopter ou fusionner explicitement la modification humaine, puis produire un nouveau plan.

## Mise à niveau des composants

La commande est `./wikidebia upgrade`, et non plus `update`.


## Correctifs 2.2.1

La publication ordinaire ne pose plus la question `Publier le débat … ? [o/N]`. Après validation, le gestionnaire transmet automatiquement le SHA-256 du plan au moteur. Avant cela, il bloque toute page Débat/Debate sans article Wikipédia, tout paramètre de débats connexes et toute valeur auteurs sérialisée comme tableau JSON.
