# Wikidéb’IA — Source active unifiée

Ce fichier est la source textuelle active générée par `./wikidebia upgrade`. Il remplace les anciennes sources séparées consacrées aux normes, au validateur et au kit.

- norme active : **1.2.54** ;
- validateur actif : **0.4.57** ;
- kit actif : **2.15.31**.

## Composants associés

- `wikidebia-normes.zip` — 1892672 octets — SHA-256 `740164d06bb4fe01f0f33def289d3fc6a6667ddfca21bac6251e0d9f3e9f07a2`
- `wikidebia-validator.zip` — 2172536 octets — SHA-256 `17a7e75dee87e6f535477dfc2492d087b943ce9c77a9a62cd8c4069d6bd01d4c`
- `wikidebia-kit.zip` — 435071 octets — SHA-256 `584498aaa771f6ee096dc2f99fb2f32ed8fd62d551905b18f3388ad597d39676`

## Norme consolidée active

Source interne : `norms/normative_reference/01_normes/WIKIDEBIA_NORME_CONSOLIDEE_1.2.54.md`  
SHA-256 : `221044078ac148dfc0f5f717fa38036c39615a6f366a31669a2a941dce3cef17`

# Norme consolidée Wikidéb’IA 1.2.54

> **Révision 1.2.54 — architecture cumulative des normes éditoriales.** Les règles éditoriales actives de la présente norme consolidée s’appliquent désormais indépendamment de la valeur déclarée dans `normative_versions.consolidated_norm`. Ce numéro reste une métadonnée de provenance, de compatibilité de format, de migration et de publication ; il n’est plus un interrupteur de fonctionnalités éditoriales. De même, les champs historiques `*_policy_revision`, `*_revision`, `argument_name_assignment_revision`, `argument_name_discovery_revision` ou analogues, lorsqu’ils sont encore présents, servent uniquement à la traçabilité et ne peuvent ni activer ni désactiver un contrôle. L’application des règles dépend de l’état fonctionnel constaté : présence d’un registre ou d’un chemin de revue, origine d’une page, statut de traduction, activation de la préservation historique avec inventaire attesté, ou version propre d’un artefact. Les anciennes formulations « activée pour la révision X » sont conservées comme historique mais sont remplacées par cette architecture pour toute validation courante. Les règles de traduction anglaise 1.2.53 restent inchangées.

> **Correctif actif du 7 août 2026 — traduction FR→EN source-authoritative et métadonnées.** Lors de la production éditoriale anglaise, la page anglaise cible est ignorée comme source de contenu : la page française validée est traduite comme si la cible anglaise n'existait pas. Les valeurs françaises réellement présentes de `avancement`, `avertissements-titre`, `avertissements-débat` et `avertissements-argument` sont traduites par une table FR→EN exhaustive ; aucune valeur de création par défaut ne peut les remplacer et un paramètre absent reste absent. Les débats connexes français ne sont projetés dans `related-debates` que si la page anglaise correspondante existe réellement ; aucun débat connexe étranger à la source française n'est ajouté. Chaque lot de traduction fait enfin l'objet d'une seconde passe explicite de comparaison FR→EN. Ce correctif précise et, pour la phase de traduction, prévaut sur les profils génériques de création lorsqu'ils prescrivent des valeurs par défaut.

> **Révision 1.2.50 — séparation création / modification.** Les listes de paramètres générés ou non générés définies par les profils de rendu ne valent que pour la création automatisée d’une page à partir de zéro. Lorsqu’une page `Débat` ou `Argument` existe déjà, en français comme en anglais, sa modification obéit à un contrat de préservation : tout paramètre top-level autorisé qui était présent dans l’état historique ou distant attesté reste présent, même si le workflow de création ne l’aurait pas généré. Les paramètres de cycle de vie et d’avertissement sont traités comme des métadonnées opaques et ne peuvent recevoir une valeur par défaut de génération. Une suppression n’est admise que si elle est explicitement décidée et enregistrée pour la page et le paramètre concernés, ou si une exception normative spécialisée l’autorise (par exemple l’omission locale de relations sur une frontière `débat-détaillé`). Les mêmes principes s’appliquent aux pages de débat.


> **Révision 1.2.51 — attribution éditoriale explicite de `nom` / `name`.** La protection historique introduite en 1.2.49 reste la règle par défaut : une absence historique de `nom` ou `name` n’est jamais comblée automatiquement. Une exception étroite est désormais admise lorsqu’une décision éditoriale explicite du propriétaire attribue à une page Argument une appellation consacrée dans la littérature. Le corpus déclare alors un registre dédié par `editorial_controls.argument_name_assignment_path`. Le champ historique `argument_name_assignment_revision`, s’il est encore présent, n’est qu’une trace de provenance. Ce registre identifie chaque page, la langue, le titre canonique, la valeur exacte à ajouter et la justification. L’inventaire historique reste inchangé et continue d’attester l’absence antérieure ; l’attribution éditoriale constitue une couche de décision séparée. Le validateur exige une concordance exacte entre le registre et le wikicode. Lors d’une reprise, le kit peut ajouter uniquement ce paramètre sur les pages listées, sans relâcher la préservation des autres paramètres historiques.
> **Révision 1.2.52 — recherche documentaire des noms consacrés des arguments nouveaux.** Pour chaque page `Argument` réellement nouvelle, la génération examine explicitement si le raisonnement possède une appellation conventionnelle reconnue dans la littérature. Cette recherche est obligatoire, mais l’ajout de `nom` / `name` reste exceptionnel : la présomption est l’absence de nom consacré. Aucun quota, objectif de remplissage ou dérivation depuis le titre n’est admis. Une appellation n’est retenue que si des sources de référence ou académiques l’emploient pour désigner substantiellement le même raisonnement dans la langue de la page, ou sous une forme étrangère elle-même consacrée. La revue consigne les requêtes, le résultat et, lorsqu’un nom est retenu, les attestations documentaires. Le validateur exige une couverture exacte de toutes les pages Argument nouvelles et une concordance stricte avec le wikicode.
> **Révision 1.2.53 — traduction anglaise par lots et adaptation documentaire.** La production anglaise est menée comme une adaptation éditoriale contrôlée, non comme une substitution lexicale. La page `Debate` constitue un lot autonome. Les pages `Argument` sont ensuite traitées par lots de vingt pages par défaut, sans dépasser vingt-cinq ; un lot documentairement dense est réduit à dix à quinze pages. Chaque argument est achevé dans un seul lot, qui inclut la traduction idiomatique, la recherche séparée de `name=`, la vérification des équivalents anglais des références françaises, la recherche de nouvelles références anglophones et le traitement des modèles `Quote`. Une référence française n’est jamais traduite artificiellement : elle n’est projetée comme référence anglaise que si une édition, traduction ou version anglaise réelle est vérifiée, avec ses métadonnées propres. Des références anglaises nouvelles sont recherchées indépendamment. L’exception documentaire des modèles `Citation` importés reste stricte : `Citation` devient `Quote`, seuls le texte de `quote` et la forme linguistique de `date` sont traduits, les autres valeurs sont conservées exactement, et `Citation traduite par IA` est ajouté à `warnings`. Une passe inter-lots finale vérifie la cohérence globale avant finalisation.


**Statut :** source normative active unique  
**Date d’effet :** 7 août 2026  
**Domaine :** production, validation et préparation à la publication de débats bilingues français–anglais sous MediaWiki  
**Remplace comme sources actives séparées :** révision 1.0.6, correctif du 23 juillet 2026 et décisions correctives du 25 juillet 2026. Ces documents restent conservés dans `history/` à titre de provenance.


> **Révision 1.2.49.** Cette révision protège le paramètre historique `nom` des pages `Argument` françaises et `name` de leurs équivalents anglais. Lorsqu’un tel paramètre existe dans une page importée ou préexistante, sa présence et sa valeur sont conservées exactement : il ne peut être supprimé, renommé, réécrit, normalisé ni remplacé par le titre canonique. Lorsqu’il était absent, le moteur n’en invente pas. L’état de présence et la valeur sont consignés dans les paramètres préservés et, pour les corpus historiques, dans le verrou de contenu confronté à l’inventaire source.

> **Révision 1.2.48.** Cette révision permet d’intégrer sans contournement les modifications manuelles explicitement approuvées par le propriétaire. Un registre local peut attester une révision distante précise, par identifiant de révision et/ou empreinte SHA-256, puis autoriser une modification contrôlée à partir de cette base. Le plan reste bloqué si la page a changé depuis l’attestation. Les paramètres de cycle de vie demeurent protégés, sauf autorisation nominative dans le registre. Cette procédure ne transforme jamais une modification humaine inconnue en mise à jour automatique.

> **Révision 1.2.47.** Cette révision protège les frontières vers un débat détaillé. Lorsqu’un paramètre historique `débat-détaillé` ou `detailed-debate` existe, il est conservé exactement dans la sortie. La présence de cette frontière autorise l’omission des paramètres locaux `justifications` et `objections`, mais uniquement lorsque cette omission est consignée dans le verrou historique et que le propriétaire en a été informé. Le validateur compare la cible du débat détaillé à la source attestée et ne confond plus l’arrêt du parcours du graphe avec la suppression du paramètre de la page.

> **Révision 1.2.46.** Cette révision remplace le contrôle trop étroit des seules « notions voisines de même rang » introduit en 1.2.45. La revue porte désormais sur toutes les notions spécialisées ou potentiellement opaques de chaque sous-partie d’introduction. Pour chaque notion identifiée, elle consigne un traitement vérifiable : lien Wikipédia à la première occurrence utile, explication intégrée, renvoi à une explication antérieure, ou justification précise que le contexte suffit. Chaque sous-partie possède un inventaire exhaustif attesté. Le validateur vérifie la concordance entre cet inventaire, le texte visible, les liens réellement présents et les traitements antérieurs déclarés. La cohérence entre notions voisines demeure une conséquence de cette revue générale, non son objet principal.

> **Révision 1.2.45.** Cette révision impose la cohérence locale des liens Wikipédia explicatifs. Lorsque plusieurs notions spécialisées de même rang sont énumérées ou comparées dans un même passage, la revue les traite comme un ensemble : si l’une reçoit `{{Lien Wikipédia}}` ou `{{Wikipedia link}}`, les autres reçoivent le même traitement lorsqu’un article vérifié existe et que le besoin explicatif est comparable. Toute asymétrie doit être justifiée notion par notion dans le registre de revue. Cette règle évite les liens ajoutés de manière ponctuelle ou arbitraire sans transformer le texte en glossaire.

> **Révision 1.2.44.** Cette révision règle la ponctuation terminale des notes `<ref>`. Une simple notice bibliographique, sitographique ou vidéographique ne reçoit pas de point final avant `</ref>` ; la ponctuation de la phrase porte après l’appel de note. Un point à l’intérieur de la balise n’est admis que lorsque le contenu de la note constitue lui-même une phrase explicative complète. Toute exception est attestée dans la revue de l’introduction.

> **Révision 1.2.43.** Cette révision corrige la politique d’introduction 1.2.42 : une sous-partie explicitement consacrée aux enjeux du débat est obligatoire. Elle ne doit cependant pas être un remplissage abstrait. Elle expose des conséquences déterminées des principales réponses possibles, précise ce que la conclusion changerait pour la compréhension du sujet et reste distincte d’un catalogue des arguments pour et contre. La revue consigne au moins deux enjeux concrets et atteste la non-redondance de la rubrique.

> **Révision 1.2.42.** Cette révision supprime quatre contraintes mécaniques qui dégradaient les pages : les sources présentant plusieurs positions sont classées dans la documentation neutre et ne sont jamais dupliquées entre orientations ; les vidéos YouTube indiquent leur créateur ou leur chaîne ; les introductions sont évaluées par leur densité informative plutôt que par une liste fixe de rubriques ; et le titre canonique peut rester le titre affiché lorsqu’il est déjà le plus clair. Toute reformulation distincte doit améliorer réellement la lecture sans modifier la thèse.

> **Révision 1.2.41.** Cette révision applique deux décisions du propriétaire. Premièrement, les mots-clés des pages nouvelles doivent employer les concepts de navigation les plus simples : un qualificatif qui ne fait que rappeler le contexte de la page est supprimé (`liberté divine` devient `liberté` à côté de `Dieu`; `épistémologie réformée` devient `épistémologie`). Les locutions qui désignent réellement un concept autonome, telles que `croyance fondamentale`, restent intactes. Deuxièmement, `./wikidebia update` sélectionne automatiquement l’unique ZIP présent dans `incoming/` et déduit la portée des langues réellement publiables (`fr` lorsque l’anglais est différé, `all` lorsque les deux langues sont prêtes) ; un identifiant ou une portée explicite n’est exigé qu’en cas d’ambiguïté ou de choix volontaire différent.

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

Chaque titre affiché fait l'objet d'une décision éditoriale page par page. Le titre canonique est conservé à l'identique lorsqu'il est déjà clair, complet et suffisamment lisible : cette identité est un choix normal, non une exception statistique, et aucun quota n'impose de reformuler les titres. Un titre affiché distinct n'est retenu que si la nouvelle formulation améliore concrètement la lecture tout en conservant exactement le sujet, le prédicat, la modalité, la relation logique, la portée et le degré de force du titre canonique.

Toute différence est consignée dans le registre individuel avec une justification propre au nœud et à la langue. La revue atteste l'équivalence sémantique et l'amélioration réelle de lisibilité. Une reformulation seulement plus courte, plus vague, plus catégorique ou plus imagée est refusée. La concision ne prime jamais sur la précision ; lorsqu'aucune meilleure formulation n'est évidente, le titre affiché reprend le titre canonique.

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

La bibliographie est généralement prioritaire. La sitographie et la vidéographie sont complémentaires. La sélection documentaire s’adapte au domaine de l’argument : publications scientifiques et synthèses pour les questions empiriques, textes officiels et doctrine pour le droit, sources primaires et travaux historiques pour l’histoire, œuvres et commentaires académiques pour la philosophie, données et rapports institutionnels pour les politiques publiques, ou toute autre source de référence adaptée au sujet. Les pages Argument ne remplissent pas de quotas : chaque famille documentaire peut contenir zéro, une ou plusieurs références selon son apport réel. Les pages Débat et Debate répartissent les références selon leur orientation réelle, sans quota par paramètre. Une source qui développe substantiellement des arguments favorables et défavorables, présente un débat contradictoire ou offre une synthèse générale appartient à la position `ni-pour-ni-contre` / neutre. Une même référence ne figure jamais simultanément dans plusieurs orientations. Une rubrique peut rester vide ou contenir une seule référence lorsqu'aucune autre source réellement pertinente n'est disponible ; elle n'est jamais remplie artificiellement pour équilibrer le tableau.

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
6. des conséquences ou enjeux uniquement lorsqu'ils apportent une information précise indispensable à la compréhension de la controverse.

D’autres sous-parties peuvent être ajoutées lorsqu’elles apportent un élément réellement nécessaire à la compréhension du sujet. Aucune liste thématique propre à un débat particulier ne devient une structure universelle applicable mécaniquement aux autres débats.

Les sous-parties suivent une progression compréhensible pour un lecteur qui découvre le sujet. Chacune répond à une question identifiable et son utilité pour la compréhension du débat apparaît dès ses premières phrases. Une sous-partie technique, consacrée par exemple à une méthode, un indicateur, un cadre juridique ou un mécanisme spécialisé, n’est introduite que si le texte explique pourquoi cet élément est déterminant pour la question débattue.

Les titres de sous-parties privilégient les formulations accessibles et informatives. Ils évitent les intitulés spécialisés ou abstraits dont le rapport avec le débat n’est pas immédiatement compréhensible.

Dans le contenu des sous-parties, une notion spécialisée dont la définition est utile mais secondaire peut être rendue explicite au survol avec `{{Lien Wikipédia}}` en français ou `{{Wikipedia link}}` en anglais. Le modèle est réservé aux notions qui risqueraient réellement d’arrêter un lecteur non spécialiste. Il ne sert ni à lier chaque nom propre, chaque institution ou chaque terme courant, ni à remplacer les explications nécessaires au sens de la question débattue.

