# Migration vers le kit 2.16.40

Aucune migration manuelle du corpus n’est requise.

Après `./wikidebia upgrade`, relancer la commande qui avait échoué. Un `review-import` interrompu avant écriture distante reprend depuis le même paquet et reconstruit le rendu avec les preuves réconciliées. Les convergences sémantiques déjà scellées ne sont pas recalculées tant que le contenu sémantique n’a pas changé.
