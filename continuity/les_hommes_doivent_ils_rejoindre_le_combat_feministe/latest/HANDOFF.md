# Handoff — Les hommes doivent-ils rejoindre le combat féministe ?

- Branche : `codex/traduction-combat-feministe`
- Correctifs GitHub synchronisés jusqu’à : `8b35e41`
- Commit de référence du snapshot : commit contenant ce fichier
- Date du snapshot : 22 octobre 2026
- Phase : `graph_publication_resume`
- Statut : `blocked_remote_publication`
- Work : `EDIT-20261022-001`
- Écritures MediaWiki effectuées : aucune

## Travail accompli

- extraction auditée : 100 arguments, 115 relations et 125 occurrences ;
- revue indépendante des 125 placements approuvée, sans mutation structurelle ;
- graphe validé puis promu dans `runtime/corpus/` ;
- workspace éditorial créé et revue combinée graphe/titres appliquée ;
- dix pages d’arguments reçoivent une correction certaine de titre canonique et
  de titre affiché, soit vingt opérations tracées ;
- aucun résumé, citation, référence, rubrique, mot-clé ou autre contenu
  historique n’a été supprimé ni réécrit ;
- premier checkpoint français rendu et validé avec le profil différentiel
  `fr_graph_checkpoint_differential_v1` ;
- 101 pages et l’agrégat français prêts sont conservés dans `wiki-pages/fr/` ;
- aucun `update-plan.json`, reçu de publication ou état d’exécution distant
  n’existe : l’échec a eu lieu pendant la première lecture de préflight ;
- tests ciblés du workflow, des deux checkpoints et du validateur : 42 réussites.

## Blocage courant

L’API publique `https://fr.wikidebates.org/w/api.php` renvoie une page Cloudflare
HTTP 403 avant toute comparaison distante. Le chemin HTTPS vers l’IPv4 Tailscale
`100.77.239.36` est intercepté par le relais HTTP géré et retombe lui aussi sur
Cloudflare. Le relais TCP brut déclaré à `proxy:8088` n’écoute pas dans cette
instance ; la politique locale ne contient par ailleurs aucune destination TCP.

Le workflow atteste explicitement :

```text
phase=graph_publication_resume
status=blocked_remote_publication
remote_publication_stage=graph
last_remote_publication_execution_started=false
```

Ne pas envoyer le checkpoint par le relais Git français sans mécanisme de retour
de reçu : ce relais ne publie pas son reçu sur GitHub et l’API actuellement
bloquée ne permettrait pas de vérifier le résultat.

## Reprise

1. Vérifier `SHA256SUMS`.
2. Restaurer `runtime/corpus/` dans `corpus/<debate_id>/`.
3. Restaurer `runtime/editorial-workspace/` dans
   `.state/editorial-workspaces/<debate_id>/EDIT-20261022-001/`.
4. Restaurer `runtime/fr-publication/graph/` dans
   `.state/fr-publication/<debate_id>/EDIT-20261022-001/graph/`.
5. Restaurer `runtime/corpus-promotion/` dans
   `.state/corpus-promotions/<debate_id>/` et `runtime/workflow/` dans
   `.state/workflows/<debate_id>/`.
6. Après rétablissement d’un accès API vérifiable, lancer :

```bash
./wikidebia workflow 'Les hommes doivent-ils rejoindre le combat féministe ?' \
  --debate-id les_hommes_doivent_ils_rejoindre_le_combat_feministe
```

La commande doit reprendre le préflight du checkpoint graphe/titres. Après son
reçu signé, elle préparera automatiquement la revue française de contenu ; la
traduction anglaise ne doit commencer qu’après le second checkpoint français.

## Correctifs génériques ajoutés pendant cette reprise

- conservation octet pour octet des preuves déjà scellées dans une sauvegarde de
  continuité (`ecb5f95`) ;
- enregistrement explicite d’un blocage réseau lors de la reprise d’un checkpoint
  (`3177331`) ;
- conversion des échecs de connexion pendant le préflight en
  `FrenchCheckpointError`, avec attestation qu’aucune écriture n’a commencé
  (`8b35e41`).

Les états antérieurs et le build préparatoire restent accessibles dans
l’historique Git de la branche.
