# Workflow de production Wikidéb’IA — norme 1.2.7

**Statut :** workflow actif générique  
**Portée :** production bilingue français–anglais, validation et publication MediaWiki

## 1. Principes

Le registre maître et les fichiers individuels sont les sources de vérité. Les titres canoniques français et anglais sont verrouillés avant la première génération des pages françaises. Les pages françaises contiennent donc immédiatement leur lien `{{Lien interlangue}}`, même si les pages anglaises sont rédigées et publiées ensuite. Leur publication n’exige pas que les pages anglaises existent déjà dans le manifeste : le titre anglais verrouillé du registre maître suffit.

Aucun paquet 1.2.x ne produit de patch interlangue tardif ni de copie `staging/interlanguage/`. Les anciens dossiers restent lisibles uniquement pour la compatibilité historique.

Chaque Work reçoit un handoff vérifié, modifie uniquement les champs autorisés et livre des rapports reproductibles. Aucune écriture distante n’est autorisée avant W11.

## 2. États actifs

```text
initialized
→ graph_draft
→ graph_validated
→ graph_locked
→ fr_debate_validated
→ fr_arguments_in_progress
→ fr_content_complete
→ fr_validated
→ en_debate_validated
→ en_arguments_in_progress
→ en_content_complete
→ en_validated
→ bilingual_validated
→ interlanguage_validated
→ release_ready
→ published
→ archived
```

Les états `interlanguage_prepared` et `interlanguage_applied` sont historiques. Le validateur peut les accepter pour les paquets antérieurs à 1.2.0, mais une nouvelle production ne les émet pas.

## 3. Work 00 — Cadrage

Définir la proposition, le périmètre, les acteurs, juridictions, ambiguïtés, exclusions, versions normatives, date de création attendue et chemins du paquet. Créer `manifest.json`, `scope.json` et le registre initial sans inventer de contenu documentaire.

## 4. Work 01 — Recherche, graphe et titres bilingues

Effectuer les recherches et passes d’omission, construire puis consolider le DAG, fixer les occurrences et lots, et verrouiller les titres canoniques et affichés français et anglais. La rédaction anglaise des pages reste différée ; seul le titre anglais est nécessaire à ce stade pour les liens français directs.

Contrôles obligatoires : DAG, absence de doublons, autonomie référentielle, titres idiomatiques, équilibre, saturation documentée, empreinte structurelle et revue humaine.

## 5. Work 02 — Page Débat française

Créer la page française avec `{{Lien interlangue}}` vers le titre canonique anglais verrouillé. Concevoir l’introduction à partir des connaissances nécessaires au lecteur : définition et périmètre, sens de la question, histoire, actualité lorsqu’elle est pertinente, connaissances préalables et enjeux. Lors de la rédaction, repérer les notions spécialisées dont une définition secondaire aiderait le lecteur : utiliser à leur première occurrence `{{Lien Wikipédia|article=…}}` en français ou `{{Wikipedia link|article=…}}` en anglais lorsque le premier paragraphe de Wikipédia suffit ; sinon conserver une explication intégrée. Vérifier la page dans la langue correspondante, réserver le paramètre d’affichage aux différences réelles de libellé et ne jamais considérer ce lien comme une référence. Chaque sous-partie répond à une question identifiable ; une section technique explique pourquoi elle compte pour le débat. L’introduction ne reproduit ni le graphe ni une checklist issue d’un corpus pilote. Produire le registre bilingue de revue des introductions. Les appels `<ref>…</ref>` sont ajoutés lorsque nécessaire ; leur contenu bibliographique ou web est rédigé directement en wikicode, sans aucun modèle MediaWiki et sans balise `<references />`. Les dates documentaires complètes sont écrites en langage naturel. Aucun minimum global ou par sous-partie n’est recherché. Toutes les références de la page Débat sont disponibles en français. La bibliographie privilégie les ouvrages fondamentaux et synthèses larges. Chacun des neuf paramètres documentaires de la page Débat contient au moins deux références distinctes.

