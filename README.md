# 🎯 Template de Projet Data Science

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python&logoColor=ffdd54)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Cookiecutter](https://img.shields.io/badge/Cookiecutter-Ready-orange?style=for-the-badge&logo=cookiecutter)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker)

</div>

> **Un template production-ready pour démarrer vos projets Data Science avec une structure claire, modulaire et reproductible.**

---

## 🚀 Pourquoi ce template ?

Ce dépôt propose une **architecture éprouvée** pour vos projets Data Science, inspirée des meilleures pratiques de l'industrie.

### ✨ Objectifs

| 🎯 Objectif | 📝 Description |
|------------|---------------|
| **Structure claire** | Organisation logique et intuitive du code |
| **Reproductibilité** | Configuration centralisée et versionnée |
| **Maintenabilité** | Code modulaire et testable |
| **Production-ready** | Prêt pour le déploiement (Docker, API, CI/CD) |

---

## 📂 Structure du projet

```
ds_project_template/
│
├── 📦 components/           # Modules de traitement métier
│   ├── data_ingestion.py    # Chargement des données
│   ├── data_transformation.py # Prétraitement et feature engineering
│   ├── model_trainer.py      # Entraînement des modèles
│   └── model_evaluation.py   # Évaluation et métriques
│
├── 🔄 pipeline/             # Orchestration du workflow
│   ├── training_pipeline.py  # Pipeline d'entraînement
│   └── prediction_pipeline.py # Pipeline d'inférence
│
├── 🛠️ utils/                # Fonctions utilitaires
│   ├── common.py             # Fonctions génériques
│   └── config_reader.py      # Lecture de configuration
│
├── 📋 logger.py             # Système de logs centralisé
├── ⚠️ exception.py          # Gestion des erreurs
│
├── ⚙️ config/
│   └── config.yaml           # Configuration globale du projet
│
├── 📊 data/
│   ├── raw/                  # Données brutes
│   ├── processed/            # Données transformées
│   └── external/             # Données externes
│
├── 🤖 models/               # Modèles entraînés et artefacts
├── 📝 logs/                 # Journaux d'exécution
├── 📓 notebooks/            # Notebooks d'exploration
│
├── 🚀 app.py                # Point d'entrée API (Flask/FastAPI)
├── 📦 requirements.txt      # Dépendances Python
├── 🔧 setup.py              # Configuration du package
├── 🐳 Dockerfile            # Containerisation
└── 📖 README.md             # Documentation
```

---

## 🛠️ Installation et utilisation

### Option 1️⃣ : Clonage direct

?> **Idéal pour** : Démarrer rapidement un nouveau projet

```bash
# Cloner le dépôt
git clone https://github.com/Souley225/DS_project_Template.git

# Renommer selon votre projet
mv DS_project_Template mon_projet_data
cd mon_projet_data

# Réinitialiser l'historique Git (optionnel)
rm -rf .git
git init
git add .
git commit -m "🎉 Initialisation du projet Data Science"
```

### Option 2️⃣ : Avec Cookiecutter (recommandé)

!> **Recommandé pour** : Générer des projets personnalisés avec vos propres paramètres

#### Étape 1 : Installer Cookiecutter

```bash
pip install cookiecutter
```

#### Étape 2 : Générer le projet

```bash
cookiecutter https://github.com/Souley225/DS_project_Template.git
```

#### Étape 3 : Configuration interactive

Cookiecutter vous demandera :

| Question | Description | Exemple |
|----------|-------------|---------|
| `project_name` | Nom de votre projet | Customer Churn Prediction |
| `author_name` | Votre nom | Souleymane Sall |
| `description` | Description courte | Prédiction du churn client avec ML |
| `license` | Type de licence | MIT |

---

## 🚀 Démarrage rapide

### 1. Créer l'environnement virtuel

```bash
# Création de l'environnement
python -m venv venv

# Activation
source venv/bin/activate    # Mac/Linux
venv\Scripts\activate       # Windows
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Configuration

Modifiez le fichier `config/config.yaml` selon vos besoins :

```yaml
data:
  raw_path: data/raw/
  processed_path: data/processed/
  
model:
  type: RandomForest
  params:
    n_estimators: 100
    max_depth: 10
    
training:
  test_size: 0.2
  random_state: 42
```

### 4. Lancer le pipeline

```bash
python pipeline/training_pipeline.py
```

---

## 🎨 Fonctionnalités clés

### 📋 Logging centralisé

```python
from logger import logging

logging.info("Démarrage du traitement des données")
logging.warning("Valeurs manquantes détectées")
logging.error("Erreur lors du chargement du modèle")
```

### ⚠️ Gestion des erreurs

```python
from exception import CustomException
import sys

try:
    # Votre code
    pass
except Exception as e:
    raise CustomException(e, sys)
```

### ⚙️ Configuration centralisée

```python
from utils.config_reader import read_config

config = read_config("config/config.yaml")
model_params = config['model']['params']
```

---

## 🔧 Personnalisation avancée

### 🔄 Intégration CI/CD

Ajoutez un workflow GitHub Actions dans `.github/workflows/`:

```yaml
name: CI/CD Pipeline
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: pytest tests/
```

### 📈 Suivi des expériences

Intégrez **MLflow** pour tracker vos expériences :

```python
import mlflow

with mlflow.start_run():
    mlflow.log_params(model_params)
    mlflow.log_metrics({"accuracy": 0.95})
    mlflow.sklearn.log_model(model, "model")
```

### 🐳 Déploiement Docker

```bash
# Construire l'image
docker build -t mon-projet-ds .

# Lancer le conteneur
docker run -p 8000:8000 mon-projet-ds
```

### 🚀 API de prédiction

Créez une API avec **FastAPI** dans `app.py` :

```python
from fastapi import FastAPI
from pipeline.prediction_pipeline import predict

app = FastAPI()

@app.post("/predict")
def make_prediction(data: dict):
    return predict(data)
```

---

## 🎯 Cas d'usage

Ce template est parfait pour :

- ✅ **Classification** : Churn prediction, fraud detection, sentiment analysis
- ✅ **Régression** : Price prediction, demand forecasting, time series
- ✅ **Clustering** : Customer segmentation, anomaly detection
- ✅ **NLP** : Text classification, entity recognition
- ✅ **Computer Vision** : Image classification, object detection

---

## 📚 Ressources complémentaires

| Ressource | Description |
|-----------|-------------|
| 🔗 [Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/) | Template original et best practices |
| 🔗 [MLflow Documentation](https://mlflow.org/docs/latest/index.html) | Suivi d'expériences ML |
| 🔗 [FastAPI](https://fastapi.tiangolo.com/) | Framework API moderne |
| 🔗 [Docker Tutorial](https://docs.docker.com/get-started/) | Containerisation |

---

## 🧪 Tests

```bash
# Installation des dépendances de test
pip install pytest pytest-cov

# Lancer les tests
pytest tests/ -v

# Avec coverage
pytest tests/ --cov=components --cov-report=html
```

---

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. 🍴 Fork le projet
2. 🌿 Créez une branche (`git checkout -b feature/AmazingFeature`)
3. 💾 Commit vos changements (`git commit -m 'Add AmazingFeature'`)
4. 📤 Push vers la branche (`git push origin feature/AmazingFeature`)
5. 🔃 Ouvrez une Pull Request

---

## 👨‍💻 Auteur

**Souleymane Sall**

- 🎓 Master en Économétrie et Statistique Appliquée
- 💼 Data Scientist & MLOps Engineer
- 💡 Passionné par la reproductibilité et l'industrialisation des modèles ML

<div align="center">

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/souleymanes-sall)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Souley225)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:sallsouleymane2207@gmail.com)

</div>

---

## 📜 Licence

Ce projet est distribué sous licence **MIT**.  
Vous êtes libre de l'utiliser, le modifier et le partager.

---

## 🌟 Remerciements

Inspiré par les meilleures pratiques de la communauté Data Science :

- [Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/)
- [MLOps Best Practices](https://ml-ops.org/)
- Retours d'expérience de projets en production

---

<div align="center">

### ⭐ Si ce template vous est utile, n'hésitez pas à lui donner une étoile !

<sub>Construit avec ❤️ pour la communauté Data Science</sub>

</div>
