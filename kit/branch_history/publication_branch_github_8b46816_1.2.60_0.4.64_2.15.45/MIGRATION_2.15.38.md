# Migration 2.15.38

Cette maintenance ajoute le rattrapage audité de la balise `translated-fr` sur les révisions anglaises déjà créées comme traductions de pages françaises.

La simulation :

```bash
./wikidebia tag-translated-fr dieu_existe_t_il --dry-run
```

lit l'état publié anglais, cible les révisions de création attestées, vérifie le créateur, le contenu, le résumé `Translation of the French page [[:fr:X|X]]` et la présence de `chatgpt`, puis exige que `translated-fr` soit une balise MediaWiki active, définie et manuelle et que le compte possède `changetags`.

L'exécution :

```bash
./wikidebia tag-translated-fr dieu_existe_t_il
```

utilise `action=tag` sur les identifiants de révision existants. Elle ne crée aucune révision, ne modifie aucun wikicode ni résumé de modification, est idempotente et produit un reçu de vérification.