La sélection des liens est précédée d’une revue sémantique complète de chaque sous-partie. La revue inventorie toute notion scientifique, philosophique, juridique, religieuse, historique ou technique qui pourrait arrêter un lecteur non spécialiste. Pour chaque notion, elle choisit et justifie un traitement :

- `wikipedia_link` lorsque le premier paragraphe d’un article vérifié fournit l’éclaircissement secondaire utile ;
- `explained_inline` lorsque le sens nécessaire au débat doit être formulé directement dans la prose ;
- `prior_treatment` lorsque la notion a déjà été liée ou expliquée dans une sous-partie antérieure et qu’un nouveau lien serait redondant ;
- `context_sufficient` seulement lorsque le passage rend déjà le sens immédiatement intelligible, avec une justification propre à la notion.

Chaque sous-partie possède une ligne d’inventaire, même lorsqu’aucune notion spécialisée n’y est retenue. L’attestation globale `specialized_terms_linked_or_explained=true` ne suffit plus. L’inventaire reproduit l’ordre des sous-parties, nomme les notions effectivement présentes et permet de vérifier tous les liens Wikipédia rendus. Les notions voisines de même rang sont naturellement traitées de manière cohérente, mais une série n’est plus nécessaire pour déclencher la revue.

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

Le nombre de sous-parties et le volume documentaire dépendent de la complexité, de l’étendue du sujet et de l’abondance de la littérature disponible. Il n’existe pas de minimum universel de cinq sous-parties ni de vingt références. Le profil local peut déclarer des minima adaptés, accompagnés d’une justification non vide ; ces minima ne doivent jamais conduire à fragmenter artificiellement l’introduction ou à ajouter des sources sans apport réel. Inversement, une page portant sur une controverse abondamment documentée ne doit pas s’arrêter à une sélection symbolique ou minimale. Chaque famille applicable (bibliographie, sitographie et vidéographie) fait l’objet d’un examen séparé. Pour une page Débat ou Debate, les paramètres documentaires restent présents mais peuvent être vides lorsque l'orientation correspondante n'offre pas de source suffisamment pertinente. Le volume total reste proportionné à l'abondance et à la qualité de la littérature. La classification suit le contenu effectif de la ressource et non un objectif de symétrie numérique.

Chaque sous-partie substantielle contient les appels de référence inline nécessaires pour soutenir les affirmations factuelles qui exigent une attribution. Dans les introductions française et anglaise, chaque appel développé est rédigé directement en wikicode lisible à l’intérieur de `<ref>…</ref>`, sans passer par un modèle MediaWiki. Les modèles `{{Référence}}`, `{{Reference}}`, les modèles bibliographiques, sitographiques ou vidéographiques spécialisés et tout autre modèle de citation sont interdits dans le corps d’une note d’introduction. La note indique directement les éléments utiles à l’identification de la source — auteur, titre, publication ou site, date en langage naturel, pagination et lien selon le cas. Une simple notice documentaire est traitée comme une notice et non comme une phrase : elle ne se termine donc pas par un point avant `</ref>`. Le signe de ponctuation de la phrase principale vient après l’appel de note (`texte<ref>Notice sans point final</ref>.`). Un point final reste admis à l’intérieur de la balise uniquement si la note contient une véritable phrase explicative complète, et cette exception est consignée dans la revue de l’introduction. Une référence nommée peut être définie sous la forme `<ref name="…">contenu rédigé directement</ref>` puis réutilisée avec `<ref name="…" />`. Les appels français sont placés avant la ponctuation finale ; les appels anglais suivent la convention anglaise. Les balises `<references />` et `<references>` ne sont jamais ajoutées : l’affichage des notes est géré par le wiki. Les mêmes sources peuvent également figurer dans les listes documentaires structurées de la page lorsque l’appel inline attribue une affirmation précise.

Aucun nombre minimal d’appels `<ref>` n’est imposé à l’introduction dans son ensemble ni à une sous-partie particulière. Une introduction principalement définitionnelle, conceptuelle ou argumentative peut donc ne contenir aucun appel inline lorsqu’elle ne formule aucune affirmation factuelle externe nécessitant une attribution. Le contrôle porte sur l’adéquation entre les affirmations présentes et leurs sources, non sur la présence mécanique d’au moins une référence.

Avant `release_ready`, une revue humaine bilingue consigne pour chaque langue que le sujet et le périmètre sont définis, que le sens de la question est expliqué, que l’histoire et l’actualité sont traitées lorsqu’elles sont pertinentes, que chaque sous-partie apporte une information distincte et nécessaire, que la progression est logique, qu’une section technique est contextualisée et que l’introduction ne reproduit ni le graphe ni une checklist propre à un corpus pilote. Une rubrique générique sur les « enjeux », la « lecture du débat » ou les « principales lignes de contestation » est supprimée lorsqu'elle se contente d'énumérer des thèmes déjà visibles dans le graphe ou d'énoncer des conséquences évidentes sans information nouvelle.

### 7.6 Sélection de la bibliographie des pages de débat

La bibliographie d’une page Débat ou Debate constitue une sélection de référence sur l’ensemble de la controverse. Elle privilégie les livres incontournables, monographies, manuels, volumes collectifs, rapports de synthèse et articles de revue réellement panoramiques. Les articles scientifiques consacrés à une expérience, un protocole ou un résultat étroit appartiennent aux pages Argument concernées et ne sont pas accumulés dans la bibliographie générale du débat.

Chaque usage bibliographique du débat indique s’il s’agit d’une œuvre fondatrice ou d’une synthèse large, ainsi qu’une justification de sélection. Une source étroite ou dépourvue de justification est bloquante.

### 7.7 Métadonnées sitographiques et conversion des auteurs

`auteurs=` ou `authors=` n’est émis que lorsqu’une personne ou une organisation est explicitement responsable du contenu. À défaut, le paramètre est omis ; le nom du site n’est jamais recopié mécaniquement comme auteur. La vérification de l’attribution est enregistrée.

Le registre JSON conserve `authors` sous forme de liste, mais cette liste ne doit jamais être sérialisée littéralement dans le wikicode. La conversion vers MediaWiki est obligatoire : une liste d’un élément devient le texte brut de cet élément (`["L'Encyclopédie philosophique"]` devient `|auteurs=L'Encyclopédie philosophique`) ; plusieurs éléments sont séparés par une virgule suivie d’une espace (`Auteur 1, Auteur 2`) ; une liste vide entraîne l’omission du paramètre. Les crochets, guillemets et virgules syntaxiques du JSON ne sont jamais publiés.

Lorsque le titre de la page et le nom du site sont identiques, seul `site=` est conservé. Les triples identiques `page`, `auteurs` et `site` sont interdits.

Pour toute référence vidéographique YouTube, `auteurs=` / `authors=` indique le créateur ou le nom de la chaîne affiché par la plateforme. Le champ n'est pas omis lorsque cette attribution est directement visible sur la page de la vidéo. Le titre de la vidéo, la plateforme et la chaîne remplissent des fonctions distinctes : le nom de YouTube n'est pas utilisé comme auteur.

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

Lors de la création d’une page de débat réellement nouvelle hors traduction, Wikidéb’IA ne produit pas `débats-connexes` ni `related-debates`. Lors de la modification d’une page préexistante hors protocole de retraduction, le paramètre est conservé exactement s’il existe déjà, avec sa valeur antérieure ; il reste absent s’il n’existait pas. **Exception FR→EN : pendant la traduction éditoriale d’une page française, `related-debates` est reconstruit uniquement à partir des entrées françaises de `débats-connexes` dont la page anglaise correspondante est vérifiée comme existante ; les autres sont omises et aucun nouveau débat connexe n’est inventé.**

### 8.0 Création et modification des paramètres protégés

Le manifeste de chaque page déclare `page_origin` (`new` ou `preexisting`) ainsi qu’un instantané de présence et de valeur des paramètres protégés. Pour une page nouvelle, les structures ci-dessous indiquent les valeurs générées. Pour une page préexistante, ces lignes sont conditionnelles :

- `avancement` / `progress` conserve exactement sa valeur antérieure et reste absent s’il était absent ;
- `avertissements-débat` / `debate-warnings` conserve exactement sa valeur antérieure et reste absent s’il était absent ;
- `avertissements-argument` / `argument-warnings` conserve exactement sa valeur antérieure et reste absent s’il était absent ;
- `débats-connexes` / `related-debates` conserve exactement sa valeur antérieure et reste absent s’il était absent.

Le moteur de mise à jour bloque toute opération qui modifierait l’un de ces paramètres sur une page existante.

**Exception de production éditoriale FR→EN :** les règles de préservation distante ci-dessus ne servent pas à choisir le contenu de la traduction. Pour produire la page anglaise, la source française prévaut et les métadonnées mappées sont traduites depuis elle. La préservation distante reste une contrainte technique distincte au moment d’une éventuelle publication.

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

Lorsqu’une page historique contient `|débat-détaillé=…`, ce paramètre est conservé exactement. Il est placé après `objections` et avant `rubriques`. Les paramètres `justifications` et `objections` peuvent être omis sur cette page frontière, même si le registre conserve des relations nécessaires au graphe général, à condition que l’omission et l’information donnée au propriétaire soient attestées dans le verrou historique. L’arrêt du parcours au débat détaillé ne permet jamais de supprimer silencieusement le paramètre.

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

The `progress=Constructed debate` and `debate-warnings=Debate generated by AI` lines apply only to a genuinely new Debate generated from scratch. **They do not apply to an English page produced as a translation of an existing French Debate:** in that workflow, `progress`, `title-warnings` and `debate-warnings` are translated from the exact French source values according to the active FR→EN mapping, and an absent source parameter remains absent. The editorial translation ignores any pre-existing English target page as a source of content.

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

Dans une traduction FR→EN, `argument-warnings=Argument generated by AI` n'est pas ajouté par défaut au seul motif que le fichier anglais vient d'être généré. `title-warnings` et `argument-warnings` sont traduits uniquement à partir des valeurs françaises présentes selon la table normative active ; un paramètre absent en français reste absent en anglais.

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

Le validateur courant conserve les contrôles éditoriaux cumulés indépendamment de la révision normative historique déclarée et maintient séparément la compatibilité technique de lecture avec les formats historiques annoncés. Chaque règle binaire nouvelle possède au moins un test positif et un test négatif. Les nombres de tests, exigences et fichiers déclarés dans les reçus doivent correspondre aux éléments réellement livrés.

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
13. utiliser `createonly` pour chaque création canonique ; une mise à jour interlangue distincte n’est admise que par le workflow fonctionnel prévu après préparation de la langue cible et reste interdite tant que cette traduction est `deferred` ;
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

La configuration de publication exécute toutes les portées applicables du validateur courant, notamment `wikicode` et `editorial` lorsque des pages sont publiées. Le kit refuse une configuration qui omet une portée obligatoire du profil actif.

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

La révision 1.2.8 ne modifie aucune exigence éditoriale de 1.2.6. Elle exige que chaque étiquette de provenance effectivement utilisée par le catalogue soit déclarée dans `source_aliases` et résolve vers au moins un fichier livré. Elle aligne les exemples actifs sur la révision courante, corrige leur langue et impose que les schémas actifs couvrent correctement les formats historiques pris en charge, sans utiliser leur numéro comme interrupteur éditorial. Les contrôles d’auto-audit doivent vérifier ces trois propriétés.


## Addendum 1.2.9 — références, acronymes et publication française indépendante

La révision 1.2.9 corrige cinq défauts observés lors d’une production réelle :

1. les dates documentaires complètes sont rendues en langage naturel, tandis que les dates de création restent au format machine ;
2. les appels inline des introductions sont rédigés directement dans `<ref>…</ref>` sans modèle de citation ;
3. chacun des neuf paramètres documentaires d’une page Débat ou Debate contient au moins deux références ;
4. un acronyme courant est employé dans `sujet-complet` ou `complete-topic` et déclaré dans le registre de revue ;
5. le kit peut publier les pages françaises avant la création des pages anglaises, à condition que les titres anglais soient verrouillés dans le registre maître et correspondent aux liens interlangues français.


## Addendum 1.2.10 — notes d’introduction rédigées directement

La règle 1.2.9 qui imposait le modèle générique `Référence`/`Reference` est remplacée. La règle introduite en 1.2.10 s’applique cumulativement : le corps d’une note développée d’introduction contient directement une référence bibliographique ou web lisible, sans aucun appel de modèle MediaWiki. Les références nommées restent admises, à condition que leur première définition soit rédigée directement. Le validateur refuse tout `{{…}}` dans le corps d’une note d’introduction et continue de refuser les dates documentaires au format machine.

Exemple français conforme :

```mediawiki
Une affirmation documentée<ref>Jean Dupont, « Titre de l’article », ''Nom de la revue'', 25 juin 2012, p. 36-37, [https://example.org texte intégral].</ref>.
```

Exemple anglais conforme :

```mediawiki
A documented claim.<ref>Jane Smith, “Article title”, ''Journal Name'', 25 June 2012, pp. 36–37, [https://example.org full text].</ref>
```


## Addendum 1.2.11 — compaction des modèles MediaWiki adjacents

La règle introduite en 1.2.11 s’applique à tout wikicode de page produit : deux modèles immédiatement successifs sont accolés sans saut de ligne, espace ni tabulation entre la fermeture du premier et l’ouverture du second. La forme `}}` suivie d’un retour à la ligne puis de `{{` est interdite ; elle est remplacée par `}}{{`. Cette règle vaut en français et en anglais, dans les pages individuelles comme dans les agrégats. Elle ne change ni le contenu des modèles ni l’ordre des paramètres : elle impose seulement une jonction compacte et déterministe entre sous-modèles adjacents.

Le validateur 0.4.13 et le kit 2.1.13 sont les versions historiques qui ont introduit les contrôles correspondants. Dans la norme cumulative courante, cette règle s’applique à tout corpus traité, indépendamment de la valeur déclarée de `consolidated_norm` ; cette valeur reste une métadonnée de provenance et de compatibilité de lecture, non un interrupteur éditorial.

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

La conversion d’un tableau JSON d’auteurs vers le wikicode emploie la virgule suivie d’une espace comme séparateur canonique : `Auteur 1, Auteur 2`. Le point-virgule, la virgule sans espace, la virgule précédée d’une espace et la virgule pleine chasse sont interdits dans les sorties générées. Une liste d’un seul élément reste une valeur scalaire et une liste vide entraîne l’omission du paramètre. La provenance des anciens paquets reste conservée, mais toute validation ou production courante applique cette forme canonique indépendamment de la révision historique déclarée, sous réserve des protections explicites de contenu historique prévues ailleurs dans la norme.

## 1.2.19 — 1er août 2026

La révision 1.2.19 corrige l’interprétation trop permissive des titres affichés. Un `titre-affiché` / `displayed-title` doit désormais être une proposition argumentative complète, et non un simple groupe nominal ou un thème abrégé. Le contexte peut raccourcir le cadrage, mais ne peut supprimer ni le prédicat ni la conclusion qui rendent l’argument intelligible. La revue individuelle atteste cette complétude dans les deux langues et le validateur courant bloque les libellés manifestement non propositionnels quelle que soit la révision historique déclarée.


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

La règle historique qui interdisait de générer `citations=` et `quotes=` sur les pages Argument est remplacée à compter de 1.2.27. Elle ne peut plus apparaître comme règle active dans le cahier des charges, le catalogue d’exigences ou les profils de rendu. Les archives antérieures conservent leur révision comme information de provenance et de lecture de format ; après interprétation, la règle éditoriale courante s’applique cumulativement.

La désignation du modèle anglais est `{{Quote}}`. La règle transitoire 1.2.29 qui conservait les noms de paramètres français est remplacée par 1.2.31 : la page anglaise utilise exclusivement les paramètres anglais déclarés, tandis que les valeurs documentaires restent conservées sauf `quote` et `date`.

Lorsqu’un ancien wikicode importé utilise le paramètre générique `avertissements=` à l’intérieur d’un modèle `Citation`, l’import peut le reconnaître comme alias historique. Cette normalisation est explicite avant le verrouillage éditorial ; elle ne permet aucune modification silencieuse des autres paramètres. Après verrouillage, seul `avertissements-citation` est rendu.


## Addendum 1.2.29 — modèle anglais Quote pour les citations traduites (règle de paramètres remplacée)

