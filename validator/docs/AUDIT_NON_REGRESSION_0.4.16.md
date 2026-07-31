# Audit de non-régression 0.4.16

Le correctif rend l’affichage des chemins absolus indépendant du dossier courant. Un chemin local absolu n’est jamais enregistré dans un rapport : seul le nom final du paquet est conservé. Les chemins relatifs fournis par l’utilisateur restent inchangés.

Les contrôles normatifs et éditoriaux 0.4.15 sont conservés sans modification. La suite est exécutée depuis le dossier du validateur et depuis un dossier courant extérieur.
