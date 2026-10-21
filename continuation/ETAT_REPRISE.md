# Reprise de la version 2 vérifiée — 21 octobre 2026

**Traduction documentaire en cours ; ni validation finale ni publication wiki.**

L'archive fournie a exactement l'empreinte
`b317df79f35b047af2bdead55c5adbdb33c835fae528ed69f0de78e5d8332eda`.
Elle reste immuable sous `/workspace/output/cannabis_traduction_2026-10-21_verifiee/`
et sur la branche de données `translation/cannabis-en-20261021-verifiee`.
Sa structure réelle commence directement par `data/`, `pages/` et `provenance/` ;
il n'y a pas de sous-dossier `corpus/` dans ce ZIP.

## Travail réalisé pendant cette reprise

- Lecture des trois fichiers de reprise et des règles du dépôt au commit main
  `0ab6e46f62f76490a81431b75e02371df08ebc28`. Copies antérieures préservées.
- Vérification des 339 empreintes de livraison et de tous les fichiers français
  contre l'archive française originale. Les 153 pages et leurs révisions concordent.
- Correspondance par titre FR, révision et empreinte : les 152 identifiants
  d'arguments diffèrent de ceux du build natif déjà présent. La table est dans
  `identity-map.json`. Les identifiants de build ne sont pas encore des IDs scellés.
- Copie anglaise de travail sous `working/`, dérivée exclusivement de la version 2.
  Elle conserve les 149 Quote, 32 résumés, 120 absences, 170 relations comprenant
  les 13 racines et les deux passages A0037/A0116.
- Six remplacements de références : deux dans l'introduction (versions anglaises
  réelles Service Public et Santé Canada), quatre liens Wikipédia dans des résumés.
  Le texte des résumés est inchangé hors ces liens et leurs libellés documentaires.
- Cinq sources sélectionnées après consultation : RAND, comité canadien de 2024,
  rapport Portugal 2019, fiche Service Public anglaise datée et synthèse NIDA.
  Registre partiel `sources_en_working.partial.json`, contrôlé par le validateur
  documentaire du kit. Ajouts ou localisations documentaires sur 19 pages.
- Requêtes bibliographiques indépendantes pour les 153 pages et requêtes de
  découverte de noms pour les 152 arguments, avec réponses et empreintes.
  Le premier passage avait rencontré la limite Crossref HTTP 429 ; les requêtes
  concernées ont été reprises avec la cadence annoncée d'une requête par seconde.
  Tous les résultats sont des **candidats** : ni clôture documentaire, ni nom
  consacré ajouté automatiquement, ni preuve d'absence d'édition anglaise.
- Inventaire de consultation des sources des 149 citations : 14 correspondances
  textuelles intégrales observées dans les pages consultées ; une quinzième
  correspondance (Q117) retrouvée dans une archive de mars 2014, avec Didier Jayle
  explicitement crédité. Une correspondance textuelle n'atteste pas à elle seule
  l'authenticité complète de l'attribution ou la vérité de l'affirmation.
- 163 contrôles d'intégrité sur la copie de travail. Ce sont des contrôles de
  transport et de conservation, pas une convergence sémantique officielle.

## État réseau réellement constaté

`environment_status` : révision 31, configuration HTTP `unrestricted`, état
`unknown`. Les consultations bornées EUDA Portugal, Santé Canada et Service
Public anglais répondent effectivement HTTP 200. L'ancien blocage de ces deux
sources n'est donc plus reproduit. D'autres limitations persistent selon la
source : challenges Le Monde (HTTP 200 sans article), CONNECT 403 pour plusieurs
sites, pages introuvables et API du wiki anglais HTTP 403.

## Problème natif identifié et corrigé séparément

Le code main ne transporte que les modèles Citation et peut de nouveau omettre
les deux passages éditoriaux. Le défaut a été reproduit avec les deux textes
réels, sans création de page finale ni écriture distante.

Correctif : branche `fix/preserve-interquotation-prose`, commit
`cc63562fc383d9ea9c003a69cf7e409ab89a12cf`, PR **en brouillon** :
https://github.com/wikidebates/wikidebia/pull/9

