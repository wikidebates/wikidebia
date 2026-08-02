# Changelog normatif

## 1.2.22 — 1er août 2026

- le titre affiché doit désormais remplir une fonction de lecture réellement distincte du titre canonique ;
- toute identité exacte devient exceptionnelle et doit être justifiée individuellement dans chaque langue ;
- le taux d'identité est plafonné à 10 % des arguments actifs par langue ;
- ajout des exigences `TTL-014` et `VAL-030` ;
- réactivation bloquante de `WDV-EDT-001` pour les corpus 1.2.22 ;
- conservation de `WDV-EDT-021` et `WDV-EDT-022` ;
- alignement recommandé : validateur 0.4.24 et kit 2.2.8.

## 1.2.21 — 1er août 2026

- correction de la collision de traçabilité qui réutilisait à tort `GR-045`, `GR-046` et `GR-047` ;
- attribution des identifiants non ambigus `GR-048`, `GR-049` et `GR-050` aux exigences de placement ;
- conservation intégrale des critères de niveau 1 et de subordination introduits en 1.2.20 ;
- aucun changement de graphe ni de contenu imposé aux corpus 1.2.20 ;
- alignement recommandé : validateur 0.4.23 et kit 2.2.7.


## 1.2.20 — 1er août 2026

- le niveau 1 est réservé aux réponses directes, autonomes et structurantes à la proposition du débat ;
- les objections ciblées, preuves secondaires, exemples, interprétations particulières, doctrines instanciées et précisions techniques sont subordonnés à leur meilleure cible immédiate ;
- ajout d’un registre de placement couvrant toutes les occurrences actives ;
- ajout des règles de placement et du contrôle `VAL-029` ; une collision d’identifiants de catalogue, corrigée en 1.2.21, subsistait dans cette livraison ;
- ajout du contrôle `WDV-EDT-022` dans le validateur 0.4.22 ;
- alignement recommandé : validateur 0.4.22 et kit 2.2.6.

## 1.2.19 — 1er août 2026

- le titre affiché devient obligatoirement une proposition argumentative complète et intelligible ;
- les simples groupes nominaux, thèmes et étiquettes doctrinales sont interdits ;
- le contexte d’affichage peut raccourcir le cadrage mais ne peut fournir un prédicat ou une conclusion absents ;
- la revue individuelle bilingue atteste la complétude de la proposition et l’intelligibilité de l’argument ;
- ajout des exigences `TTL-013` et `VAL-028` et du contrôle `WDV-EDT-021` ;
- alignement recommandé : validateur 0.4.21 et kit 2.2.5.

## Maintenance 1.2.18 — 1er août 2026

- correction du squelette anglais afin que `wikipedia-articles` ne soit jamais montré vide ;
- ajout d’un contrôle permanent de cohérence des exemples actifs ;
- alignement recommandé : validateur 0.4.20, kit 2.2.4.

## 1.2.18 — 1er août 2026

- séparateur canonique des auteurs : virgule suivie d’une espace ;
- refus du point-virgule, des virgules mal espacées et de la virgule pleine chasse dans les sorties générées ;
- compatibilité historique conservée pour les paquets déclarés sous 1.2.17 ;
- alignement avec le validateur 0.4.19 et le kit 2.2.3.


## 1.2.17 — 1er août 2026

- `articles-Wikipédia` et `wikipedia-articles` deviennent obligatoires et non vides, avec au moins un titre exact vérifié ;
- `débats-connexes` et `related-debates` sont interdits dans les sorties générées ;
- les tableaux JSON d’auteurs sont convertis en texte MediaWiki et leur sérialisation littérale est bloquée ;
- la publication ordinaire devient non interactive tout en conservant la vérification automatique de l’empreinte du plan ;
- alignement recommandé : validateur 0.4.18, kit 2.2.1.

## 1.2.16 — 31 juillet 2026

- distinction normative entre publication initiale et reprise ;
- état publié signé par débat et langue ;
- plan complet `create`, `skip`, `update`, `move`, `redirect`, `delete`, `manual_review`, `blocked` ;
- mises à jour protégées par révision/empreinte et contrôle de concurrence ;
- protection absolue des modifications humaines ;
- suppressions attestées, idempotentes et exécutées après vérification du nouveau graphe ;
- droits MediaWiki vérifiés avant écriture, sessions linguistiques séquentielles ;
- schémas, validation locale, reçus et commandes de reprise alignés sur le kit 2.2.0.

## 1.2.15 — 31 juillet 2026

- correction de la contrainte 1.2.13 qui imposait à tort l’égalité entre le nom du ZIP et `manifest.debate_id` ;
- sélection automatique d’un ZIP unique quel que soit son nom ;
- sélection exacte par nom de fichier lorsqu’il y a plusieurs ZIP ;
- `manifest.debate_id` déclaré comme identité autoritative du corpus ;
- compatibilité directe avec les anciennes archives portant des suffixes descriptifs ou une date.

