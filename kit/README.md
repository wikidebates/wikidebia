# Wikidéb’IA — Kit 2.15.9

Kit générique aligné sur la norme 1.2.34 et le validateur 0.4.36. Le profil `norm_1_2_deferred_translation` publie et met à jour les pages françaises sans titre anglais, sans page anglaise et sans lien interlangue lorsque `translation_status.en=deferred`. Les portées anglaises sont alors bloquées.

Après traduction, le passage à `ready` ou `published` réactive le profil bilingue strict et permet une reprise française ciblée pour ajouter les liens interlangues exacts. Aucun titre anglais provisoire n'est inventé et aucun lien valide existant n'est supprimé automatiquement.
