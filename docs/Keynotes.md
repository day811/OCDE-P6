# Plan d'Action pour la Mission Partie 1 : Prédiction de la Consommation Énergétique des Bâtiments

## Méthodologie CRISP-DM Appliquée

Ce plan d'action suit rigoureusement la méthodologie CRISP-DM (Cross-Industry Standard Process for Data Mining) adaptée au contexte spécifique de la prédiction de consommation énergétique des bâtiments de Seattle.[scielo+2](http://www.scielo.org.mx/scielo.php?script=sci_arttext&pid=S1405-55462023000300675)

## Phase 1 : Compréhension du Métier (Business Understanding)

**Objectifs identifiés :**

- Prédire les émissions de CO2 et la consommation totale d'énergie des bâtiments non résidentiels de SeattleMissionPartie1.txt
- Contribuer à l'objectif de neutralité carbone de Seattle d'ici 2050MissionPartie1.txt
- Optimiser les coûts de collecte de données en utilisant les données structurelles existantesMissionPartie1.txt

**Critères de succès :**

- Modèle capable de prédire avec précision la consommation énergétique à partir des caractéristiques structurelles
- Identification des facteurs principaux impactant la consommation énergétiqueMissionPartie1.txt
- Insights exploitables pour les politiques énergétiques urbaines

**Contraintes identifiées :**

- Données limitées aux relevés de 2016MissionPartie1.txt
- Restriction aux bâtiments non résidentiels uniquementMissionPartie1.txt
- Impossibilité d'utiliser les données de consommation énergétique directe (risque de data leakage)MissionPartie1.txt

## Phase 2 : Compréhension des Données (Data Understanding)

**Analyse du dataset disponible :**

Le fichier CSV échantillon révèle 44 variables structurées comprenant :2016_Building_Energy_Benchmarking_sample.csv

**Variables identifiées par catégories :**

- **Identification** : OSEBuildingID, PropertyName, Address
- **Géolocalisation** : Latitude, Longitude, Neighborhood, CouncilDistrictCode
- **Caractéristiques physiques** : YearBuilt, NumberofFloors, PropertyGFATotal, PropertyGFABuilding(s)
- **Usage** : PrimaryPropertyType, ListOfAllPropertyUseTypes, LargestPropertyUseType
- **Performance énergétique** : ENERGYSTARScore, SiteEUI, SourceEUI
- **Consommation** : SiteEnergyUse, Electricity, NaturalGas, SteamUse
- **Émissions** : TotalGHGEmissions, GHGEmissionsIntensity (variables cibles potentielles)

**Actions prévues :**

