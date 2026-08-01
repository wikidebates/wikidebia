# Guide de publication et de reprise Wikidéb’IA 2.2.4

## Nouveau débat

1. Déposer l’archive dans `incoming/`.
2. Exécuter `./wikidebia publish [SÉLECTEUR] --scope all`.
3. Conserver les reçus et états écrits sous `.state/`.

## Débat déjà publié

1. Installer le nouveau corpus sous `corpus/<debate_id>` ou déposer son ZIP dans `incoming/`.
2. Exécuter `./wikidebia update <debate_id> --dry-run`.
3. Examiner `manual_review` et `blocked`.
4. Vérifier l’empreinte du plan.
5. Exécuter `./wikidebia update <debate_id>` et confirmer exactement cette empreinte.
6. Contrôler le reçu final et les nouveaux états publiés signés.

## Mise à niveau des composants

Le mode recommandé utilise un seul fichier :

```bash
rm -f updates/*.zip
cp WIKIDEBIA_*.zip updates/
./wikidebia upgrade
```

Le ZIP complet doit contenir `wikidebia-normes.zip`, `wikidebia-validator.zip` et `wikidebia-kit.zip`. Le mode trois ZIP séparés reste accepté.

Lors de la transition depuis un ancien lanceur où la commande de composants s’appelle encore `update`, lancer une seule fois :

```bash
./wikidebia update --no-git
```

Après cette installation, employer `upgrade` pour les composants et réserver `update IDENTIFIANT` à la reprise d’un débat publié.
