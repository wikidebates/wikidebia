# Audit de non-régression 0.4.11

Le validateur refuse sous la norme 1.2.11 les jonctions de modèles comportant un retour à la ligne, y compris CRLF, plusieurs lignes vides et espaces ou tabulations autour du saut. La forme `}}{{` est acceptée. Le contrôle n’est pas activé rétroactivement pour les paquets 1.2.10. Toutes les règles documentaires et éditoriales 0.4.10 sont conservées.
