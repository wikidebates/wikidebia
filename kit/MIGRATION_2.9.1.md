# Migration vers le kit 2.9.1

Le kit 2.9.1 corrige la phase de traduction anglaise 2.9.0 en intégrant les citations déjà présentes dans les pages Argument françaises importées.

Après `--prepare`, chaque entrée d’argument du registre anglais contient une liste `citations`. Le relecteur renseigne uniquement `translated_citation` et `translated_date`, puis confirme les attestations de conservation. La finalisation refuse toute modification des paramètres source.

L’application place dans `en_content_lock.json` les paramètres de sortie déterministes : tous les paramètres documentaires sont inchangés, `citation` et `date` sont traduits, et `avertissements-citation` contient `Quote translated by AI`, précédé de `, ` lorsqu’un avertissement existait déjà.

Les workspaces 2.9.0 dont la revue anglaise n’a pas été finalisée doivent être régénérés avec `--overwrite-review`. Une traduction 2.9.0 déjà appliquée doit faire l’objet d’un nouveau Work : son verrou ne contient pas les attestations de citations 2.9.1. Aucune page finale n’est générée par cette correction.
