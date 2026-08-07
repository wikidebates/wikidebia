# Migration 2.15.27

Cette migration sépare définitivement les profils de création et de modification. Une page existante n’est plus reconstruite à partir de la seule liste des paramètres générés : ses paramètres historiques opaques sont conservés exactement et toute disparition d’un autre paramètre top-level est bloquée au moment du plan distant sauf autorisation explicite.

Le mode `historical_parameter_restoration` sert uniquement à réparer une contamination antérieure démontrée par un inventaire historique validé ; il ne fournit aucune autorisation générale de suppression.
