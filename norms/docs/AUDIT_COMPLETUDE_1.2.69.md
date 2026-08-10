# Audit de complétude — Normes 1.2.69

- 503 exigences uniques et 103 alias de provenance résolus ;
- norme 1.2.68 archivée bit à bit avant remplacement (SHA-256 `7844786596befcc41cecbc46d47cac5685459ff120490de078c315a734262bbe`) ;
- 92 fichiers normatifs synchronisés bit à bit avec le validateur ;
- aucune exigence, alias, contrôle WDV, schéma, migration, script, fonction de test ou capacité déclarative perdue par rapport à 1.2.55, 1.2.60, 1.2.61 ou 1.2.68 ;
- paramètres MediaWiki courants : `sujet-développé` / `expanded-topic` pour `Débat` / `Debate`, `débat-dédié` / `dedicated-debate` pour `Argument` ;
- les anciens noms `sujet-complet` / `complete-topic` et `débat-détaillé` / `detailed-debate` restent des alias de format historique lisibles pour les corpus antérieurs à 1.2.69 ;
- la migration vers le contrat courant conserve exactement la valeur et normalise uniquement le nom du paramètre ; ancien et nouveau noms ne coexistent pas dans une sortie courante ;
- les clés internes `complete_topic` et `detailed_debate` restent inchangées.