1. **Collecte des données complètes** depuis la source officielle de Seattle[data.seattle](https://data.seattle.gov/Built-Environment/Benchmarking-Performance-Ranges-by-Building-Type-2/sfav-5thy)
2. **Documentation exhaustive** des variables et de leur signification métier
3. **Analyse de qualité** : valeurs manquantes, outliers, cohérence
4. **Exploration des distributions** et corrélations préliminaires

## Phase 3 : Préparation des Données (Data Preparation)

**Étapes de nettoyage planifiées :**

1. **Filtrage des bâtiments pertinents** selon les critères métierMissionPartie1.txt
2. **Gestion des valeurs manquantes** avec stratégies adaptées par variable
3. **Détection et traitement des outliers** via méthodes IQR ou quantilesMissionPartie1.txt
4. **Validation de cohérence** entre variables liées

**Feature Engineering prévu :**

1. **Features temporelles** : âge du bâtiment, décennie de construction
2. **Features géographiques** : clustering par quartier, distance au centre-ville
3. **Features d'usage** : indicateurs binaires multi-usage, ratios de surfaceMissionPartie1.txt
4. **Features de structure** : ratio surface parking/totale, densité par étage
5. **Features énergétiques structurelles** : présence de différentes sources d'énergie (sans les valeurs de consommation)MissionPartie1.txt

**Préparation pour la modélisation :**

- Encodage des variables catégorielles (OneHotEncoder pour faible cardinalité, techniques de regroupement pour haute cardinalité)MissionPartie1.txt
- Normalisation/standardisation des variables numériques
- Division train/test stratifiée
- Validation croisée k-fold

## Phase 4 : Modélisation (Modeling)

**Stratégie de modélisation :**

1. **Sélection des variables cibles** : TotalGHGEmissions ou SiteEnergyUseMissionPartie1.txt
2. **Modèles de référence** : régression linéaire simple
3. **Modèles avancés** : Random Forest, Gradient Boosting, XGBoost[arxiv](https://arxiv.org/html/2309.02908v2)MissionPartie1.txt
4. **Approche progressive** : commencer simple, puis complexifier

**Méthodologie d'évaluation :**

- **Métriques** : R², MAE, RMSE pour comparaison objective[arxiv](https://arxiv.org/html/2309.02908v2)MissionPartie1.txt
- **Validation croisée** avec cross_validate de scikit-learnMissionPartie1.txt
- **Reproductibilité** via fixation des random_stateMissionPartie1.txt
- **Fonction standardisée** pour évaluer tous les modèles de façon cohérenteMissionPartie1.txt

**Optimisation planifiée :**

- GridSearchCV avec grilles restreintes (max 500 combinaisons)MissionPartie1.txt
- Tests préliminaires sur petites grilles pour validation du codeMissionPartie1.txt
- Parallélisation via Google Colab si nécessaireMissionPartie1.txt

## Phase 5 : Évaluation (Evaluation)

**Critères d'évaluation :**

1. **Performance quantitative** : métriques de régression standardisées
2. **Stabilité** : consistance via validation croisée
3. **Interprétabilité** : analyse des features importantesMissionPartie1.txt
4. **Robustesse** : performance sur données de test non vues

**Analyse des résultats :**

- **Comparaison objective** des modèles via tableau de métriquesMissionPartie1.txt
- **Feature importance** pour identifier les facteurs clésMissionPartie1.txt
- **Analyse des erreurs** pour comprendre les limites du modèle
- **Validation métier** des prédictions et insights

## Phase 6 : Déploiement (Deployment)

**Livrables finaux :**

1. **Notebook Jupyter** complet avec code documenté en anglaisMissionPartie1.txt
2. **Présentation PowerPoint** professionnelle incluant :MissionPartie1.txt
    - Contexte et objectifs du projet
    - Synthèse de l'analyse exploratoire
    - Démarche de modélisation et résultats
    - Facteurs clés impactant la consommation énergétique
    - Recommandations pour la politique énergétique

**Format de présentation :**

- Storytelling orienté métierMissionPartie1.txt
- Graphiques clairs avec axes et légendes appropriésMissionPartie1.txt
- Métriques traduites en impact businessMissionPartie1.txt
- Synthèse des insights exploitables

## Planification Temporelle

**Répartition recommandée :**

- **Phase 1-2** (Compréhension) : 15-20% du temps
- **Phase 3** (Préparation) : 40-50% du temps
- **Phase 4-5** (Modélisation-Évaluation) : 25-35% du temps
- **Phase 6** (Communication) : 10-15% du temps

**Points de vigilance critiques :**

- Éviter le data leakage en excluant les variables de consommation directeMissionPartie1.txt
- Conserver suffisamment de données après nettoyage pour l'entraînementMissionPartie1.txt
- Limiter le temps sur le feature engineering pour éviter la sur-optimisationMissionPartie1.txt
- Tester les gridsearch sur petits échantillons avant lancement completMissionPartie1.txt

Cette approche méthodologique garantit une démarche scientifique rigoureuse tout en respectant les contraintes temporelles et techniques du projet professionnel.

1. http://www.scielo.org.mx/scielo.php?script=sci_arttext&pid=S1405-55462023000300675
2. https://www.le1817.com/blog/la-methodologie-crisp-dm
3. https://www.datascience-pm.com/crisp-dm-2/
4. https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_0a73812e-2987-4226-9dd2-ad1b034a7015/393f4659-f2c9-47ae-8ab2-77ba7abcc1e0/MissionPartie1.txt
5. https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_0a73812e-2987-4226-9dd2-ad1b034a7015/e38e0f50-ab32-42f5-9b5d-a542532efaa4/2016_Building_Energy_Benchmarking_sample.csv
6. https://data.seattle.gov/Built-Environment/Benchmarking-Performance-Ranges-by-Building-Type-2/sfav-5thy
7. https://arxiv.org/html/2309.02908v2
8. https://catalog.data.gov/dataset/benchmarking-performance-ranges-by-building-type-2015-present/resource/e1e204f6-5a5d-4bc8-97d2-4588df638660
9. https://skill-lync.com/student-projects/independent-research-project-20
10. https://www.nature.com/articles/s41598-025-88603-2
11. https://www.sciencedirect.com/science/article/pii/S2352484722020601
12. https://www.kaggle.com/code/michaelfumery/seattle-building-energy-cleaning
13. https://en.wikipedia.org/wiki/Cross-industry_standard_process_for_data_mining
14. https://www.sciencedirect.com/science/article/pii/S235271022101264X
15. https://www.kaggle.com/datasets/city-of-seattle/seattle-performance-ranges-by-building-type-2016
16. https://towardsdatascience.com/how-i-created-a-data-science-project-following-a-crisp-dm-lifecycle-8c0f5f89bba1/
17. https://cs109-energy.github.io/building-energy-consumption-prediction.html
18. https://data.seattle.gov/Built-Environment/Building-Energy-Benchmarking-Data-2015-Present/teqw-tu6e
19. https://www.ibm.com/docs/fr/spss-modeler/saas?topic=dm-crisp-help-overview
20. https://www.sciencedirect.com/science/article/pii/S0378778825006747
21. https://www.datascience-pm.com/wp-content/uploads/2024/12/CRISP-DM-for-Data-Science-2025.pdf
22. https://www.sciencedirect.com/science/article/pii/S2666165924002114