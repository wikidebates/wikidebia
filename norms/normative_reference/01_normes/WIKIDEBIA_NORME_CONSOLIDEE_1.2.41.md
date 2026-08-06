# Norme consolidée Wikidéb’IA 1.2.41

**Statut :** source normative active unique  
**Date d’effet :** 6 août 2026  
**Domaine :** production, validation et préparation à la publication de débats bilingues français–anglais sous MediaWiki  
**Remplace comme sources actives séparées :** révision 1.0.6, correctif du 23 juillet 2026 et décisions correctives du 25 juillet 2026. Ces documents restent conservés dans `history/` à titre de provenance.


> **Révision 1.2.41.** Cette révision applique deux décisions du propriétaire. Premièrement, les mots-clés des pages nouvelles doivent employer les concepts de navigation les plus simples : un qualificatif qui ne fait que rappeler le contexte de la page est supprimé (`liberté divine` devient `liberté` à côté de `Dieu`; `épistémologie réformée` devient `épistémologie`). Les locutions qui désignent réellement un concept autonome, telles que `croyance fondamentale`, restent intactes. Deuxièmement, `./wikidebia update` sélectionne automatiquement l’unique ZIP présent dans `incoming/` et utilise par défaut la portée `all`; un identifiant n’est exigé qu’en cas d’ambiguïté.

> **Révision 1.2.40.** Cette révision restaure l’absence historique des résumés qui n’existaient pas dans les pages importées. Un résumé ne peut être omis que si un inventaire source attesté prouve cette absence et si le verrou de provenance classe le champ comme `historical_absent`. Les pages nouvelles et les résumés effectivement ajoutés après import restent soumis à toutes les exigences de contenu et de style.

> **Révision 1.2.39.** Cette révision conserve les protections de reprise historique non destructive introduites en 1.2.36 et ferme trois failles éditoriales constatées sur un corpus réel : les mots-clés doivent désigner des concepts atomiques plutôt que des mini-rubriques, les résumés produits par gabarit répétitif, métadiscours ou énumération de pages filles sont bloqués à l’échelle du corpus, et le nom propre « Dieu » reçoit la majuscule attendue. Toutes les règles 1.2.36 restent actives sauf contradiction explicite.

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

Lorsque la traduction anglaise est `ready` ou `published`, les productions française et anglaise doivent être fonctionnellement équivalentes : mêmes nœuds, mêmes relations, mêmes occurrences et même orientation argumentative. Elles peuvent employer une rédaction et une documentation adaptées à chaque langue. Lorsque `translation_status.en=deferred`, cette équivalence n'est pas encore contrôlable et les contrôles bilingues sont différés sans affaiblir les contrôles français.

Les sorties générées doivent être prêtes à être relues et importées, sans métadiscours, sans paramètres d’avertissement vides, sans texte extérieur au modèle principal et sans normalisation silencieuse par le validateur.

## 3. Invariants du graphe

Sont verrouillés après validation du graphe :

- `debate_id` ;
- identifiants des nœuds, relations et occurrences ;
- titre canonique français ;
- titre canonique anglais dès que la traduction quitte l’état `deferred` ;
- orientation, parenté, ordre et profondeur des relations ;
- occurrence primaire et réutilisations ;
- propriétaires et composition des lots.

Les titres affichés, rubriques, sections, mots-clés, résumés et métadonnées documentaires peuvent être corrigés lorsque le workflow l’autorise. Toute modification d’un champ inclus dans l’objet canonique de l’empreinte structurelle impose un recalcul explicite et la documentation de l’ancienne et de la nouvelle empreinte.

### 3.1 Fonction argumentative des niveaux

La profondeur n’est pas un indice d’importance, de prestige disciplinaire ou de richesse documentaire. Elle exprime la fonction logique de chaque occurrence dans le graphe.

Une occurrence de **niveau 1** est un argument principal. Elle doit simultanément :

1. répondre directement à la proposition du débat, en faveur ou en défaveur de celle-ci ;
2. rester intelligible et défendable sans qu’un autre argument serve de parent implicite ;
3. ouvrir une famille argumentative distincte pouvant organiser des justifications, objections et réponses ;
4. ne pas avoir de parent plus général, non redondant, qui exprimerait mieux la raison principale ;
5. ne pas avoir pour fonction première de soutenir, d’attaquer, d’illustrer, de spécialiser ou de nuancer un argument déterminé.

Un argument important n’est donc pas nécessairement principal. Une objection visant spécialement une preuve, un exemple historique, un résultat expérimental, une interprétation scientifique, une doctrine particulière, un mécanisme technique ou une application sectorielle appartient à un niveau supérieur lorsqu’un argument plus général peut l’accueillir sans perte substantielle.

Le test décisif est le suivant : si l’énoncé conserve essentiellement la même fonction après suppression de la branche qu’il vise, il peut être candidat au niveau 1 ; s’il perd sa cible, sa portée ou sa raison d’être, il doit être subordonné à cette cible. Ainsi, « Le remplacement de théories autrefois fécondes affaiblit l’inférence du succès scientifique au réalisme » est une objection à l’argument tiré du succès des sciences, et non une branche principale parallèle. De même, une interprétation quantique relative à la mesure relève normalement d’un argument plus général sur la dépendance des propriétés au contexte de mesure.

Une formulation propre à une école philosophique peut être de niveau 1 seulement si cette formulation constitue elle-même une réponse autonome au débat. Lorsqu’elle instancie une thèse plus générale, la thèse générale devient le parent et la doctrine en fournit une justification, une précision ou un développement.

Toute occurrence de profondeur supérieure à 1 doit viser directement son parent immédiat. Elle ne doit pas être placée sous un parent seulement voisin par thème. Une page réutilisée peut apparaître à plusieurs endroits, mais chaque occurrence reçoit séparément une justification de placement.

Avant le verrouillage du graphe, une revue sémantique couvre toutes les occurrences actives. Pour chaque niveau 1, elle atteste la réponse directe au débat, l’autonomie, la capacité à structurer une famille et l’absence de parent général préférable. Pour chaque niveau supérieur, elle atteste que le parent est la meilleure cible immédiate et que la relation déclarée correspond au raisonnement. Cette revue est enregistrée dans le fichier déclaré par `editorial_controls.graph_placement_review_path`.

## 4. Titres canoniques et titres affichés

Le titre canonique est le nom de page et la cible de relation. Il est complet, explicite, autonome et non ambigu. Il mentionne le sujet lorsque cela évite une collision avec d’autres débats.

Le titre affiché est une formulation de lecture plus concise que le titre canonique lorsque cette concision améliore réellement le rendu. Il reste cependant une proposition argumentative complète et immédiatement intelligible : le lecteur doit pouvoir identifier ce qui est affirmé, et non seulement le thème auquel l’argument se rapporte. Un simple groupe nominal, une étiquette doctrinale ou l’intitulé d’un phénomène ne suffit pas. Le titre affiché comporte au minimum un sujet et un prédicat explicites, sans point final, et conserve le lien logique décisif de l’argument. Le contexte d’affichage peut permettre d’omettre un cadrage déjà évident, mais il ne peut jamais remplacer le verbe, la conclusion ou la relation argumentative qui rendent la phrase compréhensible.

### 4.1 Autonomie référentielle du titre canonique

Le titre canonique constitue le nom permanent de la page et la cible de ses liens. Il doit être compréhensible lorsqu’il est présenté isolément, notamment dans un résultat de recherche, une liste de pages, un historique, une catégorie ou un lien dépourvu de contexte explicatif.

Il ne doit pas dépendre d’un élément extérieur au titre pour identifier son sujet. Une formulation anaphorique ou déictique est donc non conforme lorsque son antécédent n’est pas exprimé dans le titre lui-même. Sont notamment concernés les déterminants et pronoms tels que « ce », « cet », « cette », « ces », « celui-ci », « celle-ci », « il », « elle », « ils » ou « elles » lorsqu’ils renvoient seulement au parent, à la branche ou au paragraphe environnant.

Le titre canonique remplace alors l’expression contextuelle par le nom ou la désignation explicite du référent. Cette règle porte sur l’autonomie du nom de page, non sur une catégorie particulière d’objets : elle s’applique de la même manière à une méthode, une institution, une théorie, un événement, une mesure, une personne, un résultat ou tout autre sujet.

Exemple :

- non conforme : `La répétition des défaillances de cette méthode réduit sa fiabilité` ;
- conforme : `La répétition des défaillances de la méthode de contrôle croisé réduit sa fiabilité`.

Les démonstratifs et pronoms ne sont pas interdits lorsqu’ils possèdent un antécédent explicite et non ambigu dans le titre lui-même. Ainsi, un possessif comme « sa fiabilité » peut reprendre la `méthode de contrôle croisé` déjà nommée dans la même proposition.

Le titre affiché peut employer une expression contextuelle plus courte si son référent est immédiatement identifiable dans l’emplacement d’affichage, si aucune autre entité ne peut être visée et si le raisonnement reste strictement identique au titre canonique. Cette souplesse ne dispense jamais d’une phrase propositionnelle complète : « La convergence entre observateurs » est un thème, tandis que « La convergence entre observateurs indique l’existence d’objets publics » expose un argument. De même, « Les renversements de l’histoire des sciences » doit devenir une proposition telle que « Les renversements scientifiques montrent que le succès d’une théorie ne garantit pas sa vérité ».

Un titre affiché ne peut jamais être obtenu par une troncature aveugle ni réduit à un intitulé nominal. Sont notamment interdits :

- les ellipses `...` ou `…` ;
- la suppression d’un article, déterminant ou mot initial nécessaire à la grammaire ;
- un début de titre constitué d’une lettre résiduelle telle que `S ` ou `E ` ;
- une fin sur une préposition, une conjonction ou un connecteur incomplet ;
- les remplacements lexicaux qui créent un doublon, une construction hybride ou un énoncé non idiomatique ;
- la présence accidentelle de mots d’une autre langue, hors noms propres et dénominations officielles ;
- un groupe nominal qui nomme seulement un thème, un phénomène, une école ou une objection sans exprimer ce que cet élément établit ;
- une formulation dépourvue de prédicat explicite ou dont le lecteur ne peut comprendre la portée argumentative sans ouvrir la page.

Lorsqu’une substitution contextuelle est employée pour distinguer titre canonique et titre affiché, elle doit être relue dans la phrase entière. Le titre validé dans le registre doit être reproduit à l’identique dans toutes les relations, pages Débat/Debate, agrégats, projections et fichiers canoniques, agrégats et manifestes.

### 4.2 Guillemets dans les noms de pages et titres affichés

Le critère est l’accessibilité sur un clavier d’ordinateur ordinaire, sans saisie d’un code Unicode ou d’une combinaison spécialisée. Les deux sites utilisent donc les **guillemets droits doubles ASCII** `"..."` dans les titres canoniques et les titres affichés :

- français : `Le terme "effet de seuil" est défini...` ;
- anglais : `The term "threshold effect" is defined...`.

Les guillemets typographiques ou chevrons `« »`, `“ ”`, `„ ”`, `‹ ›` sont interdits dans les noms de pages et titres affichés. L’apostrophe droite ASCII `'` reste utilisée pour les élisions françaises et les contractions ou possessifs anglais ; elle ne remplace pas les guillemets d’une citation principale. Les guillemets droits doivent être équilibrés.

La copie mécanique sans revue est interdite. Chaque titre affiché fait l'objet d'une décision éditoriale page par page, consignée dans un registre de revue. Pour chaque langue, cette revue atteste explicitement que le titre forme une proposition complète, que l’argument qu’il exprime est compréhensible à la lecture du seul libellé et que la concision a été effectivement recherchée.

À compter de la norme 1.2.22, l'identité exacte avec le titre canonique est une exception. Toute identité doit être accompagnée, dans le registre individuel, d'une justification propre au nœud et à la langue expliquant pourquoi aucune formulation plus courte ne préserverait aussi bien la thèse. Les identités ne peuvent dépasser 10 % des arguments actifs dans une langue. Le seuil porte sur l’égalité normalisée après retrait des espaces périphériques et mise en minuscules ; il n’autorise ni les troncatures, ni les paraphrases artificielles. Le validateur bloque les corpus dépassant ce seuil et contrôle la présence des attestations de concision et des justifications individuelles.

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

Tout terme scientifique, technique, juridique ou philosophique indispensable est rendu compréhensible lors de sa première occurrence significative. Deux moyens sont admis : une brève explication intégrée au raisonnement, ou, lorsque le premier paragraphe de Wikipédia fournit une définition suffisante, un lien explicatif au survol avec `{{Lien Wikipédia}}` en français ou `{{Wikipedia link}}` en anglais. Le lien au survol évite de répéter dans la phrase une définition déjà disponible, mais il ne remplace jamais l’explication du mécanisme propre à l’argument. Un terme de langue courante n’a pas à être lié ou défini artificiellement, et le résumé ne doit devenir ni un glossaire ni une succession de liens.

