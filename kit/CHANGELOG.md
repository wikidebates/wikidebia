## 2.15.4 — 4 août 2026

- clarification des métriques du graphe : niveau des occurrences et profondeur en nombre d’arêtes sont désormais distincts ;
- distinction entre niveau minimal maximal des pages uniques et niveau maximal des occurrences réutilisées ;
- séparation des feuilles réelles, des pages sans sortie dans le graphe extrait et des frontières vers un débat détaillé ;
- reclassement des relations ignorées aux frontières comme informations de périmètre, et non comme avertissements ;
- ajout de contrôles d’audit sur les sommes par niveau, les profondeurs, les feuilles et les frontières ;
- clarification du résultat de `corpus-init-from-snapshot` entre occurrences dépliées par chemins et occurrences normatives ;
- extracteur porté à la version 1.0.1 ; norme 1.2.30 et validateur 0.4.32 inchangés.

## 2.15.3 — 4 août 2026

- localisation complète des paramètres du modèle anglais `Quote` ;
- correspondance canonique des noms français vers `quote`, `authors`, `work`, `issue`, `location`, `publisher`, `place`, `link` et `warnings` ;
- conservation exacte des valeurs documentaires autres que `quote` et `date` ;
- blocage des paramètres français ou sans équivalent anglais dans le rendu anglais ;
- tests de non-régression garantissant l’absence de modèles et paramètres français sur le wiki anglais ;
- alignement sur la norme 1.2.30 et le validateur 0.4.32.

# Changelog

## 2.15.2 — 4 août 2026

- alignement sur la norme 1.2.29 et le validateur 0.4.31 ;
- restauration du modèle anglais `{{Quote}}` dans `quotes=` ;
- paramètres documentaires français conservés à l’identique dans le modèle anglais ;
- ajout d’un inventaire permanent des fonctions du bundle source 2.4.0 ;
- aucune suppression des commandes, protections, profils ou tests historiques.


## 2.15.1 — 4 août 2026

- alignement sur la norme 1.2.28 et le validateur 0.4.30 ;
- correction des contradictions actives relatives aux citations ;
- inventaire `doctor` complété pour toutes les commandes du pipeline ;
- restauration des modes exécutables de `wikidebia_graph_extract.py` et `wikidebia_corpus_init.py` ;
- restauration explicite des permissions Unix après extraction ZIP et réparation du staging produit par les gestionnaires antérieurs ;
- ajout de tests permanents de cohérence normative et de non-régression des fichiers historiques.

## 2.15.0 — 4 août 2026

- ajout de `corpus-workspace-close` pour clôturer formellement un Work après exécution distante réussie ;
- vérification de la chaîne signée plan, acceptation, préflight, autorisation, reçu d’exécution et états publiés ;
- refus de clôturer tant qu’une page `pending_delete` ou un état publié incomplet subsiste ;
- validation locale fraîche de `release-copy/` sans nouvelle connexion au wiki ;
- archivage déterministe des preuves de comparaison, revue, exécution, états publiés et libération ;
- échange atomique du corpus actif avec le corpus effectivement publié, avec conservation intégrale du corpus précédent ;
- reçu final de bout en bout et index local des Works terminés ;
- clôture idempotente pour les exécutions mutantes comme pour les attestations `no_changes`.

## 2.14.0 — 4 août 2026

- ajout de `corpus-workspace-plan-execute` avec phases séparées `--prepare` et `--execute` ;
- préflight distant renouvelé, strictement en lecture seule, lié au plan et à l’acceptation signés ;
- contrôle des droits effectifs et relecture de toutes les opérations et pages `skip` avant autorisation ;
- seconde revalidation immédiate avant armement des méthodes d’écriture ;
- autorisation locale signée distincte du plan, de la revue et du préflight ;
- exécution par le moteur existant avec `createonly`, `baserevid`, relecture, états publiés et reçus signés ;
- journalisation explicite des interruptions et des écritures partielles ;
- prise en charge des modes `all`, `no-delete`, `only-delete` et de l’attestation `no_changes`.

## 2.13.0 — 3 août 2026

