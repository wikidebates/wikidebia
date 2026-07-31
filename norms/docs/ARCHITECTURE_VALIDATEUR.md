# Architecture normative et validation

Le paquet normatif 1.2.15 recommande le validateur 0.4.16. Le pipeline sépare les contraintes de schéma, les invariants structurels, les contrôles documentaires et les revues humaines.

Les dates documentaires ISO, les modèles spécialisés dans les appels inline d’introduction et les paramètres documentaires de débat contenant moins de deux notices sont bloquants. Les dates de création restent contrôlées séparément au format `AAAA-MM-JJ`. L’acronyme courant est déclaré dans le registre de revue, puis comparé à `sujet-complet` ou `complete-topic`.

La publication française seule reste sûre parce que le kit compare le lien interlangue au titre anglais verrouillé dans le registre maître, même si aucune page anglaise correspondante n’existe encore dans le manifeste.

La norme 1.2.15 ajoute un contrôle lexical déterministe sur le wikicode brut : toute jonction de modèles écrite sous la forme `}}` + saut de ligne + `{{` est bloquée et doit être compactée en `}}{{`.

Le validateur 0.4.16 produit des chemins de paquet portables ; le kit 2.1.17 contrôle l’ordre de publication et la structure de l’installation.
