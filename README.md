# 🧠 Modèle de Projet Data Science
## un template ready-to-go

Ce dépôt propose une **structure type pour vos projets Data Science**, inspirée des meilleures pratiques ().
L’objectif est simple : passer du notebook désordonné à un projet clair, modulaire et reproductible.

---

## 🚀 Structure du projet

```
ds_project_template/
│
├── components/          # Modules de traitement : ingestion, transformation, entraînement, etc.
├── pipeline/            # Scripts d’entraînement et de prédiction
├── utils/               # Fonctions utilitaires (lecture YAML, JSON, sauvegarde de modèles)
├── logger.py            # Configuration du système de logs
├── exception.py         # Gestion centralisée des erreurs
│
├── config/config.yaml   # Fichier de configuration global
├── data/raw/            # Données brutes
├── models/              # Modèles entraînés
├── logs/                # Journaux d’exécution
├── notebooks/           # Notebooks Jupyter
│
├── app.py               # Point d’entrée optionnel (API Flask/FastAPI)
├── requirements.txt     # Dépendances Python
├── setup.py             # Script d’installation du package
├── Dockerfile           # Configuration pour Docker
└── README.md            # Vous êtes ici !
```

---

## 🔧 Comment utiliser ce template

### Option 1. Cloner directement le projet

Si vous souhaitez simplement utiliser cette structure comme base pour un nouveau projet :

```bash
# 1. Cloner le dépôt
git clone https://github.com/Souley225/DS_project_Template.git

# 2. Renommer le dossier
mv DS_project_Template mon_projet_data
cd mon_projet_data

# 3. (Optionnel) Réinitialiser l’historique Git
rm -rf .git
git init
git add .
git commit -m "Démarrage de mon projet Data Science"
```

Vous pouvez ensuite remplir les fichiers `data_ingestion.py`, `model_trainer.py`, etc., selon vos besoins.

---

### Option 2. Utiliser Cookiecutter (recommandé)

Si vous voulez transformer ce dépôt en **générateur de projets personnalisés**, utilisez [**Cookiecutter**](https://cookiecutter.readthedocs.io).

#### Étape 1 : Installer Cookiecutter

```bash
pip install cookiecutter
```

#### Étape 2 : Générer un nouveau projet

```bash
cookiecutter https://github.com/Souley225/DS_project_Template.git
```

#### Étape 3 : Répondre aux questions

Cookiecutter vous demandera :

* le nom de votre projet
* votre nom ou celui de votre équipe
* une courte description
* la licence souhaitée

Il générera alors un **nouveau dossier complet**, avec cette structure adaptée à votre projet.

---

## 💡 Pourquoi utiliser ce template ?

Ce modèle est conçu pour :

* Structurer vos projets de façon claire et maintenable
* Séparer **la configuration** (fichiers YAML) du **code métier**
* Favoriser la reproductibilité et la collaboration
* Préparer le terrain pour une mise en production (CI/CD, API, Docker, etc.)

---

## 📦 Installation rapide

1. Clonez ou générez le projet (voir ci-dessus)
2. Créez un environnement virtuel :

   ```bash
   python -m venv venv
   source venv/bin/activate    # Mac/Linux
   venv\Scripts\activate       # Windows
   ```
3. Installez les dépendances :

   ```bash
   pip install -r requirements.txt
   ```

---

## 🧹 Personnalisation possible

* Ajouter un pipeline CI/CD (GitHub Actions, DVC, MLflow)
* Intégrer une API de prédiction avec FastAPI ou Flask
* Suivre les expériences avec MLflow ou Weights & Biases
* Déployer dans Docker ou sur le cloud (GCP, AWS, Azure)
* Transformer le projet en package Python via `setup.py`

---

## 👨‍💻 Auteur

**Souleymane Sall**
Master en Économétrie et Statistique Appliquée
Passionné par la modélisation, la reproductibilité et l’industrialisation des modèles de Machine Learning.

---

## 📜 Licence

Ce projet est distribué sous licence **MIT**.
Vous êtes libre de l’utiliser, le modifier et le partager.

---

## ⭐ Remerciements

Inspiré par :
* [Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/)