- ajout de `corpus-workspace-plan-review` pour préparer et finaliser la revue humaine du plan distant ;
- liaison immuable de la revue au plan, à l’inventaire distant, au reçu de comparaison et à `release-copy/` ;
- décision opération par opération, avec note obligatoire pour les déplacements, redirections et suppressions ;
- refus d’approuver tout plan contenant `manual_review` ou `blocked` ;
- production d’un handoff d’acceptation signé sans autoriser ni commencer l’exécution ;
- conservation explicite de `remote_write_authorized=false` et absence totale d’accès distant pendant la revue.

## 2.12.0 — 3 août 2026

- ajout de `corpus-workspace-remote-compare`, strictement en lecture seule ;
- comparaison de `release-copy/` au wiki avec plan signé `create/update/move/redirect/delete/skip/manual_review/blocked` ;
- priorité aux états publiés signés et repli contrôlé sur le snapshot d’extraction français ;
- inventaire distant observé, journal des lectures, validation locale du plan et reçu scellé ;
- aucune vérification de droits d’écriture et aucune mutation MediaWiki pendant cette phase.

## 2.11.0 — 3 août 2026

- ajout de `corpus-workspace-release` pour sceller `rendered-copy/` en corpus local installable ;
- création atomique d’une `release-copy/` distincte et d’un ZIP déterministe sous `.state/corpus-releases/` ;
- manifeste de libération exhaustif, reçu SHA-256 externe et validation postérieure au manifeste ;
- préparation locale de la future comparaison distante sans inventaire réseau ni plan de reprise ;
- maintien explicite de `remote_write_authorized=false` et absence de toute écriture MediaWiki.

## 2.10.0 — 3 août 2026

- ajout de `corpus-workspace-render` pour le rendu déterministe bilingue ;
- création atomique de `rendered-copy/` sans modifier les verrous précédents ;
- ajout direct et unique de `{{Lien interlangue}}` dans chaque page française ;
- absence garantie de lien interlangue dans les pages anglaises ;
- rendu des citations françaises et anglaises depuis les verrous ;
- conservation exacte des paramètres documentaires et contrôle de `Citation traduite par IA` ;
- verrouillage du graphe, génération des manifestes, lots et agrégats, puis validation bilingue complète.


## 2.9.1 — 3 août 2026

- inventaire stable des modèles `{{Citation}}` présents dans le wikicode français importé ;
- conservation exacte de tous les paramètres documentaires et de leur ordre ;
- traduction contrôlée limitée au texte de `citation` et à la forme linguistique de `date` ;
- vérification que la date anglaise désigne exactement la même date que la date française ;
- ajout déterministe de `Citation traduite par IA` dans `avertissements-citation` ;
- concaténation canonique `, Citation traduite par IA` après tout avertissement préexistant, sans doublon ;
- scellement des citations traduites dans `en_content_lock.json` et du contrat de rendu dans `en_translation_lock.json` ;
- aucune génération de page finale et aucune modification des paramètres source.


## 2.9.0 — 3 août 2026

- ajout de `./wikidebia corpus-workspace-translation --prepare|--finalize|--apply` ;
- préparation d’un registre anglais couvrant la page Debate, tous les arguments actifs, le vocabulaire contrôlé et les sources ;
- vérification de l’équivalence des titres, sections, keywords, introductions, résumés et sélections documentaires ;
- contrôle du ratio anglais/français des résumés entre 0,60 et 1,45 ;
- contrôle des limites de 10 % pour les displayed titles identiques et de 25 % pour les jeux exacts de keywords dominants ;
- exigence de deux références anglaises distinctes dans chacun des neuf paramètres documentaires de Debate ;
- scellement SHA-256 de la traduction et confirmation obligatoire avant application ;
- création atomique de `translated-copy/`, sans mutation des verrous français ni du graphe logique ;
- production des verrous anglais, du vocabulaire bilingue et du changeset de traduction ;
- aucune génération de pages MediaWiki finales, aucun accès distant et aucune publication.


## 2.8.0 — 3 août 2026