## 6. Work 03 — Arguments français

Produire les pages par lots séquentiels. Chaque page contient son lien interlangue initial, reproduit exactement les relations du registre, emploie des références françaises lorsqu’un équivalent officiel existe et justifie toute source étrangère sans équivalent. Les incises françaises utilisent des parenthèses, non des tirets cadratins appariés.

## 7. Work 04 — Validation française

Exécuter au minimum les portées `schema`, `coherence`, `graph`, `files`, `batches`, `sources`, `wikicode`, `editorial` et `workflow`. Vérifier notamment le registre de revue de l’introduction, la fonction de chaque sous-partie, la progression et l’absence de minimum mécanique ou de checklist de corpus. Corriger les pages sources puis régénérer agrégats et empreintes. Zéro erreur et zéro avertissement non résolu sont exigés.

## 8. Work 05 — Audit des titres bilingues

Vérifier que les titres anglais verrouillés sont idiomatiques, autonomes et équivalents aux titres français. Toute modification est une migration qui met à jour le registre, les pages françaises et toutes les cibles interlangues avant la production anglaise.

## 9. Work 06 — Page Debate anglaise

Créer la page anglaise autonome avec `topic` et `complete-topic`, sans `type` ni interlangue. Adapter le contexte et utiliser des sources anglaises vérifiées.

## 10. Work 07 — Arguments anglais

Produire les pages anglaises par lots avec la même structure logique, une profondeur documentaire comparable et une rédaction idiomatique. Les pages anglaises ne contiennent jamais d’interlangue.

## 11. Work 08 — Validation anglaise

Exécuter les mêmes portées applicables que pour le français, notamment `wikicode` et `editorial`. Vérifier références, titres, relations, agrégats et empreintes.

## 12. Work 09 — Validation bilingue

Contrôler l’identité des nœuds, relations, occurrences, réutilisations et propriétaires de lots, ainsi que l’équivalence substantielle des résumés, rubriques/sections et mots-clés.

## 13. Work 10 — Audit interlangue et prépublication

Vérifier exactement un `{{Lien interlangue}}` dans chaque page française, sa cible canonique anglaise, l’absence de lien en anglais et l’absence totale de patch ou staging actif. Produire `reports/validation_interlanguage.txt`, la revue finale, le manifeste de libération et le handoff W11. W10 n’écrit jamais sur le wiki.

## 14. Work 11 — Simulation, test de la page Débat et publication

1. Exécuter toutes les portées applicables du validateur, y compris `wikicode` et `editorial`.
2. Construire un plan déterministe signé par SHA-256.
3. Vérifier les modèles publics, l’identité, la balise `chatgpt`, les collisions et les empreintes.
4. Créer en premier l’unique page Débat française canonique, obligatoirement absente dans le plan, avec `createonly` ; relire la révision exacte et produire un reçu machine signé.
5. Avant toute autre écriture, recharger le même plan et le reçu, vérifier leurs empreintes et confirmer que la page Débat est toujours à la révision attestée avec le même contenu, le même résumé et la même balise.
6. Créer ensuite les autres pages françaises. Pour l’anglais, créer d’abord la page Debate puis les pages Argument anglaises. Dans chaque langue, la page principale précède donc toujours ses arguments.
7. Ne créer aucune sous-page utilisateur de test. Une page Débat française préexistante bloque le test au lieu d’être écrasée ou réutilisée comme preuve.