La révision 1.2.29 a correctement restauré le nom du modèle anglais `{{Quote}}`, mais a conservé à tort les noms de paramètres français dans ce modèle. Cette partie est remplacée par la révision 1.2.31. Les corpus déjà rendus sous 1.2.29 doivent être rendus de nouveau avant publication.

## Addendum 1.2.31 — localisation complète des modèles et paramètres anglais

Toute page anglaise utilise exclusivement les modèles et paramètres déclarés sur le wiki anglais. La traduction d’une page française ne consiste donc pas à copier son wikicode et à traduire seulement la prose : le modèle principal, ses paramètres, les sous-modèles et leurs paramètres sont projetés selon le contrat anglais actif.

Pour les citations, `{{Citation}}` devient `{{Quote}}` et la table canonique est : `citation→quote`, `auteurs→authors`, `article→article`, `ouvrage→work`, `volume→volume`, `numéro→issue`, `page→page`, `localisation→location`, `édition→publisher`, `lieu→place`, `date→date`, `lien→link`, `avertissements-citation→warnings`. Seules les valeurs de `quote` et de `date` sont traduites. Toutes les autres valeurs sont conservées exactement. La valeur de `warnings` reprend l’avertissement antérieur, le cas échéant, puis ajoute une unique mention `Citation traduite par IA` avec le séparateur exact `, `.

Un paramètre source sans équivalent anglais déclaré bloque la traduction ; il n’est jamais recopié sous son nom français. Le validateur courant refuse tout modèle français ou paramètre français dans une page anglaise rendue, quelle que soit la révision normative historique déclarée.

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

Le statut `translation_status.en=deferred` est une déclaration opérationnelle distincte de la révision éditoriale du corpus. Lorsqu’il est explicitement présent, il suspend uniquement les obligations fonctionnelles liées à la production anglaise. Il ne désactive aucune autre règle éditoriale courante. En l’absence de cette déclaration, les exigences bilingues strictes s’appliquent.

Dans ce mode, la portée française n'exige ni titre anglais, ni page anglaise, ni lien interlangue. Toute portée anglaise reste bloquée. Un statut anglais `locked`, `ready` ou `published`, une page anglaise présente dans le manifeste ou un lien interlangue français déjà rendu réactivent les contrôles stricts correspondants.

La politique normale est `editorial_controls.creation_date_policy=per_page_preserved`, y compris lorsque ce champ est omis. La date déclarée dans chaque entrée du manifeste est autoritative pour cette page et doit correspondre exactement au wikicode canonique et au registre. Une page déjà présente sur le wiki conserve sa date historique lors de toute correction, reprise, traduction tardive, déplacement ou enrichissement : elle n’a jamais à adopter la date du corpus ni la date du jour. `single_active_date` reste disponible uniquement comme option explicite pour un corpus neuf et homogène.

Une décision explicite du propriétaire peut conserver des titres affichés hérités identiques à leurs titres canoniques. Cette exception est fermée : elle exige un fichier de revue séparé, une décision non vide, la liste exhaustive des identifiants concernés et la preuve que chaque titre est déjà verrouillé et exactement identique. Le seuil normal de 10 % continue de s'appliquer à toutes les pages non couvertes.

## Addendum 1.2.38 — atomicité des mots-clés et originalité effective des résumés

La révision 1.2.38 remplace la tolérance antérieure fondée principalement sur une longueur maximale de quatre mots. Un mot-clé doit désormais nommer un concept atomique ; les expressions longues ne sont admises que comme dénominations lexicalisées justifiées individuellement dans le vocabulaire contrôlé. Les mini-rubriques productives, notamment `limites de la science`, `histoire des religions` et `construction des lois scientifiques`, sont refusées lorsqu’une forme conceptuelle simple existe. `Lois de la nature` reste conforme comme locution encyclopédique lexicalisée, sous réserve de l’attestation d’exception correspondante.

Les résumés sont contrôlés à la fois page par page et à l’échelle du corpus. Les charpentes génériques, le métadiscours, l’énumération des titres enfants et la répétition d’une même phrase dans quatre pages ou davantage sont bloquants. Le registre de revue consigne `mechanism_statement`, extrait réellement présent qui formule le mécanisme propre au nœud, et `originality_reviewed=true`. La capitalisation de `Dieu` comme nom propre est également vérifiée dans les résumés français.


### Profil éditorial rétrocompatible

Ces contrôles font partie de la norme éditoriale cumulative et s’appliquent donc sans migration du numéro de norme déclaré. Les anciens champs `quality_policy_revision` peuvent rester présents comme traces historiques, mais leur présence ou leur valeur ne sélectionne aucun contrôle. Le champ global `normative_revision`, lorsqu’il est conservé dans un registre, décrit la provenance de l’artefact et non l’activation d’une politique.



## Addendum 1.2.39 — conservation des contenus historiques et séparation des politiques éditoriales

Une correction ciblée ne confère jamais l'autorisation de réécrire les autres champs d'une page. Lorsqu'un corpus historique est repris pour corriger les mots-clés, les résumés, citations, références, relations et métadonnées existants restent inchangés, sauf décision explicite du propriétaire visant précisément l'un de ces champs. Une amélioration stylistique supposée ne constitue pas une autorisation.

Le verrou distingue la provenance du champ et non seulement celle de la page. Une page importée peut contenir un résumé historique déjà rédigé, qui doit être conservé exactement, ou ne contenir aucun résumé, auquel cas le résumé produit ultérieurement par le Work reste un contenu généré et n'est pas rendu immuable au seul motif que la page elle-même est ancienne. Le registre emploie `summary_provenance=historical_existing` ou `summary_provenance=generated_after_import`; seuls les résumés de la première catégorie sont verrouillés. Le contenu historique verrouillé est conservé même s'il ne satisfait pas une heuristique stylistique ou une règle de wikicode introduite après sa rédaction ; ces contrôles ne peuvent servir à forcer sa modification. La conformité exigée porte alors sur l'identité avec la source attestée.

Le paramètre `initialisation` demeure interdit sur une page Argument entièrement nouvelle. En revanche, lorsqu'il existait dans la page historique importée, il constitue une donnée de provenance et doit être conservé exactement. Il ne peut être supprimé, remplacé ou normalisé. Le même principe s'applique à `initialization` dans un corpus anglais historique.

Un corpus peut déclarer `editorial_controls.legacy_content_preservation`. Le fichier verrou indiqué contient, pour chaque page protégée, l'empreinte du résumé historique et l'état exact du paramètre `initialisation` ou `initialization`. Le validateur autorise ce paramètre uniquement pour les pages répertoriées et bloque toute divergence avec le verrou.

Les contrôles éditoriaux renforcés sont désormais activables séparément sur un corpus historique :

Les anciens champs `keyword_policy_revision`, `summary_policy_revision`, `capitalization_policy_revision` et `quality_policy_revision` restent acceptés pour la compatibilité des artefacts déjà produits. Ils ne servent plus à activer séparément ces contrôles : atomicité des mots-clés, originalité des résumés et capitalisation du nom propre `Dieu` sont des règles courantes cumulatives. Les générateurs n’émettent plus ces champs lorsqu’ils ne sont utiles qu’à la sélection d’une politique.


## Addendum 1.2.40 — absence historique attestée des résumés

L’absence d’un résumé dans une page Argument historique est un état de contenu qui peut être conservé lorsqu’elle est prouvée par l’inventaire source en lecture seule. Elle ne doit pas être comblée par un texte générique uniquement pour satisfaire une structure de sortie.

Le verrou de contenu emploie alors `summary_provenance=historical_absent`. Cette valeur n’est recevable que si toutes les conditions suivantes sont réunies :

1. la page est présente dans l’inventaire historique attesté ;
2. le paramètre `résumé` ou `summary` y est réellement absent ;
3. le manifeste active `legacy_content_preservation` et fournit l’inventaire historique attestant l’absence du résumé ; le champ historique `historical_summary_absence_revision`, s’il existe, est purement informatif ;
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


## Addendum 1.2.42 — classement documentaire, auteurs vidéo, densité des introductions et titres affichés

La révision 1.2.42 remplace quatre mécanismes qui produisaient des corrections artificielles :

1. aucune référence n'est dupliquée entre les orientations `pour`, `contre` et `ni-pour-ni-contre`; une source exposant plusieurs positions est classée dans la rubrique neutre, sans quota minimal par paramètre ;
2. toute vidéo YouTube indique le créateur ou la chaîne lorsque cette information est affichée par la plateforme ;
3. l'introduction privilégie la densité informative et supprime les sous-parties génériques qui répètent le graphe, notamment les catalogues d'arguments et les rubriques d'enjeux sans information propre ;
4. l'identité entre titre canonique et titre affiché est admise sans plafond. Une reformulation n'est créée que si son amélioration de lisibilité et son équivalence sémantique sont attestées. La longueur plus faible ne constitue jamais, à elle seule, une amélioration.

Ces règles sont cumulatives et s’appliquent également aux corpus historiques. Les anciens champs `debate_documentation_policy_revision`, `video_authorship_policy_revision`, `introduction_policy_revision` et `displayed_title_policy_revision` restent acceptés comme traces, sans effet d’activation. Les titres canoniques et contenus historiques explicitement protégés restent soumis à leurs règles de préservation propres.


## Addendum 1.2.43 — sous-partie obligatoire sur les enjeux du débat

La disposition 1.2.42 qui rendait facultative la présence d’une rubrique d’enjeux est remplacée. Toute introduction de page `Débat` comporte une sous-partie dédiée intitulée `Enjeux du débat`. Toute introduction de page `Debate` comporte la sous-partie fonctionnellement équivalente `Stakes of the debate`.

Cette obligation porte sur une fonction éditoriale réelle, non sur une formule de transition. La sous-partie :

1. indique ce que les principales réponses possibles changeraient dans la compréhension du sujet, les décisions, les pratiques, les institutions ou les critères de rationalité concernés ;
2. développe au moins deux conséquences concrètes propres au débat ;
3. distingue ces conséquences de la simple importance générale du sujet ;
4. ne reproduit pas la liste des arguments pour et contre et ne résume pas successivement les branches du graphe ;
5. ne se contente pas d’une énumération abstraite d’« enjeux philosophiques, sociaux, politiques, éthiques ou économiques » ;
6. reste concise et non redondante avec les autres sous-parties.

La revue d’introduction atteste `stakes_explained=true`, `dedicated_stakes_subsection_present=true`, `stakes_consequences_concrete=true`, `stakes_not_argument_catalogue=true` et `no_generic_stakes_filler=true`. La ligne correspondant à la sous-partie contient `stakes_section=true` et une liste `concrete_stakes` d’au moins deux conséquences distinctes.

Cette correction fait partie de la norme cumulative et ne nécessite aucun changement de numéro déclaré. Un ancien `introduction_policy_revision` peut être conservé comme trace de provenance, sans effet conditionnel.

## Addendum 1.2.44 — ponctuation terminale des notes de référence

Dans une note développée `<ref>…</ref>`, une notice qui se limite à identifier une source n'est pas une phrase. Elle ne reçoit aucun point final avant la fermeture de la balise, même si elle contient un auteur, un titre, une publication, une date, une pagination ou un lien. La ponctuation appartenant à la phrase du texte principal est placée après `</ref>` en français, conformément à la règle générale sur la position de l'appel de note.

Exemple conforme :

```mediawiki
Une affirmation documentée<ref>Jean Dupont, « Titre de l’article », ''Nom de la revue'', 25 juin 2012, p. 36-37, [https://example.org texte intégral]</ref>.
```

Exemple non conforme :

```mediawiki
Une affirmation documentée<ref>Jean Dupont, « Titre de l’article », ''Nom de la revue'', 25 juin 2012, p. 36-37, [https://example.org texte intégral].</ref>.
```

Un point final à l'intérieur de `<ref>` n'est admis que lorsque le corps de la note est lui-même une phrase explicative complète et non une simple notice. La revue de l'introduction atteste `reference_note_punctuation_reviewed=true`. Chaque exception est identifiée par l'empreinte SHA-256 du corps exact de la note dans `terminal_period_sentence_exceptions`, avec `complete_sentence=true` et un extrait justificatif réellement présent.

Cette règle s’applique cumulativement. Un ancien `inline_reference_punctuation_policy_revision` peut être conservé comme trace de provenance, mais n’est ni requis ni utilisé comme interrupteur.

## Addendum 1.2.45 — cohérence locale des liens Wikipédia explicatifs

La décision d’ajouter un lien explicatif ne se prend pas terme par terme sans comparaison avec le passage environnant. Pour toute série de notions spécialisées de même fonction syntaxique et de même niveau conceptuel :

1. la revue inventorie les notions de la série ;
2. elle vérifie l’existence et le titre exact de l’article dans la langue de la page ;
3. si une notion est liée et que les autres présentent un besoin explicatif comparable, toutes les notions disposant d’un article pertinent sont liées ;
4. une notion laissée sans lien dans une série partiellement liée reçoit une justification spécifique ;
5. la revue consigne le titre de la sous-partie, les termes, les articles, la décision et sa justification ;
6. le validateur vérifie que chaque lien déclaré comme retenu est réellement présent dans la sous-partie correspondante.

Exemple conforme :

```mediawiki
Le {{Lien Wikipédia|article=théisme}} affirme un Dieu personnel ; le {{Lien Wikipédia|article=déisme}} retient un créateur sans révélation ; le {{Lien Wikipédia|article=panthéisme}} identifie Dieu au réel ; le {{Lien Wikipédia|article=panenthéisme}} situe le monde en Dieu sans les confondre.
```

Lier seulement `théisme` dans cette série, sans justification propre aux trois autres notions, est non conforme.



## Addendum 1.2.52 — recherche d’une appellation consacrée pour tout argument nouveau

Lorsqu’une page `Argument` est créée par Wikidéb’IA, une recherche documentaire distincte vérifie si le raisonnement possède un nom conventionnel. Cette étape ne cherche pas à fabriquer un sous-titre : elle sert principalement à confirmer que, dans la grande majorité des cas, aucun `nom` / `name` ne doit être ajouté.

La règle active est la suivante :

1. toute page `Argument` nouvelle fait l’objet d’une recherche explicite avant verrouillage du contenu ;
2. la recherche part du raisonnement lui-même (prémisses, mécanisme et conclusion), et non du seul titre canonique ;
3. elle vérifie au minimum deux formulations de recherche suffisamment distinctes ; lorsque la littérature pertinente est internationale, une recherche dans la langue de la page est complétée par une recherche en anglais ou dans la langue académique/originale pertinente ;
4. les sources de référence, encyclopédies spécialisées, livres et articles académiques sont prioritaires ; une page populaire peut orienter la recherche mais ne suffit pas, à elle seule, à consacrer une appellation douteuse ;
5. un nom n’est retenu que lorsque la littérature l’emploie effectivement comme désignation du même raisonnement, de la même objection, défense, preuve, réfutation, paradoxe, problème ou principe argumentatif ;
6. le nom d’une doctrine, d’un thème, d’un auteur, d’un principe seulement mentionné dans le raisonnement ou une reformulation pratique du titre ne constitue pas une appellation consacrée ;
7. la valeur française doit être une appellation française attestée, ou une forme étrangère elle-même couramment employée telle quelle en français ; aucune traduction ad hoc n’est créée pour remplir `nom=` ; la règle symétrique s’applique à `name=` ;
8. en cas d’hésitation entre plusieurs étiquettes, d’attestation trop faible ou de doute sur l’identité du raisonnement, le résultat est `none` et le paramètre est omis ;
9. aucun quota minimal ou maximal de pages nommées n’est fixé. La rareté attendue des noms est une conséquence éditoriale, jamais un seuil statistique ;
10. la revue est enregistrée dans un registre déclaré par `editorial_controls.argument_name_discovery_path` ; l’ancien `argument_name_discovery_revision`, s’il est présent, n’est qu’une métadonnée de traçabilité.

Le registre contient une entrée pour chaque page Argument nouvelle dans chaque langue produite. Il consigne au minimum : la langue, l’identifiant, le titre canonique, les requêtes de recherche, une note sur le périmètre exploré, le résultat `none` ou `known_name`, la valeur retenue le cas échéant, les attestations documentaires, et une justification. Pour `known_name`, il atteste explicitement que la source désigne le même raisonnement, que l’étiquette n’a pas été inventée et qu’elle convient à la langue de la page.

