# Migration vers la norme 1.2.54 — normes éditoriales cumulatives

La révision 1.2.54 sépare explicitement **compatibilité de format** et **application des normes éditoriales**.

## Ce qui change

- `normative_versions.consolidated_norm` reste une information de provenance, de lecture/migration et de publication ; il ne sélectionne plus les règles éditoriales.
- Les champs `*_policy_revision` et `*_revision` historiques sont acceptés comme traces, mais leur valeur ne peut plus activer ou désactiver un contrôle.
- Les générateurs n’ont plus à produire ces champs lorsqu’ils ne servent qu’à sélectionner une politique.
- Les contrôles sont déterminés par l’état fonctionnel : registres réellement présents, origine des pages, statut de traduction, préservation historique et inventaire source, état distant, etc.
- Les formats d’artefacts continuent à posséder leur propre `schema`, `schema_version` ou identifiant `version`.

## Compatibilité

Les lecteurs peuvent examiner une ancienne version globale pour interpréter ou migrer un ancien format. Une fois les données interprétées, le validateur applique cependant l’ensemble des règles éditoriales actives de 1.2.54. Déclarer une ancienne norme ne constitue donc plus un moyen de contourner une exigence courante.

Les anciens champs de révision peuvent rester dans des corpus déjà produits pour assurer la reproductibilité. Il n’est pas nécessaire de les réécrire uniquement pour migrer vers 1.2.54.

## Traduction anglaise

Aucun changement de contenu n’est apporté au protocole 1.2.53 : la page `Debate` reste un lot autonome ; les arguments restent traités par lots bornés ; `name=` fait l’objet d’une recherche anglophone indépendante ; une référence française n’est projetée que si une version anglaise réelle existe ; de nouvelles références anglaises sont recherchées ; le contrat `Citation`→`Quote` reste inchangé.
