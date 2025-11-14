"""
Module d'évaluation de modèles

Ce module gère l'évaluation des performances des modèles entraînés
avec différentes métriques et génère des rapports de performance.
"""

import sys
from dataclasses import dataclass
import pandas as pd
from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    r2_score,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

from src.exception import CustomException
from src.logger import logging
from src.utils.common import load_object


@dataclass
class ModelEvaluationConfig:
    """
    Configuration pour l'évaluation de modèles

    Peut contenir des seuils de performance, chemins de rapports, etc.
    """
    performance_threshold: float = 0.6


class ModelEvaluation:
    """
    Classe responsable de l'évaluation des modèles

    Calcule différentes métriques de performance et génère des rapports
    pour comparer les modèles ou valider un modèle en production.
    """

    def __init__(self):
        """Initialise la configuration d'évaluation"""
        self.evaluation_config = ModelEvaluationConfig()

    def evaluate_regression_model(self, y_true, y_pred):
        """
        Évalue un modèle de régression avec plusieurs métriques

        Args:
            y_true: Valeurs réelles
            y_pred: Valeurs prédites

        Returns:
            dict: Dictionnaire contenant toutes les métriques

        Raises:
            CustomException: En cas d'erreur lors de l'évaluation
        """
        try:
            # Calcul des métriques de régression
            mse = mean_squared_error(y_true, y_pred)
            mae = mean_absolute_error(y_true, y_pred)
            rmse = mean_squared_error(y_true, y_pred, squared=False)
            r2 = r2_score(y_true, y_pred)

            metrics = {
                "MSE": mse,
                "MAE": mae,
                "RMSE": rmse,
                "R2_Score": r2
            }

            logging.info(f"Métriques d'évaluation : {metrics}")

            return metrics

        except Exception as e:
            logging.error("Erreur lors de l'évaluation du modèle de régression")
            raise CustomException(e, sys)

    def evaluate_classification_model(self, y_true, y_pred):
        """
        Évalue un modèle de classification avec plusieurs métriques

        Args:
            y_true: Valeurs réelles
            y_pred: Valeurs prédites

        Returns:
            dict: Dictionnaire contenant toutes les métriques

        Raises:
            CustomException: En cas d'erreur lors de l'évaluation
        """
        try:
            # Calcul des métriques de classification
            acc = accuracy_score(y_true, y_pred)
            precision = precision_score(y_true, y_pred, average='weighted')
            recall = recall_score(y_true, y_pred, average='weighted')
            f1 = f1_score(y_true, y_pred, average='weighted')

            metrics = {
                "Accuracy": acc,
                "Precision": precision,
                "Recall": recall,
                "F1_Score": f1
            }

            logging.info(f"Métriques d'évaluation : {metrics}")

            return metrics

        except Exception as e:
            logging.error("Erreur lors de l'évaluation du modèle de classification")
            raise CustomException(e, sys)

    def initiate_model_evaluation(self, test_data_path, model_path, preprocessor_path):
        """
        Lance l'évaluation complète d'un modèle sur les données de test

        Étapes :
        1. Charge les données de test
        2. Charge le modèle et le preprocessor
        3. Applique les transformations
        4. Génère les prédictions
        5. Calcule les métriques de performance

        Args:
            test_data_path: Chemin vers les données de test
            model_path: Chemin vers le modèle sauvegardé
            preprocessor_path: Chemin vers le preprocessor sauvegardé

        Returns:
            dict: Rapport d'évaluation avec toutes les métriques

        Raises:
            CustomException: En cas d'erreur lors de l'évaluation
        """
        try:
            logging.info("Démarrage de l'évaluation du modèle")

            # Chargement des données de test
            test_df = pd.read_csv(test_data_path)
            logging.info("Données de test chargées")

            # Nom de la colonne cible (à adapter)
            target_column = "target"

            # Séparation features/target
            X_test = test_df.drop(columns=[target_column], axis=1)
            y_test = test_df[target_column]

            # Chargement du modèle et du preprocessor
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)

            logging.info("Modèle et preprocessor chargés")

            # Transformation des features
            X_test_transformed = preprocessor.transform(X_test)

            # Génération des prédictions
            y_pred = model.predict(X_test_transformed)

            # Évaluation (adapter selon le type de problème)
            metrics = self.evaluate_regression_model(y_test, y_pred)

            # Vérification du seuil de performance
            if metrics["R2_Score"] < self.evaluation_config.performance_threshold:
                logging.warning(
                    f"Le modèle n'atteint pas le seuil de performance requis "
                    f"({self.evaluation_config.performance_threshold})"
                )

            logging.info("Évaluation du modèle terminée avec succès")

            return metrics

        except Exception as e:
            logging.error("Erreur lors de l'évaluation du modèle")
            raise CustomException(e, sys)


# Exemple d'utilisation :
if __name__ == "__main__":
    # obj = ModelEvaluation()
    # metrics = obj.initiate_model_evaluation(
    #     test_data_path="data/test.csv",
    #     model_path="models/model.pkl",
    #     preprocessor_path="models/preprocessor.pkl"
    # )
    # print(metrics)
    pass
