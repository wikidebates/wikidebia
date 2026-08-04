# Guide de traduction anglaise contrôlée — Kit 2.15.5

La traduction anglaise commence uniquement après le verrouillage complet des métadonnées et du contenu français. Elle travaille dans le même workspace éditorial et ne modifie ni le corpus promu, ni `working-copy/`, ni `reviewed-copy/`, ni `content-reviewed-copy/`.

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

La page Debate reçoit un titre canonique, `topic`, `complete-topic`, des sections, des keywords, une introduction structurée, des articles Wikipédia anglais vérifiés et neuf paramètres documentaires comportant chacun au moins deux références anglaises distinctes.

Chaque argument reçoit un titre canonique et un displayed title idiomatiques, des sections exactement équivalentes aux rubriques françaises, des keywords issus du vocabulaire bilingue, un summary substantiellement équivalent et une documentation anglaise adaptée. Le ratio de longueur anglais/français doit rester compris entre 0,60 et 1,45.

Les relations, occurrences, orientations et profondeurs sont linguistiquement neutres : elles ne peuvent pas être modifiées pendant cette phase.

### Citations importées

Chaque modèle `{{Citation}}` français importé est inventorié avec un identifiant stable. La projection anglaise utilise `{{Quote}}` et traduit obligatoirement tous les noms de paramètres selon le contrat du wiki anglais : `citation→quote`, `auteurs→authors`, `ouvrage→work`, `numéro→issue`, `localisation→location`, `édition→publisher`, `lieu→place`, `lien→link` et `avertissements-citation→warnings`; les noms `article`, `volume`, `page` et `date` sont identiques dans les deux langues.

Seules les valeurs de `quote` et de `date` peuvent être traduites. Les valeurs de `authors`, `article`, `work`, `volume`, `issue`, `page`, `location`, `publisher`, `place` et `link` sont reprises exactement. `warnings` reçoit toujours `Citation traduite par IA`, après un avertissement préexistant avec le séparateur exact `, `. La date traduite doit désigner la même date ; une année seule reste inchangée. Un paramètre français sans équivalent anglais déclaré bloque la finalisation.

## 3. Finalisation

```bash
./wikidebia corpus-workspace-translation <debate_id> --work-id <work_id> --finalize
```

La finalisation vérifie notamment :

- la couverture exacte de tous les arguments actifs ;
- l’unicité et l’autonomie des titres canoniques anglais ;
- le caractère propositionnel des displayed titles ;
- la limite de 10 % d’identités exactes entre titres canoniques et affichés ;
- la correspondance des sections avec les rubriques françaises ;
- la correspondance des keywords avec le vocabulaire contrôlé ;
- la limite de 25 % pour un même jeu exact de keywords ;
- l’équivalence substantielle des introductions et summaries ;
- la couverture exacte des citations françaises, la préservation de leurs paramètres, l’équivalence des dates et l’avertissement de traduction ;
- la langue et la vérification des sources anglaises ;
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