Dans un résumé français, la forme canonique est `{{Lien Wikipédia|article=Titre de la page}}`. Le paramètre facultatif `|texte-affiché=…` n’est utilisé que lorsque le texte visible souhaité diffère réellement du titre de la page. Une simple adaptation de la majuscule initiale ne justifie pas ce paramètre : dans le corps d’une phrase, `L'{{Lien Wikipédia|article=effet placebo}}` est préféré à un paramètre d’affichage redondant. En anglais, les formes correspondantes sont `{{Wikipedia link|article=Page title}}` et `|displayed-text=…`.

Le titre de l’article est vérifié dans l’édition linguistique de la page produite. Le modèle est placé sur la première occurrence utile de la notion, puis normalement omis lors des répétitions. Il n’est pas employé dans les titres, les citations, les métadonnées documentaires ni le corps des notes `<ref>…</ref>`. Si le premier paragraphe de Wikipédia est trop général, ambigu ou insuffisant pour le raisonnement, une explication concise reste obligatoire dans la prose.

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

Le résumé adopte normalement une formulation ferme, imagée et légèrement mordante qui fait apparaître la force du raisonnement et la conviction de la voix qui le défend. Une rédaction uniformément lisse, distante ou neutralisée n’est pas conforme lorsque le nœud permet une expression plus saillante. Cette fermeté ne doit pas devenir un ton militant, sarcastique ou méprisant. Le texte ne ridiculise pas l’argument adverse, ne prête pas d’intentions aux personnes ou aux institutions et ne transforme pas une proposition discutée en vérité éditoriale incontestable. La revue page par page relève une expression réellement présente dans le résumé qui rend cette force perceptible.

Les images explicatives, oppositions de formulation et phrases saillantes sont admises lorsqu’elles clarifient le mécanisme. Elles ne doivent pas devenir des slogans, être répétées mécaniquement d’une page à l’autre ou dépasser ce que permettent le titre, le graphe et les sources.

Un résumé est bloqué lorsqu’il emploie une charpente rédactionnelle générique à la place du raisonnement propre au nœud. Sont notamment non conformes les formulations telles que « Plusieurs faits ou principes sont ici interprétés… », « Cette conclusion s’appuie notamment sur les propositions suivantes… », « Les faits, principes ou expériences invoqués… », « La thèse en tire une conséquence directe… », « La critique en tire une conséquence directe… », « Le point concret est le suivant… » ou « La conséquence avancée est précise… ». Les variantes proches et les traductions fonctionnelles sont traitées de la même manière.

Le résumé ne peut pas être obtenu en recopiant ou en énumérant les titres des justifications et objections reliées. Il doit expliquer le mécanisme qui permet de passer des prémisses à la conclusion, même lorsque les pages filles fournissent le détail de ces prémisses. Une reprise de deux titres enfants ou davantage sous la forme d’une liste, d’une série de citations ou d’une phrase d’annonce constitue un signal bloquant à reprendre humainement.

À l’échelle d’un corpus, une même phrase normalisée de huit mots significatifs ou davantage ne peut apparaître dans quatre résumés ou plus, sauf citation commune explicitement balisée et documentée. La revue individuelle atteste pour chaque page que le mécanisme propre au nœud est effectivement formulé et que le résumé n’est pas une variante superficielle d’un gabarit utilisé ailleurs.

Dans la prose française, `Dieu` prend une majuscule lorsqu’il désigne le nom propre du Dieu unique des traditions monothéistes. La minuscule est conservée pour un nom commun réellement générique (`un dieu`, `les dieux`, `le dieu d’une tradition particulière`). Les occurrences telles que `dieu est`, `l’existence de dieu`, `la volonté de dieu` ou `selon laquelle dieu…` sont donc non conformes lorsqu’elles visent le nom propre.

La revue humaine page par page atteste en outre que l’ouverture développe le titre, que la pertinence d’un exemple ou d’une donnée a été examinée, que tout chiffre a fait l’objet d’une vérification documentaire explicite, et que le ton reste ferme sans devenir polémique.

## 6. Rubriques, sections et mots-clés

Les rubriques françaises autorisées sont : Aménagement, Culture, Droit, Écologie, Économie, Éducation, Éthique, Géopolitique, Histoire, Philosophie, Politique, Psychologie, Religion et spiritualité, Santé, Science, Société, Sport et loisirs, Technologie.

Chaque nœud est classé individuellement. Une à trois rubriques réellement centrales sont normalement utilisées ; une quatrième est exceptionnelle et motivée. Une rubrique peut légitimement être présente sur tous les arguments d'un débat lorsque sa pertinence est démontrée page par page ; sa fréquence locale ne constitue ni une preuve de pertinence ni une anomalie automatique. Les décisions sont consignées dans un registre de revue. Dans chaque valeur MediaWiki et dans le registre correspondant, les rubriques françaises sont rangées par ordre alphabétique français et les sections anglaises par ordre alphabétique anglais. Les sections anglaises constituent le même ensemble conceptuel que les rubriques françaises, mais leur ordre est recalculé indépendamment dans la langue anglaise.

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

Un mot-clé thématique désigne normalement **un concept atomique de navigation**. L’atomicité est sémantique, non seulement grammaticale. Une expression n’est pas rendue atomique par le simple remplacement d’un complément par un adjectif : `psychologie de la religion` ne doit donc pas devenir `psychologie religieuse`, mais être décomposée en `psychologie` et `religion`. La même règle s’applique aux intersections transparentes de disciplines, domaines ou thèmes, telles que `histoire des religions`, `science et religion`, `sociologie religieuse` ou `religious psychology` : chaque unité de base devient un mot-clé distinct et cliquable.

Une locution multi-mots reste cependant atomique lorsqu’elle nomme une catégorie conventionnelle dont le sens ne se réduit pas à la simple intersection de ses constituants. `argument d'autorité`, `problème du mal`, `lois de la nature`, `charge de la preuve` et `pari de Pascal` sont ainsi conservés comme unités. Le test décisif est le suivant : si la combinaison des mots-clés de base permet de retrouver sans perte la même catégorie, l’expression doit être décomposée ; si la locution désigne un type d’argument, une doctrine, une méthode, un phénomène ou un objet technique reconnu qui disparaîtrait lors de la séparation, elle peut rester entière.

La forme préférée est un nom unique ou un composé lexical stable de deux mots au plus. Une expression de trois mots ou davantage, ou contenant un connecteur tel que « de », « du », « des », « et », `of` ou `and`, n’est admise que lorsqu’elle constitue une dénomination encyclopédique lexicalisée impossible à simplifier sans perte. Le vocabulaire contrôlé atteste alors `atomic_concept=true`, `compositional_intersection=false`, `multiword_exception=true` et une justification spécifique non vide. Pour toute autre entrée, `compositional_intersection=false` et `multiword_exception=false` sont explicitement enregistrés.

Les mini-rubriques productives qui décrivent un angle de traitement au lieu de nommer un concept sont interdites, notamment les formes du type `limites de la science`, `histoire des religions`, `construction des lois scientifiques`, `fiabilité des preuves`, `origine de …` ou `sens de …`, lorsqu’un nom simple ou un composé stable existe (`épistémologie`, `histoire religieuse`, `loi scientifique`, `preuve`, `cosmogonie`, `sens existentiel`). Une attestation générique ne transforme pas une telle formule en mot-clé.

Un mot-clé thématique comporte au plus quarante caractères. Le vocabulaire contrôlé bilingue consigne chaque paire français–anglais, sa définition, son caractère atomique, toute exception multi-mots et, à titre informatif, ses usages dans le corpus courant.

La **graphie canonique** est obligatoire. Un nom commun ou groupe nominal commun commence par une minuscule : `revenu`, `revenu de base`, `philosophie politique`. Une majuscule initiale ou interne n’est conservée que lorsqu’elle appartient à la graphie établie d’un nom propre, d’une dénomination officielle, d’un sigle, d’un acronyme ou d’une marque : `Dieu`, `Islam`, `Union européenne`, `ONU`, `ADN`, `eBay`. Le vocabulaire contrôlé indique pour chaque entrée sa nature grammaticale, sa politique de capitalisation et, lorsqu’une majuscule est conservée, une justification non vide. Un terme ne peut pas être déclaré artificiellement nom propre afin de conserver une majuscule décorative. Deux entrées qui ne diffèrent que par la casse, telles que `revenu` et `Revenu`, constituent un doublon interdit. Les pages reproduisent exactement la graphie canonique du vocabulaire. La même règle s’applique aux keywords anglais.

Les mots-clés d’une page sont ordonnés **du plus directement pertinent au moins directement pertinent**. Le premier mot-clé désigne le concept le plus évident, central ou immédiatement caractéristique du sujet ou du mécanisme argumentatif ; les suivants élargissent progressivement le contexte. L’ordre chronologique de création, d’importation ou d’ajout dans le vocabulaire est interdit comme principe de classement. L’ordre alphabétique est également exclu, sauf coïncidence avec l’ordre de pertinence. La revue page par page atteste explicitement ce classement.

**La fréquence dans un débat particulier n’est jamais un critère d’admissibilité.** Un mot-clé peut n’apparaître que sur un seul argument du débat courant lorsque le concept est suffisamment général pour concerner d’autres arguments du wiki ou d’autres débats. Il n’existe donc ni minimum d’occurrences locales, ni plafond de taille du vocabulaire calculé en proportion du nombre d’arguments du débat.

La réutilisation effective à l’intérieur du débat reste une information utile pour la revue, mais elle ne doit pas conduire à supprimer un thème central ou à le remplacer par un terme artificiellement plus vague. Un même jeu exact dominant plus de 25 % du corpus demeure bloquant, car il signalerait une attribution mécanique et rendrait la navigation peu discriminante.

Les keywords anglais sont des équivalents idiomatiques et conservent exactement le classement français par pertinence décroissante. Pour les rubriques et sections des pages Débat/Debate, la précision prime sur l’exhaustivité : seules les catégories qui caractérisent le débat dans son ensemble sont retenues, sans ajouter une catégorie parce qu’un argument secondaire, une méthode particulière ou une sous-partie de l’introduction la mentionne. Les pages Débat/Debate utilisent normalement cinq à huit mots-clés généraux.

## 7. Documentation et références

### 7.1 Principes communs

Une source possède un identifiant documentaire unique, une notice vérifiable et des usages réciproques cohérents. Les doublons par DOI, ISBN, URL canonique ou clé normalisée sont interdits.

La bibliographie est généralement prioritaire. La sitographie et la vidéographie sont complémentaires. La sélection documentaire s’adapte au domaine de l’argument : publications scientifiques et synthèses pour les questions empiriques, textes officiels et doctrine pour le droit, sources primaires et travaux historiques pour l’histoire, œuvres et commentaires académiques pour la philosophie, données et rapports institutionnels pour les politiques publiques, ou toute autre source de référence adaptée au sujet. Les pages Argument ne remplissent pas de quotas : chaque famille documentaire peut contenir zéro, une ou plusieurs références selon son apport réel. Les pages Débat et Debate suivent toutefois une règle de couverture propre : chacun de leurs neuf paramètres documentaires (trois positions pour chacune des familles bibliographie, sitographie/webliography et vidéographie) contient au moins deux références distinctes. Cette pluralité garantit qu’aucune position n’est représentée par une notice symbolique isolée.

Sur une page `Argument`, le critère déterminant est que la source développe, explique, défende, documente ou étaye réellement le raisonnement propre à l’argument. Une source seulement contextuelle ou consacrée uniquement à des objections n’est pas retenue comme référence de cet argument. En revanche, lorsqu’une source développe bien l’argument, le fait qu’elle examine aussi des objections, des limites ou des réponses adverses ne constitue jamais un motif de retrait. L’usage documentaire consigne séparément la vérification du développement de l’argument et l’éventuelle présence d’objections ; cette seconde information est descriptive et n’invalide pas la référence.

### 7.2 Pagination bibliographique

Une page ou plage de pages utilise :

```mediawiki
|page=36-37
```

La valeur ne contient ni `page`, ni `pages`, ni `p.`, ni `pp.`. `localisation=` et `location=` sont réservés aux repères non strictement paginaires : chapitre, section, annexe, numéro ou identifiant d’article.

Une incompatibilité entre la norme et un modèle public est un blocage de publication. Elle ne doit jamais être contournée silencieusement dans le corpus ou le kit.

### 7.3 Dates sitographiques

