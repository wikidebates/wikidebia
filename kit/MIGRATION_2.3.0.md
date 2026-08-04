# Migration vers le kit 2.3.0

Le kit 2.3.0 ajoute la commande en lecture seule `./wikidebia graph-extract`.

Cette commande extrait récursivement le graphe d'une page Débat, suit les modèles `Justification` et `Objection`, résout les redirections, arrête par défaut les branches aux paramètres `débat détaillé`, conserve un cache reprenable et produit un snapshot du wikicode avec les identifiants de révision et les empreintes SHA-256.

Aucune règle normative, aucun schéma de corpus et aucun comportement de publication ou de reprise distante ne sont modifiés. Les sorties sont placées par défaut sous `.state/graph-extract/` et ne sont pas versionnées.

Exemple :

```bash
./wikidebia graph-extract "Dieu existe-t-il ?"
```
