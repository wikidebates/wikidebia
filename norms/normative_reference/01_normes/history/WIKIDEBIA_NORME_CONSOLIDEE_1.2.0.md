# Norme consolidée Wikidéb’IA 1.2.0

**Statut :** source normative active unique  
**Date d’effet :** 25 juillet 2026  
**Domaine :** production, validation et préparation à la publication de débats bilingues français–anglais sous MediaWiki  
**Remplace comme sources actives séparées :** révision 1.0.6, correctif du 23 juillet 2026 et décisions correctives du 25 juillet 2026. Ces documents restent conservés dans `history/` à titre de provenance.

## 1. Autorité et priorité

En cas de contradiction, l’ordre suivant s’applique :

1. décision explicite ultérieure du propriétaire du projet ;
2. présente norme consolidée ;
3. structures et schémas portant la même version ;
4. profils de rendu et workflow portant la même version ;
5. documents historiques et prompts, uniquement comme provenance.

Un audit décrit un état constaté ; il ne crée pas une règle supérieure à une décision normative. Aucune migration vers une version nouvelle ne peut être silencieuse.

## 2. Principes de production

Chaque débat et chaque argument possède une page dédiée. Les relations sont matérialisées par les titres canoniques des pages liées. Le registre maître JSON est la source de vérité des identifiants, titres, relations, occurrences, propriétaires de lots et états de génération.

Les productions française et anglaise doivent être fonctionnellement équivalentes : mêmes nœuds, mêmes relations, mêmes occurrences et même orientation argumentative. Elles peuvent employer une rédaction et une documentation adaptées à chaque langue.

Les sorties générées doivent être prêtes à être relues et importées, sans métadiscours, sans paramètres d’avertissement vides, sans texte extérieur au modèle principal et sans normalisation silencieuse par le validateur.

## 3. Invariants du graphe

Sont verrouillés après validation du graphe :

- `debate_id` ;
- identifiants des nœuds, relations et occurrences ;
- titres canoniques français et anglais ;
- orientation, parenté, ordre et profondeur des relations ;
- occurrence primaire et réutilisations ;
- propriétaires et composition des lots.

Les titres affichés, rubriques, sections, mots-clés, résumés et métadonnées documentaires peuvent être corrigés lorsque le workflow l’autorise. Toute modification d’un champ inclus dans l’objet canonique de l’empreinte structurelle impose un recalcul explicite et la documentation de l’ancienne et de la nouvelle empreinte.

## 4. Titres canoniques et titres affichés

Le titre canonique est le nom de page et la cible de relation. Il est complet, explicite, autonome et non ambigu. Il mentionne le sujet lorsque cela évite une collision avec d’autres débats.

Le titre affiché est une formulation de lecture. Il peut être plus court lorsque le contexte permet une omission sans ambiguïté. Il doit rester grammatical, fidèle et autonome.

Le titre canonique nomme explicitement tout protocole, projet, étude, institution, programme, résultat ou objet singulier dont dépend le raisonnement. Les formulations anaphoriques ou déictiques telles que « ce protocole », « cette étude », « sa valeur » ou « this project » sont interdites lorsqu'elles ne permettent pas d'identifier le référent hors de la branche locale. Le titre affiché peut être plus concis, mais il ne doit pas devenir incompréhensible ou équivoque.

Un titre affiché ne peut jamais être obtenu par une troncature aveugle. Sont notamment interdits :

- les ellipses `...` ou `…` ;
- la suppression d’un article, déterminant ou mot initial nécessaire à la grammaire ;
- un début de titre constitué d’une lettre résiduelle telle que `S ` ou `E ` ;
- une fin sur une préposition, une conjonction ou un connecteur incomplet ;
- les remplacements lexicaux qui créent un doublon, une construction hybride ou un énoncé non idiomatique ;
- la présence accidentelle de mots d’une autre langue, hors noms propres et dénominations officielles.

Lorsqu’une substitution contextuelle est employée pour distinguer titre canonique et titre affiché, elle doit être relue dans la phrase entière. Le titre validé dans le registre doit être reproduit à l’identique dans toutes les relations, pages Débat/Debate, agrégats, projections et fichiers de staging.

### 4.1 Guillemets dans les noms de pages et titres affichés

