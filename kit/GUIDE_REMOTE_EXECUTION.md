# Exécution distante contrôlée d’un plan accepté

Cette phase intervient après `corpus-workspace-remote-compare` et `corpus-workspace-plan-review`. Elle consomme uniquement le plan signé et son acceptation signée.

## 1. Préflight distant en lecture seule

```bash
./wikidebia corpus-workspace-plan-execute <debate_id> \
  --work-id <work_id> \
  --comparison-id <comparison_id> \
  --prepare \
  --mode all \
  --confirm-acceptance-sha256 <empreinte>
```

Le préflight recharge le plan, la comparaison, l’inventaire distant, la revue, l’acceptation et `release-copy/`. Il relit chaque page concernée, y compris les `skip`, vérifie l’identité du compte et les droits effectifs, puis scelle `execution-preflight.json`. L’adaptateur d’écriture reste désarmé et toute tentative de mutation est bloquée.

Les modes disponibles sont `all`, `no-delete` et `only-delete`. Un mode ne contenant aucune opération mutante renvoie `no_changes_in_scope` et ne peut pas être exécuté. Un plan intégralement `skip` reste exécutable comme attestation `no_changes`.

## 2. Exécution

```bash
./wikidebia corpus-workspace-plan-execute <debate_id> \
  --work-id <work_id> \
  --comparison-id <comparison_id> \
  --execute \
  --confirm-preflight-sha256 <empreinte>
```

Avant d’armer l’écriture, le kit refait immédiatement le préflight. Une divergence de révision, de contenu, de présence ou de droits bloque l’exécution sans écriture. Une autorisation locale signée est ensuite créée, puis le moteur de reprise existant applique les opérations avec `createonly`, `baserevid`, contrôle d’identité, relecture après écriture, vérification du graphe avant suppression et mise à jour signée de l’état publié.

## 3. Reçus et reprise

Les preuves sont conservées sous :

```text
.state/remote-executions/<debate_id>/<work_id>/<comparison_id>/
```

Elles comprennent le préflight, son reçu, les journaux d’événements, l’autorisation, le reçu final ou un reçu d’échec. Une interruption après une ou plusieurs écritures est consignée explicitement ; une nouvelle exécution reste idempotente grâce aux contrôles du plan et aux relectures distantes.

Cette commande effectue réellement des écritures MediaWiki uniquement avec `--execute` et après confirmation exacte du préflight.
