# Migration vers le kit 2.16.39

Aucune migration de corpus n’est requise.

Un workflow produit par 2.16.37 ou 2.16.38 et déjà arrêté à :

```text
phase=release_ready
status=release_ready
```

est repris directement en `final_publication` lors de la prochaine commande `./wikidebia workflow ...`. Le kit réutilise le `release-copy`, le reçu de release, le dernier checkpoint français et les deux convergences déjà scellées. Il ne refait aucune étape éditoriale.

En cas de conflit distant avant écriture, le Work passe à `blocked_final_publication` et les plans/diagnostics restent sous `.state/final-publication/<débat>/<work>/`. Après résolution, la même commande `workflow` reprend cette phase.