Le critère est l’accessibilité sur un clavier d’ordinateur ordinaire, sans saisie d’un code Unicode ou d’une combinaison spécialisée. Les deux sites utilisent donc les **guillemets droits doubles ASCII** `"..."` dans les titres canoniques et les titres affichés :

- français : `Le terme "psi" est défini...` ;
- anglais : `The term "psi" is defined...`.

Les guillemets typographiques ou chevrons `« »`, `“ ”`, `„ ”`, `‹ ›` sont interdits dans les noms de pages et titres affichés. L’apostrophe droite ASCII `'` reste utilisée pour les élisions françaises et les contractions ou possessifs anglais ; elle ne remplace pas les guillemets d’une citation principale. Les guillemets droits doivent être équilibrés.

La copie mécanique sans revue est interdite. Chaque titre affiché fait l'objet d'une décision éditoriale page par page, consignée dans un registre de revue. L'identité avec le titre canonique est autorisée lorsqu'elle constitue le meilleur libellé ; aucun quota global de différence ou d'identité n'est normatif.

## 5. Résumés d’arguments

Le résumé expose la version la plus forte du raisonnement porté par le nœud : prémisses, mécanisme, conclusion et portée documentée. Il ne modifie ni l’identité logique, ni l’orientation, ni la force soutenue par les sources.

Le résumé ne doit pas :

- anticiper une objection ;
- se conclure par sa propre réfutation ;
- ajouter une concession destinée seulement à équilibrer le texte ;
- diminuer artificiellement la portée de la proposition ;
- parler de « l’argument », de « la page » ou du « raisonnement présenté ».

Les limites opposables sont portées par les pages d’objections reliées. Une délimitation nécessaire à l’identité de la proposition peut être conservée lorsqu’elle est formulée positivement.

Une revue humaine bilingue est obligatoire avant `release_ready`. Les heuristiques automatiques détectent notamment les concessions finales et le métadiscours, mais ne remplacent pas cette revue.

### 5.1 Style encyclopédique grand public

Le résumé adopte un style encyclopédique destiné à un lectorat non spécialiste. Il présente l'idée centrale dès l'ouverture, puis explique le mécanisme utile à sa compréhension. Il privilégie des phrases courtes ou moyennes, de longueur variée, et évite les enchaînements de propositions longues qui donnent au texte l'allure d'un article universitaire.

Tout terme scientifique, technique, juridique ou philosophique indispensable est défini brièvement lors de sa première occurrence significative dans la page. La définition est intégrée au raisonnement, par exemple : « Le Ganzfeld est un protocole... » ou « Psi désigne... ». Un terme de langue courante n'a pas à être défini artificiellement, et le résumé ne doit pas devenir un glossaire.

La rédaction suit normalement cet ordre :

1. thèse ou idée principale ;
2. explication concrète du mécanisme ;
3. exemple, donnée ou distinction réellement utile ;
4. délimitation indispensable, seulement si elle appartient à l'identité de la proposition.

Les noms d'auteurs, d'études et de méthodes ne précèdent pas l'explication qu'ils doivent éclairer. Ils sont mentionnés uniquement lorsqu'ils ajoutent une information nécessaire. Le résumé n'explique pas tout le dossier : il développe un seul nœud logique avec assez de précision pour être compris seul.

Une revue page par page atteste, pour chaque langue produite : l'annonce directe de la thèse, l'accessibilité au grand public, le rythme des phrases et l'explication des termes techniques nécessaires. Le validateur peut signaler une accumulation de phrases longues, mais ce signal est heuristique et ne mesure ni la qualité logique ni la suffisance des définitions.

Les résumés français et anglais d’un même nœud doivent être substantiellement équivalents : mêmes prémisses principales, mêmes éléments probants décisifs, même conclusion et même portée. Une différence de longueur n’est pas en soi une faute, mais un ratio anglais/français inférieur à 0,60 ou supérieur à 1,45 déclenche un blocage automatique et une reprise humaine.

### 5.2 Ouverture, concrétisation et force expressive

La première phrase du résumé ne répète pas mécaniquement le titre canonique ou le titre affiché. Elle développe immédiatement l’argument en présentant un phénomène concret, une prémisse décisive, un mécanisme causal, une conséquence ou une distinction utile. La thèse doit rester identifiable dès l’ouverture, mais sa simple reformulation ne constitue pas un développement suffisant.

