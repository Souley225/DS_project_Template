"""
Module de gestion centralisée des exceptions

Ce module fournit une classe personnalisée pour gérer les erreurs de façon uniforme.
Il capture les informations détaillées sur les exceptions (fichier, ligne, message)
pour faciliter le débogage.
"""

import sys
from src.logger import logging


def error_message_detail(error, error_detail: sys):
    """
    Construit un message d'erreur détaillé avec le nom du fichier et le numéro de ligne

    Args:
        error: L'exception levée
        error_detail: sys module pour extraire les informations de traceback

    Returns:
        str: Message d'erreur formaté avec le contexte complet
    """
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno

    error_message = "Erreur dans le script Python [{0}] à la ligne [{1}] : {2}".format(
        file_name, line_number, str(error)
    )

    return error_message


class CustomException(Exception):
    """
    Classe d'exception personnalisée pour le projet

    Hérite de Exception et ajoute des informations détaillées sur le contexte de l'erreur
    """

    def __init__(self, error_message, error_detail: sys):
        """
        Initialise l'exception avec un message détaillé

        Args:
            error_message: Message d'erreur de base
            error_detail: sys module pour extraire le traceback
        """
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail=error_detail)

    def __str__(self):
        return self.error_message


# Exemple d'utilisation :
# try:
#     # Votre code ici
#     pass
# except Exception as e:
#     logging.error("Une erreur s'est produite")
#     raise CustomException(e, sys)
