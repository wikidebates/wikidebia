## 0.4.53 — 7 août 2026

- alignement sur la norme 1.2.50 ;
- distinction stricte entre création de page et modification d’une page existante ;
- protection exacte de l’ensemble des métadonnées historiques de cycle de vie et d’avertissement ;
- nouveau contrôle `WDV-EDT-030` : un paramètre top-level attesté sur une page historique ne peut disparaître sans autorisation page/paramètre ;
- conservation de l’absence historique d’un paramètre et interdiction d’ajouter rétroactivement les marqueurs IA ;
- prise en charge d’une restauration corrective contrôlée contre l’inventaire source ;
- 306 tests pytest réussis.

## 0.4.52 — 7 août 2026

- alignement sur la norme 1.2.49 ;
- `nom` / `name` devient un champ historique préservé lorsqu’il est attesté ;
- blocage de toute suppression, modification ou invention du paramètre ;
- confrontation de la valeur au snapshot source sous `verification_revision=0.4.52`.

## Correctif 0.4.51 — 7 août 2026

- prise en compte d’une suppression de résumé historique explicitement décidée par le propriétaire, avec provenance `owner_removed` et décision tracée ;
- maintien du verrou strict pour tous les autres résumés historiques.

## 0.4.51 — 7 août 2026

- alignement sur la norme 1.2.48 ;
- ajout du schéma `manual_remote_adoptions` ;
- ajout de `WDV-RMT-007` pour vérifier le rattachement des pages, titres et décisions d’adoption ;
- maintien du blocage des modifications humaines non attestées.

## 0.4.50 — 6 août 2026

- préservation contrôlée de `débat-détaillé` / `detailed-debate` sur les pages historiques ;
- comparaison exacte avec l’inventaire source et le verrou de contenu historique ;
- omission admise des relations locales uniquement lorsqu’elle est déclarée et que le propriétaire a été prévenu ;
- suppression des faux écarts `WDV-MWK-008` pour ces frontières attestées ;
- compatibilité conservée avec les corpus antérieurs.

## 0.4.49 — 6 août 2026

- alignement sur la norme 1.2.46 ;
- ajout de `WDV-EDT-029` pour l’inventaire exhaustif des notions spécialisées de chaque sous-partie ;
- vérification des termes visibles, des liens réellement rendus, des extraits explicatifs et des traitements antérieurs ;
- blocage des liens Wikipédia non déclarés dans l’inventaire ;
- remplacement du mécanisme principal de 1.2.45 sans rétroactivité sur les corpus historiques.

## 0.4.48 — 6 août 2026

- alignement sur la norme 1.2.45 ;
- ajout de `WDV-EDT-028` pour la cohérence locale des liens Wikipédia explicatifs ;
- vérification des groupes de notions, des articles déclarés et des liens réellement présents ;
- justification obligatoire des notions laissées sans lien dans un groupe partiellement lié ;
- compatibilité 1.2.44 conservée.

## 0.4.47 — 6 août 2026

- alignement sur la norme 1.2.44 ;
- ajout de `WDV-DOC-008` pour les points terminaux placés dans de simples notices `<ref>` ;
- exception réservée aux phrases complètes attestées par SHA-256 dans la revue de l’introduction ;
- contrôle du registre `reference_note_punctuation_reviewed` et des exceptions ;
- compatibilité avec les normes antérieures conservée.

## 0.4.46 — 6 août 2026

- alignement sur la norme 1.2.43 ;
- sous-partie dédiée aux enjeux obligatoire sous la politique 1.2.43 ;
- contrôle du titre français ou anglais, du volume minimal et de la ligne de revue correspondante ;
- au moins deux enjeux concrets distincts requis dans le registre ;
- compatibilité 1.2.42 conservée sans rétroactivité silencieuse.

## 0.4.45 — 6 août 2026

- alignement sur la norme 1.2.42 ;
- suppression du plafond statistique imposant des titres affichés distincts ;
- contrôle des références dupliquées entre orientations documentaires ;
- contrôle du créateur ou de la chaîne pour les vidéos YouTube des pages Débat ;
- revue renforcée de la densité informative des introductions ;
- compatibilité conservée avec les normes antérieures.

