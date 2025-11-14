"""
Pipeline d'entraînement complet

Ce module orchestre l'ensemble du processus d'entraînement :
- Ingestion des données
- Transformation/Prétraitement
- Entraînement du modèle
- Évaluation des performances
"""

import sys
from src.exception import CustomException
from src.logger import logging
from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.components.model_evaluation import ModelEvaluation


class TrainingPipeline:
    """
    Classe orchestrant le pipeline d'entraînement complet

    Exécute séquentiellement toutes les étapes du processus de ML :
    de l'ingestion des données brutes jusqu'à l'évaluation du modèle final.
    """

    def __init__(self):
        """Initialise le pipeline d'entraînement"""
        logging.info("Initialisation du pipeline d'entraînement")

    def run_pipeline(self):
        """
        Exécute l'ensemble du pipeline d'entraînement

        Étapes :
        1. Ingestion : Charge et divise les données
        2. Transformation : Prétraite les données
        3. Entraînement : Entraîne et sélectionne le meilleur modèle
        4. Évaluation : Évalue les performances finales

        Returns:
            dict: Résumé des résultats (score, métriques, chemins des fichiers)

        Raises:
            CustomException: En cas d'erreur dans l'une des étapes
        """
        try:
            logging.info("=" * 80)
            logging.info("DÉMARRAGE DU PIPELINE D'ENTRAÎNEMENT")
            logging.info("=" * 80)

            # Étape 1 : Ingestion de données
            logging.info("\n--- ÉTAPE 1 : INGESTION DE DONNÉES ---")
            data_ingestion = DataIngestion()
            train_data_path, test_data_path = data_ingestion.initiate_data_ingestion()

            # Étape 2 : Transformation de données
            logging.info("\n--- ÉTAPE 2 : TRANSFORMATION DE DONNÉES ---")
            data_transformation = DataTransformation()
            train_arr, test_arr, preprocessor_path = data_transformation.initiate_data_transformation(
                train_data_path, test_data_path
            )

            # Étape 3 : Entraînement du modèle
            logging.info("\n--- ÉTAPE 3 : ENTRAÎNEMENT DU MODÈLE ---")
            model_trainer = ModelTrainer()
            model_score = model_trainer.initiate_model_trainer(train_arr, test_arr)

            logging.info(f"Score R2 du modèle entraîné : {model_score}")

            # Étape 4 : Évaluation du modèle
            logging.info("\n--- ÉTAPE 4 : ÉVALUATION DU MODÈLE ---")
            model_evaluation = ModelEvaluation()
            metrics = model_evaluation.initiate_model_evaluation(
                test_data_path=test_data_path,
                model_path=model_trainer.model_trainer_config.trained_model_file_path,
                preprocessor_path=preprocessor_path
            )

            # Résumé des résultats
            results = {
                "train_data_path": train_data_path,
                "test_data_path": test_data_path,
                "preprocessor_path": preprocessor_path,
                "model_path": model_trainer.model_trainer_config.trained_model_file_path,
                "model_score": model_score,
                "evaluation_metrics": metrics
            }

            logging.info("=" * 80)
            logging.info("PIPELINE D'ENTRAÎNEMENT TERMINÉ AVEC SUCCÈS")
            logging.info("=" * 80)
            logging.info(f"\nRésultats :\n{results}")

            return results

        except Exception as e:
            logging.error("Erreur lors de l'exécution du pipeline d'entraînement")
            raise CustomException(e, sys)


# Point d'entrée pour exécuter le pipeline
if __name__ == "__main__":
    try:
        pipeline = TrainingPipeline()
        results = pipeline.run_pipeline()
        print("\n" + "=" * 80)
        print("RÉSULTATS DU PIPELINE D'ENTRAÎNEMENT")
        print("=" * 80)
        print(f"\nChemin du modèle : {results['model_path']}")
        print(f"Chemin du preprocessor : {results['preprocessor_path']}")
        print(f"Score R2 : {results['model_score']:.4f}")
        print(f"\nMétriques d'évaluation :")
        for metric, value in results['evaluation_metrics'].items():
            print(f"  - {metric}: {value:.4f}")
        print("=" * 80)

    except Exception as e:
        logging.error(f"Échec du pipeline : {str(e)}")
        raise e
