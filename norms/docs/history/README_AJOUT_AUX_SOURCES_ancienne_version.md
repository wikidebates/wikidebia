# Ajout de la norme Wikidéb’IA 1.1.9 aux sources

## Fichiers à ajouter comme sources lisibles

Ajoutez individuellement les fichiers `.md` et `.json` de ce dossier aux sources du projet. Le fichier principal est `WIKIDEBIA_NORME_CONSOLIDEE_1.1.9.md`. Les autres documents fournissent le workflow, le profil de rendu, le catalogue d’exigences, la traçabilité et les exemples de registre.

La norme 1.1.8 doit être conservée comme historique, mais la 1.1.9 devient la seule norme consolidée active.

## Fichier à ne pas utiliser comme source documentaire principale

`wikidebia-validator-0.3.1.zip` est un outil d’exécution local. Conservez-le dans le dossier v4 avec son reçu, mais privilégiez les fichiers textuels individuels de ce paquet pour les sources consultables par ChatGPT.

## Effet sur les corpus existants

L’ajout de ces sources ne modifie aucun corpus. Pour migrer un corpus vers 1.1.9, suivez `MIGRATION_1.1.9.md`, mettez à jour son manifeste et son registre de revue, puis régénérez les agrégats et empreintes documentaires. Le graphe reste inchangé.