## 0.4.44 — 6 août 2026

- alignement sur la norme 1.2.41 ;
- conservation intégrale des contrôles 0.4.43 ;
- prise en charge de la nouvelle révision normative sans migration forcée des corpus historiques ;
- compatibilité avec les verrous de résumés historiques vérifiés par 0.4.43 et 0.4.44.

## 0.4.43 — 6 août 2026

- alignement sur la norme 1.2.40 ;
- prise en charge de `summary_provenance=historical_absent` ;
- omission du résumé autorisée uniquement après vérification de l’inventaire source ;
- maintien du résumé obligatoire pour les pages nouvelles et les contenus `generated_after_import` ;
- revue des résumés adaptée aux pages historiquement dépourvues de résumé.

## 0.4.42 — 6 août 2026

- correction du verrou historique : confrontation obligatoire à l’inventaire source lorsque `verification_revision=0.4.42` ;
- refus des résumés faussement déclarés historiques, des résumés historiques classés comme générés, des valeurs `initialisation` manquantes et des empreintes de verrou divergentes ;
- ajout de trois tests d’intégration et conservation de la norme 1.2.39 ;
- alignement sur le kit 2.15.15.

## 0.4.41 — 6 août 2026

- alignement sur la norme 1.2.39 et le kit 2.15.14 ;
- séparation des profils mots-clés, résumés et capitalisation ;
- ajout de `WDV-EDT-027` et du verrou des contenus historiques ;
- autorisation conditionnelle de `initialisation` / `initialization` uniquement lorsqu'il est attesté et inchangé ;
- blocage de toute réécriture des résumés historiques verrouillés ;
- compatibilité conservée avec le profil combiné 1.2.38.

## 0.4.40 — 6 août 2026

- alignement sur la norme 1.2.38 et le kit 2.15.13 ;
- distinction entre intersections compositionnelles et locutions atomiques ;
- rejet bilingue de `psychologie religieuse`, `religious psychology`, `science et religion` et constructions analogues ;
- maintien explicite de `argument d'autorité` comme catégorie atomique ;
- ajout des schémas `keyword_vocabulary` et `summary_style_review` ;
- tests d’intégration des codes éditoriaux et du périmètre `schema` ;
- correction de la détection de `le dieu unique`.

## 0.4.39 — 5 août 2026

- alignement sur la norme 1.2.37 et le kit 2.15.12 ;
- ajout de `WDV-EDT-024` contre les résumés à gabarit, les énumérations de pages filles et les phrases répétées à l’échelle du corpus ;
- ajout de `WDV-EDT-025` pour l’atomicité des mots-clés et les exceptions multi-mots motivées ;
- ajout de `WDV-EDT-026` pour la capitalisation du nom propre `Dieu` ;
- revue des résumés renforcée par `originality_reviewed` et `mechanism_statement` ;
- compatibilité explicite conservée avec la norme 1.2.36 et toutes les révisions antérieures annoncées.

## 0.4.38 — 5 août 2026

- alignement sur la norme 1.2.36 et le kit 2.15.11 ;
- `per_page_preserved` devient la politique de date par défaut lorsque le manifeste n’en déclare aucune ;
- conservation de la cohérence page par page entre manifeste, registre et wikicode sans exiger une date globale ou la date du jour ;
- prise en charge des plans documentant la préservation automatique des paramètres historiques et les suppressions historiques explicitement autorisées ;
- maintien de la traduction anglaise différée, des contrôles éditoriaux 1.2.35 et de toutes les protections contre les modifications humaines.

## 0.4.36 — 5 août 2026

- alignement sur la norme 1.2.34 et le kit 2.15.9 ;
- ajout du statut explicite `translation_status.en=deferred` ;
- suppression ciblée de WDV-WF-005 pour les titres anglais absents uniquement dans ce mode ;
- suspension des contrôles anglais et bilingues pendant la publication française différée ;
- contrôle strict de tout lien interlangue déjà présent et de toute page anglaise manifestée ;
- blocage des titres anglais `locked` sans titre canonique ;
- maintien intégral des exigences bilingues pour les corpus antérieurs et les états `ready` ou `published` ;
- ajout des scénarios de publication française seule et de transition ultérieure vers l’anglais.

