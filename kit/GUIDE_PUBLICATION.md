# Guide opérationnel Wikidéb’IA 2.1.17

## Première installation

La racine contient le lanceur `wikidebia`. Les secrets Pywikibot sont placés ici :

```text
private/pywikibot/user-config.py
private/pywikibot/user-password.cfg
```

La configuration locale facultative est copiée depuis `config/wikidebia.example.json` vers `config/wikidebia.local.json`. Cette copie n’est pas suivie par Git.

## Publication en une commande

1. Déposer le ZIP du débat dans `incoming/`. Son nom est libre et sert seulement à sélectionner le fichier ; aucun suffixe n’est exigé ni interprété.
2. Si `incoming/` contient un seul ZIP, lancer :

```bash
./wikidebia publish --scope all
```

Sans `--yes`, la commande affiche les comptes du plan et demande une confirmation. Avec `--yes`, elle peut être utilisée dans un terminal non interactif.

Les portées sont :

- `fr-debate` : page Débat française seulement ;
- `en-debate` : page Debate anglaise seulement ;
- `fr` : Débat puis tous les Arguments français ;
- `en` : Debate puis tous les Arguments anglais ;
- `all` : français, puis anglais, avec la page principale avant les arguments dans chaque langue.

Si plusieurs ZIP sont présents, l’identifiant doit être donné explicitement :

```bash
./wikidebia publish gpa_autorisation --scope fr
```

L’argument correspond exactement au nom du fichier sans `.zip`; l’extension ne doit pas être passée dans la commande. Le `debate_id` lu dans `manifest.json` peut être différent du nom du ZIP et détermine le dossier du corpus. Après succès, le ZIP est déplacé dans `archives/debates/`. Le corpus extrait reste dans `corpus/` pour les reprises et contrôles.

## Mise à jour en une commande

Déposer une archive complète `WIKIDEBIA_SOURCES_COMPLETES_*.zip`, ou les trois archives `wikidebia-normes.zip`, `wikidebia-validator.zip` et `wikidebia-kit.zip`, dans `updates/` :

```bash
./wikidebia update
```

La commande :

1. vérifie les ZIP et leurs manifestes internes ;
2. refuse une rétrogradation non explicitement autorisée ;
3. teste les composants extraits avant installation ;
4. archive les anciens composants et les ZIP entrants ;
5. installe les nouvelles sources ;
6. met à jour le lanceur, `.gitignore` et la documentation racine ;
7. vide `updates/` ;
8. crée un commit et pousse vers `origin` lorsqu’il est configuré.

Options de maintenance :

```bash
./wikidebia update --no-push
./wikidebia update --no-git
./wikidebia update --allow-downgrade
```

## Initialisation GitHub

Créer au préalable un dépôt vide, normalement nommé `wikidebia`, puis lancer :

```bash
./wikidebia github-init URL_GIT_DU_DEPOT
```

La commande initialise Git si nécessaire, ajoute `origin`, crée le commit initial et pousse la branche courante.

## Diagnostic

```bash
./wikidebia doctor
```

Le diagnostic vérifie les versions, l’emplacement des secrets, la présence du dépôt Git, le remote `origin`, le contenu de `updates/` et l’absence du chemin absolu de l’installation dans les sources persistantes.

## Moteur bas niveau

`kit/scripts/wikidebia_publish.py` reste disponible pour les opérations manuelles auditables. Son ordre de pages complètes est néanmoins forcé à `debate`, puis `argument`, quelle que soit la langue.

Lors de la mise à jour, les ZIP encore présents dans l’ancien dossier `incoming/debates/` sont migrés automatiquement vers `incoming/`; une collision différente est bloquée sans écrasement.

## Compatibilité des corpus historiques

Les champs `normative_versions` du manifeste décrivent les versions utilisées lors de la production du corpus et ne sont pas réécrits lors d’une mise à jour locale. Le kit publie un corpus historique lorsque le validateur installé déclare sa norme compatible et renvoie un rapport positif sans erreur ni avertissement. La version réelle du validateur exécuté doit toujours être exactement celle exigée par le kit courant.

## Après un clone Git propre

Aucune installation manuelle de Pywikibot n’est normalement nécessaire. Lancez :

```bash
./wikidebia doctor
```

Le lanceur crée `.venv/`, installe les dépendances manquantes, puis exécute le diagnostic.
