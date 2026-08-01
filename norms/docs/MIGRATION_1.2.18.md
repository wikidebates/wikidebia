# Migration vers la norme 1.2.18

1. Remplacer tout séparateur ` ; ` entre auteurs par `, `.
2. Vérifier qu’aucune valeur `auteurs` ou `authors` ne contient une virgule sans exactement une espace après elle, une espace avant la virgule ou une virgule pleine chasse.
3. Conserver la conversion JSON déjà exigée : un élément devient une valeur scalaire, une liste vide omet le paramètre.
4. Conserver les contrôles 1.2.17 : article Wikipédia non vide, absence de débats connexes et publication sans invite interactive.
5. Installer le validateur 0.4.19 et le kit 2.2.3, recalculer les empreintes et relancer toutes les portées.

Les paquets qui restent déclarés sous 1.2.17 conservent leur provenance et ne reçoivent pas rétroactivement le nouveau contrôle de ponctuation.
