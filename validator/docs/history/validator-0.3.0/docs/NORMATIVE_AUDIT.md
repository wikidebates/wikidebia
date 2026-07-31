# Audit normatif — Wikidéb’IA 1.0.6

## Sources actives

Le validateur 0.2.1 est construit à partir du paquet normatif **Wikidéb’IA 1.0.6**, qui remplace les révisions 1.0.2 à 1.0.5. Les sources prioritaires intégrées sont :

- `cahier_des_charges_consolide_wikidebia.md` ;
- `requirements_catalog_wikidebia.json` — 252 exigences atomiques ;
- `MATRICE_TRACEABILITE_DESIDERATA.md` ;
- `DECISIONS_CONVERSATION_CONSOLIDEES.md` ;
- `structures_mediawiki_wikidebia.md` ;
- `profils_rendu_wikidebia.md` ;
- `schema_graphe_registre_wikidebia.md` ;
- `workflow_production_wikidebia.md` ;
- les quinze JSON Schema Draft 2020-12.

L’audit reproductible du paquet 1.0.6 a été exécuté depuis une extraction vierge et a indiqué `AUDIT GLOBAL : RÉUSSI`.

## Changements pris en compte depuis 1.0.2

### Documentation et références

- Une bibliographie doit identifier un auteur, une institution ou une responsabilité éditoriale équivalente.
- Une vidéo peut exceptionnellement ne pas avoir d’auteur dans le wikicode et dans le registre documentaire, mais le registre doit alors contenir une note de vérification non vide.
- `numéro=` et `issue=` acceptent uniquement des chiffres ; toute autre localisation doit être portée par `localisation=` ou `location=`.
- Les dates descriptives et les lieux sont adaptés à la langue de la page, sans traduire artificiellement les titres originaux.
- Dans le texte français, un appel `<ref>` précède le signe de ponctuation final.

### Profil MediaWiki

- La valeur française normative est `avancement=Débat construit`.
- Les avertissements fixes utilisent `généré avec IA` / `generated with AI`.
- Les paramètres facultatifs vides sont interdits dans les sorties générées.
- Les liens interlangues sont préparés localement puis appliqués aux pages françaises après disponibilité des cibles anglaises.

### Workflow et archives

- Les journaux d’import sont des sorties de publication, non des entrées préexistantes.
- Le manifeste interne ne s’auto-référence pas ; l’empreinte du ZIP est portée par un reçu externe.
- Le statut `migration_required` permet de représenter honnêtement les paquets historiques dont les Work et handoffs n’existaient pas.

## Clarifications d’implémentation

### Empreinte d’entrée des lots

`inputs.registry_sha256` désigne un instantané d’entrée immuable. Il est comparé au fichier déclaré par la transmission lorsqu’une correspondance est disponible. L’obsolescence du graphe est contrôlée séparément par `structural_sha256`.

### Données dérivées

Les blocs `derived` et les compteurs sont recalculés sémantiquement. Leur absence ou divergence devient bloquante lorsque le graphe est validé ou verrouillé.

### Staging interlangue en migration

Un paquet `migration_required` peut contenir un patch interlangue validé ou partiellement appliqué. Dans ce cas, le validateur contrôle également les copies de staging françaises, même si l’état global n’a pas parcouru historiquement `interlanguage_prepared`.

### Appréciation humaine

La force logique, l’équilibre des camps, les quasi-doublons sémantiques, la qualité des traductions et la fidélité substantielle des sources restent signalés comme contrôles humains par `WDV-DOC-001`.

## Résultat

Aucune modification du paquet normatif 1.0.6 n’a été nécessaire. Le validateur ajoute uniquement des invariants sémantiques et des décisions d’exécution documentées.
