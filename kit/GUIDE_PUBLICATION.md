# Guide de publication et de reprise Wikidéb’IA 2.15.2

## Extraire le graphe d'un débat existant

```bash
./wikidebia graph-extract "Dieu existe-t-il ?"
```

L'extraction est en lecture seule et écrit par défaut dans `.state/graph-extract/dieu_existe_t_il/`. Relancer la même commande réutilise le cache par page. `--force-refresh` force une nouvelle lecture distante. Le ZIP audité contient le graphe, les inventaires CSV, les rapports et le snapshot du wikicode.


## Comparer un corpus final sans l’exécuter

```bash
./wikidebia corpus-workspace-remote-compare <debate_id> \
  --work-id <work_id> \
  --confirm-release-sha256 <empreinte_de_release-copy> \
  --scope all
```

Cette commande est distincte de `update --dry-run` : elle part du workspace et de sa `release-copy/`, conserve un dossier de comparaison immuable et n’offre aucune voie d’exécution. Le plan produit doit être repris explicitement par une phase ultérieure.


## Revoir puis exécuter un plan du workspace

Après la comparaison et la revue formelle, préparer le préflight :

```bash
./wikidebia corpus-workspace-plan-execute <debate_id> \
  --work-id <work_id> \
  --comparison-id <comparison_id> \
  --prepare \
  --confirm-acceptance-sha256 <empreinte>
```

Puis exécuter uniquement après examen de ce préflight :

```bash
./wikidebia corpus-workspace-plan-execute <debate_id> \
  --work-id <work_id> \
  --comparison-id <comparison_id> \
  --execute \
  --confirm-preflight-sha256 <empreinte>
```

La deuxième commande effectue réellement les écritures distantes. Toute divergence observée juste avant l’exécution bloque le plan.

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
