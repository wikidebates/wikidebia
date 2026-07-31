# Validateur stable Wikidéb’IA 0.4.16

Validateur local Python 3 aligné sur la norme 1.2.15 et rétrocompatible avec les paquets 1.1.0 à 1.2.13. `validate` reste strictement en lecture seule ; `recalc --write` est la seule commande d’écriture locale. Aucune écriture distante n’est implémentée.

La version 0.4.16 conserve tous les contrôles 0.4.13. La correction de sélection des ZIP est mise en œuvre par le kit 2.1.17 : le nom du fichier n’est pas une propriété du corpus validé, tandis que `manifest.debate_id` reste contrôlé comme identité interne.

La source active unique embarquée est `normative_reference/01_normes/WIKIDEBIA_NORME_CONSOLIDEE_1.2.15.md`.

```bash
PYTHONPATH=validator/src .venv/bin/python validator/scripts/wikidebia_validate.py validate corpus/mon_debat
```

## Publication de corpus historiques

Les champs `normative_versions.validator` et `normative_versions.kit` du manifeste décrivent la production d’origine. Ils ne doivent pas être remplacés par les versions installées. Le validateur 0.4.16 accepte les révisions normatives explicitement listées dans `COMPATIBILITY.json`; la publication doit exécuter ce validateur courant et exiger un rapport positif.
