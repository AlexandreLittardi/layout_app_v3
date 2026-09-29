# PV Layout and Stringing — R10

Application de bureau Python/Tkinter. Aucun serveur ni navigateur requis.

## Installation et lancement

Python 3.12 recommandé, avec Tkinter. Depuis ce dossier :

```text
python -m pip install -r requirements.txt
python main.py
```

Sous Windows : `LANCER_WINDOWS.bat` après installation des dépendances.

## Changements de cette version

- Schéma : espacement accru, sélection multiple Shift/Ctrl-clic ou liste latérale, déplacement groupé ; retrait de Site wiring et Electrical data.
- Installation : déplacement et redimensionnement à la souris rétablis ; déplacement des polygones et de leurs sommets ; grille de panneaux tournée d'un seul bloc, cellules hors zone exclues, chevauchements entre zones éliminés lors de la génération.
- Hauteurs : saisie propre à chaque zone et polygone dans Installation. Les valeurs Shadow ne sont pas reprises pour le câblage.
- Câblage : parcours découpés aux frontières des surfaces ; différences de niveaux, réserves et seuil de franchissement pris en compte. Correction du détour artificiel lorsque deux extrémités se projettent sur le même chemin. Légende A/B explicitée.
- Cotations : lignes d'attache et doubles flèches ; mesures alignées, horizontales ou verticales ; axe conservé à la sauvegarde.
- Home : guide détaillé, configuration centralisée du matériel et des hypothèses, export du rapport technique.
- Spreadsheet : équipement déplacé vers Home ; explorateur de variables agrandi.
- BESS : comparaison intégrée, graphiques de fourniture de la charge et d'exports/écrêtement ; un seul bouton de calcul. Résultats périmés masqués ; hypothèses BESS sauvegardées même avant calcul ; retour sur investissement réservé à une année complète.

## Rapport technique

Home > Engineering report PDF produit le PDF, une source `.tex` et un dossier `_assets` contenant figures et `project_inputs.json`. Conserver ces fichiers ensemble.

Le PDF utilise Times New Roman depuis les polices Windows lorsqu'elles sont disponibles. Sur un système sans cette police, le repli compatible Times (Nimbus Roman incorporé si disponible, sinon Times Roman) est indiqué dans le document. Les graphiques utilisent leur propre typographie scientifique. Le PDF est généré directement, sans installer LaTeX. La source LaTeX, avec équations éditables, peut être compilée avec LuaLaTeX ; cette compilation n'a pas été exécutée dans l'environnement de développement.

Les champs manquants sont signalés. Les comparaisons énergétiques périmées ne sont pas présentées comme résultats actuels. Les résultats d'ombre sauvegardés restent des données historiques dans le JSON et nécessitent un nouveau calcul pour confirmer leur actualité. Les parcours présentés restent préliminaires, en particulier les replis directs.

## Ouverture d'un ancien projet

Les JSON existants restent lisibles et les projets fournis sont conservés. Renseigner les nouvelles hauteurs Installation, choisir le seuil de franchissement réel, puis recalculer les câbles. Les anciens parcours fondés sur les hauteurs Shadow sont volontairement invalidés. Après une rotation, régénérer le layout puis contrôler les strings/MPPT ; les coordonnées de grille peuvent changer. Sauvegarder une copie de travail du projet avant remaniement important.

## Vérification

```text
python -m unittest discover -s tests -v
python tools/test_r10_gui.py
```

25 tests automatisés de calcul et de régression passent. Import de l'application et compilation des modules vérifiés. Un rapport sur données **synthétiques de test** a été généré et ses pages inspectées ; il n'est pas livré comme étude d'un site réel.

Le second test nécessite un affichage Tkinter. Il couvre démarrage, onglets, déplacement groupé, sauvegarde/rechargement des hauteurs, cotations et paramètres BESS, et ouverture de la configuration. Il est fourni mais **n'a pas pu être exécuté ici**, faute d'affichage graphique. Une recette Windows reste nécessaire avant utilisation opérationnelle.

Voir `AUDIT_TECHNIQUE_FR.md` pour les limites et les prochaines priorités.