Le validateur bloque : une page nouvelle sans entrée de revue, un `nom` / `name` rendu après un résultat `none`, un nom différent de la valeur attestée, une appellation sans preuve documentaire, ou une revue qui couvre une page préexistante au lieu d’un argument nouveau. Les pages préexistantes restent régies par les règles 1.2.49 et 1.2.51.

## Addendum 1.2.53 — traduction anglaise par lots et adaptation documentaire

La traduction anglaise commence après verrouillage du contenu français et se déroule en unités de travail explicitement closes. Elle vise une page anglaise autonome et idiomatique, substantiellement équivalente au français, tout en adaptant la terminologie et la documentation à la littérature anglophone.

### Ordre et taille des lots

1. la page `Debate` forme à elle seule le premier lot de traduction ; elle n'est mélangée à aucune page `Argument` ;
2. les pages `Argument` sont ensuite traduites par lots de **20 pages par défaut**, avec un **maximum de 25** ;
3. lorsqu'un groupe est particulièrement dense en citations, références, ambiguïtés terminologiques ou recherches de noms consacrés, le lot est réduit à **10–15 pages** ;
4. une page Argument n'est jamais scindée entre deux lots : titre canonique, displayed title, summary, sections, keywords, citations, références et éventuel `name=` sont traités ensemble ;
5. un lot n'est considéré comme clos qu'après vérification de toutes ses pages, de leur orientation argumentative et de leur documentation ; le lot suivant ne sert pas à corriger silencieusement les omissions du précédent ;
6. après le dernier lot d'arguments, une passe globale inter-lots vérifie les choix terminologiques, les titres, le vocabulaire bilingue, les noms consacrés, la documentation, les citations et la parité du graphe avant `--finalize`.

### `name=` : recherche propre à la langue anglaise

Le paramètre français `nom=` n'est jamais traduit mécaniquement. Pour chaque page Argument anglaise, une recherche distincte vérifie l'appellation réellement attestée dans la littérature anglophone pour le même raisonnement. L'existence d'un `nom=` français constitue seulement un indice de recherche, jamais une preuve du nom anglais. Le résultat par défaut reste l'absence de `name=`. Une valeur n'est retenue que si des sources de référence ou académiques anglophones l'emploient effectivement pour désigner substantiellement le même argument, objection, défense, preuve, réfutation, paradoxe, problème ou principe. En cas d'attestation faible, d'équivalence incertaine ou de traduction seulement plausible, `name=` est omis.

### Références : équivalents anglais et enrichissement autonome

Les références françaises ne sont jamais traduites comme notices anglaises. Pour chaque référence française pertinente, la revue recherche s'il existe une **version anglaise réelle et vérifiable** : édition anglaise d'un livre, traduction publiée, version officielle d'une page, version anglaise d'un rapport, doublage ou sous-titrage officiel pertinent d'une vidéo, publication originale anglaise, ou autre équivalent documentaire effectivement disponible en anglais.

Lorsqu'un équivalent anglais existe, la page anglaise utilise la notice de **cette version anglaise**, avec son titre publié, son éditeur ou diffuseur, sa date, son URL et ses autres métadonnées propres. Les métadonnées de la version française ne sont pas transposées ni traduites artificiellement. Lorsqu'aucune version anglaise de la référence française n'existe, cette référence n'est pas transférée en anglais au seul motif qu'elle figurait dans la page française.

La recherche documentaire anglaise ne se limite jamais aux équivalents des sources françaises. Chaque page fait aussi l'objet d'une recherche de **nouvelles références anglophones** pertinentes, afin que sa documentation reflète la littérature disponible en anglais plutôt qu'une simple copie de la sélection française. La sélection conserve les règles ordinaires de pertinence, de non-redondance et de qualité documentaire ; aucun remplissage artificiel n'est admis.

Pour la page `Debate`, toutes les références de l'introduction et des paramètres documentaires doivent être réellement disponibles en anglais. Pour les pages `Argument`, la politique linguistique générale reste symétrique à celle du français, mais la projection d'une référence française vers l'anglais exige toujours l'identification d'un équivalent anglais réel ; une source étrangère éventuellement retenue en anglais doit être sélectionnée et justifiée indépendamment selon les règles générales, et non fabriquée par traduction de la notice française.

### Exception contrôlée : modèles `Citation` / `Quote`

La règle précédente sur l'adaptation des références ne modifie pas le contrat spécial des citations importées. Lors de la projection anglaise, `{{Citation}}` devient `{{Quote}}` et les noms de paramètres sont localisés selon le contrat anglais. **Seules les valeurs de `citation`→`quote` et de `date` sont traduites.** Les valeurs documentaires de `authors`, `article`, `work`, `volume`, `issue`, `page`, `location`, `publisher`, `place` et `link` sont conservées exactement et dans le même ordre. `warnings` reprend tout avertissement existant puis ajoute une seule fois `Citation traduite par IA`, avec le séparateur exact `, `.

Cette exception concerne le contenu d'un modèle de citation déjà importé ; elle n'autorise pas à traduire artificiellement une référence bibliographique, sitographique ou vidéographique pour la faire passer pour une édition anglaise.

## Complément actif 1.2.53-C — source française, métadonnées et débats connexes

### La page anglaise cible n'est pas une source de traduction

Pendant la production éditoriale anglaise, toute éventuelle page anglaise déjà présente sur le wiki est **ignorée comme source de contenu**. Le traducteur travaille à partir du corpus français validé comme si la page cible anglaise n'existait pas : il ne reprend ni sa rédaction, ni son introduction, ni ses titres, ni son `progress`, ni ses avertissements, ni sa documentation, ni ses relations. Une existence distante peut encore être consultée ultérieurement par les mécanismes techniques de publication, de concurrence ou de sécurité ; elle ne modifie pas le contenu éditorial à produire. Les vérifications d'existence de pages tierces nécessaires à `related-debates` restent autorisées.

### Table normative exhaustive des valeurs FR→EN

Pour une traduction, les valeurs ci-dessous sont traduites **uniquement lorsqu'elles sont réellement présentes dans le wikicode français**. Aucune valeur de profil de création n'est injectée à leur place. Un paramètre absent en français est absent en anglais. Pour les champs à cases multiples, toutes les valeurs présentes sont traduites séparément dans le même ordre.

| Paramètre FR | Valeur française | Paramètre EN | Valeur anglaise |
|---|---|---|---|
| `avancement` | `Ébauche` | `progress` | `Draft` |
| `avancement` | `Débat en construction` | `progress` | `Debate under construction` |
| `avancement` | `Débat construit` | `progress` | `Constructed debate` |
| `avertissements-titre` (Débat) | `Titre non standard` | `title-warnings` | `Non-standard title` |
| `avertissements-titre` (Débat) | `Titre à simplifier` | `title-warnings` | `Title to simplify` |
| `avertissements-titre` (Débat) | `Titre à expliciter` | `title-warnings` | `Title to be explained` |
| `avertissements-débat` | `Débat sensible` | `debate-warnings` | `Sensitive debate` |
| `avertissements-débat` | `Débat saugrenu` | `debate-warnings` | `Fanciful debate` |
| `avertissements-débat` | `Débat redondant` | `debate-warnings` | `Redundant debate` |
| `avertissements-débat` | `Débat déséquilibré` | `debate-warnings` | `Unbalanced debate` |
| `avertissements-débat` | `Plan à améliorer` | `debate-warnings` | `Plan to improve` |
| `avertissements-débat` | `Débat généré par IA` | `debate-warnings` | `Debate generated by AI` |
| `avertissements-titre` (Argument) | `Titre désavantageux` | `title-warnings` | `Disadvantageous title` |
| `avertissements-titre` (Argument) | `Titre peu clair` | `title-warnings` | `Unclear title` |
| `avertissements-titre` (Argument) | `Titre incomplet` | `title-warnings` | `Incomplete title` |
| `avertissements-titre` (Argument) | `Titre trop long` | `title-warnings` | `Too long title` |
| `avertissements-argument` | `Argument sensible` | `argument-warnings` | `Sensitive argument` |
| `avertissements-argument` | `Argument saugrenu` | `argument-warnings` | `Fanciful argument` |
| `avertissements-argument` | `Argument potentiellement illégal` | `argument-warnings` | `Potentially illegal argument` |
| `avertissements-argument` | `Argument généré par IA` | `argument-warnings` | `Argument generated by AI` |

Cette table est normative et exhaustive pour les options actuellement autorisées de ces champs. Une valeur française non reconnue n'est jamais traduite par approximation : elle déclenche une revue.

### `related-debates` : intersection avec les pages anglaises existantes

Si la page française possède `débats-connexes`, chaque entrée est examinée individuellement. Une entrée est projetée dans `related-debates` uniquement si la page anglaise correspondant à ce débat existe réellement et si son titre anglais est vérifié. Une entrée sans page anglaise vérifiée est omise. Aucun débat absent de `débats-connexes` n'est ajouté. Si aucune entrée française n'a d'équivalent anglais existant, `related-debates` est omis.

### Seconde passe de vérification obligatoire

Avant la clôture de chaque lot, une passe distincte de la première traduction compare le français et l'anglais. Elle contrôle au minimum : l'absence de reprise de l'ancienne page anglaise cible ; la traduction exacte des métadonnées ci-dessus ; l'absence de valeurs par défaut ajoutées ; le filtrage de `related-debates` par existence réelle des pages anglaises ; la conservation du sens et de la polarité pour/contre ; l'anglais idiomatique ; l'absence de wikicode français résiduel ; la réalité des versions anglaises des références ; et le respect des contrats spéciaux tels que `Citation`→`Quote`. La passe globale inter-lots reprend ces points à l'échelle du corpus.

## Addendum 1.2.51 — attribution éditoriale contrôlée d’un nom consacré

Le paramètre `nom` en français, ou `name` en anglais, reste facultatif et ne doit jamais être déduit mécaniquement du titre canonique, du titre affiché, des mots-clés ou du contenu du résumé. Il sert à afficher l’appellation conventionnelle d’un argument, d’une objection, d’une défense, d’un paradoxe, d’un principe ou d’un problème lorsque cette appellation est réellement reconnue dans la littérature et utile au lecteur.

La règle de préservation 1.2.49 demeure inchangée pour les valeurs historiques existantes. Une page historiquement dépourvue de `nom` / `name` peut toutefois recevoir ce paramètre si, et seulement si, toutes les conditions suivantes sont réunies :

1. le propriétaire du projet a explicitement approuvé l’attribution ;
2. le manifeste déclare `editorial_controls.argument_name_assignment_path` ; l’ancien `argument_name_assignment_revision`, s’il est présent, est une trace sans effet d’activation ;
3. le registre d’attribution identifie exactement la langue, l’identifiant logique, le titre canonique et la valeur de `nom` / `name` ;
4. chaque entrée contient une justification éditoriale non vide attestant qu’il s’agit d’une appellation consacrée et non d’un simple raccourci inventé ;
5. le registre historique reste fidèle à la source et continue d’indiquer que le paramètre était absent lorsqu’il l’était ; il n’est jamais falsifié pour faire passer l’ajout pour une donnée historique ;
6. le wikicode contient exactement la valeur approuvée, dans l’ordre canonique des paramètres : après `initialisation` / `initialization` lorsqu’il est présent, sinon en première position du modèle `Argument` ;
7. aucune page non listée ne peut recevoir un `nom` / `name` absent de sa provenance ;
8. une valeur historique déjà présente reste prioritaire et ne peut être remplacée par ce mécanisme ;
9. lors d’une reprise distante, l’exception porte uniquement sur `nom` / `name` pour les pages listées ; tous les autres paramètres protégés restent soumis à leur état historique ou distant attesté ;
10. une modification ou suppression ultérieure du nom attribué exige une nouvelle décision explicite et ne peut être déduite automatiquement.

Cette politique s’applique dès qu’un registre d’attribution est fonctionnellement déclaré par son chemin. Le validateur contrôle le registre et la concordance du wikicode, tandis que le kit de reprise traite l’attribution comme une dérogation nominative et non comme une normalisation générale. Le numéro historique associé au registre ne modifie pas ce comportement.

## Addendum 1.2.49 — préservation stricte de `nom` / `name`

Le paramètre `nom` d’une page `Argument` française, ou `name` d’une page anglaise, constitue une donnée historique protégée lorsqu’il existe déjà sur la page source ou distante attestée. Il est distinct du titre canonique, du titre affiché et de l’identifiant logique.

1. une page préexistante qui possède `nom` / `name` conserve exactement sa valeur ;
2. le paramètre ne peut être supprimé, vidé, reformulé, normalisé ou recalculé ;
3. un changement de titre canonique ou affiché ne modifie jamais `nom` / `name` ;
4. une page préexistante qui ne possédait pas ce paramètre reste sans ce paramètre ;
5. le manifeste de page enregistre l’état exact de présence et de valeur parmi les paramètres préservés ;
6. lorsqu’un corpus emploie `legacy_content_preservation`, `nom` / `name` peut être ajouté à `protected_fields` et son état est comparé à l’inventaire historique source ;
7. le rendu réémet la valeur historique avant les autres contenus de la page ;
8. toute suppression, modification ou invention non explicitement attestée est bloquante.

Cette protection s’applique aux reprises et aux nouveaux rendus d’un corpus historique. Elle n’oblige pas une page véritablement nouvelle à créer un paramètre `nom` / `name`.

## Addendum 1.2.48 — adoption contrôlée d’une révision manuelle distante

Lorsqu’une page du wiki a été créée ou modifiée manuellement après le dernier état publié signé, elle reste protégée par défaut et produit `manual_review` ou `blocked`. Une décision explicite du propriétaire peut cependant autoriser sa prise en compte comme nouvelle base distante.

Le corpus déclare alors un `manual_remote_adoption_path`. L’ancien champ `manual_remote_adoption_revision`, s’il est présent, reste une trace de provenance sans effet d’activation. Le registre correspondant :

1. identifie exactement le débat, la langue, l’identifiant logique et le titre de chaque page ;
2. atteste la révision distante observée par son identifiant MediaWiki et/ou son empreinte SHA-256 ;
3. explique la provenance et la raison de l’adoption ;
4. indique si le contenu proposé peut différer de la révision adoptée ;
5. énumère nominativement tout paramètre de cycle de vie dont la modification est autorisée ;
6. ne vaut que tant que la révision et l’empreinte distantes correspondent encore à l’attestation ;
7. est validé localement avant la construction du plan et incorporé au plan signé ;
8. n’autorise aucune page non listée et ne réduit aucune protection contre les modifications humaines ultérieures.

Lorsque la page distante correspond déjà au corpus, elle est classée `skip` et peut être incorporée au nouvel état publié après l’attestation finale. Lorsqu’elle diffère et que la modification proposée est autorisée, elle est classée `update` avec la révision adoptée comme `baserevid`. Toute divergence postérieure bloque l’exécution.

Cette procédure est distincte d’une modification manuelle de `.state/published/`, qui reste interdite. Elle est également distincte d’une normalisation silencieuse : les différences proposées et les éventuelles modifications de paramètres protégés sont explicites dans le registre et dans le plan.

Une adoption peut aussi déclarer des **relations externes préservées** lorsque la page distante contient une justification ou une objection visant une page qui n’appartient pas au graphe local du débat. Ces relations sont reproduites dans le wikicode et contrôlées par leur type, leur titre canonique et leur titre affiché, mais elles ne créent ni nœud, ni occurrence, ni page à publier dans le corpus courant. Cette exception est nominative et ne vaut que pour la page adoptée.

## Addendum 1.2.47 — préservation des frontières vers un débat détaillé

Une page `Argument` peut contenir `débat-détaillé` en français ou `detailed-debate` en anglais. Ce paramètre désigne un débat autonome qui développe la question portée par la page.

Lorsqu’il existe dans une page historique importée :