8. Le flux ordinaire est exposé par une commande intégrée unique : déposer le ZIP dans `incoming/`. Si un seul ZIP est présent, lancer `./wikidebia publish --scope PORTÉE`; s’il y en a plusieurs, lancer `./wikidebia publish IDENTIFIANT --scope PORTÉE`. Le fichier sélectionné est `incoming/IDENTIFIANT.zip`; son nom sert seulement à sélectionner l’archive et le `debate_id` interne détermine l’identité du corpus. Les portées `fr-debate`, `en-debate`, `fr`, `en` et `all` sont canoniques.
9. Après succès, le ZIP du débat est déplacé dans `archives/debates/`; le corpus extrait reste dans `corpus/`, hors Git.
8. Utiliser `createonly` pour toute création. Une modification explicitement autorisée exige `baserevid`.
9. Relire chaque révision exacte, vérifier contenu, résumé et balise, puis journaliser.
10. S’arrêter sur toute divergence, collision, perte d’identité, changement de plan ou révision concurrente.

Une mise à jour interlangue distincte n’est admise que lorsque la langue cible est préparée (`ready` ou `published`) et que le workflow la prévoit explicitement. Elle reste interdite tant que `translation_status.en=deferred`; aucun lien provisoire n’est créé.

## 15. Reprises correctives

Le cycle est `release_ready → corrective_in_progress → corrective_blocked` si nécessaire, puis retour à `release_ready` après validation complète. Les handoffs historiques sont immuables. Les constantes propres à un débat restent dans son profil local.

## 16. Livrables

Le paquet final contient le registre, le graphe, les pages individuelles, agrégats, sources, lots, rapports, revues humaines, manifestes, handoffs, journaux locaux et reçus SHA-256. Les archives de normes, validateur et kit possèdent des manifestes exhaustifs.

## Addendum 1.2.6 — contrôles éditoriaux avant libération

Avant `release_ready`, la reprise trie toutes les rubriques et sections dans leur langue, vérifie la majuscule initiale de `sujet`/`topic`, reformule les sujets complets comme compléments d’en-tête et réévalue la sélection documentaire de chaque page Débat/Debate. La revue des résumés enregistre pour chaque langue un extrait exact attestant la force expressive ; une attestation générique répétée sur toutes les pages est insuffisante.

## Addendum 1.2.7 — cohérence de livraison

Le workflow de production et de publication reste identique à celui de 1.2.6. Les composants génériques doivent toutefois refuser toute archive dont le catalogue renvoie à un fichier absent ou dont le compteur `declared_file_count` diverge.


## Publication française avant production anglaise — norme 1.2.9

Une opération W11 peut sélectionner uniquement `fr`. Le kit vérifie alors chaque cible `{{Lien interlangue}}` contre le titre anglais verrouillé dans `data/registre_debat.json`. L’absence des pages anglaises correspondantes dans `manifest.json` n’est pas bloquante. Elle le devient seulement si aucun titre anglais verrouillé ne permet de vérifier la cible française.


## Addendum 1.2.11 — passe de compaction avant validation

Après chaque génération ou correction de pages, rechercher récursivement la séquence `}}` suivie d’un ou plusieurs retours à la ligne puis de `{{`, avec d’éventuels espaces ou tabulations. Remplacer chaque occurrence par `}}{{` avant de régénérer les agrégats et les empreintes. Les portées `wikicode` et le préflight du kit bloquent toute occurrence résiduelle.
## 18. Installation, mises à jour et sauvegarde Git

L’installation est portable et pilotée par le lanceur racine `wikidebia`. Les composants entrants sont déposés dans `updates/`; `./wikidebia update` les vérifie, les teste, archive les versions précédentes dans `archives/updates/`, remplace les composants, vide `updates/` et synchronise le dépôt Git lorsque `origin` est configuré.

Le dépôt suit les sources génériques et la documentation, mais ignore `private/`, `corpus/`, `archives/`, `updates/`, `incoming/`, `logs/`, `plans/`, `.state/` et `.venv/`. Les secrets Pywikibot résident dans `private/pywikibot/`. Aucun rapport ou fichier persistant ne contient le chemin absolu de l’installation.


