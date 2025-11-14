"""
Fonctions utilitaires communes

Ce module contient des fonctions réutilisables dans tout le projet :
- Sauvegarde/Chargement d'objets (modèles, preprocessors)
- Lecture de fichiers YAML/JSON
- Évaluation de modèles
- Autres utilitaires divers
"""

import os
import sys
import pickle
import yaml
import json
import dill
import numpy as np
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

from src.exception import CustomException
from src.logger import logging


def save_object(file_path, obj):
    """
    Sauvegarde un objet Python dans un fichier pickle

    Args:
        file_path: Chemin du fichier de destination
        obj: Objet à sauvegarder

    Raises:
        CustomException: En cas d'erreur lors de la sauvegarde
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

        logging.info(f"Objet sauvegardé : {file_path}")

    except Exception as e:
        logging.error(f"Erreur lors de la sauvegarde de l'objet : {file_path}")
        raise CustomException(e, sys)


def load_object(file_path):
    """
    Charge un objet Python depuis un fichier pickle

    Args:
        file_path: Chemin du fichier à charger

    Returns:
        object: Objet chargé

    Raises:
        CustomException: En cas d'erreur lors du chargement
    """
    try:
        with open(file_path, "rb") as file_obj:
            obj = pickle.load(file_obj)

        logging.info(f"Objet chargé : {file_path}")
        return obj

    except Exception as e:
        logging.error(f"Erreur lors du chargement de l'objet : {file_path}")
        raise CustomException(e, sys)


def read_yaml(file_path):
    """
    Lit un fichier YAML et retourne son contenu

    Args:
        file_path: Chemin du fichier YAML

    Returns:
        dict: Contenu du fichier YAML

    Raises:
        CustomException: En cas d'erreur lors de la lecture
    """
    try:
        with open(file_path, "r", encoding="utf-8") as yaml_file:
            content = yaml.safe_load(yaml_file)

        logging.info(f"Fichier YAML lu : {file_path}")
        return content

    except Exception as e:
        logging.error(f"Erreur lors de la lecture du fichier YAML : {file_path}")
        raise CustomException(e, sys)


def write_yaml(file_path, content, replace=False):
    """
    Écrit du contenu dans un fichier YAML

    Args:
        file_path: Chemin du fichier de destination
        content: Contenu à écrire (dict)
        replace: Si True, écrase le fichier existant

    Raises:
        CustomException: En cas d'erreur lors de l'écriture
    """
    try:
        if replace or not os.path.exists(file_path):
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            with open(file_path, "w", encoding="utf-8") as yaml_file:
                yaml.dump(content, yaml_file)

            logging.info(f"Fichier YAML écrit : {file_path}")

    except Exception as e:
        logging.error(f"Erreur lors de l'écriture du fichier YAML : {file_path}")
        raise CustomException(e, sys)


def read_json(file_path):
    """
    Lit un fichier JSON et retourne son contenu

    Args:
        file_path: Chemin du fichier JSON

    Returns:
        dict: Contenu du fichier JSON

    Raises:
        CustomException: En cas d'erreur lors de la lecture
    """
    try:
        with open(file_path, "r", encoding="utf-8") as json_file:
            content = json.load(json_file)

        logging.info(f"Fichier JSON lu : {file_path}")
        return content

    except Exception as e:
        logging.error(f"Erreur lors de la lecture du fichier JSON : {file_path}")
        raise CustomException(e, sys)


def write_json(file_path, content):
    """
    Écrit du contenu dans un fichier JSON

    Args:
        file_path: Chemin du fichier de destination
        content: Contenu à écrire (dict)

    Raises:
        CustomException: En cas d'erreur lors de l'écriture
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(content, json_file, indent=4)

        logging.info(f"Fichier JSON écrit : {file_path}")

    except Exception as e:
        logging.error(f"Erreur lors de l'écriture du fichier JSON : {file_path}")
        raise CustomException(e, sys)


def evaluate_models(X_train, y_train, X_test, y_test, models, param):
    """
    Évalue plusieurs modèles avec optimisation des hyperparamètres

    Entraîne chaque modèle avec GridSearchCV pour trouver les meilleurs
    hyperparamètres, puis évalue sur le jeu de test.

    Args:
        X_train: Features d'entraînement
        y_train: Target d'entraînement
        X_test: Features de test
        y_test: Target de test
        models: Dictionnaire {nom_modèle: instance_modèle}
        param: Dictionnaire {nom_modèle: grille_hyperparamètres}

    Returns:
        dict: {nom_modèle: score_r2_test}

    Raises:
        CustomException: En cas d'erreur lors de l'évaluation
    """
    try:
        report = {}

        for i, (model_name, model) in enumerate(models.items()):
            logging.info(f"\nÉvaluation du modèle {i+1}/{len(models)} : {model_name}")

            # Récupération des hyperparamètres
            params = param.get(model_name, {})

            if params:
                # Optimisation avec GridSearchCV
                gs = GridSearchCV(model, params, cv=3, n_jobs=-1, verbose=1)
                gs.fit(X_train, y_train)

                # Meilleur modèle
                model.set_params(**gs.best_params_)
                logging.info(f"Meilleurs paramètres pour {model_name} : {gs.best_params_}")

            # Entraînement du modèle
            model.fit(X_train, y_train)

            # Prédictions
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            # Calcul des scores
            train_score = r2_score(y_train, y_train_pred)
            test_score = r2_score(y_test, y_test_pred)

            logging.info(f"Score R2 train : {train_score:.4f}")
            logging.info(f"Score R2 test : {test_score:.4f}")

            report[model_name] = test_score

        logging.info("\n" + "=" * 80)
        logging.info("RAPPORT D'ÉVALUATION DES MODÈLES")
        logging.info("=" * 80)
        for model_name, score in sorted(report.items(), key=lambda x: x[1], reverse=True):
            logging.info(f"{model_name:30} : R2 = {score:.4f}")
        logging.info("=" * 80)

        return report

    except Exception as e:
        logging.error("Erreur lors de l'évaluation des modèles")
        raise CustomException(e, sys)


def create_directories(path_list):
    """
    Crée une liste de répertoires

    Args:
        path_list: Liste de chemins de répertoires à créer

    Raises:
        CustomException: En cas d'erreur lors de la création
    """
    try:
        for path in path_list:
            os.makedirs(path, exist_ok=True)
            logging.info(f"Répertoire créé : {path}")

    except Exception as e:
        logging.error("Erreur lors de la création des répertoires")
        raise CustomException(e, sys)


# Exemple d'utilisation :
if __name__ == "__main__":
    # Test de lecture/écriture YAML
    # config = read_yaml("config/config.yaml")
    # print(config)
    pass
