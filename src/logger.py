"""
Module de configuration du système de logs

Ce module configure le système de journalisation pour l'ensemble du projet.
Il crée des logs avec horodatage dans le dossier 'logs/' pour tracer
l'exécution et faciliter le débogage.
"""

import os
import logging
from datetime import datetime

# Nom du fichier de log avec timestamp
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Chemin complet du dossier de logs
logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE)

# Création du dossier logs s'il n'existe pas
os.makedirs(os.path.dirname(logs_path), exist_ok=True)

# Configuration du logger
logging.basicConfig(
    filename=logs_path,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Exemple d'utilisation :
# from src.logger import logging
# logging.info("Message d'information")
# logging.warning("Message d'avertissement")
# logging.error("Message d'erreur")
