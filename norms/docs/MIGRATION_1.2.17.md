# Migration vers la norme 1.2.17

> **Note actuelle :** ce document décrit la transition historique vers 1.2.17. La convention ` ; ` mentionnée ci-dessous a été corrigée par la norme 1.2.18. Toute production ou migration courante utilise `, ` entre plusieurs auteurs.


1. Ajouter au moins un `{{Article Wikipédia|page=…}}` vérifié à chaque page Débat française et un `{{Wikipedia article|page=…}}` à chaque page Debate anglaise.
2. Retirer tous les paramètres `débats-connexes` et `related-debates` des pages générées.
3. Convertir chaque liste JSON d’auteurs : un élément en texte brut, plusieurs éléments séparés par ` ; `, liste vide omise.
4. Installer le validateur 0.4.18 et le kit 2.2.1.
5. Relancer toutes les portées de validation et régénérer les empreintes.
6. Utiliser `./wikidebia publish` normalement : aucune confirmation interactive n’est désormais demandée.
