# Wikidéb’IA — Kit 2.15.27

Le kit 2.15.27 applique le contrat de préservation 1.2.50. Le profil de **création** reste restreint ; le profil de **modification** commence au contraire par l’état existant et ne peut plus s’en servir comme cible de nettoyage.

Pour une page préexistante, les métadonnées historiques et avertissements sont réémis à l’identique. En plus, le planificateur compare directement les paramètres top-level de la révision distante avec ceux du rendu proposé et bloque toute disparition non autorisée, y compris pour un paramètre de contenu qui ne fait pas partie des métadonnées opaques. Une suppression n’est admise que par une décision explicite page/paramètre ou une exception spécialisée déjà verrouillée.

Les marqueurs `Argument généré par IA` et `Débat généré par IA` sont réservés aux pages réellement nouvelles.

Kit aligné sur la norme 1.2.50 et le validateur 0.4.53.
