# Vérification de la traduction cannabis — 21 octobre 2026

La première livraison comportait deux passages éditoriaux omis et plusieurs
écarts de traduction. Cette deuxième livraison les corrige. La première archive
et tous ses fichiers restent conservés. Aucune page wiki n’a été modifiée.

## Ce qui a été repris

La comparaison bilingue a porté sur les 153 titres canoniques, les 165 libellés
affichés, l’introduction complète, les 32 résumés, les 149 citations et les
69 entrées de vocabulaire. Elle a été menée par Codex, sans second traducteur
externe. Ce compte rendu ne vaut pas reçu officiel de convergence du kit.

Un vérificateur distinct de l’assembleur et de son premier audit a ensuite
comparé le ZIP fourni par l’utilisateur au wikicode anglais réellement livré.
Il ne se contente pas de relire les compteurs déclarés par l’assembleur.

## Erreurs trouvées et corrections

- **Deux omissions lors de l’assemblage** : le commentaire introduisant
  l’objection à Jean Costentin dans A0037 et la note distinguant dépendance
  et consommation régulière dans A0116 étaient situés entre les modèles
  `Citation`. L’assembleur ne retenait que les modèles. Les deux passages sont
  maintenant traduits et rétablis à leur position d’origine. Les deux citations
  contradictoires d’A0037 étaient déjà présentes ; c’est leur introduction qui
  manquait. Aucune citation ni aucun résumé n’a été ajouté.
- **Lien causal ajouté** : « ne s’accompagne pas d’une hausse » était rendu par
  « does not lead to increased consumption ». Le titre A0012 exprime désormais
  la concomitance de la source, sans conclure à l’absence de causalité.
- **Conséquences subies et cumul** : le titre A0002 et le libellé correspondant
  rétablissent le préjudice effectivement subi ainsi que « prison, casier ou
  les deux », plutôt qu’une simple exposition au risque.
- **Disjonctions** : le « ou » du résumé A0034 et celui de la citation Q050
  sont rétablis.
- **Portée des termes** : la précarité du résumé A0027 est rendue comme des
  conditions de vie précaires ; « abus » est précisé comme consommation
  excessive dans A0025, Q024 et Q139 ; « loi d’exception » est distinguée d’un
  jugement élogieux dans Q016 et Q095.
- **Précisions des citations** : la production est rétablie dans Q082 ; la
  banalisation de Q086 n’est plus transformée en croyance à l’innocuité totale ;
  les séquestrations avec sévices de Q089 ne deviennent pas nécessairement des
  enlèvements avec torture ; « doser » dans Q111 redevient une mesure, plutôt
  qu’une simple détection.
- **Correction éditoriale indue** : Q117 avait remplacé « majorité » par
  « largest share » pour résoudre l’incohérence avec « environ 30 % ». La
  traduction rétablit « majority » et conserve 30 %. L’incohérence appartient
  à la citation française et doit être signalée hors citation, sans la
  réécrire. Les facteurs 14 et 15 de deux citations différentes restent distincts.

Les 18 unités corrigées, avec leurs valeurs avant/après et leurs motifs, sont
consignées dans [le relevé des corrections](reviews/corrections_verification.json).
Les identifiants A0001…A0152 sont locaux à cette livraison, et non des
identifiants autoritatifs d’un corpus Wikidéb’IA.

## Contrôles effectués

- Intégrité CRC du ZIP d’entrée et vérification de ses 159 empreintes déclarées.
- Conservation octet pour octet des 160 fichiers du paquet source.
- Correspondance exacte des 153 pages avec leurs titres français, révisions
  et empreintes sources ; titres anglais uniques et limites techniques vérifiées.
- Préservation des 32 résumés présents et des 120 absences de résumé. Les
  32 rapports de longueur anglais/français restent entre 0,60 et 1,45.
- Comparaison directe des 149 citations rendues : ordre, paramètres,
  auteurs, ouvrages, articles, liens, pages, dates équivalentes et avertissements.
- Vérification spécifique des deux passages hors modèles et de leur position.
- Comparaison des 157 relations entre arguments et des 13 liens racines,
  y compris leur ordre, leurs cibles, leurs libellés et leurs orientations.
- Graphe sans cycle et 228 occurrences dépliées conservées : 13, 79, 89,
  40 et 7 occurrences selon le niveau.
- Sections et mots-clés traduits dans leur ordre source ; titres courts,
  nominaux ou contextuels conservés sous une forme équivalente.
- Conservation des champs documentaires non projetés dans la provenance,
  sans les présenter comme des références anglaises vérifiées.
- Correspondance exacte des 306 colonnes linguistiques du lecteur bilingue
  avec les fichiers français et anglais ; existence des liens locaux ; contrôle
  de la syntaxe JavaScript et du comportement de recherche.
- Contrôle des empreintes de chaque fichier de livraison, des données
  structurées, du texte agrégé, des preuves de revue et de l’archive finale.
- Vérification des deux états Git ; absence de changement suivi dans le dépôt
  initial et dans le worktree de code utilisé pour lire les règles.

Le premier audit de 21 contrôles passait malgré les deux omissions : il
comptait les modèles de citation sans vérifier tout le texte entre eux. Le
nouvel audit ajoute cette vérification à partir du ZIP source. Son résultat
initial est conservé dans `reviews/verification_initiale.json`, et le résultat
de la version corrigée dans `reviews/verification_independante.json`.

## Ce qui reste incomplet

La traduction est une livraison textuelle relue, pas une version validée pour
publication. Les règles du dépôt exigent encore une recherche documentaire
anglaise indépendante par page, la vérification des éditions, des attributions
et des citations, les cibles Wikipédia, les noms consacrés éventuels, les images
et les débats connexes. Les références françaises résiduelles de l’introduction
et de certains résumés restent à traiter.

Le contrôle réseau a été repris : l’environnement, révision 19, applique toujours
une liste de domaines restreinte. Les deux consultations officielles EUDA et
Santé Canada ont de nouveau reçu `Tunnel connection failed: 403 Forbidden`.
Le détail figure dans `reviews/network_recheck.json`. Une fidélité de traduction
ne démontre pas la vérité ou l’actualité des affirmations médicales, juridiques
et statistiques de la source.

L’intégration aux verrous français et anglais et la convergence officielle du
kit ne sont pas réalisées. Les unités listées dans `translation_units.json`
servent à naviguer dans la relecture ; elles ne constituent pas une preuve de
clôture des lots documentaires imposés par le workflow. Aucune date de création
anglaise n’est inventée et aucune initialisation française n’est recopiée.

L’état conservé est donc : **textes traduits et revérifiés, documentation à
finaliser, publication non effectuée**.