Les ZIP encore présents dans l’ancien dossier `incoming/debates/` sont migrés automatiquement vers `incoming/` pendant la mise à jour. Toute collision de noms avec un contenu différent bloque l’opération sans écrasement.


## Compatibilité de publication — norme 1.2.15

Avant de construire le plan, le kit exécute le validateur installé sur le corpus. La version réelle du validateur doit correspondre à celle exigée par le kit et le rapport doit être positif. Les versions historiques inscrites dans `manifest.json` ne sont ni comparées pour égalité aux versions installées, ni réécrites. La norme déclarée reste soumise à la liste de compatibilité et aux schémas du validateur courant.


## Reprise distante d’un corpus publié — révision 1.2.16

Une reprise compare obligatoirement le dernier état publié signé, l’état distant courant et le nouveau corpus validé. Le kit produit un plan signé comprenant `create`, `skip`, `update`, `move`, `redirect`, `delete`, `manual_review` et `blocked`. Une page absente du nouveau manifeste n’est jamais supprimée sans preuve d’appartenance à la version antérieure du même débat.

Les mises à jour et suppressions vérifient la révision ou l’empreinte attendue et utilisent le contrôle de concurrence MediaWiki. Toute modification humaine ou provenance indéterminée est classée `manual_review`. Les déplacements et fusions sont déclarés explicitement. Les suppressions sont exécutées seulement après vérification du nouveau graphe publié. Les opérations sont idempotentes et donnent lieu à un reçu final et à un nouvel état publié signé.

Le validateur contrôle localement les structures et la cohérence des plans, mais toutes les lectures et écritures MediaWiki restent dans le kit.

## Correctif 1.2.17 — contrôles avant publication

Avant la signature du plan, le validateur et le kit vérifient que chaque page Débat/Debate contient au moins un article Wikipédia vérifié, que les pages nouvelles n’ajoutent aucun `débats-connexes` ou `related-debates` et que les pages préexistantes en préservent exactement l’état et qu’aucun champ `auteurs`/`authors` ne contient un tableau JSON littéral.

La commande `./wikidebia publish` est entièrement non interactive : après validation positive et génération du plan, l’orchestrateur transmet lui-même l’empreinte SHA-256 du plan au moteur. L’option historique `--yes` reste tolérée pour compatibilité mais n’est plus nécessaire et aucune question `[o/N]` n’est affichée. La commande `update`, qui peut inclure des suppressions, conserve sa confirmation d’empreinte ou son équivalent automatisé explicite.

## Contrôle 1.2.19 des titres affichés

Avant le verrouillage du graphe et avant toute génération de page, chaque titre affiché est lu comme une phrase indépendante. La revue vérifie la présence d’un sujet, d’un prédicat et de la conclusion argumentative utile. Un intitulé nominal est reformulé, même lorsque le parent de l’occurrence permettrait d’en deviner le thème. Les quatre attestations bilingues de complétude et d’intelligibilité sont enregistrées dans le registre individuel ; une attestation absente ou fausse bloque la validation éditoriale.


## Contrôle 1.2.20 du placement des arguments

Avant `graph_validated`, effectuer une passe indépendante qui ne juge ni le style des titres ni le nombre de nœuds, mais uniquement la fonction logique des occurrences.

1. Pour chaque occurrence de niveau 1, formuler en une phrase sa réponse directe à la proposition du débat.
2. Rechercher un parent plus général non redondant. S’il existe, déplacer l’occurrence sous ce parent.
3. Vérifier si l’argument vise spécialement une preuve, une prémisse ou un mécanisme déjà présent. Dans ce cas, le rattacher comme objection ou justification à cette cible.
4. Regrouper sous une thèse générale les exemples historiques, résultats scientifiques, doctrines particulières, applications sectorielles et précisions techniques qui n’ouvrent pas une famille autonome.
5. Refaire le test après chaque déplacement, puis régénérer profondeurs, branches, lots, projections et empreinte structurelle.
6. Produire `reports/graph_placement_review.json` et le déclarer dans `editorial_controls.graph_placement_review_path`.