1. sa présence et sa valeur sont conservées exactement dans toutes les sorties ultérieures ;
2. il est inscrit dans le verrou de contenu historique et confronté à l’inventaire source ;
3. le parcours du graphe peut s’arrêter à cette frontière sans traverser les relations locales de la page ;
4. `justifications` et `objections` peuvent être omis dans le wikicode rendu afin de laisser le débat détaillé porter le développement ;
5. cette omission est explicitement enregistrée page par page ;
6. le verrou atteste que le propriétaire a été informé de la suppression des relations locales ;
7. l’omission dans le wikicode ne supprime pas nécessairement les relations du registre maître, lorsqu’elles restent utiles au graphe général ou à d’autres occurrences ;
8. une cible modifiée, un paramètre supprimé, une omission non déclarée ou une frontière ajoutée sans provenance est bloquant.

Le moteur d’extraction conserve toujours la cible de la frontière dans ses données. Le moteur de rendu réémet le paramètre historique et omet les relations locales seulement lorsque la décision est verrouillée. Pour un corpus historique, cette règle est déterminée par la présence attestée de `débat-détaillé` ou `detailed-debate`, par `legacy_content_preservation` et par son verrou de contenu ; aucun numéro de norme ne l’active.

## Addendum 1.2.46 — inventaire exhaustif des notions spécialisées des introductions

La règle 1.2.45 fondée principalement sur les groupes de notions voisines est remplacée par la présente règle cumulative. L’ancien `specialized_term_explanation_policy_revision` peut rester comme trace, sans effet d’activation. Le registre `wikipedia_link_groups` peut rester dans les archives historiques, mais ne constitue pas une preuve suffisante de revue.

Le registre actif emploie `specialized_term_inventory_reviewed=true` et `specialized_term_inventory`. Il contient exactement une entrée par sous-partie, dans le même ordre que l’introduction. Chaque entrée atteste `scan_complete=true`, fournit une note de revue substantielle et inventorie les notions spécialisées effectivement rencontrées.

Pour chaque notion :

1. `term` reproduit la forme visible dans la sous-partie ;
2. `treatment=wikipedia_link` indique l’article vérifié et correspond à un modèle réellement présent dont le texte affiché est la notion ;
3. `treatment=explained_inline` cite un extrait explicatif réellement présent ;
4. `treatment=prior_treatment` désigne une sous-partie antérieure et une notion antérieure déjà liée ou expliquée ;
5. `treatment=context_sufficient` fournit une justification spécifique expliquant pourquoi le passage suffit sans lien ni définition supplémentaire ;
6. tous les modèles `{{Lien Wikipédia}}` ou `{{Wikipedia link}}` présents dans la sous-partie figurent dans l’inventaire ;
7. une sous-partie déclarée technique ou spécialisée ne peut avoir un inventaire vide.

La revue reste qualitative. Elle n’impose pas de lier les mots courants, les noms propres évidents ni chaque discipline mentionnée. Elle exige en revanche qu’aucune notion réellement opaque ne soit oubliée derrière une attestation générale.



## Addendum 1.2.50 — préservation de tous les paramètres des pages existantes

1. **Création de zéro.** Le profil de génération reste restrictif : seuls les paramètres prévus pour une page nouvelle sont émis et les marqueurs d’origine IA ne sont ajoutés que dans ce cas.
2. **Modification d’une page existante.** Le moteur ne reconstruit jamais la page comme si elle était nouvelle. Tout paramètre top-level autorisé attesté comme présent constitue un minimum de présence et ne peut disparaître silencieusement.
3. **Métadonnées opaques.** `initialisation`/`initialization`, `nom`/`name`, les paramètres d’avertissement, `débat-détaillé`/`detailed-debate`, les dates de création et les métadonnées de cycle de vie conservent par défaut leur présence et leur valeur exactes. Les profils de création ne peuvent ni les effacer, ni les remplacer, ni y injecter un marqueur IA.
4. **Contenus éditables.** Les paramètres de contenu (`résumé`, citations, références, justifications, objections, documentation du débat, etc.) peuvent être enrichis ou corrigés ; leur paramètre top-level ne peut toutefois être supprimé s’il existait sans décision explicite de suppression.
5. **Liens interlangues.** L’absence de traduction peut interdire la création d’un nouveau lien, mais ne justifie jamais la suppression d’un `interlangue` historique.
6. **Suppressions explicites.** Toute suppression volontaire est enregistrée page par page et paramètre par paramètre avec décision propriétaire. Les exceptions déjà spécialisées (`owner_removed` pour un résumé, `relations_omitted` sur une frontière détaillée) restent valables.
7. **Débats.** Les règles 1 à 6 valent sans distinction pour `Débat` / `Debate` et `Argument`.

## Addendum 1.2.54 — architecture cumulative et séparation des versions de format

La norme active est cumulative. Sauf mention explicite dans la présente norme qu’une règle est supprimée ou remplacée, toute règle éditoriale active s’applique à tout corpus soumis au validateur courant, quelle que soit la valeur historique déclarée dans `normative_versions.consolidated_norm`.

1. `consolidated_norm` décrit la provenance normative déclarée, la compatibilité de lecture, les besoins de migration et la traçabilité d’une livraison. Il ne constitue jamais un *feature flag* éditorial.
2. Les champs dont le nom finit par `policy_revision` ou `_revision`, ainsi que les champs historiques spécialisés tels que `argument_name_assignment_revision`, `argument_name_discovery_revision` ou `manual_remote_adoption_revision`, sont des métadonnées de traçabilité lorsqu’ils existent. Une différence, une absence ou une ancienne valeur ne désactive pas une règle éditoriale active.
3. Les anciennes clauses des révisions 1.2.x indiquant qu’une politique « peut être activée » en déclarant une révision sont **remplacées** sur ce point. Elles restent lisibles comme historique de l’introduction de la règle, mais leur mécanisme d’activation par numéro n’est plus normatif.
4. Les contrôles sont commandés par les faits fonctionnels pertinents : présence d’un registre ou d’un chemin déclaré, `page_origin`, `translation_status.en`, existence d’un inventaire historique lorsque la préservation est activée, état distant attesté, ou autre donnée directement liée à l’opération contrôlée.
5. Lorsqu’un artefact ou un registre possède son propre format, sa compatibilité est déterminée par `schema`, `schema_version` ou un identifiant `version` stable propre à cet artefact. Une révision globale de la norme ne remplace pas la version de format de l’artefact.
6. La lecture de corpus anciens et les migrations peuvent continuer à examiner les versions globales pour interpréter un ancien format. Cette compatibilité de lecture ne réduit jamais les exigences éditoriales courantes après interprétation.
7. Les générateurs cessent d’émettre les champs de révision qui n’ont plus d’utilité opérationnelle. Ils peuvent conserver une révision historique lorsqu’elle est utile à la provenance ou à la reproductibilité, sans lui donner de portée conditionnelle.
8. Le validateur et le kit doivent posséder des tests d’invariance garantissant qu’à contenu fonctionnel identique, changer seulement `consolidated_norm` ou une métadonnée `*_revision` ne modifie pas le verdict éditorial.
9. Les versions du paquet, du validateur et du kit restent obligatoires pour identifier une livraison, vérifier la compatibilité technique, reproduire un environnement et piloter les migrations. Leur maintien n’autorise aucune branche éditoriale conditionnée au numéro de version.
10. La présente refonte ne modifie aucune règle de contenu de la révision 1.2.53 : lots de traduction, recherche anglophone de `name=`, adaptation réelle des références et contrat spécial `Citation`→`Quote` demeurent intégralement applicables.

## Changelog normatif

Source interne : `norms/normative_reference/01_normes/CHANGELOG_NORMATIF.md`  
SHA-256 : `4b3bcd49c53ab116f9edd7546c460d05083b4dea337fab6baf21e6737a85cc92`

## 1.2.54 — 7 août 2026 — architecture cumulative des normes éditoriales

- supprime l’activation des règles éditoriales par listes ou comparaisons de versions ;
- conserve `consolidated_norm` pour le format, les migrations, la provenance et la traçabilité uniquement ;
- transforme les anciens `*_policy_revision` / `*_revision` en métadonnées de trace sans effet de sélection ;
- fait dépendre les contrôles de l’état fonctionnel réellement pertinent ;
- conserve des versions propres aux formats d’artefacts ;
- exige des tests d’invariance pour empêcher le retour de gardes éditoriales par version ;
- aligne également le cahier des charges, le workflow, les structures MediaWiki et le schéma de graphe afin qu’aucune formulation active ne réintroduise un seuil éditorial par version ;
- préserve sans modification toutes les règles de contenu 1.2.53.
- correctif de traduction FR→EN : la page anglaise cible existante est ignorée comme source éditoriale ;
- ajout d'une table exhaustive des valeurs `avancement`/`progress`, `avertissements-titre`/`title-warnings`, `avertissements-débat`/`debate-warnings` et `avertissements-argument`/`argument-warnings` ;
- les valeurs françaises présentes sont traduites exactement et l'absence d'un paramètre reste une absence, sans injection d'un défaut de création ;
- `related-debates` ne projette que les débats connexes français dont la page anglaise existe réellement ;
- ajout d'une seconde passe FR→EN obligatoire avant clôture de chaque lot.

## 1.2.53 — 7 août 2026

- traduction anglaise organisée en lots fermés : page Debate seule, puis 20 Arguments par défaut, maximum 25 et réduction à 10–15 pour les lots documentaires denses ;
- passe globale inter-lots obligatoire avant finalisation ;
- recherche de `name=` indépendante dans la littérature anglophone, sans traduction mécanique de `nom=` ;
- interdiction de traduire artificiellement les références françaises ; projection uniquement d'une version anglaise réelle et vérifiée avec ses métadonnées propres ;
- recherche indépendante de nouvelles références anglophones ;
- confirmation du contrat `Citation`→`Quote` : seules les valeurs `quote` et `date` sont traduites et `Citation traduite par IA` est ajouté ;
- alignement recommandé : validateur 0.4.56 et kit 2.15.30.

## 1.2.52 — 7 août 2026

- recherche documentaire obligatoire d’une appellation consacrée pour chaque page Argument nouvelle ;
- présomption explicite d’absence : aucun quota et aucun objectif de remplissage de `nom` / `name` ;
- nom retenu uniquement lorsqu’il est attesté dans la littérature pour le même raisonnement et dans une forme adaptée à la langue de la page ;
- registre de revue avec requêtes, résultat `none` / `known_name` et preuves documentaires ;
- nouveau contrôle `WDV-EDT-032` ;
- alignement recommandé : validateur 0.4.55 et kit 2.15.29.

## 1.2.51 — 7 août 2026

- maintien de la préservation stricte des `nom` / `name` historiques existants ;
- ajout d’un registre d’attribution éditoriale explicite pour les appellations consacrées ajoutées à des pages auparavant dépourvues de `nom` / `name` ;
- séparation obligatoire entre la provenance historique et la nouvelle décision éditoriale ;
- dérogation limitée au seul paramètre `nom` / `name` et aux seules pages listées ;
- alignement recommandé : validateur 0.4.54 et kit 2.15.28.

## 1.2.50 — 7 août 2026

- séparation normative entre création d’une page nouvelle et modification d’une page existante ;
- préservation de présence de tout paramètre top-level autorisé attesté sur une page existante ;
- préservation exacte par défaut des métadonnées historiques et avertissements ;
- interdiction d’appliquer rétroactivement les marqueurs IA aux pages préexistantes ;
- suppression uniquement sur décision explicite page/paramètre ou exception spécialisée ;
- même contrat pour les pages Débat et Argument, françaises et anglaises ;
- alignement recommandé : validateur 0.4.53 et kit 2.15.27.

## 1.2.49 — 7 août 2026

- préservation stricte de `nom` / `name` lorsqu’il existe sur une page Argument historique ;
- interdiction de le supprimer, modifier, normaliser ou remplacer lors d’un renommage ;
- interdiction symétrique d’inventer ce paramètre lorsqu’il était absent ;
- état de présence et valeur consignés dans les paramètres préservés et dans le verrou historique ;
- alignement recommandé : validateur 0.4.52 et kit 2.15.26.

## 1.2.48 — 7 août 2026
- prise en charge nominative des relations externes préservées dans une adoption distante, sans création de nœud local ;

- adoption contrôlée des pages créées ou modifiées manuellement après le dernier état publié signé ;
- attestation par identifiant de révision et/ou empreinte SHA-256 ;
- autorisation explicite et nominative des changements de paramètres de cycle de vie ;
- maintien du blocage si la page distante a changé depuis l’attestation ;
- interdiction maintenue de modifier directement l’état publié signé ;
- nouveau contrôle `WDV-RMT-007`.

## 1.2.47 — 6 août 2026

- préservation obligatoire de `débat-détaillé` / `detailed-debate` sur les pages historiques ;
- distinction entre arrêt du parcours du graphe et suppression du paramètre MediaWiki ;
- omission autorisée de `justifications` et `objections` aux frontières uniquement après attestation page par page ;
- verrouillage de la cible par comparaison avec l’inventaire source ;
- attestation obligatoire que le propriétaire a été informé de l’omission des relations locales ;
- alignement recommandé : validateur 0.4.50 et kit 2.15.24.

## 1.2.46 — 6 août 2026

- remplacement du contrôle limité aux groupes de notions voisines par une revue exhaustive de toutes les notions spécialisées de chaque sous-partie ;
- ajout de `specialized_term_inventory_reviewed` et `specialized_term_inventory` ;
- quatre traitements vérifiables : lien Wikipédia, explication intégrée, traitement antérieur et contexte suffisant ;
- correspondance obligatoire entre l’inventaire, les textes visibles et tous les liens Wikipédia réellement rendus ;
- inventaire non vide pour toute sous-partie déclarée technique ou spécialisée ;
- nouveau contrôle `WDV-EDT-029`.

## 1.2.45 — 6 août 2026

- cohérence locale obligatoire des liens Wikipédia explicatifs ;
- examen conjoint des notions spécialisées de même rang dans une énumération ou une comparaison ;
- traitement uniforme lorsque les articles existent et que le besoin explicatif est comparable ;
- justification notion par notion de toute asymétrie ;
- nouveau registre `wikipedia_link_groups` et contrôle `WDV-EDT-028`.

## 1.2.44 — 6 août 2026

- suppression du point final dans les simples notices placées à l’intérieur de `<ref>…</ref>` ;
- maintien du point uniquement lorsque le corps de la note constitue une phrase explicative complète ;
- ponctuation de la phrase principale placée après l’appel de note ;
- exceptions liées par SHA-256 et attestées dans la revue de l’introduction ;
- activation rétrocompatible par `inline_reference_punctuation_policy_revision=1.2.44`.

## 1.2.43 — 6 août 2026

- sous-partie `Enjeux du débat` obligatoire dans toute introduction française ;
- sous-partie `Stakes of the debate` obligatoire dans toute introduction anglaise ;
- au moins deux conséquences concrètes consignées dans la revue ;
- interdiction des listes génériques de domaines et de la reproduction du graphe argumentatif ;
- activation rétrocompatible par `introduction_policy_revision=1.2.43`.

## 1.2.42 — 6 août 2026

- classement neutre obligatoire des sources présentant plusieurs positions et interdiction des doublons entre orientations ;
- suppression des quotas documentaires par paramètre de débat ;
- auteur ou chaîne obligatoire pour toute référence YouTube lorsque l'attribution est visible ;
- introduction fondée sur la densité informative, sans rubrique générique de remplissage ;
- identité titre canonique / titre affiché admise sans plafond ;
- reformulation d'un titre affiché autorisée seulement avec amélioration réelle et équivalence sémantique attestée.

## 1.2.41 — 6 août 2026

- simplification des mots-clés contextuels des pages nouvelles ;
- conservation explicite des locutions conceptuelles autonomes, dont `croyance fondamentale` ;
- sélection automatique de l’unique ZIP de `incoming/` par `./wikidebia update` ;
- portée `all` utilisée par défaut ;
- identifiant exigé uniquement en cas d’ambiguïté.

## 1.2.40 — 6 août 2026

- conservation de l’absence historique d’un résumé lorsqu’elle est attestée par l’inventaire source ;
- ajout de `summary_provenance=historical_absent` ;
- interdiction maintenue des résumés absents sur les pages nouvelles ;
- revue spécifique `historical_absence_verified` et exclusion des contrôles stylistiques inapplicables.

## 1.2.39 — 6 août 2026

