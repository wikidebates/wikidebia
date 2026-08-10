# Migration 1.2.69 — renommage des paramètres MediaWiki

Cette migration renomme quatre paramètres externes sans changer leur valeur :

- `sujet-complet` → `sujet-développé` dans `{{Débat}}` ;
- `complete-topic` → `expanded-topic` dans `{{Debate}}` ;
- `débat-détaillé` → `débat-dédié` dans `{{Argument}}` français ;
- `detailed-debate` → `dedicated-debate` dans `{{Argument}}` anglais.

Les nouvelles pages et tout nouveau rendu utilisent uniquement les noms de droite. Le kit et le validateur courants continuent de lire les noms de gauche lorsqu’un corpus antérieur à 1.2.69 les emploie. Lors d’une reprise ou d’une migration vers le contrat courant, la valeur est copiée exactement sous le nouveau nom ; l’ancien paramètre disparaît et les deux formes ne coexistent jamais.

Les clés techniques internes `complete_topic` et `detailed_debate` restent inchangées afin de préserver la compatibilité des registres et verrous historiques.
