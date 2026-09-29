# Suivi de la todo liste — R10

| Demande | État dans le code |
|---|---|
| Espacement et sélection multiple du schéma | Implémentés ; gestes et liste Shift/Ctrl, déplacement groupé |
| Retrait Site wiring / Electrical data | Retirés de la barre du schéma |
| Guide Home développé | Dix rubriques détaillées adaptées du tutoriel fourni |
| Transformation des zones à la souris | Priorité rétablie face au déplacement de vue ; sommets de polygones transformables |
| Hauteurs par polygone | Saisie et persistance ; indépendantes de Shadow |
| Rotation des panneaux | Grille rigide, filtrage aux limites, suppression des chevauchements interzones à la génération |
| Câblage 3D et zones proches | Hauteurs traversées, seuil de pont réglable, réserves et légende explicites |
| Refonte BESS | Comparaison intégrée, graphiques cohérents, calcul unique ; résultats périmés masqués |
| Rapport PDF depuis Home | PDF, LaTeX à équations éditables, figures, entrées JSON ; mise en page sobre |
| Configuration matériel depuis Home | Déplacée ; Variable explorer agrandi |
| Cotations CAO | Modes aligné/horizontal/vertical, lignes d'attache, doubles flèches, positionnement du texte |
| Revue architecture | Audit et priorités dans AUDIT_TECHNIQUE_FR.md |
| Nettoyage | Sources utiles, tests actuels et projets conservés ; doublons/caches/documents obsolètes retirés |

## Validation et limites

25 tests automatisés passent ; import de l'application et compilation réussis. Rapport de contrôle sur données synthétiques généré et vérifié visuellement. Pas d'affichage Tkinter disponible : recette graphique Windows non exécutée, script fourni. Compilation LuaLaTeX non exécutée ; le PDF est généré sans LaTeX. Se reporter à l'audit pour les limites du modèle et les travaux restant recommandés.

## Décisions explicites

- Aucun seuil de franchissement réel supposé : 0 m initialement, à régler.
- Aucune hauteur Shadow substituée à une hauteur Installation manquante.
- Résultats énergétiques historiques invalidés après changement des entrées.
- Aucun calcul de retour annuel pour un profil inférieur à une année complète.
- Aucun projet de démonstration pris pour une étude réelle.
