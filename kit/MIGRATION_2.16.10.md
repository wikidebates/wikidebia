# Migration 2.16.10 — faux positif des tournures impersonnelles

Cette maintenance ne change aucune règle éditoriale. Elle corrige uniquement l’implémentation du contrôle d’autonomie des titres canoniques français.

`Il faut…` et `Il ne faut…` sont des constructions impersonnelles et ne possèdent pas de référent extérieur au titre. Elles ne doivent donc pas déclencher `WDV-EDT-016`. Les usages réellement anaphoriques de `Il`, `Elle`, `Ils`, `Elles` et des démonstratifs restent contrôlés comme auparavant.

Cas de régression : `Il ne faut pas instaurer plus de temps libre` doit être accepté comme titre autonome.