Le cas « les bouleversements de l’histoire des sciences » sert de test de régression générique : lorsqu’il conteste l’inférence du succès scientifique à la vérité ou au réalisme, il doit être une objection sous l’argument du succès scientifique, non un argument principal parallèle.

### Renforcement 1.2.22 — concision des titres affichés

Pour chaque langue, le registre individuel contient `displayed_title_concision_reviewed_fr` ou `displayed_title_concision_reviewed_en` à `true`. Lorsqu’un titre affiché est exactement identique au titre canonique, le champ `displayed_title_identity_justification_fr` ou `displayed_title_identity_justification_en` fournit une justification spécifique, substantielle et non générique. Le taux global d’identités exactes ne dépasse pas 10 % des arguments actifs par langue. La concision ne dispense jamais des exigences de proposition complète, de prédicat explicite et d’intelligibilité autonome.


## Workflow 1.2.23

Avant validation, la revue choisit un sujet nominal conventionnel, contrôle la minuscule du complément, puis effectue une seconde recherche d’auteur chaque fois qu’une attribution provisoire reproduit le nom du site. Les reprises distantes utilisent « Corrections ». Le ZIP de livraison unique expose les trois composants à sa racine ; le gestionnaire courant sait également les découvrir dans un bundle imbriqué.

## Reprise sûre depuis la révision 1.2.25

Le planificateur peut produire `manual_review`, mais le gestionnaire et l’exécuteur refusent tous deux de l’exécuter. Aucun reçu final ni état publié n’est écrit dans ce cas. Un plan sans opération mutante renvoie `no_changes`. Une archive demandée par `--archive` est validée depuis une zone de staging ; `--dry-run` ne modifie pas le corpus installé. La promotion vers `corpus/<debate_id>/` intervient seulement après une exécution réelle sans opération non résolue.

## Attestation et portées différées depuis la révision 1.2.26

Un plan entièrement `skip` est attesté par une commande dédiée qui recharge le plan signé, relit toutes les pages et renouvelle l’état publié sans écrire sur MediaWiki. Toute archive de reprise requiert `--archive`; le staging est supprimé à chaque sortie. Si la portée demandée ne contient aucune opération mutante, la commande renvoie `no_changes_in_scope`. Avec `--no-delete`, les pages retirées mais non supprimées restent dans l’état signé sous le statut `pending_delete` jusqu’à une reprise `--only-delete`.



## Contrôle création/modification — révision 1.2.33

Avant rendu, chaque page est classée `new` ou `preexisting`. Toute page préexistante possède un instantané des paramètres protégés importés. Le rendu et le plan de mise à jour comparent cet instantané au wikicode proposé et bloquent toute mutation de `avancement`, `progress`, des avertissements IA et des débats connexes.

## Traduction anglaise différée — révision 1.2.34

Le manifeste peut déclarer `translation_status.en=deferred`. Dans ce cas, les Works français, la validation et `./wikidebia update --archive <archive> --scope fr` n'exigent ni titre anglais, ni page anglaise, ni lien interlangue. Les étapes anglaises et les contrôles bilingues sont suspendus. `--scope en` est bloqué. Après traduction, le statut passe à `ready` ou `published`; les titres anglais sont verrouillés, les pages anglaises sont ajoutées, puis une reprise française distincte ajoute les liens interlangues sans changer les dates de création. Cette section remplace toute instruction antérieure imposant le verrouillage anglais avant la génération française.

## Correctif 1.2.35 — traduction différée sur corpus historique

`translation_status.en=deferred` est lu comme un état opérationnel explicite, indépendamment de la révision éditoriale 1.2.x déclarée. `--scope fr` reste autonome ; `--scope en` est bloqué jusqu'au passage à `ready` ou `published`.

## Ponctuation des notes de référence (1.2.44)

