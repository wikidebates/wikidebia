# Migration 1.2.70

Correctif sans changement éditorial. Le validateur n’assimile plus les métadonnées françaises de source aux métadonnées de première publication anglaise : `initialisation` n’est pas projeté vers `initialization`, et `creation-date` n’est pas comparée à `date-création`. Les corpus et historiques existants ne sont pas réécrits.
