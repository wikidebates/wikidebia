# Décisions correctives à intégrer à la norme consolidée — 25 juillet 2026

## Statut

Ces décisions ont été explicitement demandées par le propriétaire du projet après la simulation locale du Work 11. Aucune page n’a été publiée sur le wiki. Elles remplacent les règles antérieures incompatibles pour la reprise corrective du débat `parapsychologie_science` et doivent être intégrées dans une norme consolidée unique.

## Ordre de priorité

Le présent document prime sur les règles 1.0.6, le correctif du 23 juillet 2026 et les audits lorsqu’ils contiennent une consigne incompatible. Les audits sont descriptifs ; ils ne peuvent pas annuler une décision corrective explicite.

## 1. Résumés d’arguments sans auto-objection

Le résumé défend la version la plus forte, convaincante, autonome et fidèle du raisonnement porté par le nœud.

Il ne doit pas :

- anticiper une objection ;
- conclure par sa propre réfutation ;
- ajouter une réserve uniquement destinée à équilibrer la présentation ;
- diminuer artificiellement la portée de l’argument par une phrase de concession ;
- contenir de métadiscours sur « l’argument », « la page » ou « le raisonnement présenté ».

Les objections et limites opposables sont portées par les pages d’objections reliées. Les délimitations indispensables à l’identité exacte de la proposition peuvent être conservées, mais doivent être formulées positivement et ne pas fonctionner comme une auto-réfutation.

La réécriture doit préserver le nœud logique : prémisses, mécanisme, conclusion, orientation et portée. Elle ne doit pas ajouter une thèse absente ni présenter comme démontré ce que les sources ne soutiennent pas.

## 2. Pagination bibliographique

Pour une page ou une plage de pages, utiliser :

```mediawiki
|page=36-37
```

La valeur ne contient pas les mots « page », « pages », « p. » ou « pp. ».

`localisation=` en français et `location=` en anglais sont réservés aux repères non strictement paginaires : chapitre, section, numéro d’article, annexe ou autre localisation de nature différente.

Le schéma et le validateur doivent être corrigés pour reconnaître cette distinction. Le paramètre anglais réellement supporté par le modèle public doit être vérifié en lecture seule ; une incompatibilité de modèle doit être signalée explicitement au lieu d’être contournée silencieusement.

## 3. Dates des références sitographiques

Le paramètre `date=` contient la date de publication ou de dernière mise à jour substantielle de la page web.

Une date de consultation ne doit jamais être placée dans `date=`. Si aucune date de publication fiable n’est identifiable, le paramètre `date=` est omis.

Aucune date ne doit être inventée. Toute date conservée doit être vérifiée sur la source ou dans des métadonnées fiables.

## 4. Éditions françaises

Dans une page française, lorsqu’un ouvrage existe dans une édition française pertinente et vérifiable, citer cette édition française : titre publié, traducteur éventuel, éditeur, lieu, année et pagination propres à cette édition.

Une édition française constitue une notice documentaire distincte de l’édition originale ou anglaise. Les articles scientifiques restent cités dans leur langue de publication, sauf existence d’une version française faisant autorité réellement utilisée.

## 5. Titres canoniques et titres affichés

Les titres canoniques restent complets, explicites, autonomes et inchangés dans cette reprise.

Les titres affichés doivent être revus individuellement. Ils peuvent être plus courts lorsque le contexte évident permet d’omettre une précision sans ambiguïté. Ils doivent rester grammaticaux, fidèles et autonomes.

La copie mécanique du titre canonique dans le titre affiché pour tout le corpus est interdite. Certains titres peuvent légitimement rester identiques lorsqu’aucun raccourcissement satisfaisant n’existe.

La modification des titres affichés français est une migration éditoriale explicitement autorisée. Elle entraîne le recalcul de l’empreinte structurelle, sans changement des 222 identifiants, des titres canoniques, des 210 relations ni des 226 occurrences.

## 6. Rubriques, sections et mots-clés

Chaque nœud doit être classé individuellement selon son contenu.

