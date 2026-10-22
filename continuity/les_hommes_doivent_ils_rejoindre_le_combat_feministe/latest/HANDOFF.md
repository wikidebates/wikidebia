# Handoff — Les hommes doivent-ils rejoindre le combat féministe ?

- Branche : `codex/traduction-combat-feministe`
- Correctifs GitHub synchronisés jusqu’à : `26fedd9`
- Commit de référence du snapshot : commit contenant ce fichier
- Date du snapshot : 22 octobre 2026
- Phase : `graph_publication_resume`
- Statut : `graph_publication_plan_ready`
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
- le préflight distant authentifié a produit le plan signé
  `runtime/fr-publication/graph/update-plan.json` : 89 mises à jour, dix
  renommages, deux pages inchangées, aucun blocage et aucune revue manuelle ;
- aucun reçu de publication ou état d’exécution distant n’existe encore ;
- tests ciblés du workflow, des deux checkpoints et du validateur : 42 réussites.
- tests ciblés du connecteur d’authentification : 60 réussites.

## État distant courant

L’accès API français et l’identité `ChatGPT@Codex-FR` ont été vérifiés. Les
secrets gérés sont transmis directement en mémoire au gestionnaire de connexion,
sans copie dans la sauvegarde. Le secret anglais est injecté, mais l’identité
essayée `ChatGPT@Codex-EN` est refusée par le wiki anglais ; elle n’est donc pas
attestée prête. Ce point ne bloque pas le checkpoint français.

Le workflow restauré conserve encore l’attestation historique antérieure au
préflight :

```text
phase=graph_publication_resume
status=blocked_remote_publication
remote_publication_stage=graph
last_remote_publication_execution_started=false
```

Le plan signé porte l’empreinte
`fc0200ff9ba45f40fdf7af6c185eb63e94fae1a8cf6de8581c3077a88106584a`.
L’exécution distante n’a pas commencé.

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
6. Vérifier que l’identité FR est toujours disponible, puis lancer :

```bash
./wikidebia workflow 'Les hommes doivent-ils rejoindre le combat féministe ?' \
  --debate-id les_hommes_doivent_ils_rejoindre_le_combat_feministe
```

La commande doit réutiliser ou vérifier le plan du checkpoint graphe/titres,
l’exécuter de façon contrôlée et produire son reçu signé. Elle préparera ensuite
automatiquement la revue française de contenu ; la traduction anglaise ne doit
commencer qu’après le second checkpoint français.

## Correctifs génériques ajoutés pendant cette reprise

- conservation octet pour octet des preuves déjà scellées dans une sauvegarde de
  continuité (`ecb5f95`) ;
- enregistrement explicite d’un blocage réseau lors de la reprise d’un checkpoint
  (`3177331`) ;
- conversion des échecs de connexion pendant le préflight en
  `FrenchCheckpointError`, avec attestation qu’aucune écriture n’a commencé
  (`8b35e41`) ;
- transmission en mémoire des BotPasswords gérés, sans fichier secret local
  (`26fedd9`).

Les états antérieurs et le build préparatoire restent accessibles dans
l’historique Git de la branche.
