# Architecture normative et validation

Le paquet normatif 1.2.17 recommande le validateur 0.4.18. Le pipeline sépare les contraintes de schéma, les invariants structurels, les contrôles documentaires et les revues humaines.

Les dates documentaires ISO, les modèles spécialisés dans les appels inline d’introduction et les paramètres documentaires de débat contenant moins de deux notices sont bloquants. Les dates de création restent contrôlées séparément au format `AAAA-MM-JJ`. L’acronyme courant est déclaré dans le registre de revue, puis comparé à `sujet-complet` ou `complete-topic`.

La publication française seule reste sûre parce que le kit compare le lien interlangue au titre anglais verrouillé dans le registre maître, même si aucune page anglaise correspondante n’existe encore dans le manifeste.

La norme 1.2.17 ajoute un contrôle lexical déterministe sur le wikicode brut : toute jonction de modèles écrite sous la forme `}}` + saut de ligne + `{{` est bloquée et doit être compactée en `}}{{`.

Le validateur 0.4.18 produit des chemins de paquet portables ; le kit 2.2.1 contrôle l’ordre de publication et la structure de l’installation.


## Reprise distante d’un corpus publié — révision 1.2.17

Une reprise compare obligatoirement le dernier état publié signé, l’état distant courant et le nouveau corpus validé. Le kit produit un plan signé comprenant `create`, `skip`, `update`, `move`, `redirect`, `delete`, `manual_review` et `blocked`. Une page absente du nouveau manifeste n’est jamais supprimée sans preuve d’appartenance à la version antérieure du même débat.

Les mises à jour et suppressions vérifient la révision ou l’empreinte attendue et utilisent le contrôle de concurrence MediaWiki. Toute modification humaine ou provenance indéterminée est classée `manual_review`. Les déplacements et fusions sont déclarés explicitement. Les suppressions sont exécutées seulement après vérification du nouveau graphe publié. Les opérations sont idempotentes et donnent lieu à un reçu final et à un nouvel état publié signé.

Le validateur contrôle localement les structures et la cohérence des plans, mais toutes les lectures et écritures MediaWiki restent dans le kit.

La révision 1.2.17 ajoute deux barrières de wikicode : article Wikipédia obligatoire et conversion textuelle des auteurs. Les paramètres de débats connexes sont interdits dans les sorties générées.
