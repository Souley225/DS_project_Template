# Dockerfile pour le projet Data Science
# Permet de containeriser l'application pour un déploiement facile

# Image de base Python
FROM python:3.10-slim

# Mainteneur du projet
LABEL maintainer="Souleymane Sall <votre.email@exemple.com>"
LABEL description="Template de projet Data Science containerisé"

# Définition du répertoire de travail
WORKDIR /app

# Installation des dépendances système
# Utile pour certains packages Python qui nécessitent des bibliothèques C
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copie du fichier requirements.txt
COPY requirements.txt .

# Installation des dépendances Python
# --no-cache-dir réduit la taille de l'image
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copie de tout le projet dans le container
COPY . .

# Installation du package en mode éditable
RUN pip install -e .

# Création des dossiers nécessaires
RUN mkdir -p data/raw data/processed models logs

# Exposition du port pour l'API Flask
EXPOSE 5000

# Variable d'environnement pour Flask
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

# Commande par défaut pour lancer l'API
CMD ["python", "app.py"]

# Commandes alternatives :
# Pour entraîner le modèle : docker run <image> python -m src.pipeline.training_pipeline
# Pour prédire : docker run <image> python -m src.pipeline.prediction_pipeline
# Pour lancer l'API : docker run -p 5000:5000 <image>

# Construction de l'image :
# docker build -t ds_project:latest .

# Lancement du container :
# docker run -p 5000:5000 ds_project:latest

# Lancement avec volumes (pour persister les données) :
# docker run -p 5000:5000 -v $(pwd)/data:/app/data -v $(pwd)/models:/app/models ds_project:latest
