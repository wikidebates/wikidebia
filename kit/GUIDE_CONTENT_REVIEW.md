# Revue française des introductions, résumés et références

Le kit 2.15.20 applique une phase de contenu après le verrouillage des titres, rubriques et mots-clés. Elle part de `reviewed-copy/`, conserve toutes les copies antérieures et ne génère toujours aucune page MediaWiki finale.

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
- la bibliographie, la sitographie et la vidéographie de chaque argument ;
- les attestations de lisibilité, de fidélité logique, de force expressive et de vérification documentaire.

Aucune proposition produite par une heuristique n’est appliquée automatiquement.

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
