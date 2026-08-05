# Guide — traduction anglaise différée

1. Déclarer `translation_status.en=deferred`.
2. Produire uniquement les fichiers et manifestes français.
3. Ne créer ni titre anglais provisoire ni `{{Lien interlangue}}`.
4. Valider et publier avec `--scope fr`.
5. Traduire ensuite l’ensemble anglais, passer à `ready`, verrouiller les titres et publier avec `--scope en`.
6. Reprendre enfin le français pour ajouter les liens interlangues exacts.
