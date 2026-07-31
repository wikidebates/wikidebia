# Validateur stable Wikidéb'IA 0.3.1

Validateur local en Python 3 pour les paquets complets de débats Wikidéb'IA, aligné sur la norme consolidée 1.1.9. Il ne dépend pas de ChatGPT à l'exécution et ne modifie jamais les fichiers pendant une validation normale.

## Fonctions couvertes

- validation JSON Schema Draft 2020-12 avec contrôle des formats ;
- cohérence du manifeste, du cadrage, du registre maître et de la projection du graphe ;
- DAG, occurrences, relations, réutilisations, profondeurs, branches et compteurs ;
- lots français et anglais, couverture, chevauchements, dépendances et obsolescence structurelle ;
- registre documentaire et usages réciproques des sources ;
- fichiers individuels, agrégats, empreintes SHA-256 et manifeste de libération ;
- wikicode français et anglais : modèles, paramètres, ordre, valeurs fixes, relations, dates, typographie documentaire et interlangues ;
- cohérence bilingue ;
- contrôles correctifs 1.1.7 : guillemets clavier, vocabulaire thématique réutilisable à l’échelle du wiki, équivalence bilingue des résumés, justification générique de chaque rubrique, pagination, dates web, documentation Débat/Debate et traçabilité déclarative ;
- préconditions du workflow, handoffs et transition optionnelle entre deux états ;
- rapports texte et JSON ;
- recalcul explicite, séparé de la validation.

Les contrôles éditoriaux qui demandent une appréciation humaine sont signalés distinctement : qualité logique, équilibre des camps, quasi-doublons sémantiques, fiabilité substantielle des sources et qualité des résumés.

## Prérequis

- Python 3.10 ou supérieur ;
- `jsonschema` 4.18 ou supérieur ;
- `referencing` 0.30 ou supérieur.

## Exécution immédiate sans installation

Depuis le dossier du validateur :

```bash
python3 scripts/wikidebia_validate.py validate /chemin/vers/debates/mon_debat
```

Rapports texte et JSON :

```bash
python3 scripts/wikidebia_validate.py validate /chemin/vers/le_paquet \
  --format both \
  --text-output reports/validator_report.txt \
  --json-output reports/validator_report.json
```

Le code de sortie vaut `1` lorsqu'au moins une erreur bloquante est présente, sinon `0`. Les avertissements seuls ne rendent pas le code de sortie non nul.

## Installation dans un environnement virtuel

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install .
wikidebia-validate validate /chemin/vers/le_paquet
```

Dans un environnement sans accès au dépôt de paquets, les dépendances doivent déjà être installées. Le lanceur `scripts/wikidebia_validate.py` évite l'installation du projet lui-même.

## Validation ciblée

Les portées disponibles sont :

```text
schema coherence graph batches sources files wikicode bilingual editorial workflow
```

Exemples :

```bash
python3 scripts/wikidebia_validate.py validate paquet --scope graph
python3 scripts/wikidebia_validate.py validate paquet --scope wikicode --scope files
```

Contrôle d'une transition précise :

```bash
python3 scripts/wikidebia_validate.py validate paquet \
  --scope workflow \
  --previous-status fr_content_complete
```

## Recalcul explicite

La commande `recalc` est la seule commande autorisée à écrire. Elle exige `--write`.

```bash
python3 scripts/wikidebia_validate.py recalc paquet --graph --write
python3 scripts/wikidebia_validate.py recalc paquet --aggregates --hashes --write
```

- `--graph` recalcule `derived_counts`, les blocs `derived`, `maximum_observed` et l'empreinte structurelle d'un graphe verrouillé ;
- `--aggregates` régénère les agrégats depuis les fichiers individuels ;
- `--hashes` recalcule les empreintes des pages et agrégats dans le manifeste et le registre.

Aucune normalisation silencieuse n'est effectuée par `validate`.

## Tests

```bash
./scripts/run_tests.sh
```

La suite contient soixante-sept cas positifs et négatifs pour les schémas, graphes, cycles, titres, compteurs, wikicode, références, interlangues, lots, empreintes, transitions et recalculs.

## Paquets historiques

Un paquet produit avant la méthode Work peut être placé à l’état `migration_required`. Le validateur contrôle alors la cohérence locale reconstruite sans prétendre que les Work, handoffs ou vérifications distantes existaient historiquement. Les divergences avec le wiki doivent rester marquées `manual_review` ou `blocked`.

## Comparaison distante en lecture seule

Le script `scripts/wikidebia_remote_compare.py` compare les fichiers déclarés dans le manifeste aux pages du wiki. Il n’implémente aucune opération de sauvegarde, publication, suppression, déplacement ou renommage.

```bash
python3 scripts/wikidebia_remote_compare.py /chemin/vers/le_paquet \
  --login \
  --text-output reports/remote_compare_read_only.txt \
  --json-output reports/remote_compare_read_only.json
