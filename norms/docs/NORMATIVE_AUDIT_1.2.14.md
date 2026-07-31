# Audit normatif 1.2.15

La révision corrige une contradiction entre la sélection automatique d’un ZIP unique et l’ancienne obligation d’égalité entre le nom du ZIP et `manifest.debate_id`. Le nom est désormais un sélecteur de fichier uniquement. L’identité du corpus reste contrôlée dans le manifeste interne, dont le `debate_id` est validé avant installation.