## 0.4.35 — 5 août 2026

- alignement sur la norme 1.2.33 ;
- ajout de `WDV-SRC-006` pour exiger qu’une référence sélectionnée sur une page Argument développe effectivement l’argument ;
- acceptation explicite d’une référence qui développe l’argument tout en traitant aussi d’objections ;
- ajout de `WDV-MWK-023` pour préserver exactement les paramètres protégés des pages préexistantes ;
- distinction entre valeurs de création et valeurs préservées lors d’une modification ;
- compatibilité des corpus 1.2.32 et antérieurs conservée.

## 0.4.34 — 4 août 2026

- alignement sur la norme 1.2.32 ;
- ajout de WDV-EDT-023 pour la capitalisation canonique des mots-clés ;
- blocage des doublons ne différant que par la casse ;
- compatibilité des corpus 1.2.31 et antérieurs conservée.

## 0.4.33 — 4 août 2026

- alignement sur la norme 1.2.31 ;
- prise en charge de `depth_policy.limit_policy=unbounded` ;
- suppression de l’avertissement de profondeur élevée sous 1.2.31 ;
- maintien des contrôles de cohérence parent-enfant et de branche ;
- ajout des contrôles de revue sur l’ordre de pertinence des mots-clés ;
- compatibilité conservée avec les normes 1.1.0 à 1.2.30.

## 0.4.32 — 4 août 2026

- alignement sur la norme 1.2.30 ;
- WDV-MWK-021 exige le modèle `Quote` et les paramètres anglais `quote`, `authors`, `work`, `issue`, `location`, `publisher`, `place`, `link` et `warnings` ;
- conservation exacte des valeurs documentaires autres que `quote` et `date` ;
- rejet des paramètres français dans les pages anglaises 1.2.30 ;
- rétrocompatibilité maintenue avec les verrous 1.2.27 à 1.2.29.

# Changelog

## 0.4.31 — 4 août 2026

- alignement sur la norme corrective 1.2.29 ;
- validation du modèle français `Citation` et du modèle anglais `Quote` ;
- maintien de la comparaison ordonnée de tous les paramètres verrouillés ;
- inventaire permanent des fonctions du validateur source 0.4.30 ;
- compatibilité conservée avec toutes les révisions antérieures.


## 0.4.30 — 4 août 2026

- alignement sur la norme corrective 1.2.28 ;
- auto-audit des structures et profils actifs relatifs aux citations ;
- contrôle de l’unicité de la source normative 1.2.28 ;
- conservation de tous les contrôles 0.4.29 et de la compatibilité historique.

## 0.4.29 — 3 août 2026

- alignement sur la norme 1.2.27 et le kit 2.15.0 ;
- validation de la présence exacte d’un lien interlangue dans chaque page française rendue et de son absence dans les pages anglaises ;
- ajout de `WDV-MWK-021` pour comparer chaque modèle `Citation` rendu aux verrous français et anglais ;
- conservation obligatoire de tous les paramètres documentaires des citations, traduction limitée à `citation` et `date`, et contrôle de l’avertissement canonique ;
- correction des heuristiques de prédicat et des identifiants alphanumériques dans la détection des données chiffrées ;
- compatibilité conservée avec les normes 1.1.0 à 1.2.26.

## 0.4.28 — 2 août 2026

- alignement sur la norme 1.2.26 ;
- prise en charge des paquets déclarant 1.2.26 sans modification des contrôles éditoriaux ;
- copie normative resynchronisée avec les exigences d’attestation `no_changes`, de sélection stricte, de staging et de suppressions différées ;
- ajout de tests de version, de schéma et d’unicité de la source normative active ;
- compatibilité conservée avec les normes 1.1.0 à 1.2.25.

## 0.4.27 — 2 août 2026