- Une à trois rubriques réellement centrales sont normalement utilisées ; une quatrième reste exceptionnelle.
- Les sections anglaises sont les équivalents conceptuels des rubriques françaises.
- Les mots-clés et keywords sont simples, stables, réutilisables et spécifiques au contenu du nœud.
- `parapsychologie`, `scientificité`, `parapsychology` et `scientific status` ne doivent pas être imposés mécaniquement à toutes les pages.
- Une combinaison uniforme sur l’ensemble du corpus doit déclencher un contrôle bloquant ou, au minimum, une alerte éditoriale forte.

## 7. Documentation des pages Débat et Debate

Les neuf catégories documentaires représentent trois types de documents croisés avec trois positions. Elles ne constituent ni un quota ni des cases à remplir.

Chaque catégorie peut contenir zéro, une ou plusieurs références selon la pertinence réelle. La documentation doit couvrir substantiellement les principaux axes du débat : histoire, institutions, protocoles, résultats, méta-analyses, critiques méthodologiques, réplication, biais, contrôles, fraude, plausibilité théorique, philosophie des sciences, psychologie anomalistique et évaluations institutionnelles.

La bibliographie est prioritaire. La sitographie et la vidéographie sont complémentaires. Les distributions artificiellement uniformes et les plafonds fixes sont interdits. Les listes françaises et anglaises sont construites séparément selon les ressources réellement disponibles dans chaque langue.

## 8. Date de création du corpus corrigé

À la demande explicite du propriétaire du projet, toutes les pages du corpus corrigé portent la date du **25 juillet 2026** :

- `|date-création=2026-07-25` pour la page Débat française et les 222 pages Argument françaises ;
- `|creation-date=2026-07-25` pour la page Debate anglaise et les 222 pages Argument anglaises ;
- même date dans les 223 copies françaises de staging interlangue ;
- même date dans les champs actifs correspondants du registre et du manifeste ;
- agrégats régénérés depuis les fichiers individuels.

Cette décision remplace, pour cette reprise, les anciennes consignes de conservation des dates du 24 juillet 2026. Elle ne modifie pas les dates de publication des sources et ne réécrit pas les traces historiques archivées.

## 9. Norme consolidée unique

La source de vérité active doit devenir un document unique, par exemple :

```text
WIKIDEBIA_NORME_CONSOLIDEE_1.1.0.md
```

Il doit intégrer :

- la norme 1.0.6 ;
- le correctif du 23 juillet 2026 ;
- les décisions du présent document ;
- les exemples MediaWiki corrigés ;
- la distinction entre contrôles automatiques et contrôles éditoriaux humains.

Les anciens fichiers correctifs sont conservés dans un dossier historique, mais ne sont plus des sources normatives actives indépendantes. Un `CHANGELOG_NORMATIF.md` décrit les évolutions sans dupliquer la norme.

## 10. Workflow correctif

Le statut `release_ready` de l’état d’entrée ne doit pas être conservé pendant que le corpus est en cours de modification. La norme et le validateur doivent définir :

- `corrective_in_progress` pendant la reprise ;
- `corrective_blocked` si une anomalie subsiste ;
- le retour à `release_ready` uniquement après validation complète.

De nouveaux handoffs et instantanés correctifs doivent être créés. Les handoffs et traces historiques W00–W10 ne doivent pas être réécrits pour faire croire qu’ils incorporaient déjà les corrections.

## 11. Publication

Aucune opération distante ne doit être effectuée pendant la reprise corrective. L’ancien kit W11 ne doit plus être utilisé. Un nouveau kit de simulation et de publication ne peut être produit qu’après validation complète du nouveau paquet `release_ready`.

Le nouveau kit doit intégrer les garde-fous éprouvés dans la version 1.1 : sessions française et anglaise traitées séquentiellement, réauthentification et contrôle de l’utilisateur à chaque phase, `assert=user`/`assertuser`, `createonly`, contrôle de révision de base, arrêt sur perte de session et possibilité de tester une seule page non canonique dans l’espace utilisateur.