- interdiction de réécrire un champ historique lors d'une correction ciblée non autorisée ;
- restauration et préservation exacte de `initialisation` / `initialization` sur les pages importées ;
- ajout d'un verrou machine des résumés et paramètres historiques ;
- séparation des politiques d'atomicité des mots-clés, d'originalité des résumés et de capitalisation ;
- compatibilité conservée avec le profil combiné 1.2.38.

## 1.2.38 — 6 août 2026

- distinction explicite entre locution atomique et intersection compositionnelle de domaines ;
- obligation de décomposer `psychologie de la religion` ou `psychologie religieuse` en `psychologie` et `religion` ;
- maintien des catégories irréductibles telles que `argument d'autorité` ;
- ajout de l’attestation `compositional_intersection=false` dans le vocabulaire contrôlé ;
- contrôle symétrique des constructions françaises et anglaises ;
- schémas dédiés au vocabulaire de mots-clés et à la revue des résumés ;
- activation complète des barrières éditoriales sur les corpus migrant vers 1.2.38.

## 1.2.37 — 5 août 2026

- remplacement du critère purement quantitatif des mots-clés par une exigence de concept atomique ;
- blocage des mini-rubriques productives telles que `limites de la science`, `histoire des religions` et `construction des lois scientifiques` ;
- maintien des locutions lexicalisées telles que `lois de la nature`, avec exception multi-mots motivée ;
- blocage des résumés construits par charpente générique, métadiscours, copie de titres enfants ou répétition d’une même phrase dans quatre pages ou davantage ;
- attestation obligatoire d’originalité et d’un extrait formulant le mécanisme propre au nœud ;
- contrôle de la majuscule de `Dieu` lorsqu’il s’agit du nom propre.

## 1.2.36 — 5 août 2026

- politique `per_page_preserved` appliquée par défaut : les pages existantes conservent leur date historique sans exigence de date du corpus ou du jour ;
- réconciliation automatique et traçable des paramètres de cycle de vie protégés pour les pages distantes exactement attestées ;
- absence d’ajout rétroactif des avertissements IA aux pages historiques ;
- suppression d’une page historique non marquée autorisée seulement par migration explicite, état distant exact et absence d’autre propriétaire connu ;
- maintien de la traduction anglaise différée et de toutes les protections contre les modifications humaines.

## 1.2.35 — 5 août 2026

- le statut anglais `deferred` devient une déclaration opérationnelle rétrocompatible avec tous les corpus historiques 1.2.x pris en charge, sans migration de leur norme éditoriale ;
- ajout de `creation_date_policy=per_page_preserved` pour conserver les dates immuables page par page ;
- encadrement d'une exception propriétaire, exhaustive et file-backed pour des titres affichés hérités déjà verrouillés ;
- maintien du contrôle strict des corpus non différés, des liens existants et des portées anglaises.

## 1.2.34 — 5 août 2026

- ajout de `translation_status.en=deferred` pour une publication française autonome ;
- titres anglais, pages anglaises et liens interlangues non requis dans cet état ;
- blocage des portées anglaises tant que la traduction est différée ;
- maintien des contrôles stricts pour les titres verrouillés, liens existants et états `ready`/`published` ;
- ajout ultérieur des liens interlangues par reprise française sans modification de la date de création ;
- remplacement explicite des anciennes obligations de verrouillage et de lien immédiats.

## 1.2.33 — 5 août 2026

- sélection des références d’Argument fondée sur le développement de l’argument ; la couverture simultanée d’objections reste admise ;
- distinction explicite entre page nouvelle et page préexistante ;
- préservation exacte de l’avancement, des avertissements et des débats connexes sur les pages existantes ;
- ajout des valeurs IA et de `Débat construit` uniquement lors de la création ;
- instantané de paramètres protégés dans les manifestes de page et garde-fou du plan de mise à jour.

## 1.2.32 — 4 août 2026

- minuscule initiale obligatoire pour les mots-clés communs ;
- conservation justifiée de la graphie canonique des noms propres, dénominations officielles, marques, sigles et acronymes ;
- interdiction des doublons ne différant que par la casse ;
- contrôle symétrique des keywords anglais ;
- compatibilité des normes 1.2.31 et antérieures conservée.

## 1.2.31 — 4 août 2026

- classement des mots-clés par pertinence décroissante, du plus direct au moins direct ;
- interdiction de l’ordre chronologique ou alphabétique comme principe de classement ;
- conservation exacte du classement conceptuel dans les keywords anglais ;
- suppression de toute cible, limite et alerte numérique de profondeur ;
- `maximum_observed` maintenu comme métrique descriptive.

## 1.2.30 — 4 août 2026

- localisation complète du modèle anglais `{{Quote}}` et de tous ses paramètres ;
- correspondances canoniques `citation→quote`, `auteurs→authors`, `ouvrage→work`, `numéro→issue`, `localisation→location`, `édition→publisher`, `lieu→place`, `lien→link` et `avertissements-citation→warnings` ;
- traduction limitée aux valeurs de `quote` et de `date` ;
- blocage de tout paramètre français ou sans équivalent déclaré dans une page anglaise ;
- alignement recommandé : validateur 0.4.32 et kit 2.15.3.

## 1.2.29 — 4 août 2026

- restauration du nom anglais `{{Quote}}` dans `quotes=` ;
- conservation des noms français de paramètres verrouillés à l’intérieur du modèle anglais ;
- traduction limitée aux valeurs de `citation` et de `date` ;
- aucune suppression ni modification des fonctions introduites avant cette correction.

## 1.2.28 — 3 août 2026

- correction documentaire de 1.2.27 sans modification du graphe ni du protocole distant ;
- suppression de l’ancienne interdiction contradictoire des citations dans les documents spécialisés ;
- maintien de `{{Citation}}` dans `quotes=` avec les mêmes paramètres documentaires français ;
- revérification du rendu des citations lors de la migration.

## 1.2.27 — 3 août 2026

- rendu déterministe bilingue depuis les verrous ;
- lien interlangue direct obligatoire dans chaque page française ;
- traduction sélective des citations et avertissement canonique ;
- alignement recommandé : validateur 0.4.29 et kit 2.10.0.

## 1.2.26 — 2 août 2026

- remplacement de l’absence d’état pour un plan entièrement `skip` par une attestation signée `no_changes` après relecture distante complète, sans écriture MediaWiki ;
- sélection d’une archive uniquement avec `--archive`, sans repli implicite depuis un identifiant ou un ZIP unique ;
- nettoyage systématique des zones de staging sur toutes les sorties ;
- statut `no_changes_in_scope` lorsqu’aucune opération mutante n’appartient à la portée demandée ;
- conservation signée des pages `pending_delete` après `--no-delete`, afin de permettre une reprise sûre avec `--only-delete` ;
- ajout des exigences `GOV-009`, `PUB-041` à `PUB-044` et `VAL-034` ;
- alignement recommandé : validateur 0.4.28 et kit 2.2.13.

## 1.2.25 — 2 août 2026

- `manual_review` devient un blocage effectif de l’exécution, au même titre que `blocked` ;
- interdiction d’écrire un reçu de succès ou un état publié lorsqu’un plan reste non résolu ;
- statut `no_changes` et absence de faux reçu pour un plan composé uniquement de `skip` ;
- staging obligatoire des archives de reprise et garantie qu’un dry-run ne modifie jamais `corpus/` ;
- priorité au corpus installé pour `update IDENTIFIANT` et sélection explicite des archives par `--archive` ;
- exclusion des corpus de débat des archives génériques et du bundle de composants ;
- ajout des exigences `GOV-008`, `FIL-019`, `PUB-037` à `PUB-040` et `VAL-033` ;
- alignement recommandé : validateur 0.4.27 et kit 2.2.12.

## 1.2.24 — 2 août 2026

- autorisation encadrée de `{{Lien Wikipédia}}` dans les introductions et résumés français ;
- équivalent anglais `{{Wikipedia link}}` ;
- paramètres localisés `texte-affiché` et `displayed-text`, omis pour une simple adaptation de casse initiale ;
- vérification de la page dans la langue correspondante, usage à la première occurrence utile et interdiction dans les notes de référence ;
- distinction explicite entre aide au survol et source documentaire ;
- ajout des exigences `ARG-035`, `DFR-047`, `DEN-008`, `MW-027`, `PRM-018` et `VAL-032` ;
- alignement recommandé : validateur 0.4.26 et kit 2.2.11.


## 1.2.23 — 2 août 2026

- minuscule initiale harmonisée pour `sujet-complet` et `complete-topic` ;
- préférence explicite pour un sujet nominal conventionnel ;
- règles auteur/site/page étendues aux pages Argument et à la vidéographie, avec seconde recherche obligatoire en cas d’égalité auteur-site ;
- résumé de modification distant simplifié en « Corrections » ;
- compatibilité du fichier unique de mise à niveau renforcée.

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

## 1.2.14 — 31 juillet 2026

- correction de la contrainte 1.2.13 qui imposait l’égalité entre le nom du ZIP et `manifest.debate_id` ;
- nom du ZIP réduit au rôle de sélecteur de fichier ;
- `manifest.debate_id` maintenu comme identité autoritative du corpus ;
- compatibilité directe avec les archives historiques dont le nom comporte un suffixe descriptif.

## 1.2.13 — 30 juillet 2026

- dossier unique `incoming/` pour les archives de débats ;
- sélection automatique lorsqu’un seul ZIP est présent ;
- sélection obligatoire par identifiant lorsqu’il y en a plusieurs ;
- suppression de toute obligation de suffixe `release_ready` dans le nom du ZIP ;
- correspondance bloquante entre `<identifiant>.zip` et `manifest.debate_id`.

## 1.2.12 — 30 juillet 2026

- publication d’un paquet `release_ready` en une commande, avec cinq portées canoniques ;
- ordre Débat/Debate puis Argument imposé dans chaque langue ;
- mise à jour atomique en une commande, sauvegarde des versions précédentes et vidage de `updates/` ;
- dépôt Git/GitHub des seules sources nécessaires ;
- exclusion des secrets, corpus, archives, entrées, plans et journaux ;
- déplacement des fichiers Pywikibot dans `private/pywikibot/` ;
- interdiction de conserver le chemin absolu de l’installation dans les fichiers persistants ;
- alignement recommandé : validateur 0.4.12 et kit 2.1.12.

## 1.2.11 — 30 juillet 2026

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

## État actif du validateur

Source interne : `validator/README.md`  
SHA-256 : `d5a42fb962ceb3c39b4565af341e6062f3d2a9f1d341e3de2e7f198ad896eab1`

# Wikidéb’IA Validator 0.4.57

La version 0.4.57 aligne le paquet sur la norme 1.2.54 et supprime les gardes de version des contrôles éditoriaux. Elle conserve les contrôles existants et embarque les nouvelles règles éditoriales de traduction anglaise par lots, d'adaptation des références à des versions anglaises réelles, de recherche anglophone autonome de `name=` et de maintien du contrat `Citation`→`Quote`. Ces exigences de recherche et d'ordonnancement restent principalement éditoriales ; les contrôles automatiques antérieurs ne sont pas relâchés.

Validateur local aligné sur la norme 1.2.54 et rétrocompatible avec les paquets antérieurs.

Les normes éditoriales courantes sont cumulatives : `consolidated_norm` et les anciens champs `*_revision` ne servent plus de feature flags. Les versions restent réservées à la compatibilité de format, aux migrations et à la traçabilité.

## Changelog du validateur

Source interne : `validator/CHANGELOG.md`  
SHA-256 : `ce67e2efa394d52fd2f9f9ffa46f21e4270256ba5c938ac56204b9d667d6fe3e`

## 0.4.57 — 7 août 2026

- applique cumulativement les règles éditoriales actives, sans garde sur `consolidated_norm` ;
- traite les anciens champs `*_policy_revision` / `*_revision` comme traces sans effet conditionnel ;
- déclenche les contrôles selon l’état fonctionnel du corpus ;
- conserve les versions pour le format, les migrations et la non-régression des sources normatives ;
- ajoute des tests d’invariance, contrôle aussi l’absence de formulations normatives actives conditionnées par version, et maintient la protection `WDV-EDT-030` sans garde de version.

## 0.4.56 — 7 août 2026

- alignement documentaire sur la norme 1.2.53 ;
- intégration des exigences de traduction anglaise par lots et de passe inter-lots ;
- intégration de la politique d'équivalents anglais réels et de recherche de nouvelles références anglophones ;
- confirmation de la recherche autonome de `name=` anglais et du contrat `Citation`→`Quote` ;
- aucun relâchement des contrôles automatiques existants ;
- correction de non-régression : sous 1.2.53, la revue des noms consacrés reste obligatoire via la politique stable `argument_name_discovery_revision=1.2.52`.

## 0.4.55 — 7 août 2026

- alignement sur la norme 1.2.52 ;
- ajout du schéma `argument_name_discovery_review.schema.json` ;
- ajout de `WDV-EDT-032` pour exiger une recherche documentaire sur chaque argument nouveau ;
- résultat `none` explicitement admis et attendu par défaut ;
- `nom` / `name` autorisé seulement si la revue conclut `known_name`, avec preuve et concordance exacte ;
- préservation 1.2.49 et attribution propriétaire 1.2.51 inchangées.

## 0.4.54 — 7 août 2026

- alignement sur la norme 1.2.51 ;
- ajout du schéma et du contrôle du registre d’attribution éditoriale de `nom` / `name` ;
- maintien de la provenance historique distincte : le verrou peut rester `present=false` tandis qu’une attribution approuvée autorise le wikicode exact ;
- conservation du blocage pour toute page non listée ou toute valeur divergente ;
- compatibilité conservée avec les corpus 1.2.50 et antérieurs.

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

## État actif du kit

Source interne : `kit/README.md`  
SHA-256 : `c15805e58ba9084b31250b73f07b94dda538e846ee2426701eee10c770e6a5c1`

# Wikidéb’IA — Kit 2.15.31

Le kit 2.15.31 applique l’architecture cumulative 1.2.54 tout en conservant la traduction anglaise 1.2.53 par lots : page Debate en lot autonome, puis lots Argument de 20 pages par défaut (25 maximum, 10–15 lorsque la documentation ou les citations sont denses), avec passe globale inter-lots avant finalisation.

La phase anglaise recherche séparément les appellations consacrées dans la littérature anglophone et n'obtient jamais `name=` par traduction mécanique de `nom=`. Les références françaises ne sont pas traduites : une version anglaise réelle doit être trouvée et citée avec ses propres métadonnées, et de nouvelles références anglophones sont recherchées indépendamment. Le contrat `Citation`→`Quote` reste inchangé : seules les valeurs `quote` et `date` sont traduites et `Citation traduite par IA` est ajouté.

La reprise distante applique cette exception uniquement à `nom` / `name`. Tous les autres paramètres historiques protégés conservent les garanties de la révision 2.15.27.

Correctif actif de traduction : le contenu d'une éventuelle page anglaise cible existante est ignoré pendant la production éditoriale ; les valeurs françaises de progression et d'avertissement sont traduites selon la table officielle sans défaut de création ; `related-debates` ne reprend que les relations françaises dont la page anglaise existe ; chaque lot reçoit une seconde passe FR→EN.

Kit aligné sur la norme 1.2.54 et le validateur 0.4.57.

Les numéros de norme et les anciens champs de révision ne sont plus des feature flags éditoriaux ; ils servent uniquement à la compatibilité technique et à la traçabilité.

## Changelog du kit

Source interne : `kit/CHANGELOG.md`  
SHA-256 : `e6ebca1fc737e6df899dd82199cb44c94551459ba71646d0fd0099ed7c283c4e`

## 2.15.31 — 7 août 2026

- supprime l’usage des révisions normatives comme feature flags éditoriaux ;
- base les contrôles et transitions sur l’état fonctionnel du corpus ;
- conserve les versions pour la compatibilité de format, les migrations et la traçabilité ;
- maintient les règles de traduction anglaise 1.2.53 sans modification ;
- ajoute des tests d’invariance et un test explicite du lien interlangue selon le statut `deferred`.

## 2.15.30 — 7 août 2026

