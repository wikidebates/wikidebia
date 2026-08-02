# Guide de publication et de reprise Wikidéb’IA 2.2.13

## Nouveau débat

Déposer le ZIP du corpus dans `incoming/`, puis lancer `./wikidebia publish [SÉLECTEUR] --scope all`.

## Débat déjà publié — corpus installé

Lancer `./wikidebia update <debate_id> --dry-run`, examiner le plan, puis relancer sans `--dry-run`. Sans `--archive`, la commande ne consulte que `corpus/<debate_id>/` et ne sélectionne jamais implicitement un ZIP de `incoming/`.

## Débat déjà publié — nouvelle archive

Utiliser explicitement :

```bash
./wikidebia update --archive <SÉLECTEUR> --dry-run
./wikidebia update --archive <SÉLECTEUR>
```

L’archive est extraite dans une zone temporaire de staging. La simulation ne modifie pas `corpus/`, puis le staging est supprimé. Le corpus actif n’est remplacé qu’après une exécution réussie ou une attestation `no_changes` réussie.

Un plan contenant `blocked` ou `manual_review` est bloquant et ne produit ni écriture MediaWiki, ni reçu de succès, ni nouvel état publié. Un plan entièrement `skip` déclenche une relecture distante complète, produit une attestation signée `no_changes` et actualise l’état publié sans éditer le wiki.

## Portées partielles

Lorsque la portée demandée ne contient aucune opération mutante, la commande renvoie `no_changes_in_scope` sans exécuter ni promouvoir un staging. Une reprise avec `--no-delete` conserve les pages à supprimer comme `pending_delete`; elles peuvent ensuite être traitées avec `--only-delete`.

## Mise à niveau des composants

Un seul fichier suffit. Vider `updates/`, y copier soit le bundle `WIKIDEBIA_SOURCES_COMPLETES_*.zip`, soit la livraison complète `WIKIDEBIA_LIVRAISON_*.zip`, puis lancer `./wikidebia upgrade`.
