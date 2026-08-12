# Audit validateur 0.4.91 — paramètres facultatifs vides des Citation/Quote

Le verrou éditorial peut conserver des sous-paramètres facultatifs historiquement présents mais vides. Le rendu canonique les omet. La comparaison `WDV-MWK-021` filtre donc uniquement ces valeurs vides lors de la construction de la liste attendue, sans modifier la provenance stockée.

Les paramètres non vides, leurs noms localisés et les valeurs documentaires préservées restent strictement contrôlés. La norme active 1.2.86 n'est pas modifiée : son profil de rendu imposait déjà l'omission des sous-paramètres facultatifs vides.