Un exemple concret, un ordre de grandeur ou une donnée chiffrée est ajouté lorsqu’il améliore réellement la compréhension ou renforce la démonstration. Son emploi n’est jamais obligatoire. Un chiffre doit être soutenu par une source documentaire de la page et présenté avec la portée, la population et le contexte nécessaires. Aucun exemple ou chiffre ne doit être ajouté pour donner artificiellement une impression de précision, de variété ou d’autorité.

Le résumé peut adopter un style légèrement mordant, entendu comme une formulation ferme, imagée et convaincue qui fait apparaître clairement la force du raisonnement. Cette fermeté ne doit pas devenir un ton militant, sarcastique ou méprisant. Le texte ne ridiculise pas l’argument adverse, ne prête pas d’intentions aux personnes ou aux institutions et ne transforme pas une proposition discutée en vérité éditoriale incontestable.

Les images explicatives, oppositions de formulation et phrases saillantes sont admises lorsqu’elles clarifient le mécanisme. Elles ne doivent pas devenir des slogans, être répétées mécaniquement d’une page à l’autre ou dépasser ce que permettent le titre, le graphe et les sources.

La revue humaine page par page atteste en outre que l’ouverture développe le titre, que la pertinence d’un exemple ou d’une donnée a été examinée, que tout chiffre a fait l’objet d’une vérification documentaire explicite, et que le ton reste ferme sans devenir polémique.

## 6. Rubriques, sections et mots-clés

Les rubriques françaises autorisées sont : Aménagement, Culture, Droit, Écologie, Économie, Éducation, Éthique, Géopolitique, Histoire, Philosophie, Politique, Psychologie, Religion et spiritualité, Santé, Science, Société, Sport et loisirs, Technologie.

Chaque nœud est classé individuellement. Une à trois rubriques réellement centrales sont normalement utilisées ; une quatrième est exceptionnelle et motivée. Une rubrique peut légitimement être présente sur tous les arguments d'un débat lorsque sa pertinence est démontrée page par page ; sa fréquence locale ne constitue ni une preuve de pertinence ni une anomalie automatique. Les décisions sont consignées dans un registre de revue. Les sections anglaises sont les équivalents conceptuels des rubriques françaises.

Chaque page d’argument reçoit normalement **deux à quatre mots-clés thématiques**. Leur fonction principale est la navigation à l’échelle de l’ensemble du wiki : un clic doit pouvoir rapprocher des arguments relevant de débats différents autour d’un même phénomène, d’une même méthode, d’une même question épistémologique ou d’un même contexte institutionnel.

Un mot-clé doit donc être :

- simple et immédiatement compréhensible ;
- central pour le raisonnement de la page ;
- assez général pour pouvoir être réutilisé dans d’autres débats du wiki ;
- assez précis pour former un regroupement utile ;
- formulé comme un nom, un groupe nominal court, un nom propre ou un acronyme reconnu.

Sont interdits :

- les verbes, adjectifs ou adverbes isolés ;
- les fragments de phrase ;
- les formulations qui résument presque toute la proposition de la page ;
- les détails propres à une étude, une date, un seuil ou un résultat lorsqu’un concept encyclopédique plus stable existe ;
- les synonymes artificiels créés pour rendre les jeux de mots-clés différents.

Un mot-clé thématique comporte normalement au plus quatre mots lexicaux et quarante caractères. Un vocabulaire contrôlé bilingue consigne chaque paire français–anglais, sa définition et, à titre informatif, ses usages dans le corpus courant.

**La fréquence dans un débat particulier n’est jamais un critère d’admissibilité.** Un mot-clé peut n’apparaître que sur un seul argument du débat courant lorsque le concept est suffisamment général pour concerner d’autres arguments du wiki ou d’autres débats. Il n’existe donc ni minimum d’occurrences locales, ni plafond de taille du vocabulaire calculé en proportion du nombre d’arguments du débat.

La réutilisation effective à l’intérieur du débat reste une information utile pour la revue, mais elle ne doit pas conduire à supprimer un thème central ou à le remplacer par un terme artificiellement plus vague. Un même jeu exact dominant plus de 25 % du corpus demeure bloquant, car il signalerait une attribution mécanique et rendrait la navigation peu discriminante.