- alignement sur la norme 1.2.25 ;
- prise en charge des paquets déclarant 1.2.25 sans modification des contrôles éditoriaux 1.2.24 ;
- conservation de `manual_review` comme catégorie valide de plan, avec comparaison obligatoire, tandis que son exécution est bloquée par le kit ;
- ajout de tests de version, de schéma et de non-régression sur la sûreté des reprises ;
- copie normative resynchronisée avec la source 1.2.25.

## 0.4.26 — 2 août 2026

- alignement sur la norme 1.2.24 ;
- ajout de `WDV-MWK-020` pour les modèles `{{Lien Wikipédia}}` et `{{Wikipedia link}}` ;
- contrôle des noms, paramètres, langues, articles non vides, paramètres d’affichage redondants et emploi interdit dans les notes `<ref>` ;
- attestations nouvelles dans les revues d’introduction et de résumés ;
- aucune requête réseau et compatibilité conservée avec les normes antérieures.


## 0.4.25 — 2 août 2026

- alignement sur la norme 1.2.23 ;
- contrôle de la minuscule initiale de `sujet-complet` et `complete-topic` ;
- attestations obligatoires sur le choix d’un sujet nominal conventionnel ;
- extension de `WDV-DOC-004` aux pages Argument et à la vidéographie, avec refus de `auteur=site` après seconde vérification ;
- compatibilité conservée avec les normes antérieures.


## 0.4.24 — 1er août 2026

- alignement sur la norme 1.2.22 ;
- réactivation bloquante de `WDV-EDT-001` lorsque plus de 10 % des titres affichés copient exactement les titres canoniques dans une langue ;
- attestations de concision obligatoires dans le registre individuel ;
- justification spécifique obligatoire pour chaque identité exacte conservée ;
- maintien de `WDV-EDT-021`, `WDV-EDT-022` et de la compatibilité 1.1.0–1.2.21.

## 0.4.23 — 1er août 2026

- alignement sur la norme 1.2.21 ;
- conservation de `WDV-EDT-022` pour les corpus 1.2.20 et 1.2.21 ;
- correction des identifiants de traçabilité du placement (`GR-048` à `GR-050`) ;
- tests renforcés sur les structures réelles des arêtes et sur la non-rétroactivité ;
- compatibilité conservée avec les normes 1.1.0 à 1.2.20.


## 0.4.22 — 1er août 2026

- alignement sur la norme 1.2.20 ;
- ajout du contrôle bloquant `WDV-EDT-022` ;
- contrôle d’un registre couvrant toutes les occurrences actives ;
- tests renforcés pour empêcher la promotion au niveau 1 d’objections ciblées et d’exemples spécialisés ;
- compatibilité conservée avec les normes 1.1.0 à 1.2.19.

## 0.4.21 — 1er août 2026

- alignement sur la norme 1.2.19 ;
- ajout de `WDV-EDT-021` pour les titres affichés manifestement réduits à un groupe nominal ;
- ajout des attestations bilingues obligatoires de complétude propositionnelle et d’intelligibilité dans la revue individuelle ;
- compatibilité conservée avec les normes 1.1.0 à 1.2.18 sans activation rétroactive ;
- aucune écriture distante.


## 0.4.20 — 1er août 2026

- maintien de tous les contrôles 0.4.19 ;
- correction de l’exemple anglais de la norme active, qui ne montre plus `wikipedia-articles` vide ;
- ajout d’un test de non-régression sur les squelettes Débat/Debate actifs ;
- copie normative resynchronisée octet par octet.

## 0.4.19 — 1er août 2026

- alignement sur la norme 1.2.18 ;
- ajout de `WDV-DOC-007` pour la virgule canonique entre auteurs ;
- refus du point-virgule, des virgules mal espacées et de la virgule pleine chasse sous 1.2.18 ;
- compatibilité historique conservée jusqu’à 1.2.17.


## 0.4.18 — 1er août 2026

- alignement sur la norme 1.2.17 ;
- ajout de `WDV-MWK-019` pour l’article Wikipédia obligatoire ;
- interdiction des paramètres de débats connexes dans les sorties 1.2.17 ;
- ajout de `WDV-DOC-006` contre les tableaux JSON dans `auteurs`/`authors` ;
- compatibilité des révisions antérieures conservée.

## 0.4.17 — 31 juillet 2026

