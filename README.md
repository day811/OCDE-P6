# Prédiction de la Consommation Énergétique des Bâtiments - Seattle

## Description du Projet

Ce projet vise à développer un modèle de Machine Learning capable de prédire la consommation énergétique des bâtiments non résidentiels de la ville de Seattle. L'objectif est de contribuer à l'initiative de la ville pour atteindre la neutralité carbone d'ici 2050 en permettant d'estimer la consommation énergétique de bâtiments pour lesquels elle n'a pas encore été mesurée.

Le projet se compose de deux parties principales :
1. **Analyse exploratoire et modélisation** : Développement d'un modèle de régression supervisée basé sur les données structurelles des bâtiments.
2. **Déploiement via API** : Exposition du modèle entraîné via une API REST construite avec BentoML et déployée sur Google Cloud Platform.

## Architecture du Projet

```
.
├── ocde_p6/
│   ├── api/
│   │   ├── __init__.py
│   │   └── service.py              # Service BentoML pour l'API
│   ├── model/
│   │   ├── __init__.py
│   │   └── model_loader.py         # Chargement du modèle
│   ├── preprocessing/
│   │   ├── __init__.py
│   │   └── transformer.py          # Transformations des données
│   ├── validation/
│   │   ├── __init__.py
│   │   └── schemas.py              # Schémas Pydantic de validation
│   └── utils/
│       ├── __init__.py
│       ├── config.py               # Configuration de l'application
│       ├── enums.py                # Énumérations pour les types de propriétés
│       ├── exceptions.py           # Exceptions personnalisées
│       └── logger.py               # Configuration du logging
├── bash/
│   ├── launchDocker.sh             # Lancement du conteneur Docker en local
│   ├── updateToGCP.sh              # Construction et déploiement sur GCP
│   ├── launchGCP.sh                # Déploiement direct sur GCP
│   ├── test_GCP.sh                 # Test de l'API déployée sur GCP
│   ├── launch_request.sh           # Test de l'API en local
│   └── stop_GCP.sh                 # Arrêt du service sur GCP
├── data/
│   └── 2016_Building_Energy_Benchmarking.csv
├── bentofile.yaml                  # Configuration BentoML
├── pyproject.toml                  # Dépendances Python (Poetry)
├── modelistation_supervisee_EDA.pdf    # Notebook d'analyse exploratoire
├── modelistation_model1.pdf            # Notebook de modélisation
└── README.md
```

## Méthodologie

### 1. Analyse Exploratoire des Données (EDA)

L'analyse exploratoire a été réalisée sur le dataset de 3 376 bâtiments de Seattle contenant 46 variables initiales. Les étapes principales incluent :

- **Nettoyage des données** : Suppression des outliers déclarés (32 bâtiments), filtrage des propriétés résidentielles non pertinentes, traitement des valeurs manquantes.
- **Sélection des variables** : Après analyse, 1 630 bâtiments non résidentiels ont été retenus avec des variables pertinentes pour la prédiction.
- **Ingénierie des features** :
  - Création de variables binaires pour les types d'énergie utilisés (`UseGas`, `UseSteam`, `UseElectricity`)
  - Calcul de la distance au centre-ville de Seattle (`CityDistance`) via la formule de Haversine
  - Calcul du nombre d'usages multiples (`MultipleUseType`)
  - Agrégation des surfaces (`SumLargestGFA`)
  - Création de variables dérivées : âge du bâtiment (`AgeProperty`), catégories d'âge (`AgeCategory`), ère énergétique (`EnergyEra`), catégories de hauteur (`HeightCategory`)
- **Target retenue** : `SiteEnergyUsekBtu` (consommation énergétique totale en kBtu) transformée en échelle logarithmique (`log1p`) pour normaliser la distribution.

### 2. Modélisation

Cinq algorithmes de régression supervisée ont été comparés via validation croisée 5-fold :

| Modèle | R² | RMSE (kBtu) | MAE (kBtu) | MAPE |
|--------|-----|-------------|------------|------|
| **RandomForest** | 0.3321 | 26,113,285 | 4,422,384 | 59.61% |
| **GradientBoosting** | 0.3156 | 26,433,910 | 4,257,251 | 56.57% |
| SVR | 0.1251 | 29,889,086 | 5,928,491 | 93.80% |
| DummyRegressor | -0.0311 | 32,447,395 | 7,452,060 | 147.00% |
| LinearRegression | -7.7848 | 94,708,167 | 6,001,406 | 56.23% |