Les keywords anglais sont des équivalents idiomatiques, dans le même ordre conceptuel. Les pages Débat/Debate utilisent normalement cinq à huit thèmes généraux.

## 7. Documentation et références

### 7.1 Principes communs

Une source possède un identifiant documentaire unique, une notice vérifiable et des usages réciproques cohérents. Les doublons par DOI, ISBN, URL canonique ou clé normalisée sont interdits.

La bibliographie est prioritaire. La sitographie et la vidéographie sont complémentaires. Une page de débat ne remplit pas des quotas : chaque catégorie peut contenir zéro, une ou plusieurs références selon leur apport réel.

### 7.2 Pagination bibliographique

Une page ou plage de pages utilise :

```mediawiki
|page=36-37
```

La valeur ne contient ni `page`, ni `pages`, ni `p.`, ni `pp.`. `localisation=` et `location=` sont réservés aux repères non strictement paginaires : chapitre, section, annexe, numéro ou identifiant d’article.

Une incompatibilité entre la norme et un modèle public est un blocage de publication. Elle ne doit jamais être contournée silencieusement dans le corpus ou le kit.

### 7.3 Dates sitographiques

`date=` contient la date de publication ou de mise à jour substantielle. Une date de consultation n’est jamais placée dans `date=`. Lorsque la date documentaire n’est pas vérifiable, le paramètre est omis. Aucune date ne peut être inventée.

### 7.4 Langue des sources et éditions linguistiques

La langue enregistrée dans le registre documentaire est la langue réelle du contenu cité, et non la langue de la page qui l’utilise. Chaque usage indique séparément la langue de la page. La vérification de langue est explicite.

Les pages Débat et Debate utilisent exclusivement des ressources intégralement disponibles dans leur propre langue, y compris les appels de référence de l’introduction et les listes documentaires structurées. Une page française de débat ne cite donc aucune ressource anglaise ; une édition, traduction, page, version doublée ou sous-titrée officiellement en français constitue une notice française distincte.

Sur une page Argument française, une édition ou traduction française pertinente et vérifiable est toujours préférée lorsqu’elle existe. Une publication scientifique primaire peut rester dans sa langue originale uniquement lorsqu’aucun équivalent français officiel et pertinent n’existe, ou lorsque la ressource étrangère est elle-même l’objet analysé. Cette décision est consignée dans l’usage documentaire. Les titres publiés ne sont jamais traduits artificiellement. La règle symétrique s’applique aux pages anglaises.

Les éditions ou traductions d’une même œuvre partagent un identifiant d’équivalence documentaire. Le validateur bloque l’emploi d’une source étrangère sur une page Argument lorsqu’un équivalent vérifié dans la langue de la page est disponible dans le registre.

### 7.5 Pages Débat / Debate

L’introduction couvre substantiellement les dimensions pertinentes : définition, histoire, institutions, protocoles, résultats, méta-analyses, réplications, biais, contrôles, fraude, théorie, plausibilité, philosophie des sciences et psychologie anomalistique.

À l’état `release_ready`, chaque introduction comporte normalement au moins cinq sous-parties substantielles et chaque page de débat au moins vingt références documentaires au total, sauf justification explicite. Une répartition artificielle d’exactement une référence dans chaque catégorie est interdite.

Chaque sous-partie substantielle de l’introduction contient au moins un appel de référence inline soutenant ses principales affirmations. Les appels français sont placés avant la ponctuation finale ; les appels anglais suivent la convention anglaise. Les balises `<references />` et `<references>` ne sont jamais ajoutées : l’affichage des notes est géré par le wiki. Les mêmes sources peuvent également figurer dans les listes documentaires structurées de la page lorsque l’appel inline attribue une affirmation précise.

### 7.6 Sélection de la bibliographie des pages de débat

La bibliographie d’une page Débat ou Debate constitue une sélection de référence sur l’ensemble de la controverse. Elle privilégie les livres incontournables, monographies, manuels, volumes collectifs, rapports de synthèse et articles de revue réellement panoramiques. Les articles scientifiques consacrés à une expérience, un protocole ou un résultat étroit appartiennent aux pages Argument concernées et ne sont pas accumulés dans la bibliographie générale du débat.

