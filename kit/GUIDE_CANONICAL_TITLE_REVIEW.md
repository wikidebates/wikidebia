# Revue des titres canoniques après l'incident cannabis

Le nom de page français ou anglais doit exposer son argument en une phrase,
sans juxtaposer plusieurs énoncés indépendants avec un point ou un point-virgule.
La demande du propriétaire du 22 octobre 2026 s'applique aux futures revues et
aux quatre corrections cannabis inventoriées séparément. Elle ne transforme
pas les libellés affichés historiques en titres de création.

La concision conserve la thèse, sa portée et ses restrictions : un titre peut
laisser son explication au texte de la page, mais ne doit pas supprimer une
condition décisive, renforcer une causalité ou changer la position argumentative.
La revue compare le nom proposé au titre source, aux citations et au contexte
du graphe. Elle ne se limite ni à la traduction littérale ni à un remplacement
de ponctuation. Aucune citation ni aucun résumé n'est réécrit à cette occasion.

`wikidebia_title_structure.py` détecte les frontières évidentes de phrases et
les points-virgules. Les initiales, abréviations usuelles et nombres décimaux
ne déclenchent pas ce contrôle. La ponctuation par virgule et les coordinations
restent soumises à une vraie revue de sens ; le détecteur n'est pas une analyse
grammaticale ou sémantique complète.

La garde intervient à la revue française, à la finalisation anglaise, à la
collecte des défauts d'une revue anglaise déjà convergée et avant une publication
initiale. L'updater bloque également une création ou un déplacement vers un nom
non conforme, y compris depuis un ancien plan signé. Un nom déjà publié n'est
jamais modifié automatiquement ; l'ajout pur de liens interlangues français
reste disponible pour préserver les autres corrections en cours.

Une attestation `approved` ou une série de booléens `True` ne démontre pas la
qualité d'un titre. Une correction postérieure à la convergence exige la
réouverture de la revue et de nouvelles preuves sur le contenu corrigé.
Les anciens ZIP, verrous et reçus restent des pièces historiques immuables.

Les quatre propositions bilingues et leurs justifications sont dans
`tests/fixtures/cannabis_title_corrections_20261022.json`. Leur état est
`editorial_reviewed_remote_checks_pending`, et non `release_ready` : ces données
ne sont ni un plan MediaWiki signé ni une archive de publication complète.