- ajout de `./wikidebia corpus-workspace-content-review --prepare|--finalize|--apply` ;
- inventaire du sujet, de l’introduction, des articles Wikipédia, des résumés et de la documentation française depuis le wikicode importé ;
- revue formelle des neuf paramètres documentaires de la page Débat, avec au moins deux références distinctes dans chacun ;
- absence de quota documentaire pour les pages Argument, mais cohérence obligatoire entre les sources retenues, leur type et leurs usages ;
- registre documentaire de travail avec vérification de langue, attribution, dédoublonnage et portée ;
- contrôle des résumés : fidélité au nœud, lisibilité grand public, ouverture développée, absence d’auto-objection, force expressive réellement présente et vérification des chiffres ;
- scellement conjoint de la revue et des sources par SHA-256 ;
- conservation de `working-copy/` et `reviewed-copy/`, puis création atomique de `content-reviewed-copy/` ;
- production de `fr_content_lock.json`, des registres compatibles avec les futurs contrôles éditoriaux et d’un changeset de contenu ;
- aucune page finale, aucune traduction, aucun plan distant et aucun accès MediaWiki.

## 2.7.0 — 3 août 2026

- ajout de `./wikidebia corpus-workspace-review --finalize|--apply` ;
- revue formelle page par page des titres canoniques, titres affichés, rubriques et mots-clés français ;
- blocage des collisions de titres, des titres affichés trop copiés et des jeux exacts de mots-clés trop dominants ;
- contrôle d’un vocabulaire français couvrant exactement les usages et attestant la portée inter-débat ;
- scellement SHA-256 de la revue et confirmation obligatoire avant application ;
- conservation intégrale de `working-copy/` et création séparée de `reviewed-copy/` ;
- recalcul explicite de l’empreinte structurelle après correction des titres ;
- production d’un verrou de métadonnées françaises et d’un changeset exhaustif ;
- imports de provenance inchangés, aucune page finale, aucune traduction et aucun accès MediaWiki.

## 2.6.0 — 3 août 2026

- ajout de `./wikidebia corpus-workspace-init <debate_id>` ;
- création atomique d'une copie éditoriale complète sous `.state/editorial-workspaces/<debate_id>/<work_id>/` ;
- conservation stricte et vérification SHA-256 du corpus promu source ;
- inventaire automatique, non correctif, des titres, rubriques et mots-clés français ;
- registres page par page, liste de tâches, vocabulaire de travail et changeset vide ;
- préparation explicite de la traduction anglaise, bloquée jusqu'à validation des métadonnées françaises ;
- aucune génération de wikicode final, aucune traduction et aucun accès MediaWiki dans cette phase.

## 2.5.0 — 3 août 2026

- ajout de `./wikidebia corpus-review-graph --prepare|--finalize` ;
- génération d’une revue globale et d’un registre de placement couvrant chaque occurrence active ;
- empreinte du build préparé et refus de toute modification non revue ;
- validation locale avant et après passage à `graph_validated` ;
- scellement SHA-256 de la décision de revue et de l’empreinte structurelle ;
- ajout de `./wikidebia corpus-promote` avec confirmation explicite de l’empreinte de revue ;
- promotion par renommage atomique, sans repli vers une copie non atomique ;
- refus des cibles préexistantes, liens symboliques, systèmes de fichiers différents et builds contenant des pages finales ;
- reçu externe de promotion sous `.state/corpus-promotions/` et empreinte vérifiée avant/après ;
- aucune génération de pages, aucun verrouillage du graphe et aucune écriture MediaWiki.

## 2.4.0 — 3 août 2026

- ajout de `./wikidebia corpus-init-from-snapshot` ;
- construction déterministe d’un corpus local `graph_draft` depuis un snapshot audité ;
- génération du registre maître, du graphe canonique, des identifiants de nœuds, relations et occurrences ;
- conservation du wikicode source sous `imports/fr/`, sans le déclarer comme sortie normative ;
- provenance par révision, URL, chaîne de redirection et SHA-256 ;
- initialisation des pages françaises et anglaises futures à l’état `pending` ;
- validation automatique des portées structurelles `schema`, `coherence`, `graph`, `files` et `workflow` ;
- vérification intégrale du manifeste SHA-256 du paquet d’extraction, y compris le graphe et le manifeste de snapshot ;
- blocage des collisions de titres après normalisation et des liens symboliques dans les ZIP ;
- confinement de toutes les sorties sous `.state/corpus-builds/` ;
- aucune promotion automatique vers `corpus/` et aucune écriture distante.

