# Migration vers le kit 2.6.0

Le kit 2.6.0 ajoute le workspace éditorial des corpus déjà promus.

Après la séquence 2.5.0 :

```bash
./wikidebia corpus-review-graph <debate_id> --prepare
./wikidebia corpus-review-graph <debate_id> --finalize
./wikidebia corpus-promote <debate_id> --confirm-review-sha256 <sha256>
```

un Work éditorial peut être ouvert avec :

```bash
./wikidebia corpus-workspace-init <debate_id>
```

La commande conserve `corpus/<debate_id>/` intact et crée une copie auditable sous `.state/editorial-workspaces/`. Les fichiers produits préparent la revue des titres, rubriques et mots-clés ainsi que la future traduction anglaise. Ils ne constituent ni des pages finales ni une autorisation de publication.

Aucune migration de norme ou de validateur n’est nécessaire : la norme reste 1.2.26 et le validateur 0.4.28.
