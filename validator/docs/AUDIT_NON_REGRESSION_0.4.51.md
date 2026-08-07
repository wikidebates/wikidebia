# Audit de non-régression — validateur 0.4.51

Le contrôle `WDV-RMT-007` autorise uniquement les révisions manuelles explicitement adoptées par un registre 1.2.48. Chaque entrée est liée à une page précise et à une révision ou une empreinte distante exacte. Une modification ultérieure, un titre divergent ou une permission de cycle de vie absente reste bloquant. Les relations externes adoptées sont vérifiées dans le wikicode sans créer artificiellement un nœud local. Les 298 tests du validateur passent sans régression.
