# Wikidéb’IA — Kit 2.15.23

La mise à niveau génère désormais un seul document textuel racine, `WIKIDEBIA_SOURCE_ACTIVE.md`, accompagné de son reçu JSON. Les anciens fichiers `WIKIDEBIA_NORMES_ACTIVES.md`, `WIKIDEBIA_VALIDATEUR_ACTIF.md` et `WIKIDEBIA_RECUS_ARCHIVES.json` sont archivés puis retirés lors de l’upgrade.
La revue de contenu inventorie désormais toutes les notions spécialisées de chaque sous-partie, au lieu de se limiter aux séries de notions voisines. Chaque lien, explication ou renvoi antérieur est vérifié.

La revue de contenu exige désormais un traitement cohérent des séries de notions spécialisées liées à Wikipédia et consigne chaque groupe dans `wikipedia_link_groups`.

Kit de production, publication et reprise aligné sur la norme 1.2.46 et le validateur 0.4.49.

La revue du contenu distingue désormais une simple notice documentaire d’une phrase explicative dans les balises `<ref>`. Les notices sont rendues sans point final avant `</ref>` ; une phrase complète peut conserver son point uniquement si son empreinte est attestée dans le registre de revue.

Pour mettre à jour un débat, déposez son ZIP dans `incoming/` puis lancez `./wikidebia update`.
