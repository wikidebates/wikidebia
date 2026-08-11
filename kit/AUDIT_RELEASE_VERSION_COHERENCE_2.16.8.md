# Audit — cohérence des versions de release 2.16.8

Le paquet 2.16.8 de transition embarque encore trois `VERSIONS.json` synchronisés afin d’être accepté par les gestionnaires antérieurs. Une fois 2.16.8 installée, `upgrade` sélectionne la version propre de chaque composant et ne traite plus les versions étrangères répétées comme une barrière de compatibilité.

La release 2.16.8 est validée en réouvrant les trois ZIP avec l’inspecteur utilisé par `./wikidebia upgrade`, puis en exécutant `verify_version_set` avant création du ZIP complet final.
