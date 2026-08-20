# Audit — statut historique du checkpoint français final — kit 2.16.43

Le correctif couvre les Work anciens déjà arrivés à `final_publication` dont l'entrée `french_content_publication` ne possède ni `receipt_sha256` ni `plan_sha256`, mais conserve un statut local non canonique.

La réconciliation n'est autorisée que si le workflow est totalement non lié, sans revue pendante, que la publication finale n'a pas commencé, qu'aucun état anglais signé n'existe, que le reçu français courant est auto-signé et publié pour le même débat/Work/stage, et que `.state/published/<débat>/fr/latest.json` atteste exactement le même `plan_sha256`.

Un workflow déjà lié à un ancien hash ou plan n'est jamais normalisé sur la seule base d'un statut historique.