## 1.2.13 — 30 juillet 2026

- dossier unique `incoming/` pour les archives de débats ;
- sélection automatique lorsqu’un seul ZIP est présent ;
- sélection obligatoire par identifiant lorsqu’il y en a plusieurs ;
- suppression de toute obligation de suffixe `release_ready` dans le nom du ZIP ;
- correspondance bloquante entre `<identifiant>.zip` et `manifest.debate_id`.

## 1.2.11 — 30 juillet 2026

## 1.2.12 — 30 juillet 2026

- publication d’un paquet `release_ready` en une commande, avec cinq portées canoniques ;
- ordre Débat/Debate puis Argument imposé dans chaque langue ;
- mise à jour atomique en une commande, sauvegarde des versions précédentes et vidage de `updates/` ;
- dépôt Git/GitHub des seules sources nécessaires ;
- exclusion des secrets, corpus, archives, entrées, plans et journaux ;
- déplacement des fichiers Pywikibot dans `private/pywikibot/` ;
- interdiction de conserver le chemin absolu de l’installation dans les fichiers persistants ;
- alignement recommandé : validateur 0.4.12 et kit 2.1.12.


- interdiction de tout saut de ligne ou espace entre deux modèles MediaWiki adjacents ;
- forme canonique obligatoire `}}{{` ;
- ajout de l’exigence automatique `MW-025` et du contrôle `WDV-MWK-018` ;
- préflight identique dans le kit 2.1.11 ;
- maintien intégral des règles 1.2.10.

## 1.2.10 — 30 juillet 2026

- suppression du modèle générique `Référence`/`Reference` dans les notes d’introduction ;
- rédaction directe du contenu documentaire dans `<ref>…</ref>` ;
- refus de tout modèle MediaWiki dans le corps d’une note développée d’introduction ;
- maintien des références nommées et de leur réutilisation autofermante ;
- maintien de toutes les autres règles 1.2.9.

## 1.2.9 — 30 juillet 2026

- dates documentaires complètes en langage naturel, dates de création inchangées au format machine ;
- modèle générique `Référence`/`Reference` obligatoire dans les appels inline des introductions ;
- au moins deux références dans chacun des neuf paramètres documentaires des pages Débat/Debate ;
- usage des acronymes courants dans `sujet-complet`/`complete-topic` ;
- publication des pages françaises autorisée avant la création des pages anglaises lorsque les titres anglais sont verrouillés dans le registre.

## 1.2.8 — 29 juillet 2026

- déclaration de toutes les étiquettes de provenance utilisées par les 320 exigences ;
- alignement des exemples actifs sur la révision 1.2.8 et correction de la langue de l’exemple anglais ;
- correction de la condition de schéma applicable aux paquets 1.2.7 et ultérieurs ;
- renforcement de l’auto-audit pour empêcher ces régressions ;
- aucune modification des exigences éditoriales 1.2.6.

# Changelog normatif

## 1.2.7 — 29 juillet 2026

- correction de tous les alias et chemins de provenance absents ;
- signalement explicite des sources d’origine non distribuées séparément ;
- correction des chemins historiques vers la norme 1.1.9 ;
- nettoyage de la matrice de traçabilité ;
- alignement recommandé : validateur 0.4.7 et kit 2.1.7 ;
- aucune modification des règles éditoriales 1.2.6.

## 1.2.6 — 29 juillet 2026

- tri alphabétique obligatoire des rubriques françaises et sections anglaises, indépendamment dans chaque langue ;
- majuscule initiale obligatoire pour `sujet` et `topic` ;
- `sujet-complet` et `complete-topic` reformulés comme compléments non interrogatifs des en-têtes de page ;
- principe explicite « préférer la précision à l’exhaustivité » pour les rubriques des pages de débat ;
- richesse documentaire proportionnée à l’abondance de la littérature, avec revue séparée des trois familles documentaires sans quota universel ;
- force expressive des résumés rendue obligatoire et attestée par un extrait réel de chaque résumé ;
- alignement recommandé : validateur 0.4.6 et kit 2.1.6.

## 1.2.5 — 28 juillet 2026

- suppression de tout minimum global ou par sous-partie pour les appels `<ref>` des introductions ;
- clarification : les références inline sont exigées uniquement pour les affirmations factuelles qui nécessitent une attribution ;
- correction du validateur afin qu’une introduction conceptuelle sans affirmation factuelle externe puisse être conforme sans appel inline ;
- droit d’exécution restauré pour le lanceur de tests du validateur ;
- maintien de toutes les règles génériques et de l’interdiction des balises `<references />`.

## 1.2.4 — 28 juillet 2026

