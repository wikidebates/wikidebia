# Audit — attestation runtime du validateur (2.16.36)

Le diagnostic `render_preflight` réel du vote électronique sous kit 2.16.35 déclarait
`validator=0.4.101`, mais appliquait encore le profil de création à exactement cinq
résumés `historical_authorized_change`. Les verrous `fr_content_lock.json` et
`en_content_lock.json` du même paquet les classaient pourtant explicitement comme
historiques, et l’exécution directe du code 0.4.101 livré retournait zéro
`WDV-EDT-013/014/015/020`.

Le correctif 2.16.36 ne modifie donc ni le corpus ni les règles éditoriales. Il
rend l’identité du code exécuté observable et obligatoire :

1. lancement par `validator/scripts/wikidebia_validate.py` avec Python `-I` ;
2. insertion explicite de `validator/src` après l’initialisation de Python ;
3. refus des modules critiques chargés hors de ce composant ;
4. SHA-256 runtime de `cli.py` et `editorial.py` inclus dans le rapport ;
5. recalcul et comparaison de ces empreintes par l’orchestrateur.

Une régression injecte volontairement une copie hostile via `sitecustomize` et
vérifie que le validateur installé reste le seul chargé.
