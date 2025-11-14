"""
Module de transformation de données

Ce module gère le prétraitement et la transformation des données :
- Imputation des valeurs manquantes
- Encodage des variables catégorielles
- Normalisation/Standardisation des variables numériques
- Création du pipeline de transformation
"""

import sys
import os
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging
from src.utils.common import save_object


@dataclass
class DataTransformationConfig:
    """
    Configuration pour la transformation de données

    Définit le chemin où sera sauvegardé le preprocessor (pipeline de transformation)
    """
    preprocessor_obj_file_path: str = os.path.join('models', 'preprocessor.pkl')


class DataTransformation:
    """
    Classe responsable de la transformation des données

    Crée un pipeline de prétraitement pour les variables numériques et catégorielles,
    puis transforme les données d'entraînement et de test.
    """

    def __init__(self):
        """Initialise la configuration de transformation"""
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        """
        Crée le pipeline de transformation des données

        Ce pipeline gère séparément les colonnes numériques et catégorielles :
        - Numériques : imputation médiane + standardisation
        - Catégorielles : imputation mode + encodage one-hot

        Returns:
            ColumnTransformer: Pipeline de prétraitement complet

        Raises:
            CustomException: En cas d'erreur lors de la création du pipeline
        """
        try:
            # Colonnes numériques et catégorielles
            # À adapter selon votre dataset
            numerical_columns = ["feature1", "feature2", "feature3"]
            categorical_columns = ["category1", "category2"]

            # Pipeline pour les variables numériques
            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),  # Imputation valeurs manquantes
                    ("scaler", StandardScaler())  # Standardisation
                ]
            )

            # Pipeline pour les variables catégorielles
            cat_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),  # Imputation valeurs manquantes
                    ("one_hot_encoder", OneHotEncoder()),  # Encodage one-hot
                    ("scaler", StandardScaler(with_mean=False))  # Standardisation (sparse matrix)
                ]
            )

            logging.info(f"Colonnes numériques : {numerical_columns}")
            logging.info(f"Colonnes catégorielles : {categorical_columns}")

            # Combinaison des deux pipelines
            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, numerical_columns),
                    ("cat_pipeline", cat_pipeline, categorical_columns)
                ]
            )

            return preprocessor

        except Exception as e:
            logging.error("Erreur lors de la création du pipeline de transformation")
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_path, test_path):
        """
        Lance la transformation des données d'entraînement et de test

        Étapes :
        1. Charge les données train/test
        2. Crée le pipeline de transformation
        3. Applique le pipeline sur les données
        4. Sauvegarde le preprocessor

        Args:
            train_path: Chemin vers les données d'entraînement
            test_path: Chemin vers les données de test

        Returns:
            tuple: (train_array, test_array, preprocessor_path)

        Raises:
            CustomException: En cas d'erreur lors de la transformation
        """
        try:
            # Lecture des données
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Lecture des données train et test terminée")
            logging.info("Obtention du preprocessor")

            # Création du pipeline de transformation
            preprocessing_obj = self.get_data_transformer_object()

            # Nom de la colonne cible (à adapter)
            target_column_name = "target"

            # Séparation features/target
            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]

            logging.info("Application du preprocessing sur les données train et test")

            # Application de la transformation
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            # Concaténation features transformées + target
            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[
                input_feature_test_arr, np.array(target_feature_test_df)
            ]

            logging.info("Sauvegarde du preprocessor")

            # Sauvegarde du preprocessor pour réutilisation en prédiction
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            logging.info("Transformation des données terminée avec succès")

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )

        except Exception as e:
            logging.error("Erreur lors de la transformation de données")
            raise CustomException(e, sys)


# Exemple d'utilisation :
if __name__ == "__main__":
    obj = DataTransformation()
    # train_arr, test_arr, _ = obj.initiate_data_transformation("data/train.csv", "data/test.csv")
