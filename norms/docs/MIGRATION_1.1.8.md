# Migration vers la norme 1.1.8

## Objet

La norme 1.1.8 ajoute des exigences rédactionnelles pour les résumés d'arguments sans modifier le graphe argumentatif :

- style encyclopédique grand public ;
- idée principale annoncée dès l'ouverture ;
- phrases de longueur variée ;
- définition intégrée des termes techniques nécessaires ;
- revue humaine page par page.

## Compatibilité

Le validateur 0.3.0 continue d'accepter les paquets déclarés sous les normes 1.1.0 à 1.1.7. Ces paquets ne sont pas obligés de déclarer les nouveaux champs tant qu'ils ne migrent pas vers 1.1.8.

Changer uniquement l'exécutable du validateur ne réécrit aucun résumé et ne modifie aucun fichier du corpus.

## Champs à ajouter lors d'une migration réelle

Dans `manifest.json.editorial_controls` :

```json
{
  "summary_style_review_path": "reports/summary_style_review.json",
  "summary_style": {
    "enabled": true,
    "min_sentences": 3,
    "long_sentence_words": 34,
    "max_average_sentence_words": 28,
    "max_long_sentence_ratio": 0.6,
    "max_sentence_words": 50
  }
}
```

Les seuils sont des signaux de relecture et non des quotas rédactionnels. Une phrase longue peut être légitime ; une phrase courte peut rester obscure.

## Registre de revue

Le fichier déclaré par `summary_style_review_path` couvre chaque nœud actif disposant d'une page et chaque langue effectivement produite. Pour chaque langue, il atteste :

- `thesis_first=true` ;
- `general_public_style=true` ;
- `sentence_rhythm_reviewed=true` ;
- `technical_terms_reviewed=true` ;
- un statut `approved` ou `revised` ;
- une note non vide.

Un exemple est fourni dans `examples/summary_style_review.example.json`.

## Séquence recommandée

1. Réécrire les résumés sans modifier les identifiants, titres, relations ni occurrences.
2. Réviser les versions française et anglaise séparément, en conservant leur équivalence substantielle.
3. Produire le registre de revue du style.
4. Déclarer la norme 1.1.8, le validateur 0.3.0 et les nouveaux contrôles dans le manifeste et le handoff courant.
5. Régénérer les agrégats et empreintes documentaires concernés.
6. Exécuter toutes les portées du validateur.

`WDV-EDT-013` est une erreur lorsque la revue obligatoire manque ou est incohérente. Il est seulement un avertissement lorsqu'une métrique de longueur de phrase paraît défavorable.
