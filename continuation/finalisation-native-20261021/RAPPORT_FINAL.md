# Traduction cannabis — reprise finalisée le 21 octobre 2026

La livraison locale est terminée et scellée au statut `release_ready`. Aucune page wiki ni aucun environnement n'a été publié. La branche principale n'a pas été modifiée.

## Archive faisant autorité

`cannabis_traduction_en_2026-10-21_finalisee.zip` contient le corpus natif complet : `output/en/` pour les 153 pages anglaises, `imports/fr/` pour les sources françaises immuables, `output/fr/` pour les seules propositions d'ajout interlangue, et les données, verrous, revues et manifestes du kit. Aucun fichier français rendu n'a été envoyé au wiki.

SHA-256 : `fbb70744a0b0d67fdf4a556999cebb038babf754386a7ca6fca43584a6340cf4`

La reprise part de la version 2 vérifiée, SHA-256 `b317df79f35b047af2bdead55c5adbdb33c835fae528ed69f0de78e5d8332eda`, conservée avec les livraisons antérieures. Les identifiants locaux de cette livraison sont raccordés aux identifiants natifs par titre français, révision et empreinte ; voir `RACCORD_IDENTITES_FINAL.json`.

## Relecture et corrections

Les 153 pages ont une note individuelle de relecture bilingue. Les titres, les 165 libellés distincts, les 32 résumés, les métadonnées et la polarité des relations ont été comparés à la source. La reprise comprend une nouvelle passe des 63 alertes sémantiques et des débuts/fins des 149 citations. Les deux passes finales emploient des méthodes différentes, par le même assistant ; elles ne constituent pas deux relectures humaines indépendantes. Le protocole historique de première rédaction par lots n'est pas reconstitué rétrospectivement.

Le journal décrit 14 ajustements de champs ou de cohérence : intensité de la répression, conditions, degrés, sujets des comparaisons, titres et un libellé contextuel. Les formats anglais ont ensuite été normalisés : sections alphabétiques, références inline sans point terminal et suppression de la balise `references` anglaise. Aucun résumé français n'a été réécrit, aucune citation n'a été supprimée, aucun des 120 résumés absents n'a été ajouté.

L'inventaire final confirme 152 arguments plus le débat, 149 citations, deux passages entre citations, 32 résumés, 120 absences et 170 occurrences de relation : 13 racines et 157 liens entre arguments. Les libellés contextuels restent attachés à leur relation. Les 145 dates de citation sont conservées sous forme anglaise. Les dates de création et initialisations françaises ne sont pas copiées en anglais ; la date locale anglaise est une date de préparation, à adapter au jour réel d'une éventuelle première publication par le workflow prévu.

## Documentation et réserves historiques

41 ressources anglaises ont été retenues pour 108 pages, après sélection par pertinence ; les 153 décisions sont consignées. Aucune référence n'a été inventée pour remplir une rubrique. La recherche des noms consacrés comprend 68 consultations Crossref réussies, après reprise des réponses 429 à un rythme réduit ; aucun nom exactement coextensif n'est retenu. Il ne s'agit pas d'une preuve universelle d'absence de nom. L'article Wikipédia anglais retenu est `Legality of cannabis`.

Quatre attributions ou citations historiques restent sans confirmation documentaire exacte : Q063, Q064, Q069 et Q103, identifiants locaux de la livraison. Elles sont traduites et conservées, sans prétendre en établir l'authenticité. Les affirmations historiques sur 260 000 emplois, le classement de l'alcool comme drogue dure et la carte juridique datée restent signalées séparément. Aucun logo n'est projeté sans vérification de la cible et des droits. Le débat connexe anglais non vérifié est omis ; le refus HTTP 403 des API wiki ne prouve pas son inexistence. Ces réserves ne sont pas effacées par un résultat de validateur.

## Contrôles et code utilisé

- 1 794 contrôles supplémentaires d'intégrité textuelle et de paramètres réussis ; aucune anomalie de paramètre non résolue.
- 3 211 contrôles indépendants de parité entre la copie relue et le corpus natif réussis.
- Convergence native enregistrée sur deux passes propres, liée à la revue `189db95cceca3792de051ff3cadf18d81a93f149870856170d677bc99efbe2f3`.
- Rendu puis réextraction de l'archive exacte : couches structurelle, documentaire, revue sémantique et archive fraîche réussies, zéro erreur et zéro avertissement.
- Tests : 684 du kit, 501 du validateur, 22 de déploiement ; auto-audit réussi.

La validation utilise les correctifs de la branche dédiée `fix/translation-imported-source-preservation`, commit `bfae7884b74ddb7cc61e59c86e8d04c8d669818f`. Ils ajoutent le gel explicite des sources publiées et la validation différentielle de leur conservation. Ils ne sont pas encore fusionnés dans le kit publié : [PR 10](https://github.com/wikidebates/wikidebia/pull/10), empilée sur [PR 9](https://github.com/wikidebates/wikidebia/pull/9). Le dernier commit de branche, `42527ffd078800ac9c4ae5f053217cc8cd3a0838`, corrige uniquement une dépendance inutile dans un test ; les deux contrôles GitHub réussissent sur ce commit. Les numéros de composants restent ceux de la base de développement ; ce rapport identifie donc aussi le commit exact utilisé.

Les reçus automatiques vérifient la structure et la cohérence des preuves de revue. Ils ne prouvent pas à eux seuls la justesse de toute traduction ni l'authenticité d'une source historique.

## Sauvegarde et reprise

La livraison et les preuves finales sont sauvegardées exclusivement sur `translation/cannabis-en-20261021-verifiee`, dans `delivery/` et `continuation/finalisation-native-20261021/`. Les anciens dossiers et commits sont conservés. Aucun PDF ou corps intégral d'article consulté n'est ajouté à cette sauvegarde.

Pour reprendre, partir du ZIP final et de son reçu, pas des anciennes copies intermédiaires. Une publication éventuelle nécessitera une tâche distincte et les contrôles distants de ce workflow. Le relais français n'a pas été utilisé pour cette traduction.
