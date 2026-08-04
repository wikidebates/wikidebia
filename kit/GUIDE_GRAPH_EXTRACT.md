# Guide d'extraction récursive des graphes

## Objet

`./wikidebia graph-extract` lit un débat déjà présent sur un wiki MediaWiki et produit une photographie locale de son graphe argumentatif. La commande ne crée, ne modifie, ne déplace et ne supprime aucune page.

Elle suit uniquement :

1. les `arguments-pour` et `arguments-contre` de la page `Débat` ;
2. les `justifications` et `objections` de chaque page `Argument` ;
3. les redirections nécessaires pour retrouver les titres canoniques.

Une page portant un paramètre `débat détaillé` reste dans le graphe, mais constitue par défaut une frontière. Le débat sous-jacent n'est jamais ouvert automatiquement.

## Commande minimale

```bash
./wikidebia graph-extract "Dieu existe-t-il ?"
```

Le dossier par défaut est :

```text
.state/graph-extract/dieu_existe_t_il/
```

## Reprise après interruption

Chaque page lue est enregistrée immédiatement dans `.cache_pages/`. Une nouvelle exécution avec le même titre et le même dossier réutilise ce cache. Le parcours logique est recalculé, mais les pages déjà acquises ne sont pas relues à distance.

```bash
./wikidebia graph-extract "Dieu existe-t-il ?"
```

Pour invalider le cache :

```bash
./wikidebia graph-extract "Dieu existe-t-il ?" --force-refresh
```

## Sorties

La commande produit :

- un registre JSON du graphe ;
- un CSV des pages uniques ;
- un CSV des relations ;
- un rapport Markdown ;
- un audit Markdown ;
- un manifeste SHA-256 ;
- un ZIP audité ;
- un snapshot du wikicode de la page Débat et de toutes les pages Argument ;
- un `snapshot_manifest.json` associant les fichiers locaux aux titres, URL, révisions, horodatages et chaînes de redirection.

Le snapshot est l'entrée de `./wikidebia corpus-init-from-snapshot`. L'extracteur lui-même reste strictement en lecture seule et ne crée aucun corpus.

## Options principales

```text
--output-dir CHEMIN       choisir un dossier de sortie situé dans l'installation
--cache-dir CHEMIN        séparer le cache des résultats
--slug TEXTE              imposer le préfixe stable des fichiers
--date AAAA-MM-JJ         fixer la date portée par les noms et manifestes
--max-pages N             arrêter avant une expansion accidentelle
--progress-every N        afficher un état toutes les N pages
--retries N               régler les nouvelles tentatives réseau
--retry-delay SECONDES    régler le délai initial de reprise
--allow-missing           exporter malgré des pages liées inexistantes
--login                   utiliser le compte Pywikibot configuré
--force-refresh           ignorer les pages déjà mises en cache
```

L'option suivante suit les relations locales d'une page frontière, sans ouvrir le débat sous-jacent :

```text
--follow-local-relations-at-detailed-debate
```

## Authentification

La lecture d'un wiki public peut fonctionner sans fichier d'identification. `--login` exige en revanche `private/pywikibot/user-config.py` et la configuration privée habituelle.

## Statut des données produites

Les fichiers sont des données d'extraction et de provenance, non un corpus `release_ready`. Ils ne remplacent ni la revue sémantique du graphe, ni la génération bilingue, ni le validateur, ni le kit de publication.