- alignement sur la norme 1.2.53 et le validateur 0.4.56 ;
- formalisation du lot Debate autonome et des lots Argument de 20 pages par défaut, 25 maximum, réduits à 10–15 lorsque la charge documentaire l'exige ;
- ajout d'une passe globale inter-lots avant finalisation ;
- recherche anglophone autonome de `name=` sans traduction mécanique de `nom=` ;
- adaptation des références uniquement à partir de versions anglaises réelles et vérifiées, plus recherche indépendante de nouvelles sources anglophones ;
- rappel explicite du contrat `Citation`→`Quote` ;
- inclusion du guide de traduction anglaise dans la source active unifiée générée par `upgrade` ;
- correction de non-régression : le registre de recherche des noms anglais reste scellé sous la révision de politique `1.2.52`, même lorsque la norme active est 1.2.53.

## 2.15.29 — 7 août 2026

- alignement sur la norme 1.2.52 et le validateur 0.4.55 ;
- ajout au workflow de génération d’une recherche documentaire sur l’éventuelle appellation consacrée de chaque argument nouveau ;
- présomption d’absence : aucun quota de `nom` / `name` et aucun nom fabriqué depuis le titre ;
- rendu de `nom` / `name` sur une page nouvelle uniquement depuis `argument_name` après revue `known_name` ;
- guide de revue enrichi avec critères de recherche et hiérarchie des sources ;
- préservation des mécanismes 1.2.49 et 1.2.51 pour les pages historiques.

## 2.15.28 — 7 août 2026

- alignement sur la norme 1.2.51 et le validateur 0.4.54 ;
- prise en charge du registre explicite d’attribution de `nom` / `name` ;
- conservation de l’absence historique par défaut et exception limitée aux pages approuvées ;
- aucune ouverture des autres paramètres protégés lors d’une reprise.

## 2.15.27 — 7 août 2026

- alignement sur la norme 1.2.50 et le validateur 0.4.53 ;
- séparation explicite création/modification dans le rendu ;
- conservation exacte des avertissements et métadonnées historiques des pages existantes ;
- contrôle générique des suppressions de paramètres top-level dans le planificateur de reprise ;
- restauration corrective possible uniquement à partir d’états historiques attestés ;
- protection équivalente des pages Débat et Argument, en français et en anglais ;
- 284 tests pytest réussis.

## 2.15.26 — 7 août 2026

- alignement sur la norme 1.2.49 et le validateur 0.4.52 ;
- capture de `nom` / `name` dans les paramètres préservés des pages Argument préexistantes ;
- rendu exact du paramètre lorsqu’il existait et absence garantie lorsqu’il était absent ;
- tests de non-régression du rendu et de la revue de contenu.

## 2.15.25 — 7 août 2026

- alignement sur la norme 1.2.48 et le validateur 0.4.51 ;
- lecture d’un registre `manual_remote_adoptions` déclaré par le corpus ;
- conversion d’une révision manuelle attestée en mise à jour contrôlée avec `baserevid` ;
- blocage si la révision ou l’empreinte distante a changé ;
- autorisation nominative obligatoire de toute modification d’un paramètre de cycle de vie ;
- maintien intégral des protections contre les modifications humaines non attestées.

## 2.15.24 — 6 août 2026

- alignement sur la norme 1.2.47 et le validateur 0.4.50 ;
- conservation exacte de `débat-détaillé` / `detailed-debate` pendant la revue et le rendu ;
- arrêt du parcours aux frontières sans suppression du paramètre historique ;
- omission des justifications et objections locales uniquement sous attestation explicite ;
- tests permanents de non-régression.

## 2.15.23 — 6 août 2026

- maintenance de rationalisation des sources après `./wikidebia upgrade` ;
- conservation à la racine de `WIKIDEBIA_SOURCE_ACTIVE.md` et `WIKIDEBIA_SOURCE_PACKAGE_RECEIPT.json` comme seules documentations actives ;
- archivage des anciens fichiers actifs séparés au lieu de leur régénération.

## 2.15.22 — 6 août 2026

- alignement sur la norme 1.2.46 et le validateur 0.4.49 ;
- remplacement de `wikipedia_link_groups` par `specialized_term_inventory` comme mécanisme principal ;
- inventaire obligatoire de chaque sous-partie et vérification de tous les liens rendus ;
- traitements `wikipedia_link`, `explained_inline`, `prior_treatment` et `context_sufficient` ;
- blocage des sous-parties techniques dont l’inventaire est vide.

## 2.15.21 — 6 août 2026

- alignement sur la norme 1.2.45 et le validateur 0.4.48 ;
- ajout de `wikipedia_link_consistency_reviewed` et `wikipedia_link_groups` ;
- vérification des liens déclarés dans chaque sous-partie ;
- justification obligatoire d’une asymétrie entre notions spécialisées de même rang ;
- tests de non-régression dédiés.

## 2.15.20 — 6 août 2026

- alignement sur la norme 1.2.44 et le validateur 0.4.47 ;
- revue obligatoire de la ponctuation terminale des notes `<ref>` ;
- absence de point par défaut dans une simple notice documentaire ;
- exceptions de phrases complètes attestées par SHA-256 ;
- tests de refus des notices ponctuées et d’acceptation des phrases attestées.

## 2.15.19 — 6 août 2026

- alignement sur la norme 1.2.43 et le validateur 0.4.46 ;
- rétablissement obligatoire de la sous-partie `Enjeux du débat` dans les introductions françaises ;
- contrôle d’au moins deux conséquences concrètes, de la densité minimale et de l’absence de catalogue argumentatif ;
- génération des champs de revue propres à cette sous-partie et tests négatifs dédiés.

## 2.15.18 — 6 août 2026

- alignement sur la norme 1.2.42 et le validateur 0.4.45 ;
- suppression des quotas documentaires par orientation dans les revues française et anglaise ;
- blocage des références utilisées dans plusieurs orientations ;
- auteur ou chaîne obligatoire pour les vidéos YouTube ;
- nouvelles attestations de densité informative des introductions ;
- suppression du plafond de 10 % d’identités entre titres canoniques et affichés ;
- titre affiché distinct accepté seulement avec équivalence sémantique et gain réel de lisibilité ;
- sélection automatique de l’unique archive et portée automatique conservées.

## 2.15.17 — 6 août 2026

- alignement sur le validateur 0.4.44 et la norme 1.2.41 ;
- sélection automatique de l’unique ZIP de `incoming/` sans `--archive` ;
- blocage avec liste des sélecteurs lorsque plusieurs ZIP sont présents ;
- détection automatique de la portée lorsque `--scope` est omis ;
- conservation des résumés obligatoires pour les pages nouvelles et de l’absence attestée pour les pages historiques ;
- conservation de toutes les protections de plan signé, concurrence, staging et modification humaine.
## 2.15.16 — 6 août 2026

- alignement sur la norme 1.2.40 et le validateur 0.4.43 ;
- prise en charge de `summary_provenance=historical_absent` pour les pages historiquement dépourvues de résumé ;
- maintien du résumé obligatoire pour les pages nouvelles ;
- vérification de l’inventaire source avant toute omission historique.

## 2.15.15 — 6 août 2026

- maintien de la norme 1.2.39 et alignement sur le validateur 0.4.42 ;
- renforcement de la confrontation des verrous historiques à l’inventaire source attesté ;
- préservation des champs historiques vérifiée avant toute planification ;
- aucune modification des mécanismes distants de publication et de reprise.

## 2.15.14 — 6 août 2026

- alignement sur la norme 1.2.39 et le validateur 0.4.41 ;
- séparation des politiques d’atomicité des mots-clés, d’originalité des résumés et de capitalisation ;
- conservation contrôlée des résumés et du paramètre `initialisation` historiques ;
- ajout d’un verrou machine empêchant toute modification hors périmètre des pages importées ;
- compatibilité conservée avec les corpus 1.2.38 et les mécanismes distants antérieurs.

## 2.15.13 — 6 août 2026

- alignement sur la norme 1.2.38 et le validateur 0.4.40 ;
- activation de la validation schématique des revues éditoriales 1.2.38 ;
- conservation intégrale des mécanismes de publication et de reprise 2.15.12.

## 2.15.12 — 5 août 2026

- alignement sur la norme 1.2.37 et le validateur 0.4.39 ;
- activation des barrières éditoriales sur les résumés répétitifs, les mots-clés non atomiques et la capitalisation de `Dieu` avant toute publication ou reprise ;
- absence de réécriture automatique silencieuse : le kit bloque et renvoie au corpus source ;
- maintien intégral des reprises historiques non destructives de 2.15.11, de la traduction différée et des protections contre les modifications humaines.

## 2.15.11 — 5 août 2026

- alignement sur la norme 1.2.36 et le validateur 0.4.38 ;
- préservation automatique des avertissements, de l’avancement, des débats connexes historiques et des dates de création des pages distantes exactement attestées ;
- génération d’un fichier effectif dérivé et signé, sans modifier le corpus source ni importer d’autres changements distants ;
- suppression des blocages massifs causés par l’ajout rétroactif de `Argument généré par IA` sur des pages historiques ;
- conservation de la date historique des pages existantes, sans exigence de date du corpus ou de date du jour ;
- suppression contrôlée d’une page historique non marquée uniquement lorsqu’une migration explicite documente son retrait et que l’état distant est exact ;
- maintien du blocage des modifications humaines et de la traduction anglaise différée.

## 2.15.10 — 5 août 2026

- reconnaissance de `translation_status.en=deferred` sur les corpus historiques de la famille 1.2.x sans migration de leur révision normative ;
- portées françaises autorisées dans cet état ;
- portées anglaises bloquées jusqu’au passage à `ready` ou `published`.

## 2.15.9 — 5 août 2026

- alignement sur la norme 1.2.34 et le validateur 0.4.36 ;
- ajout du profil `norm_1_2_deferred_translation` ;
- autorisation de `publish` et `update --scope fr` sans titre anglais ni lien interlangue lorsque `translation_status.en=deferred` ;
- blocage explicite des portées anglaises dans cet état ;
- absence totale de génération de titres anglais provisoires ou de liens fictifs ;
- validation stricte de tout lien déjà présent et préservation des liens valides existants ;
- autorisation d'une reprise française ultérieure pour ajouter `interlangue` après passage à `ready` ou `published` ;
- ajout des exemples de création française différée, création bilingue prête et reprise interlangue.

## 2.15.8 — 5 août 2026

- alignement sur la norme 1.2.33 et le validateur 0.4.36 ;
- distinction explicite entre page nouvelle et page préexistante dans les verrous et manifestes ;
- ajout de `Débat construit`, des avertissements IA et de leurs équivalents anglais uniquement lors de la création d’une page absente du wiki ;
- conservation exacte de l’avancement, des avertissements et des débats connexes lors de la modification d’une page existante ;
- blocage des mises à jour et déplacements distants qui modifieraient un paramètre protégé ;
- sélection d’une référence d’Argument uniquement lorsqu’elle développe l’argument, sans rejet lorsqu’elle traite aussi d’objections ;
- conservation intégrale des fonctions et contrats historiques.

## 2.15.7 — 4 août 2026

- contrôle canonique de la capitalisation des mots-clés français et anglais ;
- justification obligatoire des majuscules de noms propres et acronymes ;
- blocage des doublons de vocabulaire ne différant que par la casse ;
- neutralisation des greffons pytest externes pendant les tests de mise à niveau ;
- conservation des fonctions et protections 2.15.6.

## 2.15.6 — 4 août 2026

- alignement sur la norme 1.2.31 et le validateur 0.4.33 ;
- mots-clés français ordonnés par pertinence décroissante avec attestation page par page ;
- conservation exacte de cet ordre dans les keywords anglais ;
- politique de profondeur non limitée dans les nouveaux corpus ;
- suppression des limites, justifications d’exception et alertes de seuil de profondeur ;
- conservation des contrats historiques pour les corpus antérieurs.

## 2.15.5 — 4 août 2026

- correction d’une régression de compatibilité introduite dans les alias métriques de l’extracteur 1.0.1 ;
- conservation exacte des anciennes valeurs de `profondeur_minimale`, `profondeur_maximale`, `occurrences_par_profondeur` et `pages_terminales` pour les consommateurs historiques ;
- maintien parallèle des nouveaux champs explicites en niveaux et profondeurs en arêtes ;
- ajout d’un test permanent comparant les alias 1.0.0 aux métriques explicites 1.0.2 ;
- extracteur porté à la version 1.0.2 ; norme 1.2.30 et validateur 0.4.32 inchangés.

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
- alignement sur la norme 1.2.33 et le validateur 0.4.36.

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

## 2.1.16 — 31 juillet 2026

- création ou réparation automatique de `.venv/` par le lanceur ;
- installation automatique de Pywikibot et des dépendances d’exécution ;
- ajout de `requirements-runtime.txt` à la racine installée ;
- contrôle de l’environnement Python et des modules par `doctor` ;
- conservation de `.venv/` et de l’état d’installation hors de Git.

## 2.1.15 — 31 juillet 2026

- conservation des champs historiques `normative_versions` lors de la reprise d’un corpus déjà produit ;
- exécution du validateur installé et vérification de sa version réelle avant publication ;
- compatibilité explicite avec une norme de corpus antérieure supportée, sans réécriture silencieuse de sa provenance.

## 2.1.14 — 31 juillet 2026

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

- sélection automatique de l’unique ZIP présent dans `incoming/`, sans exiger `--archive` ;
- sélection automatique de la portée publiable lorsque `--scope` est omis : `fr` pour un corpus anglais différé, `all` pour un corpus bilingue prêt ;

## Guide de publication

Source interne : `kit/GUIDE_PUBLICATION.md`  
SHA-256 : `8b44e531354fe399a04adfd38500961391448075f2b08f122ac716295fbd7741`

# Guide de publication et de reprise Wikidéb’IA 2.15.9

## Extraire le graphe d'un débat existant

```bash
./wikidebia graph-extract "Dieu existe-t-il ?"
```

L'extraction est en lecture seule et écrit par défaut dans `.state/graph-extract/dieu_existe_t_il/`. Relancer la même commande réutilise le cache par page. `--force-refresh` force une nouvelle lecture distante. Le ZIP audité contient le graphe, les inventaires CSV, les rapports et le snapshot du wikicode.


## Comparer un corpus final sans l’exécuter

```bash
./wikidebia corpus-workspace-remote-compare <debate_id> \
  --work-id <work_id> \
  --confirm-release-sha256 <empreinte_de_release-copy> \
  --scope all
```

Cette commande est distincte de `update --dry-run` : elle part du workspace et de sa `release-copy/`, conserve un dossier de comparaison immuable et n’offre aucune voie d’exécution. Le plan produit doit être repris explicitement par une phase ultérieure.


## Revoir puis exécuter un plan du workspace

Après la comparaison et la revue formelle, préparer le préflight :

```bash
./wikidebia corpus-workspace-plan-execute <debate_id> \
  --work-id <work_id> \
  --comparison-id <comparison_id> \
  --prepare \
  --confirm-acceptance-sha256 <empreinte>
```

Puis exécuter uniquement après examen de ce préflight :

```bash
./wikidebia corpus-workspace-plan-execute <debate_id> \
  --work-id <work_id> \
  --comparison-id <comparison_id> \
  --execute \
  --confirm-preflight-sha256 <empreinte>
```

La deuxième commande effectue réellement les écritures distantes. Toute divergence observée juste avant l’exécution bloque le plan.

## Nouveau débat

Déposer le ZIP du corpus dans `incoming/`, puis lancer `./wikidebia publish [SÉLECTEUR] --scope all`.

## Débat déjà publié — corpus installé

Lancer `./wikidebia update <debate_id> --dry-run`, examiner le plan, puis relancer sans `--dry-run`. Sans `--archive`, la commande ne consulte que `corpus/<debate_id>/` et ne sélectionne jamais implicitement un ZIP de `incoming/`.

## Débat déjà publié — nouvelle archive

Utiliser explicitement :

```bash
./wikidebia update --archive <SÉLECTEUR> --dry-run
./wikidebia update --archive <SÉLECTEUR>
```

L’archive est extraite dans une zone temporaire de staging. La simulation ne modifie pas `corpus/`, puis le staging est supprimé. Le corpus actif n’est remplacé qu’après une exécution réussie ou une attestation `no_changes` réussie.

Un plan contenant `blocked` ou `manual_review` est bloquant et ne produit ni écriture MediaWiki, ni reçu de succès, ni nouvel état publié. Un plan entièrement `skip` déclenche une relecture distante complète, produit une attestation signée `no_changes` et actualise l’état publié sans éditer le wiki.

