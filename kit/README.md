# Kit générique Wikidéb’IA — 2.1.17

Le kit 2.1.17 fournit deux niveaux d’utilisation :

- `./wikidebia`, commande intégrée destinée à l’usage courant ;
- `kit/scripts/wikidebia_publish.py`, moteur bas niveau conservé pour l’audit et les opérations spécialisées.

## Publier un débat

Déposer le ZIP du débat dans `incoming/`. Aucun suffixe particulier n’est imposé. Si ce dossier contient un seul ZIP, lancer :

```bash
./wikidebia publish
```

S’il contient plusieurs ZIP, indiquer l’identifiant correspondant au nom du fichier sans `.zip` :

```bash
./wikidebia publish gpa_autorisation
```

Le fichier sélectionné est alors `incoming/gpa_autorisation.zip`. Son nom sert uniquement à choisir l’archive ; le champ `debate_id` du manifeste interne détermine l’identité du corpus et peut être différent. Une ancienne archive telle que `education_sexualite_ecole_fr_en_release_ready_repaired_2026-07-31.zip` reste donc publiable sans renommage lorsqu’elle est seule dans `incoming/`.

La commande extrait le paquet de façon sûre, l’installe sous `corpus/`, exécute le validateur 0.4.16, construit le plan signé, crée et revérifie la page Débat française lorsque nécessaire, publie les pages dans l’ordre canonique et archive le ZIP après succès.

Portées disponibles :

```bash
./wikidebia publish --scope fr-debate
./wikidebia publish --scope en-debate
./wikidebia publish --scope fr
./wikidebia publish --scope en
./wikidebia publish --scope all
```

Dans chaque langue, la page Débat ou Debate précède toujours les pages Argument. Le moteur refuse une configuration qui place `argument` avant `debate`.

## Mettre à jour l’installation

Déposer soit l’archive complète, soit les trois ZIP de composants dans `updates/`, puis lancer :

```bash
./wikidebia update
```

La commande vérifie les manifestes et SHA-256, compare les versions, extrait dans une zone temporaire, exécute l’auto-audit et les tests, sauvegarde les composants précédents et les fichiers entrants dans `archives/updates/`, installe les nouvelles versions et vide `updates/`. Lorsque le dépôt Git possède un remote `origin`, le commit et le push sont automatiques.

## GitHub et fichiers privés

L’initialisation du dépôt distant se fait une seule fois :

```bash
./wikidebia github-init git@github.com:COMPTE/wikidebia.git
```

Le modèle `.gitignore` exclut `private/`, `corpus/`, `archives/`, `updates/`, `incoming/`, `logs/`, `plans/`, `.state/`, `.venv/` et la configuration locale. `user-config.py` et `user-password.cfg` résident dans `private/pywikibot/`.

Toutes les configurations persistantes utilisent des chemins relatifs. Le dossier racine peut être renommé ou déplacé.

## Reconstruction automatique de l’environnement Python

Le lanceur `./wikidebia` recrée `.venv/` lorsqu’il est absent ou inutilisable. Il installe ensuite, dans cet environnement local exclu de Git, les dépendances déclarées dans `requirements-runtime.txt`, notamment Pywikibot, JSON Schema et pytest. Un clone propre du dépôt peut donc être remis en service simplement avec :

```bash
./wikidebia doctor
```

La première exécution peut télécharger les paquets Python. Les commandes suivantes réutilisent l’environnement vérifié.

## Sécurité conservée

Le moteur bas niveau conserve les plans signés, `createonly`, `baserevid`, la vérification de la révision exacte, la balise `chatgpt`, le blocage des collisions, le contrôle des liens interlangues et la compaction obligatoire `}}{{`.

Lors de la mise à jour, les ZIP encore présents dans l’ancien dossier `incoming/debates/` sont migrés automatiquement vers `incoming/`; une collision différente est bloquée sans écrasement.

## Compatibilité des corpus historiques

Les champs `normative_versions` du manifeste décrivent les versions utilisées lors de la production du corpus et ne sont pas réécrits lors d’une mise à jour locale. Le kit publie un corpus historique lorsque le validateur installé déclare sa norme compatible et renvoie un rapport positif sans erreur ni avertissement. La version réelle du validateur exécuté doit toujours être exactement celle exigée par le kit courant.
