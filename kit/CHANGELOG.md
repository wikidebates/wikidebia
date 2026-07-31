# Changelog

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
