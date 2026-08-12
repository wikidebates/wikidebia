# Audit 1.2.85 — valeur finale sélectionnée et consentement historique

Statut : **PASSED**.

Le validateur distingue la provenance historique de la valeur éditoriale effective. `preserved` impose le SHA historique ; `authorized_change` impose le SHA final propriétaire. Pour le contrat v3, `change_type` et `change_scope` doivent être identiques dans le verrou, l’autorisation et le reçu local. Les reçus v2 de 2.16.17 restent lisibles.

Une portée structurée d’introduction permet de sceller précisément les sous-parties ajoutées, modifiées ou supprimées et le réordonnancement. Toute divergence est signalée par `WDV-EDT-034`.
