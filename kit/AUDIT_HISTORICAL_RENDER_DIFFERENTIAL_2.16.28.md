# Audit — propagation de provenance au rendu — Kit 2.16.28

Le rendu final ajoute `editorial_controls.historical_text_render_validation_mode=differential_preservation_v1` au manifeste dérivé. Cette clé est un garde-fou explicite : elle autorise le validateur 0.4.96 à relire les verrous historiques legacy lors du préflight, sans réécriture du contenu.

Le correctif ne modifie ni `fr_content_lock.json`, ni les imports, ni les résumés, ni l’introduction. Les régressions de rendu vérifient que le mode est présent dans une sortie courante.
