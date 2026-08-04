# Audit normatif 1.2.28

La révision 1.2.28 corrige une contradiction interne de la livraison 1.2.27 : plusieurs documents spécialisés conservaient l’interdiction historique des citations et la structure anglaise `Quote`. La source consolidée avait priorité, mais cette divergence violait l’exigence de non-régression documentaire.

La correction ne change pas le comportement : rendu uniquement depuis les verrous, modèle `Citation` dans les deux langues, paramètres documentaires conservés, traduction limitée à `citation` et `date`, avertissement canonique ajouté une seule fois.
