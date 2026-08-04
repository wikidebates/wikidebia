# Migration vers le kit 2.5.0

Le kit 2.5.0 ajoute la revue formelle des builds `graph_draft` et leur promotion atomique contrôlée vers `corpus/<debate_id>/`.

Deux commandes sont ajoutées :

```bash
./wikidebia corpus-review-graph <debate_id> --prepare
./wikidebia corpus-review-graph <debate_id> --finalize
```

La première prépare une revue globale et un registre occurrence par occurrence. La seconde refuse toute modification du build intervenue après la préparation, contrôle les attestations, exécute le validateur local et fait passer le corpus à `graph_validated` seulement. Elle ne verrouille pas le graphe et ne génère aucune page.

Après approbation, la promotion exige l’empreinte exacte de la revue :

```bash
./wikidebia corpus-promote <debate_id> \
  --confirm-review-sha256 <empreinte>
```

La promotion refuse une cible `corpus/<debate_id>/` déjà existante, les liens symboliques, les builds altérés, les pages finales et les changements de système de fichiers. Elle utilise un renommage atomique, revérifie le corpus après bascule et écrit un reçu externe sous `.state/corpus-promotions/`.

La norme reste 1.2.26 et le validateur reste 0.4.28. Aucune écriture MediaWiki n’est ajoutée.
