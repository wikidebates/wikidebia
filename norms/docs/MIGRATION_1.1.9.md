# Migration vers la norme 1.1.9

## Objet

La norme 1.1.9 complète la norme 1.1.8 sans modifier le graphe argumentatif. Elle exige :

- une première phrase qui développe le titre au lieu de le répéter ;
- un examen explicite de la pertinence des exemples et données ;
- une vérification documentaire humaine de toute donnée chiffrée ;
- un style ferme, imagé et légèrement mordant lorsque cela sert le raisonnement ;
- l’exclusion du sarcasme, de la caricature, du militantisme et des slogans mécaniques.

## Compatibilité

Le validateur 0.3.1 continue d’accepter les paquets déclarés sous les normes 1.1.0 à 1.1.8. Les nouveaux champs ne sont obligatoires que pour les paquets qui déclarent `consolidated_norm=1.1.9`.

Changer uniquement l’exécutable du validateur ne réécrit aucun résumé, ne modifie aucun fichier du corpus et n’autorise aucune écriture distante.

## Configuration du manifeste

Dans `manifest.json.editorial_controls.summary_style`, conserver les seuils de lisibilité 1.1.8 et ajouter :

```json
{
  "opening_title_similarity_enabled": true,
  "opening_similarity_threshold": 0.84,
  "opening_max_extra_significant_words": 4,
  "quantitative_claim_review_required": true
}
```

Ces valeurs déclenchent des signaux de relecture. Elles ne constituent pas des quotas rédactionnels et ne remplacent jamais la décision humaine.

## Registre de revue

Pour chaque langue produite, le fichier déclaré par `summary_style_review_path` conserve les attestations 1.1.8 et ajoute :

- `opening_develops_title=true` ;
- `example_or_data_reviewed=true` ;
- `assertive_tone_reviewed=true` ;
- `no_artificial_example_or_number=true` ;
- `no_polemical_overstatement=true`.

Lorsqu’une donnée chiffrée est présente, `quantitative_claims_verified=true` et `quantitative_claims_note` explique brièvement ce qui a été vérifié : source, population, période, portée ou contexte pertinent. En l’absence de donnée chiffrée, `quantitative_claims_verified` peut être `false` et la note indique qu’aucune affirmation chiffrée n’est présente.

## Séquence recommandée

1. Réviser les résumés sans modifier les identifiants, titres, relations, occurrences ni lots.
2. Vérifier que chaque ouverture apporte une information absente du titre.
3. Ajouter un exemple ou un chiffre uniquement lorsqu’il améliore réellement la compréhension.
4. Vérifier et contextualiser chaque donnée chiffrée dans les sources de la page.
5. Effectuer une contre-relecture du ton : ferme et convaincu, mais non polémique.
6. Compléter le registre bilingue de revue.
7. Déclarer la norme 1.1.9 et le validateur 0.3.1 dans le manifeste et le handoff courant.
8. Régénérer les agrégats et empreintes documentaires concernés.
9. Exécuter toutes les portées applicables du validateur.

## Contrôles 0.3.1

- `WDV-EDT-014` est un avertissement lorsque la première phrase est trop proche du titre selon une heuristique prudente.
- `WDV-EDT-015` est une erreur lorsque le résumé contient une donnée chiffrée sans attestation humaine conforme dans le registre 1.1.9.
- L’absence d’exemple ou de chiffre n’est jamais une anomalie en soi.
- La qualité d’une image, le caractère réellement mordant d’une phrase et l’absence de polémique restent soumis à la revue humaine.