Chaque usage bibliographique du débat indique s’il s’agit d’une œuvre fondatrice ou d’une synthèse large, ainsi qu’une justification de sélection. Une source étroite ou dépourvue de justification est bloquante.

### 7.7 Métadonnées sitographiques

`auteurs=` ou `authors=` n’est émis que lorsqu’une personne ou une organisation est explicitement responsable du contenu. À défaut, le paramètre est omis ; le nom du site n’est jamais recopié mécaniquement comme auteur. La vérification de l’attribution est enregistrée.

Lorsque le titre de la page et le nom du site sont identiques, seul `site=` est conservé. Les triples identiques `page`, `auteurs` et `site` sont interdits.

## 8. Structures MediaWiki actives

### 8.1 Page Débat française

```mediawiki
{{Débat
|sujet=
|sujet-complet=
|avancement=Débat construit
|avertissements-débat=Débat généré par IA
|introduction={{Sous-partie
|titre=
|contenu=
}}
|articles-Wikipédia=
|arguments-pour={{Argument pour
|page=Titre canonique complet
|titre-affiché=Titre affiché
}}
|arguments-contre={{Argument contre
|page=Titre canonique complet
|titre-affiché=Titre affiché
}}
|bibliographie-pour=
|bibliographie-contre=
|bibliographie-ni-pour-ni-contre=
|sitographie-pour=
|sitographie-contre=
|sitographie-ni-pour-ni-contre=
|vidéographie-pour=
|vidéographie-contre=
|vidéographie-ni-pour-ni-contre=
|rubriques=
|mots-clés=
|interlangue={{Lien interlangue
|langue=en
|page=Titre canonique anglais
}}
|date-création=AAAA-MM-JJ
}}
```

Le paramètre `interlangue` est obligatoire dans le fichier français canonique dès sa première génération valide. Il utilise toujours `{{Lien interlangue}}` et vise le titre canonique anglais verrouillé, même si la page anglaise sera créée dans une phase ultérieure. La page anglaise peut donc être momentanément absente du wiki.

### 8.2 Page Argument française

```mediawiki
{{Argument
|avertissements-argument=Argument généré par IA
|résumé=
|références-bibliographiques={{Référence bibliographique
|auteurs=
|article=
|ouvrage=
|volume=
|numéro=
|localisation=
|page=36-37
|édition=
|lieu=
|date=
|lien=
}}
|références-sitographiques=
|références-vidéographiques=
|justifications={{Justification
|page=Titre canonique complet
|titre-affiché=Titre affiché
}}
|objections={{Objection
|page=Titre canonique complet
|titre-affiché=Titre affiché
}}
|rubriques=
|mots-clés=
|interlangue={{Lien interlangue
|langue=en
|page=Titre canonique anglais
}}
|date-création=AAAA-MM-JJ
}}
```

### 8.3 English Debate page

```mediawiki
{{Debate
|topic=
|complete-topic=
|progress=Constructed debate
|debate-warnings=Debate generated by AI
|introduction={{Subsection
|title=
|content=
}}
|wikipedia-articles=
|pro-arguments={{Pro argument
|page=Full canonical title
|displayed-title=Displayed title
}}
|con-arguments={{Con argument
|page=Full canonical title
|displayed-title=Displayed title
}}
|pro-bibliography=
|con-bibliography=
|bibliography=
|pro-webliography=
|con-webliography=
|webliography=
|pro-videography=
|con-videography=
|videography=
|sections=
|keywords=
|creation-date=YYYY-MM-DD
}}
```

### 8.4 English Argument page

```mediawiki
{{Argument
|argument-warnings=Argument generated by AI
|summary=
|bibliography={{Bibliographical reference
|authors=
|article=
|work=
|volume=
|issue=
|location=
|page=36-37
|publisher=
|place=
|date=
|link=
}}
|webliography=
|videography=
|justifications={{Justification
|page=Full canonical title
|displayed-title=Displayed title
}}
|objections={{Objection
|page=Full canonical title
|displayed-title=Displayed title
}}
|sections=
|keywords=
|creation-date=YYYY-MM-DD
}}
```

Les pages anglaises ne contiennent pas de lien interlangue.

## 9. Dates de création

