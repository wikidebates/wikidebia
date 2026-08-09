# Guide de scellement local du corpus — Kit 2.15.33

## Commande

```bash
./wikidebia corpus-workspace-release <debate_id> \
  --work-id <work_id> \
  --confirm-render-sha256 <empreinte_de_rendered-copy>
```

## Résultat

La commande crée `release-copy/` dans le workspace et un ZIP autonome sous `.state/corpus-releases/<debate_id>/<work_id>/`. Le manifeste passe à `release_ready`, mais `remote_write_authorized` reste `false`.

Le fichier `release/remote_comparison_input.json` prépare la liste locale des pages, titres et empreintes qui sera utilisée ultérieurement par la comparaison avec l’état publié. Il n’effectue aucune lecture distante et ne constitue pas un plan de reprise.

Le manifeste de libération exclut seulement son propre fichier. Le reçu du ZIP et la validation postérieure au manifeste restent externes, à côté de l’archive, afin d’éviter toute dépendance circulaire d’empreintes.
