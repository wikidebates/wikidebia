# Audit — résumés MediaWiki individualisés 1.2.79

## Décision

Les nouveaux plans de reprise d’un corpus validé ne doivent plus utiliser le résumé générique `Corrections`. Chaque mutation distante est décrite par un résumé propre à l’opération et, pour une mise à jour de contenu, aux familles de paramètres réellement modifiées.

## Contrôles attendus

- contrat de plan : `page_specific_v1` ;
- politiques distinctes pour création, diff de contenu, ajout interlangue, renommage, redirection et suppression ;
- politique et résumé incorporés au plan signé ;
- recalcul du résumé attendu immédiatement avant l’écriture ;
- relecture post-écriture du contenu, du résumé, de la balise et de la révision ;
- compatibilité de lecture des plans historiques sans contrat ;
- `review-import` intermédiaire reste sans écriture distante tant qu’aucune page finale n’est rendue.