La date de création est une décision de production distincte de la date des sources. Chaque paquet déclare sa date active attendue dans son profil de contrôle ; le validateur compare cette valeur au wikicode, au registre, au manifeste et au staging. Le code générique ne contient aucune date propre à un corpus. Une divergence est bloquante.

Pour le profil local `parapsychologie_science`, la décision corrective reste `2026-07-25` pour toutes les pages canoniques et copies françaises de staging. Les traces historiques W00–W10 conservent leurs dates d’origine.

## 10. Workflow correctif et non-régression

Le cycle correctif autorisé est :

```text
release_ready
  → corrective_in_progress
  → corrective_blocked (si une anomalie subsiste)
  → corrective_in_progress (après reprise)
  → release_ready (validation complète uniquement)
```

Le Work porte le type `corrective_prepublication`. Il crée un instantané initial, des handoffs correctifs nouveaux et une matrice de couverture. Les handoffs historiques ne sont jamais réécrits ; leurs empreintes décrivent l’état d’entrée de leur Work original. Chaque nouvelle reprise ajoute un handoff final propre à sa révision vers W11.

Une seule norme consolidée est active à la racine du dossier `normative/`. Toute version consolidée antérieure est déplacée dans `normative/history/`. Les documents spécialisés — structures, profils, workflow, catalogue d’exigences et matrice de traçabilité — doivent pointer vers la même révision active et ne peuvent conserver une règle remplacée comme règle active.

Le retour à `release_ready` exige :

- zéro erreur bloquante ;
- zéro avertissement non résolu ;
- revue éditoriale humaine enregistrée ;
- cohérence bilingue ;
- manifeste de libération cohérent ;
- preuve de l’absence d’écriture distante ;
- audit de non-régression comparant la norme, le kit, les pages, les invariants, les fichiers et les exigences cumulées ;
- kit de publication produit séparément, inclus dans la livraison complète et non exécuté.

Aucune reprise corrective ne peut supprimer silencieusement une fonction, un contrôle, un test, un rapport, un fichier normatif ou une étape du kit. Une suppression intentionnelle exige une décision explicite, une justification et une trace dans le changelog.

## 11. Validateur

`validate` est strictement en lecture seule. Toute écriture locale dérivée passe par une commande distincte, explicitement demandée, telle que `recalc --write`. Le validateur n’effectue aucune connexion au wiki.

Les contrôles sont répartis entre schémas JSON, cohérence et fichiers, graphe, lots, sources, wikicode, bilinguisme, workflow, contrôles éditoriaux automatisables et revue humaine obligatoire.

La version 0.2.9 conserve les contrôles antérieurs et ajoute des contrôles bloquants pour les appels de référence des introductions, l’unicité de la norme active, la présence du handoff correctif courant et la cohérence de la révision normative. Chaque règle nouvelle possède au moins un test positif et un test négatif lorsque la règle est binaire. Le validateur conserve tous les contrôles des versions précédentes.

Les longueurs indicatives des résumés restent des guides éditoriaux et non des quotas. Une distribution systématiquement courte déclenche une information de revue humaine, sans provoquer de remplissage artificiel. La revue doit confirmer que chaque page demeure autonome, informative et fidèle à un seul nœud.

## 12. Publication W11

Aucune écriture distante n’est autorisée pendant une reprise W10 corrective. Le kit W11 est livré sans exécution et sans secret.

Avant toute publication, W11 doit :

