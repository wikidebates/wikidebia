# Wikidéb’IA

Installation portable des normes, du validateur et du kit de publication.

## Publication en une commande

Déposer le ZIP du débat dans `incoming/`. Aucun suffixe particulier n’est exigé. Si le dossier contient un seul ZIP, lancer :

```bash
./wikidebia publish
```

Si plusieurs ZIP sont présents, indiquer l’identifiant correspondant au nom du fichier sans `.zip` :

```bash
./wikidebia publish gpa_autorisation
```

Le fichier attendu est alors `incoming/gpa_autorisation.zip`. Son nom sert uniquement à sélectionner l’archive ; le `debate_id` du manifeste interne détermine l’identité du corpus et peut être différent.

Portées disponibles :

```bash
./wikidebia publish --scope fr-debate
./wikidebia publish --scope en-debate
./wikidebia publish --scope fr
./wikidebia publish --scope en
./wikidebia publish --scope all
```

La page Débat/Debate est toujours traitée avant les pages Argument de la même langue.

## Mise à jour en une commande

Déposer l’archive complète ou les trois ZIP de composants dans `updates/`, puis lancer :

```bash
./wikidebia update
```

Les versions précédentes et les ZIP entrants sont déplacés dans `archives/updates/`. Le dossier `updates/` est vidé après succès. Lorsque `origin` est configuré, le commit et le `git push` sont automatiques.

## Environnement Python automatique

`.venv/` n’est jamais enregistré dans Git. Lorsqu’il manque après un clone ou devient inutilisable après un déplacement, toute commande `./wikidebia …` le recrée et installe les dépendances de `requirements-runtime.txt`, dont Pywikibot. La commande suivante suffit pour préparer et contrôler un clone propre :

```bash
./wikidebia doctor
```

## Données privées

Les identifiants Pywikibot résident dans `private/pywikibot/`. Ce dossier, ainsi que `corpus/`, `archives/`, `updates/`, `incoming/`, `logs/` et `plans/`, est exclu de Git.

Lors de la mise à jour, les ZIP encore présents dans l’ancien dossier `incoming/debates/` sont migrés automatiquement vers `incoming/`; une collision différente est bloquée sans écrasement.

## Corpus produits avec une version antérieure

La mise à jour de Wikidéb’IA ne modifie pas les versions inscrites dans le manifeste d’un débat. Un corpus produit sous une norme antérieure compatible peut être publié normalement : le kit exécute le validateur installé, vérifie sa version réelle et exige un rapport positif. Il ne faut donc pas remplacer manuellement `normative_versions.validator` ou `consolidated_norm` par les versions locales.

## Synchronisation GitHub

Les pushes sont non interactifs : le lanceur ne demande jamais de mot de passe GitHub. Après authentification avec GitHub CLI, exécuter :

```bash
gh auth login -h github.com -p https
gh auth setup-git --hostname github.com
./wikidebia github-sync
```

Lors du passage précis de 2.1.16 à 2.1.17, utiliser d’abord `./wikidebia update --no-git`; `github-sync` créera ensuite le commit sécurisé et le poussera.

`./wikidebia doctor` vérifie les exclusions Git sensibles et bloque tout fichier local suivi ou non ignoré.
