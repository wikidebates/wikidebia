# Revue française du contenu et de la documentation

> Depuis 1.2.54, les normes éditoriales sont cumulatives : les anciennes métadonnées de révision ne servent plus à sélectionner les contrôles.

La phase de contenu intervient après le verrouillage et la publication du graphe et des titres. Elle prend désormais aussi en charge les **rubriques et mots-clés**, afin qu’ils soient publiés au second checkpoint avec l’introduction, les résumés et la documentation. Elle part de `reviewed-copy/`, conserve toutes les copies antérieures et ne génère toujours aucune page MediaWiki finale.


## Protection des textes historiques

Pour une page importée avec `page_origin=preexisting`, l’introduction du Débat et les résumés des Arguments sont **protégés par défaut**. `--prepare` recopie leur valeur historique avec `decision=keep`; une absence historique de résumé reste absente. ChatGPT peut renseigner `suggested_change` sans modifier `proposed_*`. Les règles de style de création ne sont pas appliquées rétroactivement à un texte simplement préservé.

Si le propriétaire approuve une correction pendant que la revue est ouverte, le ZIP rendu peut porter `decision=change`, la valeur finale et un `historical_change_request` précis (`field_key`, `final_value`, `change_type`, `rationale`, `owner_instruction_reference`). Ce contenu ne s’autorise jamais lui-même : `./wikidebia review-import` bloque encore le delta. Après accord explicite du propriétaire, lancer le **même ZIP** avec `./wikidebia review-import --authorize-historical-changes` (ou avec le `debate_id` en cas d’ambiguïté). Le kit crée alors localement un reçu de consentement lié au ZIP exact et à chaque SHA avant/après, finalise la même `fr_content_review` et publie le delta au checkpoint français n°2. Une autorisation ne couvre aucun autre champ. Une opération corrective séparée n’est nécessaire que si la demande arrive après la clôture du checkpoint.

Après ce consentement, la valeur finale proposée est la **valeur éditoriale sélectionnée** : l’historique reste sa provenance, mais l’extraction de `review.subsections`, les contrôles structurels, le verrou, le changeset, le rendu, le checkpoint 2 et la traduction utilisent le texte final autorisé. Pour une modification structurelle d’introduction, `historical_change_request.change_scope` peut décrire précisément les sous-parties ajoutées, modifiées, supprimées et un éventuel réordonnancement. Les contrôles de création s’appliquent alors seulement aux sous-parties ajoutées ou substantiellement réécrites. Une portée « ajouter `Enjeux du débat` » bloque toute autre modification silencieuse de l’introduction.

## 1. Préparer la revue

```bash
./wikidebia corpus-workspace-content-review <debate_id> \
  --work-id <work_id> \
  --prepare
```

La commande lit le wikicode importé et crée :

```text
reviews/fr/content_review.json
reviews/fr/classification_review.json
data/keyword_vocabulary_working.json
data/sources_working.json
audits/fr_content_inventory.json
audits/fr_content_inventory.md
```

Le registre couvre :

- `sujet` et `sujet-développé` de la page Débat ;
- l’introduction et chacune de ses sous-parties ;
- les articles Wikipédia français vérifiés ;
- les neuf paramètres documentaires de la page Débat ;
- le résumé de chaque argument comme contexte ; pour une page préexistante sa valeur et sa présence sont protégées et non réécrites ;
- les données de contenu des arguments français importés ; les arguments réellement nouveaux ne sont pas créés par cette commande et doivent, lorsqu’un corpus en contient, être accompagnés de la revue documentaire 1.2.53 décrite ci-dessous ;
- la bibliographie, la sitographie et la vidéographie de chaque argument ;
- les attestations de lisibilité, de fidélité logique, de force expressive et de vérification documentaire.

Aucune proposition produite par une heuristique n’est appliquée automatiquement.


## Recherche d’un nom consacré pour un argument nouveau

Cette exigence relève du contrat général de génération 1.2.53. La commande `corpus-workspace-content-review` ci-dessus part d’un snapshot importé et ne crée donc pas elle-même de nouvel argument français. Lorsqu’un corpus généré contient des pages `Argument` françaises nouvelles, il doit fournir `reviews/argument_name_discovery_review.json` avant validation ; le validateur 0.4.61 bloque toute page nouvelle non couverte. La phase de traduction anglaise du kit construit la partie anglaise de ce registre pour les pages anglaises nouvelles.

La recherche est **obligatoire**, mais l’ajout d’un nom ne l’est pas. Le cas normal est `outcome=none`. Il ne faut jamais chercher à augmenter artificiellement le nombre de pages possédant `nom-consacré=`.

Pour chaque argument nouveau :