`date=` contient la date de publication ou de mise à jour substantielle. Lorsqu’une date complète est connue, elle est écrite en langage naturel dans la langue de la page (`25 juin 2012` en français, `25 June 2012` en anglais), jamais au format machine `2012-06-25`. Une année seule, par exemple `2012`, reste admise lorsqu’elle est la seule précision documentaire disponible. Une date de consultation n’est jamais placée dans `date=`. Lorsque la date documentaire n’est pas vérifiable, le paramètre est omis. Aucune date ne peut être inventée. Cette règle ne concerne pas `date-création` ni `creation-date`, qui restent obligatoirement au format `AAAA-MM-JJ`.

### 7.4 Langue des sources et éditions linguistiques

La langue enregistrée dans le registre documentaire est la langue réelle du contenu cité, et non la langue de la page qui l’utilise. Chaque usage indique séparément la langue de la page. La vérification de langue est explicite.

Les pages Débat et Debate utilisent exclusivement des ressources intégralement disponibles dans leur propre langue, y compris les appels de référence de l’introduction et les listes documentaires structurées. Une page française de débat ne cite donc aucune ressource anglaise ; une édition, traduction, page, version doublée ou sous-titrée officiellement en français constitue une notice française distincte.

Sur une page Argument française, une édition ou traduction française pertinente et vérifiable est toujours préférée lorsqu’elle existe. Une source primaire ou académique peut rester dans sa langue originale uniquement lorsqu’aucun équivalent français officiel et pertinent n’existe, ou lorsque la ressource étrangère est elle-même l’objet analysé. Cette décision est consignée dans l’usage documentaire. Les titres publiés ne sont jamais traduits artificiellement. La règle symétrique s’applique aux pages anglaises.

Les éditions ou traductions d’une même œuvre partagent un identifiant d’équivalence documentaire. Le validateur bloque l’emploi d’une source étrangère sur une page Argument lorsqu’un équivalent vérifié dans la langue de la page est disponible dans le registre.

### 7.5 Finalité et organisation des introductions Débat / Debate

L’introduction apporte de manière synthétique les éléments nécessaires pour comprendre le débat avant la lecture des arguments. Elle permet au lecteur d’identifier le sujet, le sens exact de la question, son contexte et ses principaux enjeux. Elle ne constitue ni une revue exhaustive de la littérature, ni un résumé successif des arguments pour et contre, ni une reproduction des branches du graphe argumentatif.

Elle traite normalement, dans un ordre adapté au sujet :

1. de la définition du ou des sujets et de la délimitation du périmètre ;
2. du sens précis de la question débattue, de ses principales interprétations et des distinctions nécessaires pour éviter les confusions ;
3. des repères historiques permettant de comprendre l’apparition et l’évolution du débat ;
4. de l’état actuel du débat lorsqu’il demeure contemporain, notamment ses principaux acteurs, institutions, évolutions ou cadres applicables ;
5. des concepts, mécanismes, méthodes, données ou contextes indispensables à la compréhension du désaccord ;
6. des enjeux intellectuels, sociaux, éthiques, politiques, juridiques, économiques, scientifiques ou pratiques du débat.

D’autres sous-parties peuvent être ajoutées lorsqu’elles apportent un élément réellement nécessaire à la compréhension du sujet. Aucune liste thématique propre à un débat particulier ne devient une structure universelle applicable mécaniquement aux autres débats.

Les sous-parties suivent une progression compréhensible pour un lecteur qui découvre le sujet. Chacune répond à une question identifiable et son utilité pour la compréhension du débat apparaît dès ses premières phrases. Une sous-partie technique, consacrée par exemple à une méthode, un indicateur, un cadre juridique ou un mécanisme spécialisé, n’est introduite que si le texte explique pourquoi cet élément est déterminant pour la question débattue.

Les titres de sous-parties privilégient les formulations accessibles et informatives. Ils évitent les intitulés spécialisés ou abstraits dont le rapport avec le débat n’est pas immédiatement compréhensible.

Dans le contenu des sous-parties, une notion spécialisée dont la définition est utile mais secondaire peut être rendue explicite au survol avec `{{Lien Wikipédia}}` en français ou `{{Wikipedia link}}` en anglais. Le modèle est réservé aux notions qui risqueraient réellement d’arrêter un lecteur non spécialiste. Il ne sert ni à lier chaque nom propre, chaque institution ou chaque terme courant, ni à remplacer les explications nécessaires au sens de la question débattue.

Exemples français conformes :

```mediawiki
L'Alaska a mis en place l'{{Lien Wikipédia|article=Alaska Permanent Fund}}, une forme particulière de revenu de base.
{{Lien Wikipédia|article=Basic Income Earth Network}}
{{Lien Wikipédia|article=Monnaie locale|texte-affiché=monnaie locale complémentaire}}
L'{{Lien Wikipédia|article=effet placebo}} est étudié dans certains protocoles expérimentaux.
```

Le paramètre `|texte-affiché=` est réservé à une différence lexicale ou grammaticale réelle. Pour la seule minuscule initiale exigée par la phrase, le nom passé à `|article=` peut commencer par une minuscule. L’anglais suit la même règle avec `{{Wikipedia link|article=…}}` et `|displayed-text=…`. Le lien au survol est un outil d’explication et de navigation, non une référence : toute affirmation factuelle qui exige une attribution conserve son appel `<ref>…</ref>`.

Le rendu français repose sur le modèle MediaWiki suivant, fourni par le propriétaire du projet :

```mediawiki
<span class="hover-wikipedia">[https://fr.wikipedia.org/wiki/{{{article}}} {{{texte-affiché|{{{article}}}}}}]</span>
```

Cette implémentation confirme que le paramètre `article` détermine à la fois la cible Wikipédia et, par défaut, le texte visible. Le modèle anglais `Wikipedia link` suit la convention fonctionnelle correspondante avec `article` et `displayed-text`; son code interne n’est pas imposé par la norme tant que ce comportement est respecté.

Le nombre de sous-parties et le volume documentaire dépendent de la complexité, de l’étendue du sujet et de l’abondance de la littérature disponible. Il n’existe pas de minimum universel de cinq sous-parties ni de vingt références. Le profil local peut déclarer des minima adaptés, accompagnés d’une justification non vide ; ces minima ne doivent jamais conduire à fragmenter artificiellement l’introduction ou à ajouter des sources sans apport réel. Inversement, une page portant sur une controverse abondamment documentée ne doit pas s’arrêter à une sélection symbolique ou minimale. Chaque famille applicable (bibliographie, sitographie et vidéographie) fait l’objet d’un examen séparé. Pour une page Débat ou Debate, les neuf paramètres documentaires sont tous présents et chacun contient au moins deux références distinctes ; une référence unique dans un paramètre est insuffisante. Au-delà de ce plancher structurel, le volume total reste proportionné à l’abondance et à la qualité de la littérature, sans remplissage artificiel.

Chaque sous-partie substantielle contient les appels de référence inline nécessaires pour soutenir les affirmations factuelles qui exigent une attribution. Dans les introductions française et anglaise, chaque appel développé est rédigé directement en wikicode lisible à l’intérieur de `<ref>…</ref>`, sans passer par un modèle MediaWiki. Les modèles `{{Référence}}`, `{{Reference}}`, les modèles bibliographiques, sitographiques ou vidéographiques spécialisés et tout autre modèle de citation sont interdits dans le corps d’une note d’introduction. La note indique directement les éléments utiles à l’identification de la source — auteur, titre, publication ou site, date en langage naturel, pagination et lien selon le cas. Une référence nommée peut être définie sous la forme `<ref name="…">contenu rédigé directement</ref>` puis réutilisée avec `<ref name="…" />`. Les appels français sont placés avant la ponctuation finale ; les appels anglais suivent la convention anglaise. Les balises `<references />` et `<references>` ne sont jamais ajoutées : l’affichage des notes est géré par le wiki. Les mêmes sources peuvent également figurer dans les listes documentaires structurées de la page lorsque l’appel inline attribue une affirmation précise.

Aucun nombre minimal d’appels `<ref>` n’est imposé à l’introduction dans son ensemble ni à une sous-partie particulière. Une introduction principalement définitionnelle, conceptuelle ou argumentative peut donc ne contenir aucun appel inline lorsqu’elle ne formule aucune affirmation factuelle externe nécessitant une attribution. Le contrôle porte sur l’adéquation entre les affirmations présentes et leurs sources, non sur la présence mécanique d’au moins une référence.

Avant `release_ready`, une revue humaine bilingue consigne pour chaque langue que le sujet et le périmètre sont définis, que le sens de la question est expliqué, que l’histoire et l’actualité sont traitées lorsqu’elles sont pertinentes, que les enjeux sont explicites, que chaque sous-partie est nécessaire, que la progression est logique, qu’une section technique est contextualisée et que l’introduction ne reproduit ni le graphe ni une checklist propre à un corpus pilote.

### 7.6 Sélection de la bibliographie des pages de débat

La bibliographie d’une page Débat ou Debate constitue une sélection de référence sur l’ensemble de la controverse. Elle privilégie les livres incontournables, monographies, manuels, volumes collectifs, rapports de synthèse et articles de revue réellement panoramiques. Les articles scientifiques consacrés à une expérience, un protocole ou un résultat étroit appartiennent aux pages Argument concernées et ne sont pas accumulés dans la bibliographie générale du débat.

Chaque usage bibliographique du débat indique s’il s’agit d’une œuvre fondatrice ou d’une synthèse large, ainsi qu’une justification de sélection. Une source étroite ou dépourvue de justification est bloquante.

### 7.7 Métadonnées sitographiques et conversion des auteurs

`auteurs=` ou `authors=` n’est émis que lorsqu’une personne ou une organisation est explicitement responsable du contenu. À défaut, le paramètre est omis ; le nom du site n’est jamais recopié mécaniquement comme auteur. La vérification de l’attribution est enregistrée.

Le registre JSON conserve `authors` sous forme de liste, mais cette liste ne doit jamais être sérialisée littéralement dans le wikicode. La conversion vers MediaWiki est obligatoire : une liste d’un élément devient le texte brut de cet élément (`["L'Encyclopédie philosophique"]` devient `|auteurs=L'Encyclopédie philosophique`) ; plusieurs éléments sont séparés par une virgule suivie d’une espace (`Auteur 1, Auteur 2`) ; une liste vide entraîne l’omission du paramètre. Les crochets, guillemets et virgules syntaxiques du JSON ne sont jamais publiés.

Lorsque le titre de la page et le nom du site sont identiques, seul `site=` est conservé. Les triples identiques `page`, `auteurs` et `site` sont interdits.

### 7.8 Incises parenthétiques dans la prose française

Dans la prose française générée, une incise explicative, une apposition ou une énumération insérée à l’intérieur d’une phrase est délimitée par des parenthèses, et non par une paire de tirets cadratins.

Exemple non conforme :

`La mesure concerne plusieurs services essentiels — l’eau, l’énergie, les transports et la santé — sans s’appliquer aux activités de loisir.`

Exemple conforme :

`La mesure concerne plusieurs services essentiels (l’eau, l’énergie, les transports et la santé) sans s’appliquer aux activités de loisir.`

Cette règle vise les tirets cadratins appariés employés comme signes de parenthèse dans les introductions, résumés et autres passages rédactionnels français. Elle n’interdit pas les traits d’union, les plages numériques, les listes MediaWiki, les titres d’œuvres cités fidèlement ni les tirets présents dans une citation reproduite comme telle.

## 8. Structures MediaWiki actives

### 7.9 Articles Wikipédia obligatoires et préservation conditionnelle des débats connexes

Toute page `Débat` française contient un paramètre `articles-Wikipédia` non vide avec au moins un sous-modèle `{{Article Wikipédia|page=…}}`. Toute page `Debate` anglaise contient de même `wikipedia-articles` avec au moins un `{{Wikipedia article|page=…}}`. Les titres exacts sont recherchés et vérifiés dans l’édition linguistique correspondante ; l’absence de résultat ne peut pas être déclarée sans recherche. Un article directement centré sur le sujet est privilégié, mais des articles de cadrage étroitement liés sont admis lorsque le titre exact du débat n’a pas de page dédiée.

Lors de la création d’une page de débat qui n’existait pas, Wikidéb’IA ne produit pas `débats-connexes` ni `related-debates`. Lors de la modification d’une page préexistante, le paramètre est conservé exactement s’il existe déjà, avec sa valeur antérieure ; il reste absent s’il n’existait pas. La modification ne doit donc ni supprimer une liste existante de débats connexes, ni en inventer une nouvelle.

### 8.0 Création et modification des paramètres protégés

Le manifeste de chaque page déclare `page_origin` (`new` ou `preexisting`) ainsi qu’un instantané de présence et de valeur des paramètres protégés. Pour une page nouvelle, les structures ci-dessous indiquent les valeurs générées. Pour une page préexistante, ces lignes sont conditionnelles :

