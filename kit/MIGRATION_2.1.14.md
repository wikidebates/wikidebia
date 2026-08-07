# Migration vers le kit 2.1.14

1. Remplacer le kit 2.1.13 par le kit 2.1.14.
2. Conserver les ZIP de débats directement dans `incoming/`.
3. Lorsqu’un seul ZIP est présent, `./wikidebia publish` le sélectionne quel que soit son nom.
4. Lorsqu’il y en a plusieurs, l’argument de commande sélectionne exactement le nom du ZIP sans `.zip`.
5. Le champ `manifest.debate_id` est l’identité autoritative du débat et détermine le dossier `corpus/<debate_id>` ainsi que la configuration de publication ; il n’a pas à être identique au nom du ZIP.

Cette correction rend compatibles les archives historiques portant des suffixes descriptifs ou une date, sans diminuer les contrôles sur le manifeste interne, l’extraction sûre et la validation du corpus.
