"""
Module pipeline

Contient les pipelines d'orchestration :
- training_pipeline : Pipeline complet d'entraînement
- prediction_pipeline : Pipeline de prédiction et inférence
"""

from src.pipeline.training_pipeline import TrainingPipeline
from src.pipeline.prediction_pipeline import PredictPipeline, CustomData

__all__ = [
    "TrainingPipeline",
    "PredictPipeline",
    "CustomData",
]
