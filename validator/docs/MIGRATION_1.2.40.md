# Migration du validateur 0.4.43 / norme 1.2.40

Le validateur accepte l’omission du paramètre de résumé uniquement pour les pages importées classées `historical_absent`, vérifiées contre l’inventaire source. Toute omission sur une page nouvelle ou un résumé `generated_after_import` reste bloquante.

Le registre de revue distingue `historical_existing`, `historical_absent` et les résumés nouveaux. Le validateur refuse toute absence non prouvée et toute réintroduction silencieuse sur une page verrouillée comme historiquement vide.