```

La connexion Pywikibot reste dans un environnement d’exécution privé séparé. Elle n’est jamais incorporée à l’archive publique du validateur ni au paquet documentaire du débat.

## Intégration Pywikibot

Avant toute écriture distante, un script Pywikibot peut exécuter le validateur comme sous-processus et refuser de poursuivre si le code de sortie est non nul. Il peut aussi consommer le rapport JSON pour afficher les codes stables et les chemins concernés.

Le validateur n'effectue lui-même aucune connexion au wiki et ne modifie aucune page distante.

## Documents

- `docs/ARCHITECTURE.md` : architecture et flux de validation ;
- `docs/CONTROL_CATALOG.md` : catalogue des codes stables ;
- `docs/NORMATIVE_AUDIT.md` : audit des normes et décisions d'implémentation ;
- `docs/NORMATIVE_CORRECTION_2026-07-23.md` : correctif actif postérieur à la révision 1.1.0 ;
- `docs/MIGRATION_1.1.9.md` : procédure d’adoption des règles d’ouverture, d’exemples, de données chiffrées et de ton sans modification du graphe ;
- `docs/TEST_REPORT.txt` : résultat reproductible de la suite livrée ;
- `normative_reference/` : copie de la norme active 1.1.9, des historiques, du catalogue d’exigences et de la matrice de traçabilité.

## Norme consolidée 1.1.9

La source normative active unique est `normative_reference/01_normes/WIKIDEBIA_NORME_CONSOLIDEE_1.1.9.md`. Les normes antérieures sont conservées dans `history/`. Les paquets correctifs peuvent déclarer `corrective_in_progress`, `corrective_blocked`, `corrective_prepublication` et `publication_gate`.

La portée `editorial` automatise les contrôles objectivables sans remplacer la revue humaine bilingue enregistrée dans le paquet.

## Contrôles éditoriaux 1.1.9

La version 0.3.1 conserve `WDV-EDT-013` pour la lisibilité des phrases et ajoute :

- `WDV-EDT-014` : avertissement heuristique lorsque la première phrase répète ou paraphrase trop étroitement le titre ;
- `WDV-EDT-015` : erreur lorsqu’une donnée chiffrée ne possède pas l’attestation humaine documentaire exigée.

Le manifeste d’un paquet 1.1.9 déclare `editorial_controls.summary_style` et `editorial_controls.summary_style_review_path`. Le registre de revue atteste l’ouverture développée, la pertinence des exemples ou données, l’absence de précision artificielle et un ton ferme sans polémique.

L’absence d’exemple ou de chiffre n’est jamais une anomalie. Le validateur ne décide pas si une phrase est élégante, réellement mordante ou suffisamment convaincante : ces appréciations restent humaines.

## Compatibilité

Le validateur 0.3.1 accepte les paquets déclarés sous les normes 1.1.0 à 1.1.8 sans exiger les nouveaux champs 1.1.9. Il ne modifie aucun fichier pendant `validate` et n’autorise aucune écriture distante.

Exemple de configuration 1.1.9 :

```json
{
  "summary_style_review_path": "reports/summary_style_review.json",
  "summary_style": {
    "enabled": true,
    "min_sentences": 3,
    "long_sentence_words": 34,
    "max_average_sentence_words": 28,
    "max_long_sentence_ratio": 0.6,
    "max_sentence_words": 50,
    "opening_title_similarity_enabled": true,
    "opening_similarity_threshold": 0.84,
    "opening_max_extra_significant_words": 4,
    "quantitative_claim_review_required": true
  }
}
```

## Ajout aux sources du projet

L’archive complète `wikidebia-validator-0.3.1.zip` est destinée à être ajoutée
comme deuxième source du projet, avec `wikidebia-normes-1.1.9.zip`. Elle contient
le code exécutable, les schémas, les tests, la documentation et la copie normative
nécessaire à l’audit. Son fichier `COMPATIBILITY.json` indique les révisions
normatives prises en charge.

Les documents et rapports remplacés de la version 0.3.0 sont conservés dans `docs/history/validator-0.3.0/`.
