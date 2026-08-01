# Architecture du validateur 0.4.17

Le validateur sépare schémas, cohérence, graphe, lots, sources, fichiers, wikicode, bilinguisme, éditorial et workflow. La commande `validate-plan` ajoute une voie indépendante pour contrôler les artefacts de reprise distante.

Cette voie charge exclusivement un fichier local, applique `remote_update_plan.schema.json`, recalcule son empreinte déterministe et contrôle les invariants de sûreté. Elle n’importe pas Pywikibot, n’ouvre aucune session et n’effectue aucune comparaison distante.

Les schémas `published_state`, `remote_migrations`, `remote_update_plan` et `remote_update_receipt` formalisent la frontière entre le validateur local et le kit distant. Le kit conserve seul la responsabilité des droits, révisions, lectures, écritures, déplacements et suppressions MediaWiki.

Les chemins persistants restent portables et aucune information secrète n’est traitée.