**Optimisation** : Le modèle GradientBoosting a été optimisé via GridSearchCV sur 36 combinaisons d'hyperparamètres :
- Meilleurs hyperparamètres : `learning_rate=0.05`, `max_depth=3`, `n_estimators=200`, `subsample=0.8`
- **Performance finale sur le jeu de test** : R²=0.87, RMSE=8,708,608 kBtu, MAE=3,180,539 kBtu, MAPE=45.56%

**Features les plus importantes** :
1. `SumLargestGFA` (surface agrégée en log) : 66.74%
2. `building_volume` : 6.87%
3. Type de propriété principal (Supermarché, Entrepôt, Centre de distribution)
4. Usage du gaz naturel (`UseGas`)
5. Distance au centre-ville

## Installation et Prérequis

### Prérequis

- **Python** : >= 3.13
- **Poetry** : Gestionnaire de dépendances Python
- **Docker** : Pour la containerisation
- **Google Cloud SDK** : Pour le déploiement sur GCP (optionnel)
- **BentoML** : >= 1.4.26

### Installation depuis un dépôt Git

#### 1. Cloner le dépôt

```bash
git clone <url-du-depot>
cd <nom-du-projet>
```

#### 2. Créer et activer l'environnement virtuel avec Poetry

```bash
# Installer Poetry si ce n'est pas déjà fait
curl -sSL https://install.python-poetry.org | python3 -

# Installer les dépendances
poetry install

# Activer l'environnement virtuel
poetry shell
```

#### 3. Vérifier l'installation

```bash
# Vérifier que BentoML est installé
bentoml --version

# Vérifier que le modèle est disponible
bentoml models list
```

Si le modèle n'est pas présent, vous devrez l'entraîner en exécutant le notebook de modélisation ou charger un modèle pré-entraîné.

#### 4. Charger le modèle BentoML (si nécessaire)

Si vous disposez d'un modèle pré-entraîné sauvegardé :

```bash
bentoml models import <chemin-vers-le-modele.bentomodel>
```

## Utilisation Locale

### 1. Lancer le service BentoML en développement

```bash
bentoml serve ocde_p6.api.service:BuildingEnergyService --reload
```

Le service sera accessible à l'adresse : `http://localhost:3000`

### 2. Tester l'API localement

#### Via curl

```bash
bash bash/launch_request.sh
```

Ou manuellement :

```bash
curl -X POST http://127.0.0.1:3000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "input_data": {
      "first_use_type": "Hotel",
      "second_largest_property_use_type": "None",
      "multiple_use_type": 1,
      "sum_largest_GFA": 88434.0,
      "use_steam": true,
      "use_gas": false,
      "number_of_floors": 12.0,
      "number_of_buildings": 1.0,
      "city_distance": 8.5,
      "neighborhood": "DOWNTOWN",
      "year_built": 1999
    }
  }'
```

#### Via l'interface Swagger

Accédez à `http://localhost:3000` dans votre navigateur pour utiliser l'interface interactive Swagger UI.

### 3. Vérifier la santé du service

```bash
curl http://localhost:3000/health
```

## Déploiement avec Docker et Google Cloud Platform

### Étape 1 : Construction de l'image Docker avec BentoML

BentoML simplifie la création d'images Docker grâce au fichier `bentofile.yaml` qui définit la configuration du service.

#### 1.1. Vérifier le fichier bentofile.yaml

Le fichier `bentofile.yaml` contient :

```yaml
service: "ocde_p6.api.service:BuildingEnergyService"
name: "building_energy_prediction"
description: "API for predicting building energy consumption in Seattle"

models:
  - "building_energy_rf_pipeline:latest"

include:
  - "ocde_p6/"
  - "*.py"

python:
  packages:
    - "pandas>=1.5.0"
    - "scikit-learn>=1.3.0"
    - "pydantic>=1.10.0"
    - "numpy>=1.24.0"

docker:
  base_image: "python:3.11-slim"
  system_packages:
    - git
  env:
    - LOG_LEVEL=INFO
```

#### 1.2. Construire le Bento

```bash
bentoml build
```

Cette commande crée un "Bento" (artefact déployable) qui encapsule le service, le modèle et toutes les dépendances.

#### 1.3. Créer l'image Docker

```bash
bentoml containerize building_energy_prediction:latest -t building_energy_prediction:latest
```

Cette commande génère une image Docker nommée `building_energy_prediction:latest`.

