# Audit de complétude et de non-régression — validateur 0.3.1

Date : 27 juillet 2026

## Comparaison avec 0.3.0

- 121 fichiers dans 0.3.0 ; 126 fichiers avant archivage complémentaire dans 0.3.1.
- Aucun fichier 0.3.0 n'a disparu sans équivalent : la norme active 1.1.8 a été déplacée dans `normative_reference/01_normes/history/` avec une empreinte SHA-256 strictement identique.
- 88 fichiers communs sont restés identiques octet par octet.
- Les modifications de code restantes correspondent à la version, à l'activation de 1.1.9, aux contrôles `WDV-EDT-014` et `WDV-EDT-015`, au schéma déclaratif associé et à la correction de la version affichée par `recalc`.
- Les anciens rapports et documents remplacés sont maintenant archivés dans `docs/history/validator-0.3.0/`.

## Norme et exigences

- La norme 1.1.9 reprend intégralement le texte de la 1.1.8 et ajoute la section 5.2 et l'addendum 1.1.9.
- Les 282 exigences antérieures sont conservées sans suppression ni modification de fond.
- Cinq exigences nouvelles sont ajoutées : `ARG-029` à `ARG-033`.

## Tests exécutés

- 67 tests pytest réussis.
- Auto-audit UTF-8, fins de ligne, syntaxe Python et JSON réussi.
- Toutes les empreintes du manifeste interne concordent.
- Test réel sur le corpus `reseaux_sociaux_adolescents` déclaré en 1.1.8 : les validateurs 0.3.0 et 0.3.1 produisent exactement les mêmes résultats, métriques et constats, soit 0 erreur, 0 avertissement et 1 information.

## Conclusion

Aucune fonctionnalité ni exigence antérieure n'est supprimée. Les seules suppressions textuelles apparentes correspondent à des mises à jour de version ou à des documents remplacés dont les versions exactes sont désormais archivées.
