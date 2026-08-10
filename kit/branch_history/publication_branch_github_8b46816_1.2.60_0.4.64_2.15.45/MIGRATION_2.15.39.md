# Migration 2.15.39

Cette maintenance corrige la relecture post-écriture des balises MediaWiki.

Après une écriture réussie, les métadonnées de révision — en particulier les balises — peuvent apparaître avec un léger retard sur les lectures suivantes. Le chemin `update` applique désormais la même politique bornée que `publish` : jusqu’à 8 relectures espacées de 2 secondes avant de conclure à l’absence de `chatgpt`.

Le rattrapage `tag-translated-fr` applique également une relecture bornée après `action=tag`, afin d’éviter le même faux négatif lors de l’ajout rétroactif de `translated-fr`.

Aucune écriture n’est répétée pendant ces tentatives : seules les lectures de vérification sont rejouées.