## 2.3.0 — 3 août 2026

- ajout de la commande native et strictement en lecture seule `./wikidebia graph-extract` ;
- parcours récursif Débat → arguments principaux → justifications et objections ;
- résolution des redirections, déduplication des pages, calcul des profondeurs, occurrences, réutilisations et cycles ;
- arrêt par défaut aux frontières `débat détaillé` ;
- cache persistant et snapshot complet du wikicode avec provenance SHA-256.

## 2.2.13 — 2 août 2026

- sélection d’archive strictement explicite avec `--archive` ;
- attestation signée des plans entièrement `skip` ;
- nettoyage systématique du staging ;
- conservation des suppressions différées et prise en charge de `no_changes_in_scope`.

## 2.2.12 — 2 août 2026

- blocage effectif des plans contenant `manual_review`, dans le gestionnaire comme dans l’exécuteur ;
- interdiction de produire un reçu ou un nouvel état publié lorsqu’aucune opération exécutable n’a été appliquée ;
- statut explicite `no_changes` pour les plans composés uniquement de `skip` ;
- priorité au corpus installé pour `./wikidebia update IDENTIFIANT` ;
- ajout de `--archive SÉLECTEUR` pour sélectionner explicitement une archive ;
- staging des archives de reprise et garantie qu’un `--dry-run` ne modifie jamais `corpus/` ;
- alignement sur la norme 1.2.25 et le validateur 0.4.27.

## 2.2.11 — 2 août 2026

- alignement sur la norme 1.2.24 et le validateur 0.4.26 ;
- activation de la barrière de validation des liens Wikipédia explicatifs dans les introductions et résumés ;
- ajout des configurations de création 1.2.24 ;
- conservation de la reprise non interactive, du résumé « Corrections », du bundle unique et des contrôles de sûreté.


## 2.2.10 — 2 août 2026

- suppression de la confirmation interactive de `./wikidebia update IDENTIFIANT` ;
- transmission automatique de l’empreinte du plan signé au moteur d’exécution ;
- conservation de `--yes` comme option de compatibilité silencieuse ;
- maintien intégral des contrôles de signature, de révision distante, de droits, de modifications humaines et de suppression sûre ;
- aucune modification de la norme 1.2.23 ni du validateur 0.4.25.

## 2.2.9 — 2 août 2026

- alignement sur la norme 1.2.23 et le validateur 0.4.25 ;
- résumé de reprise par défaut remplacé par « Corrections » ;
- découverte sûre des composants dans un bundle direct ou une archive de livraison enveloppante ;
- test de compatibilité avec un unique ZIP de livraison et avec le gestionnaire antérieur ;
- aucune modification des protections de concurrence et de suppression.


## 2.2.8 — 1er août 2026

- alignement sur la norme 1.2.22 et le validateur 0.4.24 ;
- activation du contrôle de concision effective des titres affichés avant publication et reprise ;
- ajout des exemples de création 1.2.22 ;
- conservation intégrale des protections de publication, reprise, déplacement et suppression sûre ;
- aucune modification des opérations distantes hors validation préalable.

## 2.2.7 — 1er août 2026

- alignement sur la norme 1.2.21 et le validateur 0.4.23 ;
- réparation des exemples de configuration historiques, qui utilisent désormais le kit et le validateur courants tout en exigeant leur norme de corpus ;
- ajout d’un test validant tous les exemples contre le schéma actif ;
- aucune modification des opérations distantes de publication, reprise, déplacement ou suppression.


## 2.2.6 — 1er août 2026

- alignement sur la norme 1.2.20 et le validateur 0.4.22 ;
- maintien du bundle complet unique et de la compatibilité avec les corpus historiques ;
- aucune modification des barrières de publication et de reprise distante ;
- le validateur courant impose désormais le registre de placement des occurrences pour les nouveaux corpus 1.2.20.

