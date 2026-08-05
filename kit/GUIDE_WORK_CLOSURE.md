# Clôture formelle d’un Work — Kit 2.15.11

Cette phase intervient uniquement après une exécution distante terminée avec un reçu signé `executed` ou `no_changes`. Elle ne contacte pas MediaWiki.

## Commande

```bash
./wikidebia corpus-workspace-close <debate_id> \
  --work-id <work_id> \
  --comparison-id <comparison_id> \
  --confirm-execution-sha256 <empreinte_du_reçu>
```

## Vérifications bloquantes

La commande recharge et vérifie la chaîne complète : plan, acceptation, préflight, autorisation, reçu d’exécution, `release-copy/` et états publiés signés. Toutes les pages du corpus final doivent être présentes dans les états publiés avec le même titre et la même empreinte. Une page `pending_delete`, une révision absente, une langue non attestée ou une divergence de reçu bloque la clôture.

Une validation locale fraîche du corpus final est exécutée avant toute promotion. Cette validation écrit ses rapports sous `.state/work-closures/` et ne modifie pas `release-copy/`.

## Promotion locale et archive

Le corpus actif `corpus/<debate_id>/` est échangé atomiquement avec une copie exacte de `release-copy/` au moyen d’un échange de dossiers sur le même système de fichiers. Le corpus actif précédent est ensuite conservé sous :

```text
archives/completed-works/<debate_id>/<work_id>/<comparison_id>/previous-corpus/
```

Les preuves de libération, comparaison, revue, exécution et états publiés sont regroupées dans `work-evidence.zip`, avec un manifeste SHA-256 exhaustif.

## Reçu final

Le reçu de clôture se trouve sous :

```text
.state/work-closures/<debate_id>/<work_id>/<comparison_id>/work-closure-receipt.json
```

Il lie toutes les empreintes de la chaîne, le corpus actif final, le corpus précédent, l’archive de preuves et les états publiés. Un index est également écrit sous `.state/completed-works/<debate_id>/`. La commande est idempotente tant que le corpus actif et le reçu restent intacts.