1. exécuter une simulation globale déterministe et signer le plan par SHA-256 ;
2. vérifier en lecture seule la compatibilité réelle des modèles publics ;
3. refuser de poursuivre si un paramètre normatif requis n’est pas accepté ;
4. traiter séquentiellement les phases `fr → en`, les fichiers français contenant déjà leur lien interlangue définitif ;
5. dans les phases française et anglaise, traiter toutes les pages Argument avant la page Débat ;
6. réauthentifier et vérifier l’identité à chaque phase et avant chaque écriture ;
7. utiliser `assert=user` et `assertuser` ;
8. classifier chaque titre distant comme `absent`, `equivalent_existing`, `collision` ou `manual_review` ;
9. ne jamais écraser une page existante par défaut : une page équivalente est ignorée et une collision bloque le plan ;
10. comparer les contenus local et distant par SHA-256 et enregistrer les identifiants de révision ;
11. utiliser `createonly` pour chaque création canonique ; aucune mise à jour interlangue distincte n’est prévue pour un paquet 1.2.0 ;
12. relire chaque page après écriture, vérifier son contenu et enregistrer la nouvelle révision ;
13. s’arrêter sur perte de session, collision, divergence, droits insuffisants ou révision concurrente ;
14. permettre un test isolé sur une seule sous-page non canonique de l’espace utilisateur, puis la relire ;
15. écrire des journaux JSONL privés de simulation, test et import ;
16. reprendre uniquement à partir du couple titre + SHA-256 de contenu et de révisions réelles vérifiées ;
17. refuser l’exécution si le corpus, le validateur, la norme ou le plan ont changé depuis la simulation ;
18. charger pour le test et la publication le fichier de plan signé produit par la simulation, sans le reconstruire silencieusement ;
19. incorporer au plan les empreintes du manifeste, du manifeste de libération et du validateur, puis les revérifier avant toute écriture ;
20. reconnaître comme état de reprise valide une page française déjà identique à son fichier canonique, lien interlangue compris ;
21. exiger avant le mode de publication canonique un reçu machine du test utilisateur, lié au plan signé et revérifié à distance immédiatement avant toute écriture.

Les fichiers d’authentification, cookies, secrets et identifiants privés ne sont jamais inclus dans une archive publique.

## 13. Contrôles propres aux reprises W10.R1 et ultérieures

Le paquet final conserve exactement 222 identifiants, 210 relations, 226 occurrences et 18 lots, ainsi que les propriétaires. Toute modification explicitement autorisée d’un titre canonique est documentée avec l’ancienne et la nouvelle empreinte ; les autres titres canoniques restent verrouillés. Le paquet documente les 446 pages canoniques, les 223 copies françaises de staging, les migrations documentaires et la couverture de toutes les décisions correctives.

Le statut local `release_ready` n’implique pas l’autorisation de publier. Le champ `publication_gate` demeure à `remote_write_authorized=false` jusqu’à la réussite du préflight et du test utilisateur W11.

## 14. Renforcement éditorial cumulatif W10.R2–W10.R7

Avant `release_ready`, le corpus doit présenter :

1. zéro titre canonique ou affiché contenant une ellipse, une troncature grammaticale ou des guillemets non conformes ;
2. zéro lettre initiale résiduelle issue d’une suppression d’article ;
3. concordance exacte de tous les titres affichés entre registre, relations, agrégats et staging ;
4. deux à quatre mots-clés nominaux par page, issus du vocabulaire contrôlé bilingue ;
5. zéro mot-clé français non traduit dans la liste anglaise ;
6. vocabulaire thématique évalué à l’échelle du wiki, sans exigence de répétition dans le débat courant ;
7. revue page par page de la pertinence des mots-clés ;
8. équivalence substantielle des résumés bilingues ;
9. appels de référence inline dans chaque sous-partie des introductions française et anglaise ;
10. maintien de tous les invariants verrouillés du graphe ;
11. recalcul explicite de toutes les empreintes de fichiers et, si nécessaire, de l’empreinte structurelle ;
12. absence totale d’écriture distante ;
13. audit de non-régression des normes, du validateur et du kit W11.

Le paquet déclare dans son manifeste les chemins du vocabulaire contrôlé, du registre individuel, des rapports requis et du handoff correctif courant. Le validateur ne déduit jamais ces chemins d’un sujet, d’un numéro de Work ou d’une rubrique particulière. Il ne peut jamais bloquer un mot-clé au seul motif qu’il n’apparaît qu’une fois dans le débat courant.

## 15. Livrables minimaux d’une reprise prépublication

La livraison complète contient au minimum :

- le corpus bilingue `release_ready` et son reçu ;
- la norme consolidée active et son changelog ;
- le validateur aligné et sa suite de tests ;
- le kit W11 aligné, non exécuté, et ses tests ;
- un paquet de revue des pages ;
- l’audit de non-régression ;
- les reçus SHA-256 de chaque archive.

La présence de ces éléments est vérifiée avant livraison. Leur absence constitue une régression bloquante.


## Addendum 1.1.5 — preuve du test utilisateur W11

