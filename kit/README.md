# Kit générique Wikidéb’IA — 2.2.0

Le kit sépare désormais trois opérations : publier un nouveau corpus, reprendre un corpus déjà publié et mettre à niveau les composants de l’installation.

## Publication initiale

Déposer le ZIP du débat dans `incoming/`, puis lancer :

```bash
./wikidebia publish
```

Avec plusieurs ZIP, fournir le nom du fichier sans `.zip`. Le nom extérieur sélectionne l’archive ; `manifest.debate_id` reste l’identité du corpus. La publication valide le corpus avec le validateur 0.4.17, produit un plan signé, traite la page Débat avant les arguments et conserve un état publié signé contenant les révisions MediaWiki obtenues.

## Reprise d’un débat déjà publié

```bash
./wikidebia update IDENTIFIANT --dry-run
./wikidebia update IDENTIFIANT
```

Le moteur compare le dernier état publié signé, le wiki courant et le nouveau corpus. Il produit les catégories `create`, `skip`, `update`, `move`, `redirect`, `delete`, `manual_review` et `blocked`. Une page absente du nouveau manifeste n’est jamais supprimée sans preuve qu’elle appartenait à la version antérieure du même débat.

Portées disponibles :

```bash
./wikidebia update IDENTIFIANT --scope fr
./wikidebia update IDENTIFIANT --scope en
./wikidebia update IDENTIFIANT --no-delete
./wikidebia update IDENTIFIANT --only-delete
./wikidebia update IDENTIFIANT --dry-run
```

Une exécution réelle affiche l’empreinte SHA-256 du plan et demande sa confirmation, sauf avec `--yes`. Les mises à jour utilisent la révision distante attendue et `baserevid`. Une modification humaine ou indéterminée est classée `manual_review` avec comparaison de l’ancienne version, de la version distante et de la proposition.

Les suppressions exigent l’ancien état publié, une révision distante inchangée, les marqueurs Wikidéb’IA, l’absence de réutilisation connue et le droit effectif `delete`. Le kit ne pose jamais de bandeau à la place d’une suppression. Les nouvelles pages sont vérifiées avant la première suppression.

Le dernier recours est un inventaire signé et en lecture seule placé sous `.state/inventories/<debate_id>/<langue>.json`, explicitement borné aux pages rattachées au débat.

## Mise à niveau de l’installation

Déposer les composants dans `updates/`, puis lancer :

```bash
./wikidebia upgrade
```

Cette commande valide et teste les paquets en zone temporaire, archive les versions précédentes, installe atomiquement les nouveaux composants et synchronise Git lorsque configuré.

## Droits MediaWiki

- création et modification : `edit`, `createpage` ;
- déplacement : `move` ;
- suppression : `delete` ;
- consultation d’archives supprimées : `browsearchive`, éventuellement `deletedhistory`.

Un groupe administrateur n’est pas requis lorsque ces droits sont attribués à un groupe limité ou au compte bot. Le préflight vérifie tous les wikis sélectionnés avant la première écriture.

## Authentification et sécurité

La famille personnalisée `wikidebates`, les BotPasswords et la configuration `private/pywikibot/` sont réutilisés. Les langues sont traitées séquentiellement. Les secrets, corpus, plans, journaux, états, archives et environnements virtuels restent exclus de Git. Aucun chemin absolu persistant n’est produit.

Le moteur bas niveau se trouve dans `scripts/wikidebia_update.py`. Le validateur ne réalise aucune lecture ou écriture distante.
