"""
Script d'installation du package

Ce fichier permet d'installer le projet comme un package Python.
Utile pour importer les modules facilement et pour le déploiement.

Installation :
    pip install -e .          # Mode développement (éditable)
    pip install .             # Installation standard
"""

from setuptools import find_packages, setup
from typing import List

HYPEN_E_DOT = '-e .'


def get_requirements(file_path: str) -> List[str]:
    """
    Lit le fichier requirements.txt et retourne la liste des dépendances

    Args:
        file_path: Chemin vers le fichier requirements.txt

    Returns:
        List[str]: Liste des packages requis
    """
    requirements = []

    with open(file_path, 'r', encoding='utf-8') as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n", "") for req in requirements]

        # Retirer '-e .' si présent (pour l'installation en mode éditable)
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)

    return requirements


# Configuration du package
setup(
    name='ds_project_template',
    version='1.0.0',
    author='Souleymane Sall',
    author_email='votre.email@exemple.com',
    description='Template de projet Data Science structuré et modulaire',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Souley225/DS_project_Template',

    # Recherche automatique de tous les packages dans src/
    packages=find_packages(),

    # Installation des dépendances depuis requirements.txt
    install_requires=get_requirements('requirements.txt'),

    # Classificateurs pour PyPI (optionnel)
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],

    # Version Python minimale requise
    python_requires='>=3.8',

    # Fichiers supplémentaires à inclure dans le package
    include_package_data=True,

    # Scripts en ligne de commande (optionnel)
    entry_points={
        'console_scripts': [
            'train-model=src.pipeline.training_pipeline:main',
            'predict=src.pipeline.prediction_pipeline:main',
        ],
    },

    # Mots-clés pour la recherche
    keywords='data-science machine-learning ml template',

    # Informations de licence
    license='MIT',
)

"""
Utilisation après installation :

1. Installation en mode développement :
   pip install -e .

2. Imports dans votre code :
   from src.components.data_ingestion import DataIngestion
   from src.pipeline.training_pipeline import TrainingPipeline
   from src.utils.common import save_object, load_object

3. Utilisation des scripts CLI (si entry_points configurés) :
   train-model
   predict
"""
