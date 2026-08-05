# Guide de revue formelle du plan distant — Kit 2.15.9

## Principe

La revue du plan est une phase locale située après `corpus-workspace-remote-compare` et avant toute exécution distante. Elle ne relit pas MediaWiki et ne modifie aucune preuve de comparaison. Elle lie les décisions humaines à l'empreinte exacte du plan, de l'inventaire distant, du reçu de comparaison et de `release-copy/`.

## Préparation

```bash
./wikidebia corpus-workspace-plan-review <debate_id> \
  --work-id <work_id> \
  --comparison-id <comparison_id> \
  --prepare
```

Le registre est créé sous :

```text
.state/remote-plan-reviews/<debate_id>/<work_id>/<comparison_id>/plan-review.json
```

Chaque opération reçoit un identifiant stable et une décision à compléter. Les opérations mutantes utilisent `approved` ou `rejected`; les opérations `skip` utilisent `acknowledged`. Une note est obligatoire pour chaque `move`, `redirect` et `delete` approuvé.

## Finalisation

```bash
./wikidebia corpus-workspace-plan-review <debate_id> \
  --work-id <work_id> \
  --comparison-id <comparison_id> \
  --finalize
```

Une approbation exige un plan sans `manual_review` ni `blocked`, toutes les opérations mutantes approuvées, tous les `skip` attestés et toutes les attestations globales vraies. Un rejet exige un motif explicite.

Une approbation produit `plan-acceptance.json`, mais conserve :

```json
{
  "execution_started": false,
  "remote_write_authorized": false,
  "remote_write_performed": false
}
```

L'exécution reste une phase distincte qui devra recharger le plan, le reçu de comparaison et l'acceptation par leurs empreintes.