## 2.2.5 — 1er août 2026

- alignement sur la norme 1.2.19 et le validateur 0.4.21 ;
- conservation intégrale de la publication, de la reprise distante, des suppressions sûres et du bundle unique ;
- activation du nouveau contrôle éditorial des titres affichés avant publication ;
- aucune modification des plans historiques déjà signés.


## 2.2.4 — 1er août 2026

- maintenance de non-régression sans changement de norme ;
- correction de l’exemple anglais actif `wikipedia-articles` dans les sources normatives livrées ;
- ajout de tests permanents sur les squelettes français et anglais ;
- conservation du bundle complet unique et de toutes les barrières 2.2.0–2.2.3.

## 2.2.3 — 1er août 2026

- rétablissement du bootstrap depuis un seul ZIP complet avec les gestionnaires historiques ;
- retrait de `PACKAGE_RECEIPT.json` des trois ZIP de composants livrés, afin de respecter leur inventaire strict historique ;
- acceptation et vérification d’un reçu facultatif par le gestionnaire courant ;
- test d’intégration du bundle complet avec le gestionnaire 2.1.17 ;
- documentation explicite de la transition `update` vers `upgrade`.

## 2.2.2 — 1er août 2026

- précontrôle du séparateur canonique `, ` entre plusieurs auteurs ;
- refus du point-virgule, des virgules mal espacées et de la virgule pleine chasse pour les corpus 1.2.18 ;
- alignement sur la norme 1.2.18 et le validateur 0.4.19.

## 2.2.1 — 1er août 2026

- suppression de la question interactive de `./wikidebia publish` ;
- transmission automatique de l’empreinte du plan signé ;
- préflight bloquant pour les articles Wikipédia absents ou vides ;
- préflight bloquant pour `débats-connexes` / `related-debates` ;
- préflight bloquant pour les tableaux JSON dans `auteurs` / `authors` ;
- alignement sur la norme 1.2.17 et le validateur 0.4.18.

## 2.2.0 — 31 juillet 2026

- `./wikidebia update IDENTIFIANT` devient la commande de reprise d’un débat déjà publié ;
- l’ancienne mise à niveau des composants devient `./wikidebia upgrade` ;
- état publié et reçus signés par débat et langue ;
- opérations `create`, `skip`, `update`, `move`, `redirect`, `delete`, `manual_review` et `blocked` ;
- détection des modifications humaines avec triple comparaison et absence d’écrasement par défaut ;
- mises à jour avec `baserevid`, revérification de révision et plans signés ;
- retraits calculés depuis l’ancien état publié, protection contre les réutilisations inter-débats et vérification des marqueurs ;
- contrôle global des droits avant la première écriture, notamment `delete` ;
- ordre sûr avec vérification du nouveau graphe avant suppression, idempotence et reprise après interruption ;
- portées `--scope`, `--no-delete`, `--only-delete` et `--dry-run` ;
- quinze scénarios obligatoires plus un test d’inventaire distant signé.

## 2.1.17 — 31 juillet 2026

- restauration complète des exclusions Git sensibles ;
- retrait automatique de l’index des fichiers locaux déjà suivis, sans suppression du disque ;
- contrôle bloquant avant chaque `git add -A` ;
- diagnostic des règles `.gitignore`, des fichiers sensibles suivis et des chemins dangereux non ignorés ;
- push Git non interactif avec message d’authentification clair ;
- ajout de `./wikidebia github-sync` pour reprendre un push après authentification ;
- dépendances d’exécution bornées, dont Pywikibot 11.x.

## 2.1.17 — 31 juillet 2026

- création ou réparation automatique de `.venv/` par le lanceur ;
- installation automatique de Pywikibot et des dépendances d’exécution ;
- ajout de `requirements-runtime.txt` à la racine installée ;
- contrôle de l’environnement Python et des modules par `doctor` ;
- conservation de `.venv/` et de l’état d’installation hors de Git.