- remplacement de la checklist d’introduction issue d’un corpus pilote par une architecture fonctionnelle applicable à tous les débats ;
- définition obligatoire du sujet, du sens de la question, des repères historiques et actuels pertinents, des connaissances préalables et des enjeux ;
- suppression des minima universels de cinq sous-parties et vingt références ; les minima éventuels sont locaux et justifiés ;
- registre bilingue obligatoire de revue des introductions ;
- contextualisation obligatoire de toute sous-partie technique ;
- retrait des exemples, identifiants et configurations propres aux corpus pilotes dans les composants génériques actifs ;
- alignement recommandé : validateur 0.4.4 et kit 2.1.4.

## 1.2.3 — 28 juillet 2026

- remplacement du test sur sous-page utilisateur par un test direct de la page Débat française canonique ;
- création `createonly` de cette page comme première écriture distante ;
- blocage si la page Débat existe déjà au moment du plan ou de l’écriture ;
- reçu signé lié au titre canonique, au fichier local, au contenu et à la révision créée ;
- revérification de la révision courante avant toute autre page ;
- alignement recommandé : validateur 0.4.3 et kit 2.1.3.

## 1.2.2 — 28 juillet 2026

- intégration complète du workflow interlangue direct dans les documents actifs ;
- correction des squelettes et listes de contrôle qui conservaient encore l’ancien ajout tardif ;
- retrait des constantes propres à un corpus pilote de la norme générique ;
- manifestes SHA-256 exhaustifs et compteurs documentaires reproductibles ;
- portées `wikicode` et `editorial` obligatoires avant publication ;
- reçu de test utilisateur signé et revérifié à distance avant toute écriture canonique ;
- alignement recommandé : validateur 0.4.2 et kit 2.1.2.

## 1.2.1 — 28 juillet 2026

- reformulation de la règle des titres canoniques autour de l’autonomie référentielle, indépendamment de la nature du référent ;
- distinction explicite entre le nom de page autonome et le titre affiché pouvant exploiter son contexte immédiat ;
- emploi obligatoire des parenthèses pour les incises explicatives de la prose française, à la place des tirets cadratins appariés ;
- ajout des contrôles `WDV-EDT-016` révisé et `WDV-MWK-015`.

## 1.2.0 — 28 juillet 2026

- `{{Lien interlangue}}` devient le sous-modèle unique de toutes les pages françaises, débat compris ;
- les liens français sont intégrés dès la première génération, avant la création ultérieure des pages anglaises ;
- les titres anglais sont verrouillés avant la production française ;
- suppression de toute génération de `<references />` ;
- la page Debate anglaise utilise `topic` et `complete-topic` et interdit `type` ;
- les pages de débat utilisent exclusivement des sources dans leur langue ;
- les pages Argument préfèrent l’équivalent officiel dans leur langue ;
- la bibliographie de débat privilégie les ouvrages fondamentaux et synthèses larges ;
- les métadonnées sitographiques redondantes sont interdites et l’auteur peut être omis ;
- les titres canoniques doivent nommer explicitement leurs référents.

# Changelog normatif 1.1.9

- la première phrase doit développer le titre au lieu de le répéter ou de le paraphraser étroitement ;
- les exemples, ordres de grandeur et chiffres sont facultatifs et ne sont ajoutés que lorsqu’ils éclairent réellement le raisonnement ;
- toute donnée chiffrée fait l’objet d’une vérification documentaire humaine explicite ;
- un style ferme, imagé et légèrement mordant est admis, sans sarcasme, caricature, militantisme ni slogan mécanique ;
- le registre de revue bilingue atteste ces décisions page par page ;
- le validateur 0.3.1 ajoute `WDV-EDT-014` et `WDV-EDT-015`.

Toutes les exigences 1.1.8 restent actives sauf contradiction explicite ci-dessus.

## Historique 1.1.8

- style encyclopédique grand public obligatoire pour les résumés ;
- idée principale annoncée dès l'ouverture ;
- phrases de longueur variée et refus des enchaînements universitaires soporifiques ;
- définition immédiate des termes scientifiques ou techniques nécessaires ;
- revue page par page déclarée dans le manifeste ;
- heuristique non bloquante sur la longueur des phrases.

Toutes les exigences 1.1.7 restent actives sauf contradiction explicite ci-dessus.

## Historique 1.1.7

- remplacement des avertissements « généré avec IA / generated with AI » par « généré par IA / generated by AI » ;
- résumés de modification localisés ChatGPT 5.6 ;
- balise de modification obligatoire `chatgpt` ;
- vérification de la révision exacte après écriture, avec normalisation limitée des fins de ligne ;
- migration sûre des pages déjà créées depuis l’état W10.R7.

Toutes les exigences 1.1.6 restent actives sauf contradiction explicite ci-dessus.


## 1.2.23 — 2 août 2026

- minuscule initiale harmonisée pour `sujet-complet` et `complete-topic` ;
- préférence explicite pour un sujet nominal conventionnel ;
- règles auteur/site/page étendues aux pages Argument et à la vidéographie, avec seconde recherche obligatoire en cas d’égalité auteur-site ;
- résumé de modification distant simplifié en « Corrections » ;
- compatibilité du fichier unique de mise à niveau renforcée.
