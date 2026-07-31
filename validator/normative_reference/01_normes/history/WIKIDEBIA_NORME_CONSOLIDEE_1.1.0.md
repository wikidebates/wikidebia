# Norme consolidée Wikidéb’IA 1.1.0

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

La copie mécanique du titre canonique dans tous les titres affichés est interdite. Une identité ponctuelle reste possible lorsqu’aucun raccourcissement satisfaisant n’existe. À l’état `release_ready`, une identité dominante supérieure à 80 % déclenche une erreur éditoriale.

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

## 6. Rubriques, sections et mots-clés

Les rubriques françaises autorisées sont : Aménagement, Culture, Droit, Écologie, Économie, Éducation, Éthique, Géopolitique, Histoire, Philosophie, Politique, Psychologie, Religion et spiritualité, Santé, Science, Société, Sport et loisirs, Technologie.

Chaque nœud est classé individuellement. Une à trois rubriques réellement centrales sont normalement utilisées ; une quatrième est exceptionnelle et motivée. Les sections anglaises sont les équivalents conceptuels des rubriques françaises.

Les mots-clés et keywords sont spécifiques, stables et réutilisables. `parapsychologie`, `scientificité`, `parapsychology` et `scientific status` ne sont pas imposés mécaniquement. Une combinaison unique dominant plus de 90 % du corpus à l’état `release_ready` est bloquante.

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

### 7.4 Éditions françaises

Sur une page française, une édition française pertinente et vérifiable d’un ouvrage est citée avec son titre publié, ses traducteurs éventuels, son éditeur, son lieu, son année et sa pagination propres. Elle constitue une notice distincte de l’édition originale. Les titres d’articles scientifiques ne sont pas traduits artificiellement.

### 7.5 Pages Débat / Debate

L’introduction couvre substantiellement les dimensions pertinentes : définition, histoire, institutions, protocoles, résultats, méta-analyses, réplications, biais, contrôles, fraude, théorie, plausibilité, philosophie des sciences et psychologie anomalistique.

À l’état `release_ready`, chaque introduction comporte normalement au moins cinq sous-parties substantielles et chaque page de débat au moins vingt références documentaires au total, sauf justification explicite. Une répartition artificielle d’exactement une référence dans chaque catégorie est interdite.

## 8. Structures MediaWiki actives

### 8.1 Page Débat française

```mediawiki
{{Débat
|sujet=
|sujet-complet=
|avancement=Débat construit
|avertissements-débat=Débat généré avec IA
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
|interlangue={{Interlangue
|langue=en
|page=Titre canonique anglais
}}
|date-création=AAAA-MM-JJ
}}
```

Le paramètre `interlangue` n’apparaît que dans le staging français ou après la phase interlangue autorisée.

### 8.2 Page Argument française

```mediawiki
{{Argument
|avertissements-argument=Argument généré avec IA
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
|type=Is
|topic=
|progress=Constructed debate
|debate-warnings=Debate generated with AI
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
|argument-warnings=Argument generated with AI
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

La date de création est une décision de production distincte de la date des sources. Pour la reprise `parapsychologie_science` W10.R1, toutes les pages canoniques et copies françaises de staging portent `2026-07-25`. Les traces historiques W00–W10 conservent leurs dates d’origine.

Le validateur compare le wikicode, le registre, le manifeste et le staging. Une divergence est bloquante.

## 10. Workflow correctif

Le cycle correctif autorisé est :

```text
release_ready
  → corrective_in_progress
  → corrective_blocked (si une anomalie subsiste)
  → corrective_in_progress (après reprise)
  → release_ready (validation complète uniquement)
```

Le Work porte le type `corrective_prepublication`. Il crée un instantané initial, des handoffs correctifs nouveaux et une matrice de couverture. Les handoffs historiques ne sont jamais réécrits ; leurs empreintes décrivent l’état d’entrée de leur Work original.

Le retour à `release_ready` exige :

- zéro erreur bloquante ;
- zéro avertissement non résolu ;
- revue éditoriale humaine enregistrée ;
- cohérence bilingue ;
- manifeste de libération cohérent ;
- preuve de l’absence d’écriture distante ;
- kit de publication produit séparément et non exécuté.

## 11. Validateur

`validate` est strictement en lecture seule. Toute écriture locale dérivée passe par une commande distincte, explicitement demandée, telle que `recalc --write`. Le validateur n’effectue aucune connexion au wiki.

Les contrôles sont répartis entre :

- schémas JSON ;
- cohérence et fichiers ;
- graphe, lots et sources ;
- wikicode et bilinguisme ;
- workflow ;
- contrôles éditoriaux automatisables ;
- revue humaine obligatoire.

La version 0.2.2 ajoute les codes `WDV-DOC-002`, `WDV-DOC-003` et `WDV-EDT-001` à `WDV-EDT-006`. Chaque règle nouvelle possède au moins un test positif et un test négatif lorsque la règle est binaire.

## 12. Publication W11

Aucune écriture distante n’est autorisée pendant W10.R1. Le kit W11 est livré sans exécution et sans secret.

Avant toute publication, W11 doit :

1. exécuter une simulation globale ;
2. vérifier en lecture seule la compatibilité réelle des modèles publics ;
3. refuser de poursuivre si un paramètre normatif requis n’est pas accepté ;
4. traiter séquentiellement les phases `fr → en → fr_interlanguage` ;
5. réauthentifier et vérifier l’identité à chaque phase ;
6. utiliser `assert=user` et `assertuser` ;
7. utiliser `createonly` pour une création et une révision de base pour une modification ;
8. s’arrêter sur perte de session, collision, divergence, droits insuffisants ou révision concurrente ;
9. permettre un test isolé sur une seule page non canonique de l’espace utilisateur ;
10. reprendre uniquement à partir de journaux de révisions réelles.

Les fichiers d’authentification, cookies, secrets et identifiants privés ne sont jamais inclus dans une archive publique.

## 13. Contrôles propres à W10.R1

Le paquet final doit conserver exactement 222 identifiants, 210 relations, 226 occurrences et 18 lots, ainsi que tous les titres canoniques et propriétaires. Il documente l’empreinte structurelle avant et après correction, les 446 pages canoniques, les 223 copies françaises de staging, les migrations documentaires et la couverture des huit axes correctifs.

Le statut local `release_ready` n’implique pas l’autorisation de publier. Le champ `publication_gate` peut rester bloqué pour une incompatibilité distante tout en attestant que le corpus local est validé.
