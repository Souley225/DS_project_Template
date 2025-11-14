"""
Module d'ingestion de données

Ce module gère le chargement des données depuis différentes sources (CSV, base de données, API, etc.)
et leur division en ensembles d'entraînement et de test.
"""

import os
import sys
from dataclasses import dataclass
import pandas as pd
from sklearn.model_selection import train_test_split

from src.exception import CustomException
from src.logger import logging


@dataclass
class DataIngestionConfig:
    """
    Configuration pour l'ingestion de données

    Définit les chemins où seront stockées les données brutes et divisées
    """
    train_data_path: str = os.path.join('data', 'train.csv')
    test_data_path: str = os.path.join('data', 'test.csv')
    raw_data_path: str = os.path.join('data', 'raw', 'data.csv')


class DataIngestion:
    """
    Classe responsable de l'ingestion et de la division des données

    Elle charge les données depuis une source, les sauvegarde en format brut,
    puis les divise en ensembles d'entraînement et de test.
    """

    def __init__(self):
        """Initialise la configuration d'ingestion"""
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        """
        Lance le processus d'ingestion de données

        Étapes :
        1. Lit les données depuis la source (ici un CSV d'exemple)
        2. Sauvegarde les données brutes
        3. Divise en train/test
        4. Retourne les chemins des fichiers créés

        Returns:
            tuple: (chemin_train, chemin_test)

        Raises:
            CustomException: En cas d'erreur lors de l'ingestion
        """
        logging.info("Démarrage de l'ingestion de données")

        try:
            # Lecture des données depuis la source
            # Remplacer par votre source de données réelle (DB, API, etc.)
            df = pd.read_csv('data/raw/data.csv')
            logging.info("Lecture du dataset terminée")

            # Création des répertoires si nécessaire
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            # Sauvegarde des données brutes
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            logging.info("Sauvegarde des données brutes effectuée")

            # Division train/test
            logging.info("Division train/test initiée")
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            # Sauvegarde des ensembles
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info("Ingestion de données terminée avec succès")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            logging.error("Erreur lors de l'ingestion de données")
            raise CustomException(e, sys)


# Exemple d'utilisation :
if __name__ == "__main__":
    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()
    print(f"Données d'entraînement : {train_data}")
    print(f"Données de test : {test_data}")
