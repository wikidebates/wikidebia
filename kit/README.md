# Kit Wikidéb’IA 2.2.2

Le kit publie et reprend les corpus Wikidéb’IA avec plans signés. La version 2.2.2, alignée sur la norme 1.2.18 et le validateur 0.4.19, conserve les quatre barrières 2.2.1 et impose en plus la forme canonique `Auteur 1, Auteur 2` pour plusieurs auteurs.

```bash
./wikidebia publish
./wikidebia update IDENTIFIANT --dry-run
./wikidebia upgrade
```

`publish` calcule et transmet automatiquement l’empreinte du plan ; `update` conserve sa confirmation explicite car il peut déplacer ou supprimer des pages.