## Portées partielles

Lorsque la portée demandée ne contient aucune opération mutante, la commande renvoie `no_changes_in_scope` sans exécuter ni promouvoir un staging. Une reprise avec `--no-delete` conserve les pages à supprimer comme `pending_delete`; elles peuvent ensuite être traitées avec `--only-delete`.

## Mise à niveau des composants

Un seul fichier suffit. Vider `updates/`, y copier soit le bundle `WIKIDEBIA_SOURCES_COMPLETES_*.zip`, soit la livraison complète `WIKIDEBIA_LIVRAISON_*.zip`, puis lancer `./wikidebia upgrade`.

## Publication française avec anglais différé (1.2.35, compatible avec les corpus historiques 1.2.x)

Le corpus déclare `translation_status.en=deferred`, ne manifeste que les pages françaises et omet `interlangue`. Utiliser `./wikidebia publish --scope fr` ou `./wikidebia update --archive <archive> --scope fr`. Toute portée anglaise est refusée jusqu'au passage à `ready` ou `published`.

## Guide de revue du contenu

Source interne : `kit/GUIDE_CONTENT_REVIEW.md`  
SHA-256 : `8163dcf1c03fbe3c4fb447a3814396e10fe2b8806d3b297ffdadad335fac5efa`

# Revue française des introductions, résumés et références

> Depuis 1.2.54, les normes éditoriales sont cumulatives : les anciennes métadonnées de révision ne servent plus à sélectionner les contrôles.

Le kit 2.15.31 applique une phase de contenu après le verrouillage des titres, rubriques et mots-clés. Elle part de `reviewed-copy/`, conserve toutes les copies antérieures et ne génère toujours aucune page MediaWiki finale.

## 1. Préparer la revue

```bash
./wikidebia corpus-workspace-content-review <debate_id> \
  --work-id <work_id> \
  --prepare
```

La commande lit le wikicode importé et crée :

```text
reviews/fr/content_review.json
data/sources_working.json
audits/fr_content_inventory.json
audits/fr_content_inventory.md
```

Le registre couvre :

- `sujet` et `sujet-complet` de la page Débat ;
- l’introduction et chacune de ses sous-parties ;
- les articles Wikipédia français vérifiés ;
- les neuf paramètres documentaires de la page Débat ;
- le résumé de chaque argument ;
- les données de contenu des arguments français importés ; les arguments réellement nouveaux ne sont pas créés par cette commande et doivent, lorsqu’un corpus en contient, être accompagnés de la revue documentaire 1.2.53 décrite ci-dessous ;
- la bibliographie, la sitographie et la vidéographie de chaque argument ;
- les attestations de lisibilité, de fidélité logique, de force expressive et de vérification documentaire.

Aucune proposition produite par une heuristique n’est appliquée automatiquement.


## Recherche d’un nom consacré pour un argument nouveau

Cette exigence relève du contrat général de génération 1.2.53. La commande `corpus-workspace-content-review` ci-dessus part d’un snapshot importé et ne crée donc pas elle-même de nouvel argument français. Lorsqu’un corpus généré contient des pages `Argument` françaises nouvelles, il doit fournir `reviews/argument_name_discovery_review.json` avant validation ; le validateur 0.4.57 bloque toute page nouvelle non couverte. La phase de traduction anglaise du kit construit la partie anglaise de ce registre pour les pages anglaises nouvelles.

La recherche est **obligatoire**, mais l’ajout d’un nom ne l’est pas. Le cas normal est `outcome=none`. Il ne faut jamais chercher à augmenter artificiellement le nombre de pages possédant `nom=`.

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

- l’inventaire exhaustif, sous-partie par sous-partie, des notions spécialisées, avec vérification de chaque lien, explication intégrée, traitement antérieur ou justification contextuelle ;

- la couverture exacte de tous les arguments actifs ;
- l’existence d’une introduction structurée en sous-parties ;
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
- l’absence de métadiscours et d’auto-objection dans les résumés ;
- la présence réelle de l’expression attestant la force du résumé ;
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

Cette phase ne traduit rien, ne produit pas `output/`, ne contacte pas MediaWiki et ne construit pas de plan de reprise distante.

## Rapport de tests du kit

Source interne : `kit/TEST_REPORT.txt`  
SHA-256 : `69c624e95fc6149ecd04562e3b72dc7aec5f4c46f4a6d898c678e6993001932d`

Tests pytest : 290 réussis, 0 échec.

## Guide de traduction anglaise

Source interne : `kit/GUIDE_TRANSLATION_REVIEW.md`  
SHA-256 : `ce4b5738b1e5ebb564572297aa182dde0c23f1b278c1aadf9188bdd3ec35bfa1`

# Guide de traduction anglaise contrôlée — Kit 2.15.31

> Les règles ci-dessous sont cumulatives et ne dépendent pas d’un numéro `*_revision`. Cette architecture cumulative a été formalisée par la révision 1.2.54.

La traduction anglaise commence uniquement après le verrouillage complet des métadonnées et du contenu français. Elle travaille dans le même workspace éditorial et ne modifie ni le corpus promu, ni `working-copy/`, ni `reviewed-copy/`, ni `content-reviewed-copy/`.

## 0. Protocole de lots pour la traduction

La traduction est une adaptation idiomatique et documentaire, pas une substitution mot à mot. Elle est effectuée dans l'ordre suivant :

1. **Lot Debate** : la page `Debate` complète constitue un lot autonome, avec son introduction, ses titres, ses sections, ses keywords, ses liens Wikipédia anglais et toute sa documentation anglaise.
2. **Lots Argument** : 20 pages Argument par lot par défaut, jamais plus de 25. Réduire à 10–15 pages lorsque le groupe comporte beaucoup de citations, de références, de recherches terminologiques ou de noms consacrés à vérifier.
3. Une page Argument est entièrement achevée dans le même lot : canonical title, displayed title, summary, sections, keywords, `name=` éventuel, citations et références.
4. Chaque lot est relu et clos avant le suivant. Il faut notamment vérifier le sens et l'orientation de chaque argument à partir du summary français, des citations, justifications et objections disponibles, afin d'éviter une inversion pour/contre.
5. Après le dernier lot, effectuer une passe globale inter-lots sur la terminologie, les titres, le vocabulaire bilingue, les `name=`, les références, les citations et la parité du graphe avant `--finalize`.

Ces tailles sont des bornes de qualité de travail, non des quotas de contenu. Un lot peut être réduit davantage si cela améliore la fiabilité de la recherche documentaire.

## 0.1 Règle source-authoritative et métadonnées FR→EN

Pour la rédaction de la traduction, **faire comme si la page anglaise cible n'existait pas**. Une éventuelle page anglaise déjà publiée ne sert pas de source pour le texte, les titres, le plan, `progress`, les avertissements, les références ou les relations. Le corpus français validé est la source éditoriale. Les contrôles techniques distants nécessaires à une future publication restent séparés de cette règle.

Traduire les métadonnées réellement présentes, sans appliquer les valeurs de création par défaut :

- `avancement` : `Ébauche`→`Draft` ; `Débat en construction`→`Debate under construction` ; `Débat construit`→`Constructed debate` ;
- `avertissements-titre` du Débat : `Titre non standard`→`Non-standard title` ; `Titre à simplifier`→`Title to simplify` ; `Titre à expliciter`→`Title to be explained` ;
- `avertissements-débat` : `Débat sensible`→`Sensitive debate` ; `Débat saugrenu`→`Fanciful debate` ; `Débat redondant`→`Redundant debate` ; `Débat déséquilibré`→`Unbalanced debate` ; `Plan à améliorer`→`Plan to improve` ; `Débat généré par IA`→`Debate generated by AI` ;
- `avertissements-titre` de l'Argument : `Titre désavantageux`→`Disadvantageous title` ; `Titre peu clair`→`Unclear title` ; `Titre incomplet`→`Incomplete title` ; `Titre trop long`→`Too long title` ;
- `avertissements-argument` : `Argument sensible`→`Sensitive argument` ; `Argument saugrenu`→`Fanciful argument` ; `Argument potentiellement illégal`→`Potentially illegal argument` ; `Argument généré par IA`→`Argument generated by AI`.

Un paramètre absent en français reste absent en anglais. Une valeur non reconnue déclenche une revue ; elle n'est pas traduite par approximation. Pour un champ multiple, traduire chaque valeur présente dans le même ordre.

Pour `related-debates`, partir uniquement des débats connexes français et vérifier l'existence de chaque page anglaise correspondante. Ajouter seulement les cibles anglaises vérifiées comme existantes ; ne rien inventer et omettre le paramètre si aucune cible anglaise n'existe.

Avant de clore le lot, refaire une passe distincte de vérification FR→EN : métadonnées exactes, absence de défauts ajoutés, débats connexes vérifiés, sens et polarité conservés, anglais idiomatique, aucun wikicode français résiduel, références anglaises réelles et contrat `Citation`→`Quote` respecté.

## 1. Préparation

```bash
./wikidebia corpus-workspace-translation <debate_id> --work-id <work_id> --prepare
```

La commande exige un workspace au statut `fr_content_applied` et une préparation anglaise `ready_for_translation`. Elle produit :

- `reviews/en/translation_review.json` ;
- `data/sources_en_working.json` ;
- `audits/en_translation_inventory.json` ;
- `audits/en_translation_inventory.md`.

Le registre couvre la page Debate, chaque argument actif, le vocabulaire contrôlé français–anglais et les sources anglaises. Aucune traduction automatique n’est appliquée.

## 2. Revue à compléter

La page Debate reçoit un titre canonique, `topic`, `complete-topic`, des sections, des keywords, une introduction structurée, des articles Wikipédia anglais vérifiés et une documentation classée selon sa contribution réelle, sans quota par paramètre. Une source couvrant les deux positions est placée dans la rubrique neutre.

Chaque argument reçoit un titre canonique et un displayed title idiomatiques, des sections exactement équivalentes aux rubriques françaises, des keywords issus du vocabulaire bilingue, un summary substantiellement équivalent et une documentation anglaise adaptée. Le ratio de longueur anglais/français doit rester compris entre 0,60 et 1,45. La traduction vérifie explicitement la polarité du raisonnement : le titre seul ne suffit pas lorsqu'il peut être ambigu ; le summary français, les citations, justifications et objections disponibles servent à confirmer si l'argument soutient ou combat la thèse parente.

Les relations, occurrences, orientations et profondeurs sont linguistiquement neutres : elles ne peuvent pas être modifiées pendant cette phase.

### Références anglaises

Une référence française n'est **jamais traduite comme notice anglaise**. Pour chaque référence française pertinente, rechercher si une version anglaise réelle existe : édition ou traduction anglaise publiée, publication originale anglaise, version anglaise officielle d'une page ou d'un rapport, version audiovisuelle anglaise officielle, ou autre équivalent documentaire vérifiable.

Si cet équivalent existe, enregistrer et citer **la version anglaise elle-même**, avec son titre publié, son éditeur/diffuseur, sa date, son lien et ses autres métadonnées vérifiées. Ne jamais traduire librement le titre ou recopier les métadonnées françaises comme si elles appartenaient à une édition anglaise. Si aucune version anglaise n'existe, ne pas transférer cette référence au seul motif qu'elle existe en français.

Chaque page anglaise fait en outre l'objet d'une **recherche indépendante de nouvelles références anglophones**. La documentation anglaise doit refléter la littérature réellement disponible en anglais et peut donc différer de la sélection française tout en conservant une profondeur et une qualité comparables. Pour la page Debate, toutes les références doivent être réellement disponibles en anglais. Pour les pages Argument, la politique linguistique générale demeure symétrique à celle du français ; une éventuelle source non anglaise est sélectionnée indépendamment selon cette politique, jamais produite par traduction artificielle d'une notice française.

### Citations importées

Chaque modèle `{{Citation}}` français importé est inventorié avec un identifiant stable. La projection anglaise utilise `{{Quote}}` et traduit obligatoirement tous les noms de paramètres selon le contrat du wiki anglais : `citation→quote`, `auteurs→authors`, `ouvrage→work`, `numéro→issue`, `localisation→location`, `édition→publisher`, `lieu→place`, `lien→link` et `avertissements-citation→warnings`; les noms `article`, `volume`, `page` et `date` sont identiques dans les deux langues.

Seules les valeurs de `quote` et de `date` peuvent être traduites. Les valeurs de `authors`, `article`, `work`, `volume`, `issue`, `page`, `location`, `publisher`, `place` et `link` sont reprises exactement. `warnings` reçoit toujours `Citation traduite par IA`, après un avertissement préexistant avec le séparateur exact `, `. La date traduite doit désigner la même date ; une année seule reste inchangée. Un paramètre français sans équivalent anglais déclaré bloque la finalisation.

## 3. Finalisation

Avant d’exécuter `--finalize`, la revue éditoriale du travail doit avoir contrôlé et consigné : la clôture de chaque lot ; l’existence d’un équivalent anglais réel pour toute référence française projetée ; la recherche indépendante de nouvelles références anglophones ; la recherche autonome de `name=` dans la littérature anglophone ; et la passe globale inter-lots. Ces opérations de recherche ne sont pas toutes déductibles automatiquement du wikicode final : elles restent des obligations éditoriales même lorsque le validateur ne peut en vérifier que les traces structurées disponibles.

```bash
./wikidebia corpus-workspace-translation <debate_id> --work-id <work_id> --finalize
```

La finalisation vérifie notamment :

- la couverture exacte de tous les arguments actifs ;
- l’unicité et l’autonomie des titres canoniques anglais ;
- le caractère propositionnel des displayed titles ;
- la possibilité de conserver le titre canonique comme displayed title lorsqu’il est déjà le plus clair ;
- pour tout displayed title distinct, l’équivalence sémantique et le gain réel de lisibilité ;
- la correspondance des sections avec les rubriques françaises ;
- la correspondance des keywords avec le vocabulaire contrôlé ;
- la limite de 25 % pour un même jeu exact de keywords ;
- l’équivalence substantielle des introductions et summaries ;
- la couverture exacte des citations françaises, la préservation de leurs paramètres, l’équivalence des dates et l’avertissement de traduction ;
- la langue et la vérification des sources anglaises ;
- l’absence de doublon documentaire entre orientations et l’attribution des vidéos YouTube ;
- la présence des attestations éditoriales requises ;
- l’absence de page finale et d’accès distant.

La revue et le registre documentaire anglais sont scellés par SHA-256.

## 4. Application

```bash
./wikidebia corpus-workspace-translation <debate_id> --work-id <work_id> --apply --confirm-review-sha256 <empreinte>
```

L’application crée atomiquement `translated-copy/`. Cette copie contient notamment :

- `data/en_page_metadata_lock.json` ;
- `data/en_content_lock.json` ;
- `data/en_translation_lock.json` ;
- `data/keyword_vocabulary_bilingual.json` ;
- `changes/en_translation_changeset.json` ;
- les projections anglaises du registre maître ;
- les rapports de validation de la traduction.

Les verrous français et les imports de provenance doivent rester identiques octet par octet. Aucune page sous `output/` n’est créée.

## Ordre des keywords

La traduction conserve terme à terme l’ordre français de pertinence décroissante. Chaque entrée Debate et Argument atteste `keywords_order_preserved_by_relevance=true`.

## Sortie du mode différé

Une revue de traduction validée remplace `translation_status.en=deferred` par `ready`. Elle verrouille les titres anglais, prépare les pages anglaises et réactive les contrôles bilingues. Les liens français sont ajoutés ensuite par une reprise explicite ; ils ne sont jamais anticipés.



## Noms consacrés des arguments anglais

Un `name=` anglais n’est jamais obtenu par simple traduction d’un `nom=` français. Pour chaque page Argument anglaise nouvelle, la revue recherche séparément l’appellation réellement employée dans la littérature anglophone. Le résultat par défaut reste l’absence de nom ; une valeur n’est verrouillée que si la littérature désigne le même raisonnement sous cette appellation. L'existence d'un `nom=` français sert uniquement de piste pour les requêtes. Une traduction anglaise plausible mais non attestée ne doit jamais être inscrite dans `name=`.