Le mode de publication canonique W11 exige un reçu machine du test sur sous-page utilisateur. Ce reçu contient le SHA-256 du plan signé, l'identité vérifiée, le titre non canonique, le SHA-256 du contenu relu, l'identifiant de révision et le statut `passed`. Le mode `publish --execute` refuse de démarrer sans `--user-test-receipt`, si le reçu ne correspond pas au plan courant ou si sa signature interne est invalide.

## Addendum 1.1.5 — revue individuelle

La conformité des titres affichés et des rubriques ne se déduit pas d'un seuil statistique global. Le paquet `release_ready` contient un registre couvrant chaque nœud actif et indiquant la décision sur le titre ainsi qu'une justification non vide pour chacune des rubriques retenues. Aucune rubrique n'est obligatoire, présumée pertinente ou soumise à un traitement spécial.


## Addendum 1.1.7 — généralité des contrôles

Les contrôles éditoriaux sont formulés sur les propriétés choisies par l’IA, et non sur une valeur particulière. Pour chaque nœud actif, le registre de revue contient une justification distincte pour chaque rubrique retenue. Le validateur exige une correspondance exacte entre les clés de justification et les rubriques de la page ; une justification d’une rubrique absente ou l’absence de justification d’une rubrique présente est bloquante.

Les décisions locales — date de création, chemins des rapports, seuils documentaires du profil, Work courant et handoff — sont déclarées dans le manifeste du paquet. Elles ne sont jamais codées en dur dans le moteur générique. Les invariants propres à un corpus peuvent figurer dans une annexe ou un profil local, sans devenir une règle universelle.


## Addendum 1.1.7 — avertissements et publication traçable

Les valeurs actives d’avertissement sont exactement `Débat généré par IA`, `Argument généré par IA`, `Debate generated by AI` et `Argument generated by AI`. Les formulations avec `avec IA` ou `with AI` sont interdites dans les pages actives.

Toute écriture distante produite par le kit W11 emploie un résumé localisé : `Contenu généré par ChatGPT 5.6` en français et `Content generated by ChatGPT 5.6` en anglais. La balise de modification `chatgpt` est obligatoire et doit être déclarée active par le wiki avant toute écriture. Après une écriture, le kit relit la révision exacte renvoyée par l’API et vérifie son contenu normalisé, son résumé et sa balise ; il ne se fie pas uniquement à la dernière révision visible.

## Addendum 1.1.8 — lisibilité des résumés

La norme 1.1.8 rend obligatoire le style encyclopédique grand public des résumés : idée principale annoncée dès l'ouverture, phrases de longueur variée, explication immédiate des termes techniques nécessaires et suppression des développements universitaires qui n'aident pas à comprendre le nœud. Le validateur 0.3.0 ajoute `WDV-EDT-013`, un avertissement heuristique sur l'accumulation de phrases longues, ainsi qu'un contrôle bloquant de la revue humaine page par page. Toutes les exigences 1.1.7 restent actives sauf contradiction explicite.

## Addendum 1.1.9 — ouverture développée, exemples probants et force expressive

La norme 1.1.9 interdit qu’une première phrase se contente de répéter ou de paraphraser étroitement le titre. Elle autorise les exemples et données uniquement lorsqu’ils éclairent réellement le mécanisme et exige une vérification documentaire explicite de toute donnée chiffrée. Elle autorise un style ferme, imagé et légèrement mordant, mais exclut le sarcasme, la caricature, le militantisme et les slogans mécaniques.

Le validateur 0.3.1 ajoute `WDV-EDT-014`, avertissement heuristique sur la proximité excessive entre le titre et la première phrase, et `WDV-EDT-015`, contrôle de l’attestation humaine des affirmations chiffrées. La pertinence d’un exemple et la justesse du ton restent des contrôles humains. Toutes les exigences 1.1.8 restent actives sauf contradiction explicite.


## Addendum 1.2.0 — interlangues directs, documentation localisée et titres autonomes

La révision 1.2.0 remplace toute disposition antérieure qui imposait `{{Interlangue}}` à la page Débat, différait l’insertion des liens français, exigeait `<references />`, utilisait `|type=` dans la page Debate anglaise, autorisait des références étrangères sur une page de débat malgré une version locale, ou permettait des titres canoniques à référent implicite. Les pages françaises utilisent toutes `{{Lien interlangue}}` dès leur création ; les titres anglais sont verrouillés avant cette création, mais les pages anglaises restent produites ensuite.