#### 1.4. Tester l'image Docker localement

```bash
bash bash/launchDocker.sh
```

Ou manuellement :

```bash
docker run -it --rm -p 3000:3000 building_energy_prediction:latest
```

### Étape 2 : Configuration de Google Cloud Platform

#### 2.1. Créer un projet GCP

```bash
# Se connecter à GCP
gcloud auth login

# Créer un nouveau projet (remplacer PROJECT_ID par votre ID)
gcloud projects create PROJECT_ID

# Définir le projet actif
gcloud config set project PROJECT_ID
```

#### 2.2. Activer les APIs nécessaires

```bash
# Activer l'API Cloud Run
gcloud services enable run.googleapis.com

# Activer l'API Artifact Registry
gcloud services enable artifactregistry.googleapis.com
```

#### 2.3. Créer un dépôt Artifact Registry

```bash
gcloud artifacts repositories create bentoml-repo \
  --repository-format=docker \
  --location=europe-west1 \
  --description="Docker repository for BentoML models"
```

#### 2.4. Configurer l'authentification Docker

```bash
gcloud auth configure-docker europe-west1-docker.pkg.dev
```

### Étape 3 : Déploiement sur Google Cloud Run

#### 3.1. Configurer les variables d'environnement

Éditez le fichier `bash/updateToGCP.sh` et vérifiez les variables :

```bash
PROJECT_ID="votre-project-id"
REGION="europe-west1"
REPOSITORY="bentoml-repo"
IMAGE_NAME="building-energy-prediction"
SERVICE_NAME="building-energy-prediction"
```

#### 3.2. Pousser l'image vers Artifact Registry et déployer

```bash
bash bash/updateToGCP.sh
```

Ce script effectue les opérations suivantes :
1. **Tag de l'image Docker** : Associe l'image locale à l'URL du registre GCP
   ```bash
   docker tag building_energy_prediction:latest \
       europe-west1-docker.pkg.dev/PROJECT_ID/bentoml-repo/building-energy-prediction:latest
   ```

2. **Push de l'image** : Téléverse l'image vers Artifact Registry
   ```bash
   docker push europe-west1-docker.pkg.dev/PROJECT_ID/bentoml-repo/building-energy-prediction:latest
   ```

3. **Déploiement sur Cloud Run** : Crée ou met à jour le service
   ```bash
   gcloud run deploy building-energy-prediction \
       --image europe-west1-docker.pkg.dev/PROJECT_ID/bentoml-repo/building-energy-prediction:latest \
       --region europe-west1 \
       --platform managed \
       --port 3000 \
       --allow-unauthenticated \
       --memory 2Gi \
       --cpu 2 \
       --timeout 300 \
       --max-instances 10
   ```

#### 3.3. Récupérer l'URL du service

Après le déploiement, l'URL du service sera affichée. Vous pouvez également la récupérer avec :

```bash
gcloud run services describe building-energy-prediction \
    --region europe-west1 \
    --format 'value(status.url)'
```

### Étape 4 : Tester l'API déployée sur GCP

```bash
bash bash/test_GCP.sh
```

