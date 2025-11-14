"""
Module d'entraînement de modèles

Ce module gère l'entraînement de plusieurs modèles de Machine Learning,
l'optimisation des hyperparamètres et la sélection du meilleur modèle.
"""

import os
import sys
from dataclasses import dataclass

from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging
from src.utils.common import save_object, evaluate_models


@dataclass
class ModelTrainerConfig:
    """
    Configuration pour l'entraînement de modèles

    Définit le chemin où sera sauvegardé le modèle entraîné
    """
    trained_model_file_path: str = os.path.join("models", "model.pkl")


class ModelTrainer:
    """
    Classe responsable de l'entraînement et de la sélection du meilleur modèle

    Teste plusieurs algorithmes, optimise leurs hyperparamètres,
    et sélectionne le modèle avec les meilleures performances.
    """

    def __init__(self):
        """Initialise la configuration d'entraînement"""
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_array, test_array):
        """
        Lance l'entraînement de plusieurs modèles et sélectionne le meilleur

        Étapes :
        1. Sépare les features et la cible
        2. Définit les modèles à tester
        3. Définit les grilles d'hyperparamètres
        4. Entraîne et évalue chaque modèle
        5. Sélectionne le meilleur modèle
        6. Sauvegarde le meilleur modèle

        Args:
            train_array: Données d'entraînement (features + target)
            test_array: Données de test (features + target)

        Returns:
            float: Score R2 du meilleur modèle sur les données de test

        Raises:
            CustomException: Si aucun modèle ne dépasse le seuil de performance
        """
        try:
            logging.info("Division des données train et test")
            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1]
            )

            # Dictionnaire de modèles à tester
            models = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "XGBRegressor": XGBRegressor(),
                "AdaBoost Regressor": AdaBoostRegressor(),
            }

            # Grilles d'hyperparamètres pour chaque modèle
            params = {
                "Decision Tree": {
                    'criterion': ['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                },
                "Random Forest": {
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                },
                "Gradient Boosting": {
                    'learning_rate': [.1, .01, .05, .001],
                    'subsample': [0.6, 0.7, 0.75, 0.8, 0.85, 0.9],
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                },
                "Linear Regression": {},
                "XGBRegressor": {
                    'learning_rate': [.1, .01, .05, .001],
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                },
                "AdaBoost Regressor": {
                    'learning_rate': [.1, .01, 0.5, .001],
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                }
            }

            # Évaluation de tous les modèles
            model_report: dict = evaluate_models(
                X_train=X_train,
                y_train=y_train,
                X_test=X_test,
                y_test=y_test,
                models=models,
                param=params
            )

            # Sélection du meilleur score
            best_model_score = max(sorted(model_report.values()))

            # Nom du meilleur modèle
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]

            # Vérification du seuil de performance minimum
            if best_model_score < 0.6:
                raise CustomException("Aucun modèle n'a atteint le seuil de performance", sys)

            logging.info(f"Meilleur modèle trouvé : {best_model_name}")
            logging.info(f"Score R2 sur le test : {best_model_score}")

            # Sauvegarde du meilleur modèle
            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

            # Prédiction avec le meilleur modèle
            predicted = best_model.predict(X_test)
            r2_square = r2_score(y_test, predicted)

            return r2_square

        except Exception as e:
            logging.error("Erreur lors de l'entraînement du modèle")
            raise CustomException(e, sys)


# Exemple d'utilisation :
if __name__ == "__main__":
    # obj = ModelTrainer()
    # score = obj.initiate_model_trainer(train_array, test_array)
    # print(f"Score R2 : {score}")
    pass