- alignement sur la norme 1.2.16 et le kit 2.2.0 ;
- ajout des schémas d’état publié, de migrations, de plan et de reçu de reprise ;
- ajout de `validate-plan`, strictement local et en lecture seule ;
- contrôles WDV-RMT-001 à WDV-RMT-006 sur l’intégrité et la sécurité des plans distants ;
- aucune connexion ni écriture MediaWiki dans le validateur.

## 0.4.16 — 31 juillet 2026

- chemins de paquet absolus rendus indépendants du dossier courant ;
- aucun fragment de chemin absolu local n’est conservé dans les rapports ;
- compatibilité maintenue avec les normes 1.1.0 à 1.2.15 ;
- alignement des métadonnées avec le kit 2.1.17.

## 0.4.15 — 31 juillet 2026

- alignement sur la norme 1.2.15 ;
- conservation de tous les contrôles du validateur 0.4.13 ;
- prise en charge des paquets déclarant 1.2.15 ;
- copie normative synchronisée avec la correction séparant le nom du ZIP du `debate_id` interne.

## 0.4.13 — 30 juillet 2026

- alignement sur la norme 1.2.13 ;
- copie normative mise à jour pour le dossier unique `incoming/` et la sélection des ZIP par identifiant ;
- compatibilité conservée avec les normes 1.1.0 à 1.2.12 ;
- aucun changement des contrôles de contenu par rapport à 0.4.12.

## 0.4.12 — 30 juillet 2026

- alignement sur la norme 1.2.12 et le kit 2.1.12 ;
- rapports portables : `package_root` ne conserve plus de chemin absolu ;
- compatibilité maintenue avec les normes 1.1.0 à 1.2.11 ;
- copie normative et exemples actifs mis à jour.


## 0.4.11 — 30 juillet 2026

- alignement sur la norme 1.2.11 ;
- ajout du contrôle bloquant `WDV-MWK-018` ;
- détection des séquences `}}` suivies d’un ou plusieurs retours à la ligne puis de `{{`, avec espaces ou tabulations facultatifs ;
- forme canonique exigée : `}}{{` ;
- compatibilité maintenue avec les normes 1.1.0 à 1.2.10.

## 0.4.10 — 30 juillet 2026

- alignement sur la norme 1.2.10 ;
- remplacement du modèle générique `Référence`/`Reference` par des notes d’introduction rédigées directement ;
- refus de tout modèle MediaWiki dans le corps d’une note développée d’introduction ;
- contrôle des dates machine dans le texte direct des notes ;
- compatibilité maintenue avec les normes 1.1.0 à 1.2.10.

## 0.4.9 — 30 juillet 2026

- alignement sur la norme 1.2.9 ;
- refus des dates documentaires au format ISO machine, sans toucher aux dates de création ;
- contrôle du modèle générique `Référence`/`Reference` dans les introductions ;
- minimum de deux notices dans chacun des neuf paramètres documentaires de Débat/Debate ;
- contrôle de l’usage des acronymes courants déclarés dans `sujet-complet`/`complete-topic` ;
- compatibilité maintenue avec les normes 1.1.0 à 1.2.9.

## 0.4.8 — 29 juillet 2026

- alignement sur la norme 1.2.8 ;
- contrôle bloquant de l’ordre alphabétique des rubriques et sections par langue ;
- contrôle bloquant de la majuscule initiale de `sujet` et `topic` ;
- détection heuristique bloquante des formes interrogatives dans `sujet-complet` et `complete-topic` ;
- extension des registres de revue à la précision des rubriques, à la profondeur documentaire et à la force expressive ;
- ajout de 1.2.7 et 1.2.8 à la condition de schéma exigeant les contrôles éditoriaux ;
- auto-audit des étiquettes de provenance, des chemins normatifs et de la révision des exemples actifs ;
- compatibilité maintenue avec les normes 1.1.0 à 1.2.8.

## 0.4.5 — 28 juillet 2026

- alignement sur la norme 1.2.5 ;
- suppression du minimum automatique d’un appel `<ref>` par introduction ;
- maintien de l’interdiction des balises `<references />` et du contrôle de la revue humaine.
