"""
Pipeline de prédiction

Ce module gère l'inférence sur de nouvelles données :
- Chargement du modèle et du preprocessor
- Transformation des données d'entrée
- Génération de prédictions
"""

import sys
import pandas as pd
from src.exception import CustomException
from src.logger import logging
from src.utils.common import load_object


class PredictPipeline:
    """
    Classe gérant le pipeline de prédiction

    Charge le modèle entraîné et le preprocessor, puis génère des prédictions
    sur de nouvelles données.
    """

    def __init__(self):
        """Initialise le pipeline de prédiction"""
        logging.info("Initialisation du pipeline de prédiction")

    def predict(self, features):
        """
        Génère des prédictions sur de nouvelles données

        Args:
            features: DataFrame pandas contenant les features

        Returns:
            array: Prédictions du modèle

        Raises:
            CustomException: En cas d'erreur lors de la prédiction
        """
        try:
            logging.info("Début de la prédiction")

            # Chemins des fichiers modèle et preprocessor
            model_path = 'models/model.pkl'
            preprocessor_path = 'models/preprocessor.pkl'

            # Chargement du modèle et du preprocessor
            logging.info("Chargement du modèle et du preprocessor")
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)

            # Transformation des données
            logging.info("Transformation des données d'entrée")
            data_scaled = preprocessor.transform(features)

            # Prédiction
            logging.info("Génération des prédictions")
            preds = model.predict(data_scaled)

            logging.info("Prédiction terminée avec succès")
            return preds

        except Exception as e:
            logging.error("Erreur lors de la prédiction")
            raise CustomException(e, sys)


class CustomData:
    """
    Classe pour structurer les données d'entrée personnalisées

    Permet de créer facilement un DataFrame à partir de valeurs individuelles
    pour effectuer des prédictions.
    """

    def __init__(
        self,
        feature1: float,
        feature2: float,
        feature3: str,
        # Ajouter tous vos features ici
    ):
        """
        Initialise les données personnalisées

        Args:
            feature1: Première feature numérique
            feature2: Deuxième feature numérique
            feature3: Feature catégorielle
            ...
        """
        self.feature1 = feature1
        self.feature2 = feature2
        self.feature3 = feature3

    def get_data_as_dataframe(self):
        """
        Convertit les données en DataFrame pandas

        Returns:
            DataFrame: Données structurées prêtes pour la prédiction

        Raises:
            CustomException: En cas d'erreur lors de la conversion
        """
        try:
            # Création d'un dictionnaire avec les données
            custom_data_input_dict = {
                "feature1": [self.feature1],
                "feature2": [self.feature2],
                "feature3": [self.feature3],
                # Ajouter tous vos features ici
            }

            # Conversion en DataFrame
            df = pd.DataFrame(custom_data_input_dict)

            logging.info("Données converties en DataFrame")
            logging.info(f"Colonnes du DataFrame : {df.columns.tolist()}")

            return df

        except Exception as e:
            logging.error("Erreur lors de la conversion des données")
            raise CustomException(e, sys)


# Exemple d'utilisation :
if __name__ == "__main__":
    try:
        # Création d'un objet avec des données personnalisées
        data = CustomData(
            feature1=10.5,
            feature2=20.3,
            feature3="category_A"
        )

        # Conversion en DataFrame
        pred_df = data.get_data_as_dataframe()
        print("Données d'entrée :")
        print(pred_df)

        # Prédiction
        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(pred_df)

        print("\nRésultats de la prédiction :")
        print(results)

    except Exception as e:
        logging.error(f"Erreur : {str(e)}")
        raise e