Une simple notice documentaire placée dans `<ref>…</ref>` ne se termine pas par un point avant `</ref>`. Le point de la phrase principale vient après l’appel de note. Un point terminal interne est réservé à une phrase explicative complète et doit être attesté dans la revue par l’empreinte du corps exact de la note.

## Cohérence locale des liens Wikipédia explicatifs (1.2.45)

Les notions spécialisées de même rang énumérées ou comparées dans un même passage sont revues comme un groupe. Lier une seule notion alors que les notions voisines disposent d’articles pertinents et présentent le même besoin explicatif est interdit sans justification explicite. Le registre `wikipedia_link_groups` consigne la sous-partie, les termes, les articles, la décision et toute exception.



## Inventaire général des notions spécialisées (1.2.46)

La revue ne se limite pas aux séries de notions comparables. Chaque sous-partie est examinée intégralement et reçoit une entrée dans `specialized_term_inventory`. Toute notion susceptible d’arrêter un lecteur est liée, expliquée, rattachée à un traitement antérieur ou déclarée intelligible en contexte avec une justification spécifique. Tous les liens Wikipédia réellement présents sont recensés. Le registre `wikipedia_link_groups` de 1.2.45 est remplacé comme mécanisme actif par cet inventaire général.

## Traduction anglaise adaptative — révisions 1.2.53 et 1.2.55

Après verrouillage du français, la page Debate anglaise est traduite et documentée comme un lot autonome. Les pages Argument sont ensuite relues en unités internes de 10 pages par défaut, réduites à 5–8 pour les groupes riches en citations, recherches documentaires, ambiguïtés terminologiques ou anomalies de préservation. Une livraison longue peut agréger plusieurs unités déjà closes ; une page Argument est entièrement traitée dans une seule unité.

Chaque unité inclut : traduction idiomatique ; contrôle de l'orientation argumentative ; recherche autonome d'un éventuel `name=` anglais ; comparaison des formes anglaises concurrentes sans normaliser artificiellement `X argument`, `Argument from X`, les possessifs ou d'autres constructions attestées ; vérification que le nom couvre exactement la portée de la page ; recherche d'une version anglaise réelle pour les références françaises pertinentes sans traduction artificielle de leurs notices ; recherche de nouvelles références anglophones ; traitement des `Citation`→`Quote` selon le contrat qui ne traduit que `quote` et `date` et ajoute `AI-translated quote`. Les checklists et exemples sont des garde-fous et non des patrons de rédaction.

Une passe globale inter-unités est obligatoire avant finalisation afin d'harmoniser terminologie, titres, vocabulaire, documentation et noms consacrés et de vérifier la parité complète du graphe. Lorsqu'un résumé français est historiquement absent et verrouillé comme tel, l'anglais conserve cette absence et aucun résumé de remplacement n'est généré.

## Architecture cumulative depuis 1.2.54

Les numéros de norme et les anciens champs `*_policy_revision` / `*_revision` ne sélectionnent plus les règles éditoriales. Le workflow applique la norme consolidée courante à partir de l’état fonctionnel du corpus. Les versions globales restent disponibles pour la lecture d’anciens formats, les migrations, la provenance et l’identification d’une livraison. Un registre ou un artefact dont le format évolue utilise sa propre version de schéma.

## Résumé de publication des traductions anglaises

Pour une page anglaise créée comme traduction d’une page française verrouillée, le résumé MediaWiki est individualisé : `Translation of the French page: [[:fr:X|X]]`, où `X` est le titre canonique français de la même `page_id`. Le plan signé conserve cette valeur page par page ; l’exécuteur la recalcule depuis le manifeste avant écriture et la relecture de la révision créée en vérifie l’identité exacte. Le résumé générique anglais reste réservé aux créations qui ne sont pas des traductions. Ce lien d’historique ne remplace pas le lien interlangue rendu dans la page française après passage à `ready`.

