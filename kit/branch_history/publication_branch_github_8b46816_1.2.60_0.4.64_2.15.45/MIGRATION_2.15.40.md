# Migration 2.15.40

Cette maintenance corrige la résolution de la révision de création utilisée par `tag-translated-fr`.

L'état publié peut légitimement pointer vers une révision postérieure à la création lorsqu'une modification automatisée secondaire (par exemple une mise à jour portant la balise `argument added`) intervient pendant ou immédiatement après la publication. Le rattrapage ne suppose donc plus que `revision_id` de l'état publié est nécessairement la révision de création.

Si la révision attestée par l'état publié n'est pas une création, le kit relit l'historique de la page et ne retient la première révision que si elle satisfait simultanément les garde-fous suivants : titre exact, `parentid=0`, auteur attendu, résumé exact `Translation of the French page [[:fr:X|X]]` et présence préalable de la balise `chatgpt`.

Le plan signé conserve à la fois la révision d'état publiée et la révision de création résolue. L'exécution ne balise que cette dernière. Aucun wikicode, résumé ou horodatage n'est modifié.
