# Migration 1.2.58 — `nom-consacré` / `established-name`

Cette révision renomme uniquement le paramètre MediaWiki facultatif d’appellation consacrée du modèle `Argument` : `nom` devient `nom-consacré` en français et `name` devient `established-name` en anglais. Le paramètre reste situé immédiatement après `initialisation` / `initialization`.

Les identifiants internes `argument_name_*` et les champs JSON génériques `name` ne sont pas renommés. Les noms de pages, de sites, d’auteurs et de modèles ne sont pas concernés.

Les pages nouvelles ne doivent plus émettre `nom` / `name`. Pour éviter toute régression destructive, une page préexistante qui possède encore l’ancien paramètre peut le conserver exactement jusqu’à une migration explicitement décidée.
