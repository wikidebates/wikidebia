# Migration vers la norme 1.2.10

1. Remplacer chaque note d’introduction de la forme `<ref>{{Référence|…}}</ref>` ou `<ref>{{Reference|…}}</ref>` par une référence rédigée directement dans `<ref>…</ref>`.
2. Ne conserver aucun modèle MediaWiki dans le corps d’une note développée d’introduction.
3. Conserver les dates documentaires en langage naturel et les dates de création au format `AAAA-MM-JJ`.
4. Les références nommées restent utilisables : la première définition contient le texte direct, les occurrences suivantes peuvent utiliser `<ref name="…" />`.
5. Déclarer `consolidated_norm` à `1.2.10`, utiliser le validateur 0.4.10 et le kit 2.1.10.
