# Handoff — Les hommes doivent-ils rejoindre le combat féministe ?

- Branche : `codex/traduction-combat-feministe`
- Commit de référence du snapshot : commit contenant ce fichier
- Date du snapshot : 24 octobre 2026
- Phase : `final_publication`
- Statut local : `release_ready`
- Work actif : `EDIT-20261023-001`
- Publication anglaise distante commencée : non

## Point de reprise

La traduction française vers l’anglais est terminée, relue par deux passes
sémantiques convergentes, rendue et empaquetée. La release complète et validée
est conservée dans :

```text
runtime/final-checkpoint/release/les_hommes_doivent_ils_rejoindre_le_combat_feministe.zip
```

Empreintes courantes :

- revue anglaise :
  `75dc7ef38c90a0cabd6247c7ccea55bfe0ba22bf3d88502402854939852981dc` ;
- copie traduite :
  `c4811acc57803056e6b3117a755f07fd3a37d17b3f4f8cedbb9f32ed2bd7c405` ;
- copie rendue :
  `a4d8eb2a12113cda269970f1270cc4909d57be75affb092d0bc705ae5cae0c06` ;
- copie de release :
  `65d4a71510b05f4d25b39b2ab6bb9d4c8feb8b0460cb0dd21d04edf8dedd6b22` ;
- archive de release :
  `9e221ecb06eef460f1abeda04a858c50edc2c83f6b5e59411a847609052d8f18`.

La validation finale compte zéro erreur et zéro avertissement. Après intégration
des correctifs parallèles et de la réconciliation post-checkpoint, la suite
ciblée combinée compte 282 réussites.
L’audit couvre les 125 libellés de relation.

La revue française de contenu complétée, intégrée depuis le travail parallèle,
porte l’empreinte
`26d3c3de52b9d90a837d58bb73bef66bba7ccaa746b7564bdb1029823fe7cb07`.
Elle conserve les 22 résumés historiques, les 78 absences de résumé, les sept
citations et les deux références web historiques. Les changements de
classification restent traçables dans cette revue.

## Titres affichés contextuels

La régression venait du fait que les titres affichés étaient protégés au niveau
du nœud, sans verrouiller chaque occurrence dans les relations. Cinq libellés
historiques différaient du titre global : `E00043`, `E00045`, `E00047`,
`E00048` sous `A0007`, et `E00097` sous `A0028`.

Les cinq formes françaises ont été rétablies sur le wiki français. Le plan et
le reçu signés se trouvent dans :

- `runtime/fr-publication/content/contextual-displayed-title-restoration-plan.json` ;
- `runtime/fr-publication/content/contextual-displayed-title-restoration-receipt.json`.

Le rendu, les deux checkpoints français, la revue anglaise et le validateur
utilisent désormais les libellés contextuels. Les cinq traductions anglaises
proviennent des titres affichés historiques, et non des reformulations globales.

## Portabilité et audit distant

La trace non normative `reports/initial_validation_execution.json` est exclue
de l’empreinte portable du build. La compatibilité avec les anciennes traces
reste limitée aux deux champs de chemin absolu et contrôlée par leur SHA-256
historique.

Le mode d’audit distant intégré aux outils de publication est strictement en
lecture seule et n’exige aucun identifiant d’écriture. L’audit des opérations
parallèles du 24 octobre a confirmé que les huit dernières révisions françaises
sont exactement les corrections attendues et que les 101 pages relues
correspondent aux empreintes de l’état publié.

## Règle `oe`

Les consignes du dépôt interdisent désormais de remplacer `oe` par `œ`, aussi
bien lors de la génération d’un débat que lors d’une traduction. Les formes
historiques qui contiennent déjà `œ` restent inchangées.

Deux titres canoniques corrigés auparavant ont été rétablis avec `oe` (`A0084`
et `A0085`). Quatre liens entrants ont été réécrits et les anciennes formes avec
ligature redirigent vers les formes accessibles au clavier. L’état distant a été
relu sans divergence. Les preuves se trouvent dans :

- `runtime/fr-publication/content/oe-canonical-title-restoration-plan.json` ;
- `runtime/fr-publication/content/oe-canonical-title-restoration-receipt.json` ;
- `runtime/published/fr/latest.json`.

## Reprise de la publication finale

La baseline finale accepte désormais les deux corrections françaises
postérieures au checkpoint uniquement après vérification de leur succession
signée : même Work, même corpus, même ensemble de 101 pages, révisions
monotones et reçus de correction valides.

Le préflight du 24 octobre a authentifié l’accès français puis a échoué sur
l’authentification anglaise avant toute écriture distante. Le runtime utilisait
encore l’ancien secret, car le nouveau brouillon d’environnement n’avait pas
encore été publié. Après application du secret renouvelé, restaurer le workspace
depuis l’archive de release et les états `runtime/editorial-workspace/workspace.json`
et `runtime/workflow/workflow.json`, puis reprendre uniquement la phase
`final_publication` avec un préflight distant neuf.

La phase doit créer les 101 pages anglaises puis ajouter les liens interlangues
aux 101 pages françaises. Elle ne doit modifier aucun autre contenu français.

## État des accès

L’accès français `ChatGPT@Codex-FR` a servi uniquement aux corrections décrites
ci-dessus et a été vérifié après écriture. Aucun secret n’est inclus dans cette
sauvegarde. Le brouillon d’environnement révision 2 enregistre les identités non
secrètes `ChatGPT@Codex-FR` et `ChatGPT@Codex-EN`. Le secret anglais du runtime
courant doit être considéré comme invalide jusqu’à la publication de ce
brouillon ; ne pas reprendre automatiquement une tentative de connexion avant
le redémarrage de l’environnement.

## Retest de l’accès anglais

Après resynchronisation au commit `55f8987`, un nouveau test authentifié et
strictement sans écriture a été exécuté depuis le runtime courant. Le secret
d’accès HTTP `WIKIDEBIA_API_TOKEN` y est prêt, mais les deux variables attendues
pour le BotPassword anglais sont absentes :

- `WIKIDEBIA_EN_BOT_USERNAME` ;
- `WIKIDEBIA_EN_BOT_PASSWORD`.

Pywikibot s’est donc arrêté avant l’authentification avec une identité anglaise
non définie. Aucune écriture distante n’a commencé. Le correctif `3631a48`
transforme désormais ce cas en diagnostic explicite et testé, au lieu de laisser
remonter l’erreur interne de Pywikibot. La publication finale pourra reprendre
dès qu’un nouvel environnement exposera ces deux variables, avec le nom de bot
`ChatGPT@Codex-EN`, et que le contrôle de l’utilisateur actif retournera
exactement `ChatGPT`.
