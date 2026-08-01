# Kit Wikidéb’IA 2.2.1

Le kit publie et reprend les corpus Wikidéb’IA avec plans signés. La version 2.2.1, alignée sur la norme 1.2.17 et le validateur 0.4.18, ajoute quatre barrières : article Wikipédia obligatoire, absence de débats connexes rendus, refus des tableaux JSON dans les auteurs et publication ordinaire sans invite interactive.

```bash
./wikidebia publish
./wikidebia update IDENTIFIANT --dry-run
./wikidebia upgrade
```

`publish` calcule et transmet automatiquement l’empreinte du plan ; `update` conserve sa confirmation explicite car il peut déplacer ou supprimer des pages.
