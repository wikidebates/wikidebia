# Guide de traduction anglaise contrôlée — Kit 2.15.30

La traduction anglaise commence uniquement après le verrouillage complet des métadonnées et du contenu français. Elle travaille dans le même workspace éditorial et ne modifie ni le corpus promu, ni `working-copy/`, ni `reviewed-copy/`, ni `content-reviewed-copy/`.

## 0. Protocole de lots pour la traduction

La traduction est une adaptation idiomatique et documentaire, pas une substitution mot à mot. Elle est effectuée dans l'ordre suivant :

1. **Lot Debate** : la page `Debate` complète constitue un lot autonome, avec son introduction, ses titres, ses sections, ses keywords, ses liens Wikipédia anglais et toute sa documentation anglaise.
2. **Lots Argument** : 20 pages Argument par lot par défaut, jamais plus de 25. Réduire à 10–15 pages lorsque le groupe comporte beaucoup de citations, de références, de recherches terminologiques ou de noms consacrés à vérifier.
3. Une page Argument est entièrement achevée dans le même lot : canonical title, displayed title, summary, sections, keywords, `name=` éventuel, citations et références.
4. Chaque lot est relu et clos avant le suivant. Il faut notamment vérifier le sens et l'orientation de chaque argument à partir du summary français, des citations, justifications et objections disponibles, afin d'éviter une inversion pour/contre.
5. Après le dernier lot, effectuer une passe globale inter-lots sur la terminologie, les titres, le vocabulaire bilingue, les `name=`, les références, les citations et la parité du graphe avant `--finalize`.

Ces tailles sont des bornes de qualité de travail, non des quotas de contenu. Un lot peut être réduit davantage si cela améliore la fiabilité de la recherche documentaire.

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
