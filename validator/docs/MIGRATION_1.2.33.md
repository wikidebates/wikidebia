# Migration vers la norme 1.2.33

Les paquets 1.2.33 ajoutent aux manifestes de page :

- `page_origin`, valant `new` ou `preexisting` ;
- `preserved_parameters`, vide pour une page nouvelle et exhaustif pour les paramètres protégés d’une page préexistante.

Les usages `supports_summary` d’une référence d’Argument déclarent :

- `argument_development_verified=true` ;
- `also_develops_objections`, booléen descriptif qui n’entraîne aucun rejet lorsqu’il vaut `true`.

Les corpus déclarant une norme antérieure conservent leur contrat historique.
