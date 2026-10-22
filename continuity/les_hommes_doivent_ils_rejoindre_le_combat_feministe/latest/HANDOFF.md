# Handoff — Les hommes doivent-ils rejoindre le combat féministe ?

- Branche : `codex/traduction-combat-feministe`
- Base GitHub synchronisée : `91fdb36`
- Date du snapshot : 22 octobre 2026
- Phase : `graph_review`, retour corrigé prêt à être réimporté
- Work réservé : `EDIT-20261022-001`
- Écritures MediaWiki effectuées : aucune

## Travail accompli

- extraction auditée importée : 100 arguments, 115 relations, 125 occurrences ;
- graphe sans cycle, page manquante ni avertissement d’extraction ;
- revue indépendante des 125 placements terminée ;
- dix corrections de titres certaines ou nécessaires à leur autonomie préparées ;
- aucun résumé, citation ou autre contenu historique supprimé ou réécrit ;
- correctif générique ajouté pour préserver une classification historiquement
  absente pendant le checkpoint « graphe + titres », avec preuve par la revue
  approuvée, son verrou et l’import exact ;
- la preuve lit désormais les octets historiques sans leur appliquer la règle
  de saut de ligne réservée aux fichiers générés ;
- la sauvegarde conserve aussi octet pour octet le reçu d'exécution de la
  validation initiale déjà inclus dans l'empreinte source, y compris ses deux
  chemins historiques absolus ; les nouvelles exécutions utilisent désormais
  des chemins relatifs, mais une ancienne preuve scellée ne doit pas être
  normalisée rétroactivement ;
- le checkpoint « graphe + titres » possède désormais un profil de validation
  différentiel : chaque sortie doit être reconstruite exactement depuis son
  import, avec pour seules mutations les paramètres de relations autorisés ;
- le checkpoint de contenu conserve le profil complet, dont le contrôle du
  wikicode final ;
- tests ciblés, tests de corpus et tests d’orchestration : 106 réussites.

## Prochaine commande

Restaurer le ZIP de `reviews/` dans `incoming/`, restaurer les deux dossiers de
`runtime/` dans leurs emplacements `.state/`, puis lancer :

```bash
./wikidebia review-import les_hommes_doivent_ils_rejoindre_le_combat_feministe
```

Cette commande doit finaliser la revue et préparer le premier checkpoint
français. Avant toute écriture distante, contrôler le plan produit par le kit.

## Incident corrigé

Le kit 2.16.47 ne transmettait pas au validateur isolé le registre approuvé qui
prouve que rubriques et mots-clés restent différés pendant la revue de titres.
Le correctif copie le registre finalisé dans la copie revue, recalcule et vérifie
son empreinte cryptographique, puis n’accorde l’exception qu’aux champs vides
attestés simultanément par ce registre signé, son verrou dérivé et le wikicode
importé intact.

Une seconde anomalie faisait ensuite valider le checkpoint « graphe + titres »
comme s’il contenait déjà les résumés, classifications, sources et verrous du
checkpoint final. Le kit sépare maintenant les deux profils : le premier exige
la preuve différentielle et tous les contrôles structurels, tandis que le
second reste soumis au contrôle documentaire et wikicode complet.

Lors de la première projection de continuité, les deux chemins absolus du reçu
`reports/initial_validation_execution.json` avaient été rendus relatifs après
le calcul de `source_build_sha256`. Cette modification pourtant informative
invalidait la preuve cryptographique au réimport. Les octets historiques ont été
restaurés ; la correction générique qui produit des chemins relatifs reste
applicable uniquement aux nouvelles validations.

## Vérification

Vérifier `SHA256SUMS` avant restauration. Le commit Git contenant ce fichier est
le commit de référence du snapshot ; les états antérieurs restent dans
l’historique de la branche.