Ou manuellement (remplacer l'URL par celle de votre service) :

```bash
curl -X POST https://building-energy-prediction-XXX.europe-west1.run.app/predict \
  -H "Content-Type: application/json" \
  -d '{
    "input_data": {
      "first_use_type": "Hotel",
      "second_largest_property_use_type": null,
      "multiple_use_type": 1,
      "sum_largest_GFA": 88434.0,
      "use_steam": true,
      "use_electricity": true,
      "use_gas": false,
      "number_of_floors": 12.0,
      "number_of_buildings": 1.0,
      "city_distance": 8.5,
      "neighborhood": "DOWNTOWN",
      "year_built": 1999
    }
  }'
```

### Étape 5 : Gestion du service déployé

#### Arrêter le service

```bash
bash bash/stop_GCP.sh
```

Ou manuellement :

```bash
gcloud run services delete building-energy-prediction --region europe-west1
```

#### Mettre à jour le service

Pour déployer une nouvelle version après modification du code :

```bash
# 1. Reconstruire le Bento
bentoml build

# 2. Recréer l'image Docker
bentoml containerize building_energy_prediction:latest -t building_energy_prediction:latest

# 3. Déployer sur GCP
bash bash/updateToGCP.sh
```

#### Consulter les logs

```bash
gcloud run services logs read building-energy-prediction --region europe-west1
```

## Schéma de Validation des Données

L'API utilise **Pydantic** pour valider les données d'entrée. Voici les champs requis :

| Champ | Type | Description | Contraintes |
|-------|------|-------------|-------------|
| `first_use_type` | Enum | Type d'usage principal | Valeurs définies dans `FirstUseTypeEnum` |
| `second_largest_property_use_type` | Enum (optional) | Type d'usage secondaire | Valeurs définies dans `SecondUseTypeEnum` |
| `multiple_use_type` | int | Nombre d'usages différents | Entre 1 et 10 |
| `sum_largest_GFA` | float | Surface totale (pieds carrés) | ≥ 0 |
| `use_steam` | bool | Utilisation de vapeur | true/false |
| `use_gas` | bool | Utilisation de gaz naturel | true/false |
| `number_of_floors` | float | Nombre d'étages | Entre 1 et 100 |
| `number_of_buildings` | float | Nombre de bâtiments | ≥ 1 |
| `city_distance` | float | Distance au centre-ville (miles) | Entre 0 et 20 |
| `neighborhood` | str | Quartier de Seattle | Texte libre |
| `year_built` | int | Année de construction | Entre 1900 et 2025 |

### Valeurs autorisées pour `first_use_type`

- Data Center
- Distribution Center
- Hospital
- K-12 School
- Laboratory
- Large Office
- Manufacturing/Industrial Plant
- Other
- Parking
- Restaurant
- Self-Storage Facility
- Supermarket / Grocery Store
- University
- Warehouse
- Worship Facility
- Value not listed

### Valeurs autorisées pour `second_largest_property_use_type`

- Data Center
- Laboratory
- Office
- Parking
- Restaurant
- Value not listed
- None

## Format de Réponse de l'API

### Succès

```json
{
  "prediction": 8110619.91,
  "input_data": {
    "first_use_type": "Hotel",
    "second_largest_property_use_type": "None",
    "multiple_use_type": 1,
    "sum_largest_GFA": 88434.0,
    "use_steam": true,
    "use_gas": false,
    "number_of_floors": 12.0,
    "number_of_buildings": 1.0,
    "city_distance": 8.5,
    "neighborhood": "DOWNTOWN",
    "year_built": 1999
  },
  "status": "success"
}
```

### Erreur de validation

```json
{
  "error": "Input validation failed: ...",
  "status": "validation_error"
}
```

### Erreur du modèle

```json
{
  "error": "Model error: ...",
  "status": "model_error"
}
```

## Structure du Pipeline de Transformation

Le pipeline de preprocessing applique les transformations suivantes dans l'ordre :

1. **Preprocessing personnalisé** (`fix_floors_and_discretize`) :
   - Correction des valeurs de `NumberofFloors` (minimum 1)
   - Création de variables dérivées : `log_GFA`, `GFA_per_floor`, `building_volume`
   - Discrétisation de la surface : `PropertySize` (Small, Mid, Large, XLarge)
   - Calcul de l'âge : `AgeProperty` et `AgeCategory` (New, Recent, Old)
   - Création de `EnergyEra` (Pre-Crisis si construit avant 1973, sinon Modern)
   - Création de `HeightCategory` (Low, Mid, High)

2. **Encodage et normalisation** :
   - OneHotEncoding pour les variables catégorielles
   - StandardScaler pour les variables numériques

3. **Prédiction** :
   - Application du modèle GradientBoosting optimisé
   - Transformation inverse (`expm1`) pour retourner la prédiction en kBtu

## Dépendances Principales

Voir `pyproject.toml` pour la liste complète. Principales dépendances :

- `pandas` >= 0.3.1
- `scikit-learn` >= 1.7.2
- `bentoml` >= 1.4.26
- `pydantic` >= 1.10.0
- `numpy` >= 1.24.0

## Auteur

**day811**

## Licence

Ce projet a été réalisé dans le cadre d'une formation OpenClassrooms de Data Engineer.

## Notes Importantes

- **Arrêt du service GCP** : Pensez à arrêter le service Cloud Run après vos tests pour éviter des frais inutiles.
- **Sécurité** : Dans un environnement de production, configurez l'authentification et les autorisations appropriées.
- **Monitoring** : Utilisez Google Cloud Monitoring pour surveiller les performances et les erreurs en production.
- **Scaling** : Le paramètre `--max-instances` dans le script de déploiement contrôle l'autoscaling du service.
