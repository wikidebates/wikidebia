# Migration 2.15.43

La norme 1.2.58 renomme exclusivement le paramètre MediaWiki d’appellation consacrée du modèle `Argument` : `nom` devient `nom-consacré` en français et `name` devient `established-name` en anglais. Ce paramètre reste le deuxième emplacement top-level, immédiatement après `initialisation` / `initialization`.

Le changement ne vise pas les titres canoniques ou affichés, les noms de sites, les auteurs, les noms de modèles ni les champs JSON génériques `name`. Les identifiants internes `argument_name_*` et les registres documentaires conservent donc leur structure.

Toute nouvelle page Argument et toute nouvelle attribution éditoriale utilisent exclusivement `nom-consacré` / `established-name`. Une page préexistante portant encore `nom` / `name` est conservée exactement : l’upgrade ne migre pas silencieusement son wikicode lors d’une autre modification. Les manifestes antérieurs à 1.2.58, qui ne suivaient que l’ancien paramètre, restent lisibles et restaurables.
