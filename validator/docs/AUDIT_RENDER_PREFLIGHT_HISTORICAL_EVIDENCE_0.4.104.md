# Audit — préflight différentiel des preuves historiques 0.4.104

Le diagnostic réel `revenu_de_base_render_preflight_diagnostic.zip` exposait vingt erreurs issues de quatre causes racines : une règle de prose appliquée à un résumé historique, un avertissement de sous-partie anglais provenant d’une introduction française historique, des métadonnées de mots-clés atomiques devenues incohérentes avec le format multi-mots courant, et un ancien registre d’introduction non autoritatif.

Le correctif maintient les verrous FR/EN comme source de vérité. Aucun titre, résumé, introduction, mot-clé ni relation du graphe n’est réécrit par le validateur. Les dérogations sont bornées par la provenance historique ou par une attestation explicite du vocabulaire contrôlé. Les contenus nouveaux restent soumis à l’ensemble des contrôles courants.
