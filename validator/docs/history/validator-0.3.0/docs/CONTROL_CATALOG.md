# Catalogue stable des codes de contrôle

| Code | Signification | Niveau habituel |
|---|---|---|
| `WDV-SCH-001` | Fichier JSON illisible | ERROR |
| `WDV-SCH-002` | Schéma JSON introuvable ou non applicable | ERROR |
| `WDV-SCH-003` | Violation de JSON Schema | ERROR |
| `WDV-FS-001` | Fichier obligatoire manquant | ERROR |
| `WDV-FS-002` | Chemin non sûr ou extérieur au paquet | ERROR |
| `WDV-FS-003` | Empreinte SHA-256 incorrecte | ERROR |
| `WDV-FS-004` | Fichier déclaré mais absent | ERROR |
| `WDV-FS-005` | Normalisation textuelle non conforme | ERROR |
| `WDV-FS-006` | Fichier orphelin ou dupliqué | ERROR |
| `WDV-GRA-001` | Identifiant dupliqué | ERROR |
| `WDV-GRA-002` | Titre canonique dupliqué ou collision normalisée | ERROR |
| `WDV-GRA-003` | Référence à un nœud inexistant | ERROR |
| `WDV-GRA-004` | Référence à une relation ou occurrence inexistante | ERROR |
| `WDV-GRA-005` | Cycle détecté | ERROR |
| `WDV-GRA-006` | Autojustification ou auto-objection | ERROR |
| `WDV-GRA-007` | Relation directe dupliquée | ERROR |
| `WDV-GRA-008` | Occurrence incohérente avec sa relation | ERROR |
| `WDV-GRA-009` | Profondeur ou branche incorrecte | ERROR |
| `WDV-GRA-010` | Occurrence primaire absente ou multiple | ERROR |
| `WDV-GRA-011` | Occurrence secondaire développée | ERROR |
| `WDV-GRA-012` | Nœud ou occurrence orphelin | ERROR/WARNING |
| `WDV-GRA-013` | Compteur dérivé incorrect | ERROR/WARNING |
| `WDV-GRA-014` | Projection JSON divergente du registre maître | ERROR |
| `WDV-GRA-015` | Empreinte structurelle incorrecte | ERROR |
| `WDV-GRA-016` | Titre non conforme | ERROR |
| `WDV-GRA-017` | Branches principales incomplètes | ERROR |
| `WDV-BAT-001` | Lot inconnu ou identifiant de nœud inexistant | ERROR |
| `WDV-BAT-002` | Chevauchement entre lots | ERROR |
| `WDV-BAT-003` | Lacune de couverture des lots | ERROR |
| `WDV-BAT-004` | Dépendance de lot incohérente | ERROR |
| `WDV-BAT-005` | Lot obsolète ou empreinte d'entrée incohérente | ERROR/WARNING |
| `WDV-MWK-001` | Wikicode mal formé | ERROR |
| `WDV-MWK-002` | Modèle principal incorrect | ERROR |
| `WDV-MWK-003` | Paramètre inconnu ou interdit | ERROR |
| `WDV-MWK-004` | Paramètre obligatoire absent | ERROR |
| `WDV-MWK-005` | Paramètre vide interdit | ERROR |
| `WDV-MWK-006` | Ordre des paramètres incorrect | ERROR |
| `WDV-MWK-007` | Valeur fixe incorrecte | ERROR |
| `WDV-MWK-008` | Relation MediaWiki absente, supplémentaire ou erronée | ERROR |
| `WDV-MWK-009` | Rubrique, section ou mot-clé non conforme | ERROR |
| `WDV-MWK-010` | Date de création incorrecte | ERROR |
| `WDV-MWK-011` | Lien interlangue prématuré, absent ou erroné | ERROR |
| `WDV-MWK-012` | Sous-modèle ou paramètre documentaire incorrect | ERROR |
| `WDV-MWK-013` | Agrégat incohérent avec les fichiers individuels | ERROR |
| `WDV-MWK-014` | Langue ou typographie documentaire non conforme | ERROR |
| `WDV-BIL-001` | Identifiants ou pages bilingues divergents | ERROR |
| `WDV-BIL-002` | Relations bilingues divergentes | ERROR |
| `WDV-BIL-003` | Occurrence primaire ou réutilisation bilingue divergente | ERROR |
| `WDV-BIL-004` | Correspondance rubriques-sections divergente | ERROR/WARNING |
| `WDV-BIL-005` | Titre interlangue divergent | ERROR |
| `WDV-BIL-006` | Asymétrie éditoriale bilingue substantielle | ERROR |
| `WDV-WF-001` | État global incompatible avec les fichiers présents | ERROR |
| `WDV-WF-002` | Transition d'état interdite | ERROR |
| `WDV-WF-003` | Validation préalable absente ou échouée | ERROR |
| `WDV-WF-004` | Transmission incompatible avec le paquet | ERROR |
| `WDV-WF-005` | Champ verrouillé ou version normative incohérente | ERROR |
| `WDV-SRC-001` | Source dupliquée ou identifiant documentaire dupliqué | ERROR |
| `WDV-SRC-002` | Usage de source vers une page inexistante | ERROR |
| `WDV-SRC-003` | Source rejetée encore utilisée ou source vérifiée inutilisée | ERROR |
| `WDV-DOC-001` | Contrôle éditorial humain requis ou enregistré | INFO |
| `WDV-DOC-002` | Pagination bibliographique incorrecte | ERROR |
| `WDV-DOC-003` | Date sitographique non documentaire | ERROR |
| `WDV-EDT-001` | Titres affichés copiés mécaniquement | ERROR |
| `WDV-EDT-002` | Classification ou mots-clés mécaniques | ERROR |
| `WDV-EDT-003` | Résumé contenant une auto-objection ou du métadiscours | ERROR |
| `WDV-EDT-004` | Documentation de la page de débat insuffisante ou mécanique | ERROR |
| `WDV-EDT-005` | Migration corrective des dates incomplète | ERROR |
| `WDV-EDT-006` | Traçabilité corrective ou revue humaine absente | ERROR |
| `WDV-EDT-007` | Titre affiché tronqué, elliptique ou grammaticalement mal formé | ERROR |
| `WDV-EDT-008` | Mot-clé non nominal, non traduit ou absent du vocabulaire contrôlé | ERROR |
| `WDV-EDT-009` | Guillemets canoniques non conformes | ERROR |
| `WDV-EDT-010` | Appels de référence inline des introductions absents ou mal placés | ERROR |
| `WDV-EDT-011` | Régression normative, norme active multiple ou handoff courant absent | ERROR |
| `WDV-EDT-012` | Revue individuelle des titres affichés et rubriques absente ou incohérente | ERROR |
| `WDV-EDT-013` | Style du résumé trop lourd ou revue des termes techniques absente | ERROR/WARNING |
| `WDV-INT-001` | Erreur interne du validateur | ERROR |

Le niveau exact dépend de l’état du paquet. Une anomalie tolérable pendant un brouillon peut devenir bloquante après validation ou verrouillage.