- `avancement` / `progress` conserve exactement sa valeur antérieure et reste absent s’il était absent ;
- `avertissements-débat` / `debate-warnings` conserve exactement sa valeur antérieure et reste absent s’il était absent ;
- `avertissements-argument` / `argument-warnings` conserve exactement sa valeur antérieure et reste absent s’il était absent ;
- `débats-connexes` / `related-debates` conserve exactement sa valeur antérieure et reste absent s’il était absent.

Le moteur de mise à jour bloque toute opération qui modifierait l’un de ces paramètres sur une page existante.

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
|articles-Wikipédia={{Article Wikipédia
|page=Article vérifié directement lié au sujet
}}
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

Les lignes `avancement=Débat construit` et `avertissements-débat=Débat généré par IA` de cet exemple valent uniquement pour une page nouvellement créée par Wikidéb’IA. Sur une page préexistante, elles sont remplacées par la conservation exacte de l’état antérieur.

Le paramètre `interlangue` dépend de l'état de traduction anglaise. Avec `translation_status.en=deferred`, il est absent du wikicode français et aucun titre anglais n'est requis. Avec un état `ready` ou `published`, il contient exactement un `{{Lien interlangue}}` visant le titre canonique anglais verrouillé. Une page anglaise peut rester momentanément absente du wiki uniquement lorsque son titre est déjà verrouillé et que l'état déclaré autorise cette préparation.

Lorsque le sujet possède un acronyme courant et non ambigu, `sujet-complet` ou `complete-topic` l’emploie de préférence à la répétition de la forme développée. Exemple : `|sujet=Gestation pour autrui` et `|sujet-complet=l’autorisation de la GPA`. Le registre de revue indique, pour chaque langue, l’acronyme retenu ou atteste qu’aucun acronyme courant n’est applicable.

Avec `translation_status.en=deferred`, les pages anglaises sont absentes du manifeste, leurs titres peuvent être absents, nuls ou `unassigned`, et les pages françaises ne contiennent aucun lien interlangue. Après traduction, le statut passe à `ready` ou `published`, les titres anglais sont verrouillés, les pages anglaises sont ajoutées au manifeste et une reprise française peut ajouter les liens interlangues exacts.

### 8.2 Page Argument française

