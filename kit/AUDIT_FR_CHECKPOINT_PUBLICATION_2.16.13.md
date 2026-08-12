# Audit — checkpoint français et réimport 2.16.13

## Invariants

- aucune préparation anglaise avant publication ou attestation `no_changes` du français scellé ;
- aucun lien interlangue ajouté tant que le titre anglais n’est pas verrouillé ;
- toutes les mutations distantes héritent du contrat `page_specific_v1` et de la balise `chatgpt` ;
- redirections/suppressions implicites interdites au checkpoint de contenu ;
- plan sauvegardé et exécution idempotente après interruption ;
- une publication française commencée est une frontière irréversible : le rollback local ne masque jamais une écriture distante ;
- sélection du retour par `debate_id` interne depuis `incoming/` ;
- validation précoce de `sources_working.json.document_kind`.
