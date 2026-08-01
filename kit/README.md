# Kit Wikidéb’IA 2.2.3

Le kit publie et reprend les corpus Wikidéb’IA avec plans signés. La version 2.2.3, alignée sur la norme 1.2.18 et le validateur 0.4.19, conserve les barrières éditoriales 2.2.2 et rétablit la mise à niveau depuis un seul ZIP complet.

```bash
./wikidebia publish
./wikidebia update IDENTIFIANT --dry-run
./wikidebia upgrade
```

Pour une mise à niveau, déposer de préférence **le seul bundle complet** dans `updates/`, puis lancer `./wikidebia upgrade`. Le mode trois ZIP reste accepté pour compatibilité. Avec un ancien lanceur où `update` désigne encore les composants, utiliser exceptionnellement `./wikidebia update --no-git`.
