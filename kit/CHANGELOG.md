# Changelog

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
