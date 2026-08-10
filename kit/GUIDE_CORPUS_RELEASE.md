# Guide de scellement local du corpus — Kit 2.15.48

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

## Scellement 2.15.34 — validation de l'artefact exact

Une validation du dossier de travail ne suffit pas. Après création du ZIP déterministe, le kit calcule son SHA-256, extrait **ce ZIP exact** dans un nouveau répertoire temporaire sûr, vérifie ses chemins et son CRC, puis relance le validateur complet sur cette extraction fraîche. Le reçu enregistre le SHA-256 audité et le résultat de cette validation. Un audit ultérieur doit toujours partir de l'archive et de son empreinte, jamais d'un workspace intermédiaire mutable.

## 2.15.35 — ressources globales et statuts de release

Avant le premier contrôle du paquet final, le kit régénère `data/documentary_resources.json` depuis les octets exacts de `data/sources.json`. Une collision incompatible d’identité DOI/URL bloque la release. Le reçu externe distingue `structural`, `documentary`, `semantic_review` et `fresh_archive`; la dernière couche n’est passée qu’après création et réextraction du ZIP exact.



## Correctif 2.15.38 — provenance, Quote et inventaire final

La recherche d’`established-name=` enregistre sa provenance réelle. Une nouvelle page anglaise utilise `actual_log` ou `fresh_recheck`; `historical_reconstruction` ne sert qu'à décrire honnêtement une décision ancienne. Chaque `Quote` est relue de début à fin contre la `Citation` source ; sous un ratio lexical de 0,60, une seconde revue explicite est requise. La release calcule `release/content_inventory.json`, en lie l'empreinte au reçu, puis le recalcule sur l'extraction fraîche.