Le correctif transporte `citation_passages` dans les verrous français et anglais,
conserve les ancrages, exige traduction et revue explicites, inclut ces textes
dans l'empreinte sémantique et réinsère la prose dans les rendus FR/EN. Il refuse
les anciens verrous qui l'omettaient. Tests kit, validateur, auto-audit et
22 tests de déploiement réussis localement ; 14 régressions ciblées passent.
Les deux passages réels ont été projetés par le rendu corrigé, à leur position,
sans citation perdue. **Aucune fusion dans main n'a été effectuée.**

`native-import.pending.json` fournit un raccord sans perte : 153 pages,
149 identités de citations et les deux passages relus séparément. Ce fichier
est une préparation d'intégration, pas un verrou natif ou un reçu officiel.
Deux sous-paramètres positionnels vides, ignorés par l'extracteur natif, sont
consignés sans modification de la provenance de livraison.

## Ce qui reste ouvert

1. Terminer la sélection et la lecture documentaire par page à partir des
   résultats enregistrés. Aucun des 153 lots documentaires n'est déclaré clos.
   Les métadonnées Crossref et titres de résultats ne prouvent ni langue,
   équivalence de portée, lecture intégrale, édition anglaise ni nom consacré.
2. Authentifier les citations et éditions restantes. Le lien actuel Q117 mène
   à une page de jeux d'argent, mais son texte historique est retrouvé ; le
   lien de Quote reste inchangé selon le contrat du kit, l'archive est dans le
   dossier de vérification. Q120 est déjà abrégée dans la source française par
   rapport au texte CNN : préciser l'écart hors citation, sans le corriger
   silencieusement. Q063, Q064, Q069 et Q103 exigent une attention particulière
   sur les titres et attributions exacts ; une recherche infructueuse ne
   démontre pas une fabrication.
3. Traiter les références françaises encore présentes dans A0014 (modèle Appel),
   A0052 (titre d'ouvrage français), A0106 (renvoi à Costentin) et A0143
   (Croix-Bleue). Ne pas inventer de contrepartie anglaise ni retirer un passage.
   Les métadonnées françaises des Quote demeurent exactes et doivent le rester.
4. L'image `World-cannabis-laws.png` existe sur Commons, mais sa fiche la classe
   parmi les cartes contestées et sa dernière version indiquée date de 2024.
   Son existence ne valide pas l'actualité géopolitique de la carte en 2026.
   Le miroir PeerTube consulté annonce une licence inconnue et ne démontre pas
   l'identité du créateur officiel ; aucune attribution validée n'est inventée.
   Les débats connexes restent non vérifiés, donc non ajoutés.
5. Reprendre le vrai workflow natif de conservation historique : revue du
   graphe, promotion, workspace éditorial, verrous français, puis import des
   traductions existantes via la table d'identité. Le build actuel est encore
   `graph_draft`, sans workspace Work ni verrous français finalisés ; le
   préflight natif le signale. Ne pas fabriquer les statuts et empreintes.
   Le correctif de transport de prose doit être disponible dans le code utilisé.
6. Achever les revues anglaises, les contrôles complets et deux passes
   sémantiques réellement effectuées sur la même empreinte finale. Aucun reçu
   de convergence officiel n'est déclaré à ce stade.

## Conservation et reprise pratique

La livraison V2 et ses audits restent des pièces historiques immuables. Son
lecteur HTML montre la version 2 ; la copie documentaire courante est sous
`working/pages/en/` et `working/lecture_integrale_en.wiki`. Le manifeste de travail
et `documentary-changes.json` donnent les nouveaux textes et leurs empreintes.
Le snapshot français n'a pas été réécrit ; aucun résumé ajouté ni aucune citation
supprimée ou modifiée. Aucune date de création anglaise n'a été choisie.

Les corps des consultations restent localement sous `research/responses/`.
GitHub conserve les URL, dates, empreintes, observations et notices utiles,
ainsi que les scripts de reprise ; les pages web intégrales ne sont pas copiées
sur cette branche. Les futurs relecteurs peuvent refaire les consultations.

Ne pas fusionner la branche de données dans main. Ne pas utiliser le relais
français pour l'anglais et ne jamais fusionner `wiki-fr-publication` dans main.
Aucune page wiki et aucune configuration d'environnement n'ont été publiées.