## 2.1.15 — 31 juillet 2026

- correction de la sélection automatique d’un ZIP unique dont le nom diffère du `debate_id` interne ;
- le nom du ZIP devient uniquement un sélecteur de fichier, tandis que `manifest.debate_id` reste l’identité autoritative du corpus ;
- prise en charge des anciennes archives portant des suffixes comme `_fr_en_release_ready_repaired_2026-07-31` ;
- affichage explicite du fichier sélectionné et de l’identifiant interne avant la planification ;
- maintien de la sélection exacte par nom de fichier lorsqu’il y a plusieurs ZIP.

## 2.1.13 — 30 juillet 2026

- remplacement de `incoming/debates/` par le dossier unique `incoming/` ;
- suppression de toute convention de nommage `release_ready` pour les ZIP de débats ;
- sélection automatique lorsque `incoming/` contient un seul ZIP ;
- sélection explicite par `./wikidebia publish IDENTIFIANT` lorsqu’il en contient plusieurs ;
- contrôle bloquant de la correspondance entre `<identifiant>.zip` et le `debate_id` du manifeste ;
- migration automatique des ZIP déjà présents dans l’ancien dossier `incoming/debates/`.

## 2.1.12 — 30 juillet 2026

- ajout de la commande portable `./wikidebia publish` qui extrait, valide, planifie, teste et publie un débat en une seule invocation ;
- portées `all`, `fr`, `en`, `fr-debate` et `en-debate` ;
- ordre Débat/Debate puis Argument imposé dans chaque langue ;
- ajout de `./wikidebia update` avec sauvegarde atomique dans `archives/`, vidage de `updates/`, tests et synchronisation Git ;
- déplacement automatique des secrets Pywikibot vers `private/pywikibot/` ;
- ajout de `./wikidebia github-init` et `./wikidebia doctor` ;
- chemins de configuration exclusivement relatifs et installation portable.


## 2.1.11 — 30 juillet 2026

- alignement sur la norme 1.2.11 et le validateur 0.4.11 ;
- aucune modification du protocole de publication 2.1.9 ;
- exemples et contrôles de version actualisés pour les notes d’introduction rédigées directement.

## 2.1.9 — 30 juillet 2026

- alignement sur la norme 1.2.9 et le validateur 0.4.9 ;
- publication française autorisée sans entrée anglaise dans le manifeste, lorsque le titre anglais est verrouillé dans le registre maître ;
- suppression de l’obligation d’inclure la page Débat française dans chaque plan de création ;
- ajout d’une configuration d’exemple française seule.

## 2.1.8 — 29 juillet 2026

- alignement sur la norme 1.2.8 et le validateur 0.4.8 ;
- contrôle préflight de l’ordre alphabétique des rubriques et sections ;
- contrôle de la majuscule initiale de `sujet` et `topic` ;
- refus des formes interrogatives dans `sujet-complet` et `complete-topic` ;
- maintien du test direct de la page Débat française canonique ;
- aucune exigence propre au kit sur le nombre d’appels `<ref>` ;
- 26 tests automatisés réussis.

## 2.1.4 — 2026-07-28

- alignement sur la norme 1.2.4 et le validateur 0.4.4 ;
- le contrôle éditorial du validateur inclut désormais la revue bilingue des introductions ;
- retrait des configurations propres aux corpus pilotes du kit générique ; elles restent dans les corpus concernés ;
- remplacement complet du test sur sous-page utilisateur par le mode `debate-test` ;
- création avec `createonly` de l’unique page Débat française canonique du plan ;
- reçu signé lié au plan, au fichier de débat, au titre canonique et à la révision distante ;
- revérification de la révision courante, du contenu, du résumé et de la balise avant toute autre écriture ;
- blocage si la page Débat existe déjà lors du plan ou si elle change après le test ;
- 21 tests automatisés réussis.

## 2.1.2 — 2026-07-28

- alignement sur la norme 1.2.2 et le validateur 0.4.2 ;
- portées `wikicode` et `editorial` obligatoires ;
- ancien mode de test sur sous-page utilisateur, remplacé par 2.1.4.