1. partir du raisonnement complet (prémisses, mécanisme, conclusion), pas seulement de son titre ;
2. effectuer au moins deux recherches terminologiques distinctes ;
3. lorsque la littérature pertinente est internationale, vérifier également l’anglais ou la langue académique/originale pertinente ;
4. privilégier les encyclopédies spécialisées, ouvrages et articles académiques ;
5. ne retenir un nom que si ces sources emploient réellement cette étiquette pour le **même raisonnement** ;
6. ne pas transformer en nom d’argument un thème, une doctrine, un auteur, un principe seulement mobilisé ou un raccourci inventé ;
7. en français, ne pas fabriquer une traduction d’un nom anglais : employer une forme française attestée ou, si c’est l’usage établi, la forme étrangère elle-même ;
8. au moindre doute sérieux, conclure `none`.

La fiche `reviews/argument_name_discovery_review.json` conserve les requêtes, le périmètre de recherche, le résultat et la justification. Si le résultat est `known_name`, elle conserve aussi au moins une attestation documentaire avec l’appellation telle qu’elle est utilisée et sa localisation.

La rareté des arguments nommés est donc attendue, mais elle n’est pas contrôlée par un quota : certains corpus spécialisés peuvent naturellement en contenir davantage que d’autres.

## 2. Finaliser la revue

Après avoir complété le registre de contenu et le registre documentaire :

```bash
./wikidebia corpus-workspace-content-review <debate_id> \
  --work-id <work_id> \
  --finalize
```

La finalisation vérifie notamment :

- que chaque `document_kind` de `data/sources_working.json` appartient directement à l’enum accepté par le registre documentaire final, afin de bloquer l’erreur avant la projection vers `data/sources.json` ;

- l’inventaire exhaustif, sous-partie par sous-partie, des notions spécialisées, avec vérification de chaque lien, explication intégrée, traitement antérieur ou justification contextuelle ;

- la couverture exacte de tous les arguments actifs ;
- pour une introduction nouvellement créée ou explicitement réécrite, l’existence d’une structure conforme ; une introduction historique préservée n’est pas normalisée rétroactivement ;
- la présence d’au moins un article Wikipédia français vérifié ;
- l’absence de doublon entre les orientations pour, contre et neutre ;
- le classement neutre des sources qui développent substantiellement les deux positions ;
- l’absence de quota minimal par paramètre documentaire ;
- l’absence de quota documentaire imposé aux pages Argument ;
- la cohérence entre les sources retenues et leurs usages déclarés ;
- la langue française des références utilisées sur la page Débat ;
- la vérification de la langue et de l’attribution des sources web et vidéo ;
- la présence du créateur ou de la chaîne pour toute vidéo YouTube ;
- la densité informative et la non-redondance des sous-parties ;
- l’présence obligatoire d’une rubrique « Enjeux du débat » qui expose au moins deux conséquences concrètes sans recopier le graphe ;
- l’absence de point final dans une simple notice `<ref>` ; toute note conservant un point doit être une phrase complète attestée par SHA-256 ;
- pour les résumés nouveaux ou explicitement réécrits, l’absence de métadiscours et d’auto-objection ; les résumés historiques préservés ne sont pas réécrits pour ce motif ;
- pour les résumés nouveaux ou explicitement réécrits, la présence réelle de l’expression attestant la force du résumé ;
- la vérification explicite des affirmations chiffrées lorsqu’elles existent.

La revue et le registre documentaire sont liés par SHA-256. La finalisation ne modifie pas `reviewed-copy/`.

## 3. Appliquer la revue

```bash
./wikidebia corpus-workspace-content-review <debate_id> \
  --work-id <work_id> \
  --apply \
  --confirm-review-sha256 <empreinte>
```

L’application crée atomiquement :

```text
content-reviewed-copy/
```

Cette copie contient notamment :

```text
data/fr_content_lock.json
data/sources.json
changes/fr_content_changeset.json
reviews/introduction_review.json
reviews/summary_style_review.json
reviews/fr/content_review.json
```

Les états antérieurs restent intacts :

```text
corpus/<debate_id>/
working-copy/
reviewed-copy/
content-reviewed-copy/
```

Le registre maître reçoit seulement les identifiants des sources françaises sélectionnées pour chaque argument. Le verrou de métadonnées françaises, les imports et le graphe restent inchangés. Après succès, la préparation anglaise passe à `ready_for_translation`.

La primitive basse `--apply` reste locale. Dans le workflow utilisateur `review-import`, son succès déclenche ensuite le **checkpoint français 2.16.13** : rendu FR sans interlangue, plan de reprise signé, publication/attestation distante, puis seulement préparation de la traduction anglaise.
