# Migration 2.16.8

Aucune migration manuelle des workflows n’est requise. Les états existants restent identifiés par leur schéma et leurs preuves de provenance ; le numéro du kit producteur n’est pas une condition de reprise.

Lorsqu’un `review-import` local échoue pendant l’avancement mécanique qui suit la revue, la transaction restaure désormais l’état précédent afin que le même ZIP puisse être réimporté. Si des actions structurelles ont déjà été écrites sur le wiki, leurs plans et reçus constituent une frontière irréversible : ces actions ne sont ni annulées ni rejouées, et le workflow reprend depuis l’état post-action attesté.