```mediawiki
{{Argument
|avertissements-argument=Argument généré par IA
|résumé=
|citations={{Citation
|citation=
|auteurs=
|article=
|ouvrage=
|volume=
|numéro=
|page=
|localisation=
|édition=
|lieu=
|date=
|lien=
|avertissements-citation=
}}
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

Les lignes `avertissements-argument=Argument généré par IA` de la structure française valent uniquement pour une page Argument nouvellement créée. Une page Argument préexistante conserve exactement sa valeur antérieure ou l’absence du paramètre.

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
|wikipedia-articles={{Wikipedia article
|page=Verified article directly related to the topic
}}
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

The `progress=Constructed debate` and `debate-warnings=Debate generated by AI` lines apply only to a newly created Debate page. A pre-existing page preserves the exact previous presence and value of these parameters.

### 8.4 English Argument page

```mediawiki
{{Argument
|argument-warnings=Argument generated by AI
|summary=
|quotes={{Quote
|quote=
|authors=
|article=
|work=
|volume=
|issue=
|page=
|location=
|publisher=
|place=
|date=
|link=
|warnings=Citation traduite par IA
}}
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

La date de création est une décision de production distincte de la date des sources. Elle seule utilise systématiquement le format machine `AAAA-MM-JJ` dans `date-création` et `creation-date`; les dates documentaires complètes utilisent le langage naturel. Chaque paquet déclare la date attendue pour chaque langue dans son manifeste ou son profil local. Le validateur compare cette valeur au wikicode, au registre et aux manifestes de pages. Le moteur générique ne contient aucune date propre à un corpus.

La date devient immuable dès la première validation du fichier de la page. Elle ne change ni lors d’une correction, ni lors d’un enrichissement, ni lors d’une nouvelle tentative d’import. L'ajout ultérieur d'un lien interlangue après une phase `deferred` est un enrichissement de la page existante : il ne change jamais sa date de création.

Les décisions propres à un corpus, y compris une date corrective historique, sont conservées dans son profil local ou ses rapports de migration, jamais dans la norme universelle.

## 9.1 Préservation automatique des pages historiques lors d’une reprise

Lorsqu’une page du nouveau corpus correspond à une page distante attestée dans l’état publié et que la révision distante courante correspond encore exactement à cet état, le kit construit un contenu effectif dérivé. Il y recopie uniquement les paramètres de cycle de vie protégés de la page distante : date de création, avertissements, avancement et paramètres historiques explicitement énumérés par le profil de rendu. Le reste du contenu provient du nouveau corpus validé.

Cette réconciliation ne constitue ni une importation de modifications humaines, ni une normalisation silencieuse du corpus source. Le fichier original reste inchangé ; le plan signé référence le fichier effectif dérivé, son empreinte et le détail des valeurs préservées. Toute divergence distante non attestée reste classée `manual_review`.

Une page existante sans avertissement IA ne reçoit donc pas rétroactivement `Argument généré par IA` ou `Débat généré par IA`. Une valeur historique particulière, par exemple un avertissement éditorial ou un avancement antérieur, est conservée. Les pages réellement nouvelles reçoivent au contraire les valeurs de création prévues par le profil actif.

Pour une suppression, l’absence de marqueur Wikidéb’IA reste bloquante par défaut. Elle peut être levée uniquement pour une page historique lorsque le registre de migrations déclare explicitement son retrait, que le titre n’appartient à aucun autre débat connu et que la révision ainsi que l’empreinte distantes correspondent exactement à l’état attesté. L’exécuteur revérifie ces conditions immédiatement avant la suppression.

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

Le validateur recommandé 0.4.13 conserve les contrôles antérieurs, applique les règles 1.2.6 à 1.2.9 aux paquets qui les déclarent et maintient la compatibilité explicite avec les révisions historiques annoncées. Chaque règle binaire nouvelle possède au moins un test positif et un test négatif. Les nombres de tests, exigences et fichiers déclarés dans les reçus doivent correspondre aux éléments réellement livrés.

Les longueurs indicatives des résumés restent des guides éditoriaux et non des quotas. Une distribution systématiquement courte déclenche une information de revue humaine, sans provoquer de remplissage artificiel. La revue doit confirmer que chaque page demeure autonome, informative et fidèle à un seul nœud.

## 12. Publication W11

Aucune écriture distante n’est autorisée pendant une reprise W10 corrective. Le kit W11 est livré sans exécution et sans secret.

Avant toute publication, W11 doit :

1. exécuter une simulation globale déterministe et signer le plan par SHA-256 ;
2. vérifier en lecture seule la compatibilité réelle des modèles publics ;
3. refuser de poursuivre si un paramètre normatif requis n’est pas accepté ;
4. effectuer comme première écriture distante un test sur l’unique page Débat française canonique du plan ;
5. exiger que cette page soit absente lors de la simulation, la créer avec `createonly`, relire la révision exacte et produire un reçu machine signé ;
6. avant toute autre écriture, recharger le même plan et le reçu, vérifier leurs empreintes, puis confirmer que la page Débat est toujours à la révision attestée avec le même contenu, le même résumé et la même balise ;
7. après ce test, créer les autres pages françaises, puis les pages anglaises, les pages Argument précédant la page Debate dans la phase anglaise ;
8. réauthentifier et vérifier l’identité à chaque phase et avant chaque écriture ;
9. utiliser `assert=user` et `assertuser` ;
10. classifier chaque titre distant comme `absent`, `equivalent_existing`, `collision` ou `manual_review` ;
11. ne jamais écraser une page existante par défaut : une page équivalente est ignorée et une collision bloque le plan ; la page Débat française préexistante bloque spécifiquement le test ;
12. comparer les contenus local et distant par SHA-256 et enregistrer les identifiants de révision ;
13. utiliser `createonly` pour chaque création canonique ; aucune mise à jour interlangue distincte n’est prévue pour un paquet 1.2.x ;
14. relire chaque page après écriture, vérifier son contenu et enregistrer la nouvelle révision ;
15. s’arrêter sur perte de session, collision, divergence, droits insuffisants ou révision concurrente ;
16. ne créer aucune sous-page utilisateur pour le test de publication ;
17. écrire des journaux JSONL privés de simulation, test et import ;
18. reprendre uniquement à partir du couple titre + SHA-256 de contenu et de révisions réelles vérifiées ;
19. refuser l’exécution si le corpus, le validateur, la norme ou le plan ont changé depuis la simulation ;
20. charger pour le test et la publication le fichier de plan signé produit par la simulation, sans le reconstruire silencieusement ;
21. incorporer au plan les empreintes du manifeste, du manifeste de libération et du validateur, puis les revérifier avant toute écriture ;
22. reconnaître comme état de reprise valide la page Débat française créée par le test seulement si son reçu reste valide et sa révision courante inchangée ;
23. exiger pour la suite de la publication le reçu machine du test de la page Débat canonique, lié au plan signé et revérifié à distance immédiatement avant toute autre écriture.

Les fichiers d’authentification, cookies, secrets et identifiants privés ne sont jamais inclus dans une archive publique.

## 13. Profils locaux et invariants propres à un corpus

Les nombres de nœuds, relations, occurrences, lots et pages, les dates correctives, les chemins de rapports et les Work particuliers sont des données locales. Ils sont déclarés dans le manifeste, le profil de contrôle ou les rapports du corpus concerné. Ils ne deviennent jamais des constantes de la norme, du validateur ou du kit génériques.

Une reprise corrective conserve les invariants déclarés par son paquet et documente toute migration autorisée. Le statut local `release_ready` n’implique pas l’autorisation de publier : le champ de publication reste fermé jusqu’à la validation complète, au préflight et au test canonique de la page Débat W11.

## 14. Renforcement éditorial cumulatif

Avant `release_ready`, le corpus doit présenter :

1. zéro titre canonique ou affiché contenant une ellipse, une troncature grammaticale ou des guillemets non conformes ;
2. zéro lettre initiale résiduelle issue d’une suppression d’article ;
3. concordance exacte de tous les titres affichés entre registre, relations, agrégats et fichiers canoniques ;
4. deux à quatre mots-clés nominaux par page, issus du vocabulaire contrôlé bilingue ;
5. zéro mot-clé français non traduit dans la liste anglaise ;
6. vocabulaire thématique évalué à l’échelle du wiki, sans exigence de répétition dans le débat courant ;
7. revue page par page de la pertinence des mots-clés ;
8. équivalence substantielle des résumés bilingues ;
9. appels de référence inline placés sur les affirmations factuelles qui nécessitent une attribution, sans quota mécanique par sous-partie ;
10. maintien de tous les invariants verrouillés du graphe ;
11. recalcul explicite de toutes les empreintes de fichiers et, si nécessaire, de l’empreinte structurelle ;
12. absence totale d’écriture distante ;
13. audit de non-régression des normes, du validateur et du kit W11.

Le paquet déclare dans son manifeste les chemins du vocabulaire contrôlé, du registre individuel, des rapports requis et du handoff correctif courant. Le validateur ne déduit jamais ces chemins d’un sujet, d’un numéro de Work ou d’une rubrique particulière. Il ne peut jamais bloquer un mot-clé au seul motif qu’il n’apparaît qu’une fois dans le débat courant.

## 15. Cohérence des livrables et garde-fous de publication

Les archives de normes, du validateur et du kit comportent un manifeste SHA-256 exhaustif. Tout fichier livré, y compris un manifeste historique placé dans un sous-dossier, est soit déclaré avec sa taille et son empreinte, soit explicitement exclu par un chemin précis. Le reçu externe indique des nombres exacts et reproductibles.

La configuration de publication d’un paquet 1.2.x exécute toutes les portées applicables du validateur, notamment `wikicode` et `editorial` lorsque des pages sont publiées. Le kit refuse une configuration qui omet une portée obligatoire du profil actif.

La première écriture canonique de W11 est le test de l’unique page Débat française. La page doit être absente dans le plan et est créée avec `createonly`. Son reçu machine est lié au plan signé, au titre canonique, au fichier local, au contenu relu, à la révision distante, à l’identité vérifiée, au résumé et à la balise de modification. Avant toute autre écriture, le kit recharge ce reçu, en vérifie l’empreinte et confirme que la page courante reste exactement à la révision attestée. Aucune sous-page utilisateur n’est créée.

Les exemples, guides et listes de contrôle livrés avec la norme doivent eux-mêmes respecter la règle active : toute page française d’exemple contient son unique `{{Lien interlangue}}`, et aucun exemple actif ne décrit une phase tardive d’ajout interlangue.

## 16. Livrables minimaux d’une reprise prépublication

La livraison complète contient au minimum :

- le corpus bilingue `release_ready` et son reçu ;
- la norme consolidée active et son changelog ;
- le validateur aligné et sa suite de tests ;
- le kit W11 aligné, non exécuté, et ses tests ;
- un paquet de revue des pages ;
- l’audit de non-régression ;
- les reçus SHA-256 de chaque archive.

La présence de ces éléments est vérifiée avant livraison. Leur absence constitue une régression bloquante.


## Addendum 1.1.5 — ancienne preuve de test, remplacée par 1.2.3

Cette ancienne disposition imposait un test dans l’espace utilisateur. Elle est conservée uniquement comme provenance et n’est plus applicable. La règle active est le test direct de la page Débat française canonique défini par la révision 1.2.3.

## Addendum 1.1.5 — revue individuelle

La conformité des titres affichés et des rubriques ne se déduit pas d'un seuil statistique global. Le paquet `release_ready` contient un registre couvrant chaque nœud actif et indiquant la décision sur le titre ainsi qu'une justification non vide pour chacune des rubriques retenues. Aucune rubrique n'est obligatoire, présumée pertinente ou soumise à un traitement spécial.


## Addendum 1.1.7 — généralité des contrôles

Les contrôles éditoriaux sont formulés sur les propriétés choisies par l’IA, et non sur une valeur particulière. Pour chaque nœud actif, le registre de revue contient une justification distincte pour chaque rubrique retenue. Le validateur exige une correspondance exacte entre les clés de justification et les rubriques de la page ; une justification d’une rubrique absente ou l’absence de justification d’une rubrique présente est bloquante.

Les décisions locales — date de création, chemins des rapports, seuils documentaires du profil, Work courant et handoff — sont déclarées dans le manifeste du paquet. Elles ne sont jamais codées en dur dans le moteur générique. Les invariants propres à un corpus peuvent figurer dans une annexe ou un profil local, sans devenir une règle universelle.


## Addendum 1.1.7 — avertissements et publication traçable

Lorsqu’une page est créée par Wikidéb’IA, les valeurs ajoutées sont exactement `Débat généré par IA`, `Argument généré par IA`, `Debate generated by AI` et `Argument generated by AI`. Les formulations avec `avec IA` ou `with AI` sont interdites pour ces créations. Lorsqu’une page préexistante est modifiée, le paramètre d’avertissement n’est ni ajouté, ni supprimé, ni réécrit : sa présence et sa valeur antérieures sont conservées exactement.

Toute écriture distante produite par le kit W11 emploie un résumé localisé : `Contenu généré par ChatGPT 5.6` en français et `Content generated by ChatGPT 5.6` en anglais. La balise de modification `chatgpt` est obligatoire et doit être déclarée active par le wiki avant toute écriture. Après une écriture, le kit relit la révision exacte renvoyée par l’API et vérifie son contenu normalisé, son résumé et sa balise ; il ne se fie pas uniquement à la dernière révision visible.

## Addendum 1.1.8 — lisibilité des résumés

La norme 1.1.8 rend obligatoire le style encyclopédique grand public des résumés : idée principale annoncée dès l'ouverture, phrases de longueur variée, explication immédiate des termes techniques nécessaires et suppression des développements universitaires qui n'aident pas à comprendre le nœud. Le validateur 0.3.0 ajoute `WDV-EDT-013`, un avertissement heuristique sur l'accumulation de phrases longues, ainsi qu'un contrôle bloquant de la revue humaine page par page. Toutes les exigences 1.1.7 restent actives sauf contradiction explicite.

## Addendum 1.1.9 — ouverture développée, exemples probants et force expressive

La norme 1.1.9 interdit qu’une première phrase se contente de répéter ou de paraphraser étroitement le titre. Elle autorise les exemples et données uniquement lorsqu’ils éclairent réellement le mécanisme et exige une vérification documentaire explicite de toute donnée chiffrée. Elle autorise un style ferme, imagé et légèrement mordant, mais exclut le sarcasme, la caricature, le militantisme et les slogans mécaniques.

Le validateur 0.3.1 ajoute `WDV-EDT-014`, avertissement heuristique sur la proximité excessive entre le titre et la première phrase, et `WDV-EDT-015`, contrôle de l’attestation humaine des affirmations chiffrées. La pertinence d’un exemple et la justesse du ton restent des contrôles humains. Toutes les exigences 1.1.8 restent actives sauf contradiction explicite.


## Addendum 1.2.0 — interlangues directs, documentation localisée et titres autonomes

La révision 1.2.0 remplace toute disposition antérieure qui imposait `{{Interlangue}}` à la page Débat, différait l’insertion des liens français, exigeait `<references />`, utilisait `|type=` dans la page Debate anglaise, autorisait des références étrangères sur une page de débat malgré une version locale, ou permettait des titres canoniques à référent implicite. Les pages françaises utilisent toutes `{{Lien interlangue}}` dès leur création ; les titres anglais sont verrouillés avant cette création, mais les pages anglaises restent produites ensuite.


## Addendum 1.2.2 — cohérence intégrée et publication vérifiable

La révision 1.2.2 intègre directement les règles 1.2.x dans les structures, profils, schéma du registre et workflow au lieu de les laisser seulement dans un addendum correctif. Elle supprime des documents actifs les exemples sans lien interlangue, les états de staging tardif et les constantes propres à un corpus. Elle exige des manifestes d’archive exhaustifs, des compteurs documentaires exacts, l’exécution des portées `wikicode` et `editorial` avant publication et un reçu de test alors effectué dans l’espace utilisateur ; ce mécanisme est remplacé par le test canonique de la page Débat en 1.2.3.


## Addendum 1.2.3 — test canonique de la page Débat

Le test de publication ne s’effectue plus dans l’espace utilisateur. Il consiste à créer en premier la page Débat française canonique prévue par le plan signé. Cette page doit être distante absente au moment de la simulation et au moment de l’écriture. Toute page préexistante bloque le test ; elle n’est ni écrasée ni assimilée à une preuve de bon fonctionnement.

Le reçu du test identifie le débat, l’opération, le titre canonique, le chemin et l’empreinte du fichier local, le contenu attendu, la révision créée, l’utilisateur, le résumé et la balise. Avant la publication des autres pages, la révision courante de la page Débat doit être exactement celle du reçu. Une nouvelle révision, même proche ou équivalente, impose une nouvelle simulation et une revue explicite.


## Addendum 1.2.4 — introduction orientée vers la compréhension et généralité des composants

La révision 1.2.4 remplace toute checklist d’introduction issue d’un corpus particulier par une règle fonctionnelle applicable à tous les débats : définir le sujet et le périmètre, expliquer le sens de la question, donner les repères historiques et actuels pertinents, fournir les connaissances préalables nécessaires et exposer les enjeux. Le nombre de sous-parties et de références est déterminé par la complexité du sujet et justifié dans le profil local, sans minimum universel mécanique.

Une revue bilingue de l’introduction est obligatoire. Elle relie chaque sous-partie réelle à une fonction explicite, atteste la progression, la contextualisation des sections techniques, l’absence de duplication du graphe et l’absence de checklist propre à un débat pilote. Les configurations, identifiants, titres, exemples et seuils propres à un corpus ne figurent pas dans les composants génériques actifs ; ils restent uniquement dans le paquet du corpus concerné ou dans des archives de provenance clairement historiques.


## Addendum 1.2.5 — références d’introduction guidées par les affirmations

La présence d’appels `<ref>` dans une introduction dépend exclusivement des affirmations factuelles qui exigent une attribution. Aucun minimum global ou par sous-partie n’est normatif. Le validateur contrôle l’interdiction des balises `<references />`, l’activation du contrôle documentaire et la revue humaine des affirmations, sans exiger qu’une introduction contienne au moins un appel inline. Toutes les exigences 1.2.4 restent actives sauf cette clarification corrective.

## Addendum 1.2.6 — métadonnées de débat, classement, documentation et force expressive

La révision 1.2.6 impose l’ordre alphabétique des rubriques françaises et des sections anglaises, chacune selon sa propre langue. L’équivalence bilingue porte sur l’ensemble conceptuel, non sur une position identique dans les listes.

Les valeurs `sujet=` et `topic=` commencent par une majuscule et désignent le débat sous la forme la plus nominale et conventionnelle possible : substantif, syntagme nominal, nom d’une doctrine, d’un courant ou d’un « -isme » lorsque cette désignation résume correctement la controverse. Une périphrase descriptive n’est conservée que lorsqu’aucun nom conceptuel suffisamment précis n’existe. Les valeurs `sujet-complet=` et `complete-topic=` en découlent et complètent naturellement les en-têtes « Arguments pour et contre… » et « Pros and cons of… ». Leur premier caractère alphabétique est une minuscule dans les deux langues. Une majuscule initiale n’est admise que si un nom propre ou un acronyme ne peut grammaticalement être précédé d’un déterminant ou d’un autre cadrage nominal ; cette exception est justifiée dans le registre de revue. Elles ne recopient pas la question sous la forme `si`, `whether`, `faut-il`, `should` ou équivalente.

Pour les rubriques et sections d’une page Débat/Debate, la précision prime sur l’exhaustivité. Une catégorie n’est retenue que si elle caractérise la controverse dans son ensemble. La revue de la page atteste également que la profondeur documentaire est proportionnée à l’abondance de la littérature et examine séparément bibliographie, sitographie et vidéographie sans imposer de quota universel.

La force expressive des résumés n’est plus une simple permission abstraite. Chaque revue linguistique identifie une expression réellement présente dans le résumé qui rend la conviction et la fermeté du raisonnement perceptibles, tout en confirmant l’absence de sarcasme, de caricature et de militantisme.

## Addendum 1.2.7 — cohérence de provenance et auto-audit

La révision 1.2.7 ne modifie aucune règle éditoriale introduite en 1.2.6. Elle corrige la livraison générique : tous les alias et chemins du catalogue d’exigences désignent désormais des fichiers réellement présents ; les sources d’origine non distribuées séparément sont signalées comme telles au lieu d’être déclarées conservées ; la matrice de traçabilité est nettoyée ; et l’auto-audit vérifie le champ réel `declared_file_count` du manifeste et du reçu.

Une archive ne peut être déclarée autonome lorsque son catalogue renvoie à un chemin absent. Toute source historique non livrée séparément doit être remplacée par une provenance consolidée explicite, sans inventer ni prétendre reproduire le document d’origine.


## Addendum 1.2.8 — traçabilité exhaustive et cohérence des exemples

La révision 1.2.8 ne modifie aucune exigence éditoriale de 1.2.6. Elle exige que chaque étiquette de provenance effectivement utilisée par le catalogue soit déclarée dans `source_aliases` et résolve vers au moins un fichier livré. Elle aligne les exemples actifs sur la révision courante, corrige leur langue, et étend les conditions de schéma applicables aux paquets 1.2.7 et 1.2.8. Les contrôles d’auto-audit doivent vérifier ces trois propriétés.


## Addendum 1.2.9 — références, acronymes et publication française indépendante

La révision 1.2.9 corrige cinq défauts observés lors d’une production réelle :

1. les dates documentaires complètes sont rendues en langage naturel, tandis que les dates de création restent au format machine ;
2. les appels inline des introductions sont rédigés directement dans `<ref>…</ref>` sans modèle de citation ;
3. chacun des neuf paramètres documentaires d’une page Débat ou Debate contient au moins deux références ;
4. un acronyme courant est employé dans `sujet-complet` ou `complete-topic` et déclaré dans le registre de revue ;
5. le kit peut publier les pages françaises avant la création des pages anglaises, à condition que les titres anglais soient verrouillés dans le registre maître et correspondent aux liens interlangues français.


## Addendum 1.2.10 — notes d’introduction rédigées directement

La règle 1.2.9 qui imposait le modèle générique `Référence`/`Reference` est remplacée. Pour tout paquet déclarant la norme 1.2.10, le corps d’une note développée d’introduction contient directement une référence bibliographique ou web lisible, sans aucun appel de modèle MediaWiki. Les références nommées restent admises, à condition que leur première définition soit rédigée directement. Le validateur refuse tout `{{…}}` dans le corps d’une note d’introduction et continue de refuser les dates documentaires au format machine.

Exemple français conforme :

```mediawiki
Une affirmation documentée<ref>Jean Dupont, « Titre de l’article », ''Nom de la revue'', 25 juin 2012, p. 36-37, [https://example.org texte intégral].</ref>.
```

Exemple anglais conforme :

```mediawiki
A documented claim.<ref>Jane Smith, “Article title”, ''Journal Name'', 25 June 2012, pp. 36–37, [https://example.org full text].</ref>
```


## Addendum 1.2.11 — compaction des modèles MediaWiki adjacents

Dans tout wikicode de page produit sous la norme 1.2.11, deux modèles immédiatement successifs sont accolés sans saut de ligne, espace ni tabulation entre la fermeture du premier et l’ouverture du second. La forme `}}` suivie d’un retour à la ligne puis de `{{` est interdite ; elle est remplacée par `}}{{`. Cette règle vaut en français et en anglais, dans les pages individuelles comme dans les agrégats. Elle ne change ni le contenu des modèles ni l’ordre des paramètres : elle impose seulement une jonction compacte et déterministe entre sous-modèles adjacents.

Le validateur 0.4.13 signale cette anomalie avec `WDV-MWK-018`. Le kit 2.1.13 l’intercepte également avant la construction d’un plan de publication. Les paquets déclarant une norme antérieure conservent leur comportement historique jusqu’à migration explicite.

## 12. Installation portable, publication intégrée et sauvegarde des sources

### 12.1 Publication d’un débat en une commande

L’installation fournit un lanceur racine portable nommé `wikidebia`. Le ZIP d’un débat est déposé directement dans `incoming/`, sans suffixe de nom imposé. S’il est le seul ZIP du dossier, `wikidebia publish` le sélectionne automatiquement. Si plusieurs ZIP sont présents, la commande exige un identifiant et sélectionne exactement `incoming/<identifiant>.zip`. Le nom de base de l’archive sert uniquement à sélectionner le fichier ; le champ `debate_id` du manifeste détermine l’identité du corpus. Une seule invocation exécute l’extraction sûre, l’installation locale du corpus, toutes les portées de validation requises, la construction du plan signé, le test canonique français lorsqu’une page Débat doit être créée, la publication et l’archivage du ZIP après succès.

Les portées canoniques sont `all`, `fr`, `en`, `fr-debate` et `en-debate`. `fr-debate` et `en-debate` ne créent que la page principale de la langue choisie ; `fr` et `en` créent la page principale puis toutes les pages Argument de cette langue ; `all` applique la même séquence au français puis à l’anglais.

Dans chaque langue, la page Débat ou Debate est toujours traitée avant les pages Argument. En français, lorsqu’elle est absente, sa création `createonly` et sa revérification restent la première écriture distante du plan. En anglais, la page Debate est également publiée avant les arguments anglais. Une configuration qui demande l’ordre inverse est refusée.

### 12.2 Mise à jour atomique en une commande

Les nouvelles archives de normes, de validateur et de kit sont déposées dans `updates/`, de préférence dans une seule archive ZIP. Cette archive unique peut être le bundle contenant directement `wikidebia-normes.zip`, `wikidebia-validator.zip` et `wikidebia-kit.zip`, ou une archive de livraison qui contient ces trois composants à sa racine et éventuellement un bundle interne supplémentaire. Le gestionnaire courant sait aussi retrouver les composants dans un unique niveau d’archive enveloppante. La commande `wikidebia upgrade` vérifie les inventaires et SHA-256, contrôle la cohérence des versions, extrait dans une zone temporaire, compare la copie normative, exécute l’auto-audit et toutes les suites de tests, puis remplace atomiquement `norms/`, `validator/` et `kit/`. Lors de la transition depuis un gestionnaire antérieur où cette opération s’appelait encore `update`, l’archive de livraison conserve les trois ZIP de composants à sa racine afin de rester installable en un seul fichier.

Avant remplacement, les composants actifs et les fichiers entrants sont déplacés dans un sous-dossier horodaté de `archives/updates/`. Après succès, `updates/` est vide. Une mise à jour incomplète, divergente ou dont les tests échouent ne remplace aucun composant actif.

### 12.3 Dépôt Git et périmètre sauvegardé

Le dépôt Git, destiné notamment à un dépôt GitHub dont le nom contient normalement `wikidebia`, versionne uniquement les sources nécessaires et portables : `norms/`, `validator/`, `kit/`, le lanceur, les documents actifs, les exemples de configuration, la documentation et les contrôles d’intégration continue. Après une mise à jour réussie, ces modifications sont commitées et poussées automatiquement lorsque le remote `origin` est configuré.

Ne sont jamais versionnés : `private/`, `corpus/`, `archives/`, `updates/`, `incoming/`, `logs/`, `plans/`, `.state/`, l’environnement virtuel et la configuration locale. Le fichier `.gitignore` actif exprime explicitement ces exclusions.

### 12.4 Secrets et portabilité des chemins

`user-config.py` et `user-password.cfg` résident dans `private/pywikibot/`, avec des permissions restrictives, et ne sont jamais placés à la racine ni suivis par Git. Lors de la première mise à jour, les fichiers historiques présents à la racine sont déplacés automatiquement vers ce dossier privé sans écrasement silencieux.

Aucun fichier persistant situé dans l’installation ne conserve le chemin absolu du répertoire racine. Les configurations, plans, journaux, rapports, manifestes et scripts utilisent des chemins relatifs ou des identifiants portables. Les chemins absolus ne peuvent exister qu’en mémoire pendant l’exécution. L’installation reste donc déplaçable et renommable sans réécriture manuelle des sources.

## Addendum 1.2.13 — sélection sûre des archives de débat

Le dossier d’entrée des débats est le dossier unique `incoming/`; aucun sous-dossier `incoming/debates/` n’est utilisé et aucun autre type d’entrée n’y est prévu. Le nom d’une archive est `<debate_id>.zip`. Le suffixe éditorial `release_ready` n’est ni exigé ni interprété comme un identifiant.

Lorsque `incoming/` contient exactement un ZIP, `./wikidebia publish` utilise ce fichier. Lorsqu’il en contient plusieurs, la commande sans identifiant est bloquée et affiche les identifiants disponibles ; `./wikidebia publish IDENTIFIANT` sélectionne uniquement `incoming/IDENTIFIANT.zip`. L’extension `.zip` ne fait pas partie de l’identifiant. Avant extraction durable ou publication, le kit vérifie que le nom du fichier et le champ `debate_id` du manifeste sont identiques.


Les ZIP encore présents dans l’ancien dossier `incoming/debates/` sont migrés automatiquement vers `incoming/` pendant la mise à jour. Toute collision de noms avec un contenu différent bloque l’opération sans écrasement.


## Addendum 1.2.15 — séparation entre le nom du ZIP et l’identité du débat

La révision 1.2.15 corrige le contrôle trop strict introduit en 1.2.13. Le nom du ZIP est un sélecteur de fichier, pas l’identité normative du débat. Lorsque `incoming/` contient un seul ZIP, ce fichier est utilisé quel que soit son nom. Lorsqu’il en contient plusieurs, l’argument de `./wikidebia publish` correspond exactement au nom du ZIP sans l’extension `.zip`.

Après extraction sûre, le champ `manifest.debate_id` devient l’identité autoritative : il détermine le dossier `corpus/<debate_id>`, les plans, les journaux et la configuration de publication. Il peut différer du nom du ZIP. Cette règle rend directement compatibles les archives historiques telles que `education_sexualite_ecole_fr_en_release_ready_repaired_2026-07-31.zip`, sans renommage et sans affaiblir la validation du manifeste ou du corpus.


## Addendum 1.2.16 — reprise distante contrôlée d’un corpus publié

### 1. Nature d’une reprise

La reprise d’un débat déjà publié est une opération distincte d’une publication initiale. Elle compare trois états : la dernière version effectivement publiée par Wikidéb’IA, l’état distant courant et le nouveau corpus validé. Le plan classe chaque page dans une et une seule catégorie : `create`, `skip`, `update`, `move`, `redirect`, `delete`, `manual_review` ou `blocked`.

Le nouveau manifeste ne constitue jamais, à lui seul, une preuve d’appartenance historique. Une page absente du nouveau corpus ne peut être retirée que si un état publié antérieur signé atteste qu’elle appartenait au même `debate_id` et à la même langue.

### 2. État publié et source de vérité

Après chaque publication ou reprise réussie, le kit conserve un état publié signé par débat et par langue. Cet état contient au minimum : `debate_id`, langue, version du corpus, date de publication, titre canonique, identifiant logique, type de page, empreinte SHA-256 du contenu, identifiant de révision MediaWiki, statut et référence du reçu final. Le dernier reçu local et cet état sont prioritaires. À défaut, le kit peut utiliser le dernier manifeste installé ou archivé, ou un inventaire distant en lecture seule explicitement rattaché au débat. Il refuse toute suppression si aucune de ces preuves n’est disponible.

Les pages retirées sont calculées par différence entre les pages attestées de la dernière version publiée et les pages du nouveau corpus. Chaque retrait conserve l’ancien identifiant, l’ancienne empreinte, la dernière révision connue, le motif (`suppression`, `fusion`, `renommage` ou `remplacement`), la cible éventuelle et le résultat de la vérification distante.

### 3. Mises à jour et modifications humaines

Une mise à jour automatique est autorisée uniquement lorsque la page appartient au même débat dans les deux versions, que son identité logique est conservée ou explicitement migrée, que l’état distant courant correspond à la dernière empreinte ou révision publiée par Wikidéb’IA, que le nouveau corpus a été validé et que le plan signé est verrouillé. L’écriture MediaWiki utilise un contrôle de concurrence tel que `baserevid` ou un horodatage de base. Toute modification intervenue après la préparation du plan bloque l’écriture.

Le kit distingue un état distant inchangé, une publication automatisée ultérieure connue, une modification humaine et une provenance indéterminée. Une modification humaine ou indéterminée est classée `manual_review`. Le rapport fournit l’ancienne version publiée, la version distante courante et la nouvelle version proposée. Aucun écrasement n’est effectué par défaut.

### 4. Retraits, renommages et fusions

Avant une suppression, le kit vérifie cumulativement l’appartenance historique, l’absence du nouveau corpus, l’absence de réutilisation connue par un autre débat, l’absence de déplacement ou d’autonomisation, la concordance de la révision et de l’empreinte distantes avec l’état publié attendu, la présence des marqueurs Wikidéb’IA et le droit MediaWiki `delete`. Une divergence postérieure classe la page `manual_review`. Le kit ne remplace jamais une suppression par un bandeau de demande de suppression.

Un changement de titre conservant l’identité logique produit une opération `move`. Une fusion déclare sa cible et une politique explicite `redirect` ou `delete`; les liens entrants sont relevés dans le plan. Une ancienne page ne reste pas active sans relation déclarée avec le nouveau graphe.

### 5. Plan, ordre et reprise

Le plan distant contient les huit listes d’opérations, leurs préconditions, les empreintes anciennes et nouvelles, la révision distante attendue, la justification et le résultat. Sa sérialisation est déterministe, son empreinte SHA-256 est enregistrée et l’exécution réelle exige la confirmation de cette empreinte ou un mécanisme automatisé équivalent explicitement sécurisé.

L’ordre normal est : validation complète; comparaison distante en lecture seule; signature du plan; création ou mise à jour de la page Débat/Debate; création des arguments; mise à jour des arguments conservés; déplacements et redirections; vérification du graphe publié; suppressions finales; reçu final et nouvel état publié. Une erreur avant la vérification du graphe interdit les suppressions finales.

Toutes les opérations sont idempotentes. Une nouvelle exécution reconnaît les créations, mises à jour, déplacements et suppressions déjà achevés, et bloque les pages modifiées entre-temps. Les commandes canoniques sont `./wikidebia update IDENTIFIANT`, avec les portées `--scope fr`, `--scope en`, `--no-delete`, `--only-delete` et `--dry-run`. La mise à niveau des composants est exposée séparément par `./wikidebia upgrade`.

### 6. Droits, authentification et séparation des responsabilités

Les droits requis sont contrôlés avant la première écriture : `edit` et `createpage` pour créer ou modifier, `move` pour déplacer, `delete` pour supprimer, et, lorsque nécessaire, `browsearchive` ou `deletedhistory` pour consulter l’historique supprimé. Aucun groupe administrateur n’est exigé si les droits effectifs sont attribués à un groupe plus limité ou au compte bot. L’absence de `delete` arrête une portée comportant des suppressions avant toute écriture et sans invite Pywikibot interactive.

La reprise réutilise la famille `wikidebates`, la configuration privée `private/pywikibot/`, les BotPasswords et le traitement séquentiel des langues. Les erreurs de connexion sont journalisées proprement. Le validateur reste strictement local et en lecture seule : il contrôle les schémas et la cohérence d’un plan, d’un état ou d’un reçu, mais ne compare ni ne modifie le wiki.

### 7. Sécurité et généralité

Aucune constante active ne dépend d’un débat pilote, d’un titre, d’un nombre de pages ou d’une date de migration particulière. Aucun secret n’est incorporé aux archives. Les plans, journaux, reçus et états publiés conservent les résultats de chaque opération. Le cas `education_sexualite_ecole` peut servir de test d’intégration externe, mais ne constitue ni une règle ni une configuration embarquée.

## Addendum 1.2.17 — Wikipédia, débats connexes, auteurs et publication non interactive

La révision 1.2.17 rend bloquante l’absence d’article Wikipédia dans les pages Débat/Debate, interdit l’émission des paramètres de débats connexes, impose la conversion des listes JSON d’auteurs en texte MediaWiki et supprime l’invite interactive de la commande `./wikidebia publish`. Le plan SHA-256 reste calculé, verrouillé et transmis automatiquement au moteur d’exécution ; la suppression de l’invite ne supprime donc ni le plan signé ni les contrôles de concurrence.


## Correction 1.2.18 — séparateur canonique des auteurs

La conversion d’un tableau JSON d’auteurs vers le wikicode emploie la virgule suivie d’une espace comme séparateur canonique : `Auteur 1, Auteur 2`. Le point-virgule, la virgule sans espace, la virgule précédée d’une espace et la virgule pleine chasse sont interdits dans les sorties générées. Une liste d’un seul élément reste une valeur scalaire et une liste vide entraîne l’omission du paramètre. Cette correction ne réinterprète pas rétroactivement les paquets qui demeurent déclarés sous la norme 1.2.17 ; leur provenance est conservée, mais toute nouvelle production ou migration vers 1.2.18 doit appliquer la forme canonique.

## 1.2.19 — 1er août 2026

La révision 1.2.19 corrige l’interprétation trop permissive des titres affichés. Un `titre-affiché` / `displayed-title` doit désormais être une proposition argumentative complète, et non un simple groupe nominal ou un thème abrégé. Le contexte peut raccourcir le cadrage, mais ne peut supprimer ni le prédicat ni la conclusion qui rendent l’argument intelligible. La revue individuelle atteste cette complétude dans les deux langues et le validateur 0.4.21 bloque les libellés manifestement non propositionnels sous cette seule révision.


## Compléments normatifs de la révision 1.2.23

1. Il n’existe pas de règle de capitalisation différente entre le français et l’anglais pour le complément du sujet : `sujet-complet` et `complete-topic` sont tous deux insérés après un en-tête déjà commencé et prennent donc normalement une minuscule initiale.
2. Le libellé court `sujet`/`topic` est conceptuel et nominal. Par exemple, `Réalité indépendante des perceptions` devient `Réalisme philosophique`, puis `sujet-complet=le réalisme philosophique`; l’anglais correspondant est `topic=Philosophical realism` et `complete-topic=philosophical realism`.
3. Les contrôles de redondance documentaire portent sur toutes les occurrences de références, y compris dans les pages Argument. Une égalité auteur-site déclenche obligatoirement une seconde recherche d’attribution ; elle ne peut subsister dans la sortie finale.
4. Les reprises distantes emploient par défaut le résumé de modification court `Corrections`, sans identifiant technique ni empreinte de manifeste.
5. Une livraison complète reste directement utilisable comme unique fichier de mise à niveau et contient donc les trois ZIP de composants à sa racine.


## Addendum 1.2.24 — liens Wikipédia explicatifs au survol

La révision 1.2.24 autorise et encadre `{{Lien Wikipédia}}` dans les contenus d’introduction et les résumés français, ainsi que `{{Wikipedia link}}` dans leurs équivalents anglais. Le modèle porte un paramètre obligatoire `article`; le paramètre d’affichage est `texte-affiché` en français et `displayed-text` en anglais. Une simple différence de majuscule initiale se traite dans `article` sans paramètre d’affichage. L’usage est limité à la première occurrence utile d’une notion réellement spécialisée, après vérification de la page dans la langue correspondante. Ces liens n’ont aucune valeur de citation et ne remplacent ni les références factuelles ni l’explication du raisonnement.

## Addendum 1.2.25 — exécution sûre des reprises et staging des archives

Une reprise distante distingue strictement le **plan**, l’**exécution**, le **corpus actif** et l’**état publié**. Les catégories `blocked` et `manual_review` désignent toutes deux des opérations non résolues. Leur présence interdit toute écriture MediaWiki, toute création d’un reçu de succès et toute réécriture de `.state/published/`. Cette barrière est appliquée à la fois par le gestionnaire de commande et par l’exécuteur du plan signé, afin qu’un appel direct à l’exécuteur ne puisse la contourner.

Un plan composé uniquement de `skip` ne constitue pas une exécution. La commande renvoie un statut explicite `no_changes`; elle ne produit pas de reçu d’exécution et ne réécrit pas l’état publié. L’état publié n’est renouvelé qu’après l’application et la vérification d’au moins une opération exécutable parmi `create`, `update`, `move`, `redirect` et `delete`.

`--dry-run` est sans effet sur le corpus actif. Lorsqu’une archive est utilisée pour préparer une reprise, elle est extraite dans une zone temporaire de staging située sous `.state/`. Le plan référence cette copie immuable; `corpus/<debate_id>/` n’est remplacé qu’après une exécution réelle réussie ou après une exécution réelle concluant à `no_changes`, à condition qu’aucune opération `blocked` ou `manual_review` ne subsiste. Une simulation ne promeut jamais le staging.

`./wikidebia update <debate_id>` vise en priorité le corpus déjà installé. Une archive de même nom présente dans `incoming/` ne peut plus le remplacer implicitement. La sélection d’une archive est explicite avec `./wikidebia update --archive <sélecteur>`; son nom reste un sélecteur de fichier et `manifest.debate_id` demeure l’identité autoritative. La commande affiche avant planification la source réellement utilisée et l’identifiant interne du débat.

Les archives génériques de normes, de validateur, de kit et le bundle complet de composants ne contiennent aucun corpus de débat. Un corpus peut être livré séparément uniquement lorsqu’il est explicitement demandé.

## Addendum 1.2.26 — attestation sans changement, sélection stricte et portées différées

La disposition 1.2.25 selon laquelle un plan composé uniquement de `skip` ne réécrit jamais l’état publié est remplacée. Un tel plan ne constitue toujours pas une exécution mutante et ne produit aucune écriture MediaWiki. Il donne toutefois lieu à une **attestation signée `no_changes`** : l’exécuteur recharge le plan signé, relit chaque page distante, vérifie son identité exacte avec le corpus local et enregistre les identifiants de révision réellement observés. Ce n’est qu’après cette relecture complète que le reçu `no_changes` et le nouvel état publié signé sont écrits. Une divergence entre le plan et le wiki bloque l’attestation. Cette actualisation empêche qu’un ancien état local transforme à tort une modification ultérieure en `manual_review`.

La sélection d’une archive de reprise est strictement explicite. Sans `--archive`, `./wikidebia update <debate_id>` ne consulte que `corpus/<debate_id>/`; si ce corpus est absent, la commande s’arrête en indiquant d’utiliser `--archive`. Une archive unique dans `incoming/` n’est jamais sélectionnée implicitement, même lorsqu’aucun corpus n’est installé. Lorsque plusieurs corpus sont installés et qu’aucun identifiant n’est fourni, la commande les énumère et refuse de choisir.

Toute zone de staging créée pour une archive est supprimée à la fin de la commande, qu’il s’agisse d’un dry-run, d’un plan bloqué, d’une révision manuelle, d’une attestation `no_changes`, d’une exécution réussie ou d’une erreur. Le corpus actif n’est promu qu’après une attestation `no_changes` réussie ou l’application réussie des opérations sélectionnées.

La décision de poursuivre dépend des opérations mutantes incluses dans la portée demandée. Si le plan contient des opérations mutantes mais qu’aucune n’appartient à la portée choisie, la commande renvoie `no_changes_in_scope`, ne lance pas l’exécuteur et ne promeut pas un corpus placé en staging.

Une reprise effectuée avec `--no-delete` conserve dans l’état publié signé les pages attestées de l’état antérieur dont la suppression est différée. Elles portent le statut `pending_delete`, restent attribuées à leur débat et sont relues pour vérifier qu’elles n’ont pas changé. Une exécution ultérieure avec `--only-delete` peut ainsi retrouver et supprimer ces pages en appliquant toutes les protections habituelles. L’état final ne les retire qu’après leur suppression effectivement vérifiée.



## Addendum 1.2.27 — rendu bilingue déterministe, citations traduites et liens interlangues directs

Le rendu final part exclusivement des verrous éditoriaux français et anglais scellés. Il ne réinterprète pas le graphe, ne change aucun identifiant, aucune relation ni aucune occurrence, et produit une copie distincte du corpus traduit. Le graphe et les titres canoniques sont verrouillés avant l’émission des fichiers MediaWiki.

Une page française dont `translation_status.en=deferred` ne contient aucun paramètre `interlangue`. Dès que la traduction est `ready` ou `published`, chaque page française `Débat` ou `Argument` contient exactement un `{{Lien interlangue|langue=en|page=…}}` visant le titre canonique anglais verrouillé. Les pages anglaises ne contiennent jamais de paramètre `interlangue`.

Les citations d’une page Argument française sont rendues dans `citations=` sous la forme de modèles `{{Citation}}`. Leur projection anglaise est rendue dans `quotes=` avec le modèle anglais `Quote`. Pour chaque citation anglaise :

1. chaque nom de paramètre français est remplacé par son nom anglais déclaré : `citation→quote`, `auteurs→authors`, `ouvrage→work`, `numéro→issue`, `localisation→location`, `édition→publisher`, `lieu→place`, `lien→link` et `avertissements-citation→warnings`; les noms identiques dans les deux langues (`article`, `volume`, `page`, `date`) restent identiques ;
2. seule la valeur de `quote`, issue de `citation`, est traduite ;
3. la valeur de `date` est traduite dans la langue anglaise sans changer la date représentée ; une année seule reste inchangée ;
4. toutes les autres valeurs documentaires sont conservées exactement, dans le même ordre conceptuel ;
5. le paramètre `warnings` contient la mention exacte `Citation traduite par IA` ;
6. si un avertissement existe déjà, la mention est ajoutée après sa valeur avec exactement une virgule et une espace : `Avertissement existant, Citation traduite par IA` ;
7. la mention n’est jamais dupliquée ; un paramètre vide est traité comme absent.

Le registre de traduction, les verrous de contenu, le rendu et le validateur comparent la liste ordonnée complète des paramètres après application de cette table de correspondance. Toute valeur documentaire modifiée, tout nom de paramètre français conservé dans la page anglaise, toute date différente, toute citation omise ou ajoutée, ou tout avertissement absent, dupliqué ou mal séparé bloque la validation.


## Addendum 1.2.28 — resynchronisation corrective des documents actifs

La règle historique qui interdisait de générer `citations=` et `quotes=` sur les pages Argument est remplacée à compter de 1.2.27. Elle ne peut plus apparaître comme règle active dans le cahier des charges, le catalogue d’exigences ou les profils de rendu. Les corpus antérieurs restent interprétés selon leur révision déclarée.

La désignation du modèle anglais est `{{Quote}}`. La règle transitoire 1.2.29 qui conservait les noms de paramètres français est remplacée par 1.2.31 : la page anglaise utilise exclusivement les paramètres anglais déclarés, tandis que les valeurs documentaires restent conservées sauf `quote` et `date`.

Lorsqu’un ancien wikicode importé utilise le paramètre générique `avertissements=` à l’intérieur d’un modèle `Citation`, l’import peut le reconnaître comme alias historique. Cette normalisation est explicite avant le verrouillage éditorial ; elle ne permet aucune modification silencieuse des autres paramètres. Après verrouillage, seul `avertissements-citation` est rendu.


## Addendum 1.2.29 — modèle anglais Quote pour les citations traduites (règle de paramètres remplacée)

La révision 1.2.29 a correctement restauré le nom du modèle anglais `{{Quote}}`, mais a conservé à tort les noms de paramètres français dans ce modèle. Cette partie est remplacée par la révision 1.2.31. Les corpus déjà rendus sous 1.2.29 doivent être rendus de nouveau avant publication.

## Addendum 1.2.31 — localisation complète des modèles et paramètres anglais

Toute page anglaise utilise exclusivement les modèles et paramètres déclarés sur le wiki anglais. La traduction d’une page française ne consiste donc pas à copier son wikicode et à traduire seulement la prose : le modèle principal, ses paramètres, les sous-modèles et leurs paramètres sont projetés selon le contrat anglais actif.

Pour les citations, `{{Citation}}` devient `{{Quote}}` et la table canonique est : `citation→quote`, `auteurs→authors`, `article→article`, `ouvrage→work`, `volume→volume`, `numéro→issue`, `page→page`, `localisation→location`, `édition→publisher`, `lieu→place`, `date→date`, `lien→link`, `avertissements-citation→warnings`. Seules les valeurs de `quote` et de `date` sont traduites. Toutes les autres valeurs sont conservées exactement. La valeur de `warnings` reprend l’avertissement antérieur, le cas échéant, puis ajoute une unique mention `Citation traduite par IA` avec le séparateur exact `, `.

Un paramètre source sans équivalent anglais déclaré bloque la traduction ; il n’est jamais recopié sous son nom français. Le validateur refuse tout modèle français ou paramètre français dans une page anglaise rendue sous 1.2.31.

## Addendum 1.2.34 — publication française autonome et traduction anglaise différée

Cet addendum remplace toute disposition antérieure imposant le verrouillage préalable d'un titre anglais ou l'insertion immédiate d'un lien interlangue. Il s'applique uniquement lorsqu'un paquet déclare explicitement :

```json
{
  "translation_status": {
    "en": "deferred"
  }
}
```

### États autorisés

- `pending` : la traduction est planifiée ; les contraintes anglaises dépendent des champs déjà verrouillés ;
- `deferred` : la traduction anglaise n'a pas commencé et aucun titre anglais n'est requis ;
- `ready` : les contenus anglais et leurs titres sont préparés et soumis aux contrôles bilingues ;
- `published` : les contenus anglais sont publiés et restent soumis aux mêmes contrôles stricts.

### Règles de l'état `deferred`

1. le titre canonique anglais peut être absent, nul ou `unassigned` ;
2. le titre affiché anglais peut être absent ;
3. la cible interlangue anglaise peut être nulle ;
4. le paramètre `interlangue` est absent du wikicode français ;
5. aucune page anglaise n'est exigée dans le manifeste ;
6. les contrôles d'équivalence bilingue ne s'exécutent pas ;
7. les contrôles des résumés, références, sections, keywords et relations anglaises sont différés ;
8. `WDV-WF-005` n'est pas émis du seul fait de l'absence d'un titre anglais ;
9. `publish` ou `update --scope fr` est autorisé ;
10. le kit n'invente aucun titre anglais et n'insère aucun lien fictif.

### Incohérences toujours bloquantes

Restent bloquants : un état de titre anglais `locked` avec titre absent ; un `{{Lien interlangue}}` vide ; une cible différente du titre verrouillé ; une page anglaise présente dans le manifeste sans titre anglais valide ; un statut `ready` ou `published` sans contenus anglais complets ; et toute portée anglaise lorsque l'état reste `deferred`. Un lien interlangue valide déjà présent sur une page préexistante n'est jamais supprimé automatiquement ; il reste soumis aux contrôles stricts.

### Passage ultérieur à l'anglais

Après traduction, le paquet passe de `deferred` à `ready` ou `published`, verrouille les titres anglais, ajoute les pages anglaises au manifeste, réactive les contrôles bilingues et ajoute les liens interlangues français par une reprise explicite. La date de création française reste inchangée.

## Addendum 1.2.35 — compatibilité historique de la traduction différée et conservation des données importées

Le statut `translation_status.en=deferred` est une déclaration opérationnelle distincte de la révision éditoriale du corpus. Lorsqu'il est explicitement présent, il s'applique à toute révision 1.2.x prise en charge par le validateur courant. Son ajout ne constitue pas une migration normative et ne déclenche pas rétroactivement les règles éditoriales introduites après la révision déclarée du corpus. En l'absence de cette déclaration, les corpus historiques conservent leurs exigences bilingues strictes.

Dans ce mode, la portée française n'exige ni titre anglais, ni page anglaise, ni lien interlangue. Toute portée anglaise reste bloquée. Un statut anglais `locked`, `ready` ou `published`, une page anglaise présente dans le manifeste ou un lien interlangue français déjà rendu réactivent les contrôles stricts correspondants.

La politique normale est `editorial_controls.creation_date_policy=per_page_preserved`, y compris lorsque ce champ est omis. La date déclarée dans chaque entrée du manifeste est autoritative pour cette page et doit correspondre exactement au wikicode canonique et au registre. Une page déjà présente sur le wiki conserve sa date historique lors de toute correction, reprise, traduction tardive, déplacement ou enrichissement : elle n’a jamais à adopter la date du corpus ni la date du jour. `single_active_date` reste disponible uniquement comme option explicite pour un corpus neuf et homogène.

Une décision explicite du propriétaire peut conserver des titres affichés hérités identiques à leurs titres canoniques. Cette exception est fermée : elle exige un fichier de revue séparé, une décision non vide, la liste exhaustive des identifiants concernés et la preuve que chaque titre est déjà verrouillé et exactement identique. Le seuil normal de 10 % continue de s'appliquer à toutes les pages non couvertes.

## Addendum 1.2.38 — atomicité des mots-clés et originalité effective des résumés

La révision 1.2.38 remplace la tolérance antérieure fondée principalement sur une longueur maximale de quatre mots. Un mot-clé doit désormais nommer un concept atomique ; les expressions longues ne sont admises que comme dénominations lexicalisées justifiées individuellement dans le vocabulaire contrôlé. Les mini-rubriques productives, notamment `limites de la science`, `histoire des religions` et `construction des lois scientifiques`, sont refusées lorsqu’une forme conceptuelle simple existe. `Lois de la nature` reste conforme comme locution encyclopédique lexicalisée, sous réserve de l’attestation d’exception correspondante.

Les résumés sont contrôlés à la fois page par page et à l’échelle du corpus. Les charpentes génériques, le métadiscours, l’énumération des titres enfants et la répétition d’une même phrase dans quatre pages ou davantage sont bloquants. Le registre de revue consigne `mechanism_statement`, extrait réellement présent qui formule le mécanisme propre au nœud, et `originality_reviewed=true`. La capitalisation de `Dieu` comme nom propre est également vérifiée dans les résumés français.


### Profil éditorial rétrocompatible

Ces contrôles peuvent être appliqués à un corpus historique sans migration globale de sa révision normative. Le manifeste déclare alors `editorial_controls.quality_policy_revision=1.2.38`. Cette déclaration active exclusivement l’atomicité sémantique des mots-clés, l’originalité effective des résumés et la vérification de la majuscule de `Dieu`; elle ne rend pas rétroactives les autres exigences introduites après la révision déclarée du corpus. Le vocabulaire contrôlé et la revue des résumés portent eux aussi `quality_policy_revision=1.2.38`, tandis que leur champ `normative_revision` continue de correspondre à la révision propre du corpus.



## Addendum 1.2.39 — conservation des contenus historiques et séparation des politiques éditoriales

Une correction ciblée ne confère jamais l'autorisation de réécrire les autres champs d'une page. Lorsqu'un corpus historique est repris pour corriger les mots-clés, les résumés, citations, références, relations et métadonnées existants restent inchangés, sauf décision explicite du propriétaire visant précisément l'un de ces champs. Une amélioration stylistique supposée ne constitue pas une autorisation.

Le verrou distingue la provenance du champ et non seulement celle de la page. Une page importée peut contenir un résumé historique déjà rédigé, qui doit être conservé exactement, ou ne contenir aucun résumé, auquel cas le résumé produit ultérieurement par le Work reste un contenu généré et n'est pas rendu immuable au seul motif que la page elle-même est ancienne. Le registre emploie `summary_provenance=historical_existing` ou `summary_provenance=generated_after_import`; seuls les résumés de la première catégorie sont verrouillés. Le contenu historique verrouillé est conservé même s'il ne satisfait pas une heuristique stylistique ou une règle de wikicode introduite après sa rédaction ; ces contrôles ne peuvent servir à forcer sa modification. La conformité exigée porte alors sur l'identité avec la source attestée.

Le paramètre `initialisation` demeure interdit sur une page Argument entièrement nouvelle. En revanche, lorsqu'il existait dans la page historique importée, il constitue une donnée de provenance et doit être conservé exactement. Il ne peut être supprimé, remplacé ou normalisé. Le même principe s'applique à `initialization` dans un corpus anglais historique.

Un corpus peut déclarer `editorial_controls.legacy_content_preservation`. Le fichier verrou indiqué contient, pour chaque page protégée, l'empreinte du résumé historique et l'état exact du paramètre `initialisation` ou `initialization`. Le validateur autorise ce paramètre uniquement pour les pages répertoriées et bloque toute divergence avec le verrou.

Les contrôles éditoriaux renforcés sont désormais activables séparément sur un corpus historique :

- `keyword_policy_revision=1.2.39` active l'atomicité des mots-clés ;
- `summary_policy_revision=1.2.39` active les contrôles d'originalité des résumés ;
- `capitalization_policy_revision=1.2.39` active le contrôle de la majuscule du nom propre `Dieu`.

L'ancien champ combiné `quality_policy_revision=1.2.38` reste accepté pour compatibilité et conserve son comportement historique. Il ne doit plus être employé lorsqu'une correction ne porte que sur une partie de ces contrôles. Pour un nouveau corpus déclarant directement la norme 1.2.39, les trois politiques sont actives par défaut.


## Addendum 1.2.40 — absence historique attestée des résumés

L’absence d’un résumé dans une page Argument historique est un état de contenu qui peut être conservé lorsqu’elle est prouvée par l’inventaire source en lecture seule. Elle ne doit pas être comblée par un texte générique uniquement pour satisfaire une structure de sortie.

Le verrou de contenu emploie alors `summary_provenance=historical_absent`. Cette valeur n’est recevable que si toutes les conditions suivantes sont réunies :

1. la page est présente dans l’inventaire historique attesté ;
2. le paramètre `résumé` ou `summary` y est réellement absent ;
3. le manifeste active `legacy_content_preservation` et la politique `historical_summary_absence_revision=1.2.40` ;
4. la page produite omet entièrement le paramètre, sans valeur vide ni texte provisoire ;
5. la revue individuelle consigne `status=historical_absent` et `historical_absence_verified=true`.

Cette dérogation est fermée. Elle ne s’applique jamais à une page nouvelle, à une page absente de l’inventaire, ni à un résumé déjà présent dans la source. Un résumé ajouté ultérieurement après un véritable travail éditorial reçoit la provenance `generated_after_import` et redevient obligatoire, contrôlé et révisable comme tout contenu généré.

Les résumés historiques réellement présents restent classés `historical_existing` et demeurent verrouillés à l’identique. Les contrôles de gabarit, d’originalité et de style ne servent ni à créer un résumé fictif sur une page historiquement vide, ni à réécrire rétroactivement un résumé historique protégé.


## Addendum 1.2.41 — mots-clés simples et sélection implicite non ambiguë des reprises

### Mots-clés des pages nouvelles

Pour une page nouvellement produite, le mot-clé retient le concept de navigation le plus simple qui conserve le sens utile. Un adjectif ou complément qui rappelle seulement le sujet du débat ne crée pas une catégorie autonome. Lorsque `Dieu` figure déjà parmi les mots-clés, `liberté divine`, `justice divine`, `attributs divins` ou `révélation divine` deviennent normalement `liberté`, `justice`, `attributs` ou `révélation`. De même, une doctrine employée seulement comme cadrage d’une question plus générale peut être ramenée à son domaine : `épistémologie réformée` devient `épistémologie`.

Cette simplification ne détruit pas les dénominations lexicalisées. Une locution reste entière lorsqu’elle désigne un concept reconnu qui ne se reconstitue pas sans perte par la juxtaposition de termes plus généraux. `Croyance fondamentale`, `dilemme d’Euthyphron`, `pari de Pascal`, `problème du mal`, `simplicité divine` et `effondrement modal` peuvent ainsi être conservés.

Une correction ciblée des pages nouvelles ne modifie pas les mots-clés des pages historiques, sauf décision séparée du propriétaire.

### Sélection d’une archive pour `update`

La sélection strictement explicite imposée en 1.2.26 est remplacée par la règle suivante :

1. si `incoming/` contient exactement un ZIP, `./wikidebia update` sélectionne ce ZIP, l’extrait en staging et utilise le `debate_id` de son manifeste ;
2. si plusieurs ZIP sont présents, la commande sans identifiant refuse de choisir et affiche leurs sélecteurs ; `./wikidebia update IDENTIFIANT` sélectionne exactement `incoming/IDENTIFIANT.zip` ;
3. si aucun ZIP n’est présent, la commande revient au corpus installé : elle sélectionne l’unique corpus disponible ou exige son identifiant lorsqu’il y en a plusieurs ;
4. lorsqu’un identifiant correspond à la fois à un ZIP entrant et à un corpus installé, le ZIP entrant est prioritaire, puisqu’il représente la nouvelle version demandée ;
5. `--archive` reste accepté pour compatibilité, mais n’est plus nécessaire dans le cas non ambigu ;
6. lorsque `--scope` est omis, la portée est déduite des langues validées et non différées du corpus : `fr` pour un corpus français dont l’anglais est différé, `all` lorsque les deux langues sont publiables ; une portée explicite n’est requise que pour imposer volontairement un autre choix.

Le staging, le dry-run, les plans signés, les contrôles de concurrence et les protections contre les modifications humaines restent inchangés.
