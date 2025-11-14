"""
Application Flask pour l'API de prédiction

Point d'entrée principal pour exposer le modèle via une API REST.
Permet de faire des prédictions via des requêtes HTTP.
"""

from flask import Flask, request, render_template, jsonify
import pandas as pd
import sys

from src.pipeline.prediction_pipeline import CustomData, PredictPipeline
from src.exception import CustomException
from src.logger import logging
from src.utils.common import read_yaml

# Création de l'application Flask
app = Flask(__name__)

# Chargement de la configuration
try:
    config = read_yaml("config/config.yaml")
    API_HOST = config.get("api", {}).get("host", "0.0.0.0")
    API_PORT = config.get("api", {}).get("port", 5000)
    API_DEBUG = config.get("api", {}).get("debug", False)
except Exception as e:
    logging.warning("Impossible de charger la config, utilisation des valeurs par défaut")
    API_HOST = "0.0.0.0"
    API_PORT = 5000
    API_DEBUG = False


@app.route('/')
def index():
    """
    Route principale - Page d'accueil de l'API

    Returns:
        str: Page HTML d'accueil
    """
    return """
    <h1>API de Prédiction - Data Science Project</h1>
    <p>Bienvenue sur l'API de prédiction. Utilisez les endpoints suivants :</p>
    <ul>
        <li><b>GET /health</b> - Vérifier l'état de l'API</li>
        <li><b>POST /predict</b> - Faire une prédiction (JSON)</li>
        <li><b>GET /predict_form</b> - Formulaire de prédiction (HTML)</li>
    </ul>
    """


@app.route('/health', methods=['GET'])
def health():
    """
    Endpoint de santé pour vérifier que l'API fonctionne

    Returns:
        JSON: Statut de l'API
    """
    return jsonify({
        "status": "healthy",
        "message": "L'API fonctionne correctement",
        "version": "1.0.0"
    })


@app.route('/predict', methods=['POST'])
def predict_api():
    """
    Endpoint de prédiction via JSON

    Accepte un JSON avec les features et retourne la prédiction.

    Exemple de requête :
    {
        "feature1": 10.5,
        "feature2": 20.3,
        "feature3": "category_A"
    }

    Returns:
        JSON: Résultat de la prédiction
    """
    try:
        # Récupération des données JSON
        data = request.get_json()

        if not data:
            return jsonify({
                "error": "Aucune donnée fournie",
                "message": "Veuillez fournir un JSON valide"
            }), 400

        logging.info(f"Requête de prédiction reçue : {data}")

        # Création d'un DataFrame à partir du JSON
        # Adapter selon vos features
        df = pd.DataFrame([data])

        # Pipeline de prédiction
        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(df)

        # Formatage de la réponse
        response = {
            "prediction": float(results[0]),
            "status": "success",
            "input_data": data
        }

        logging.info(f"Prédiction réussie : {results[0]}")

        return jsonify(response), 200

    except Exception as e:
        logging.error(f"Erreur lors de la prédiction : {str(e)}")
        return jsonify({
            "error": "Erreur lors de la prédiction",
            "message": str(e)
        }), 500


@app.route('/predict_form', methods=['GET', 'POST'])
def predict_form():
    """
    Endpoint avec formulaire HTML pour faire des prédictions

    GET : Affiche le formulaire
    POST : Traite les données du formulaire et retourne la prédiction

    Returns:
        HTML: Formulaire ou résultat de prédiction
    """
    if request.method == 'GET':
        # Affichage du formulaire
        return """
        <h1>Formulaire de Prédiction</h1>
        <form method="POST">
            <label>Feature 1 (numérique):</label><br>
            <input type="number" step="any" name="feature1" required><br><br>

            <label>Feature 2 (numérique):</label><br>
            <input type="number" step="any" name="feature2" required><br><br>

            <label>Feature 3 (catégoriel):</label><br>
            <input type="text" name="feature3" required><br><br>

            <input type="submit" value="Prédire">
        </form>
        """

    try:
        # Récupération des données du formulaire
        data = CustomData(
            feature1=float(request.form.get('feature1')),
            feature2=float(request.form.get('feature2')),
            feature3=request.form.get('feature3')
        )

        # Conversion en DataFrame
        pred_df = data.get_data_as_dataframe()

        # Pipeline de prédiction
        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(pred_df)

        logging.info(f"Prédiction via formulaire : {results[0]}")

        return f"""
        <h1>Résultat de la Prédiction</h1>
        <p><b>Prédiction :</b> {results[0]:.4f}</p>
        <br>
        <a href="/predict_form">Faire une nouvelle prédiction</a>
        """

    except Exception as e:
        logging.error(f"Erreur lors de la prédiction : {str(e)}")
        return f"""
        <h1>Erreur</h1>
        <p>Une erreur s'est produite : {str(e)}</p>
        <br>
        <a href="/predict_form">Réessayer</a>
        """


@app.route('/batch_predict', methods=['POST'])
def batch_predict():
    """
    Endpoint pour prédictions en batch (plusieurs observations)

    Accepte un JSON avec une liste d'observations.

    Exemple de requête :
    {
        "data": [
            {"feature1": 10.5, "feature2": 20.3, "feature3": "A"},
            {"feature1": 15.2, "feature2": 18.7, "feature3": "B"}
        ]
    }

    Returns:
        JSON: Liste des prédictions
    """
    try:
        # Récupération des données JSON
        request_data = request.get_json()
        data_list = request_data.get("data", [])

        if not data_list:
            return jsonify({
                "error": "Aucune donnée fournie",
                "message": "Veuillez fournir une liste de données"
            }), 400

        logging.info(f"Requête de prédiction batch : {len(data_list)} observations")

        # Création d'un DataFrame
        df = pd.DataFrame(data_list)

        # Pipeline de prédiction
        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(df)

        # Formatage de la réponse
        predictions = [float(pred) for pred in results]
        response = {
            "predictions": predictions,
            "count": len(predictions),
            "status": "success"
        }

        logging.info(f"Prédictions batch réussies : {len(predictions)} résultats")

        return jsonify(response), 200

    except Exception as e:
        logging.error(f"Erreur lors de la prédiction batch : {str(e)}")
        return jsonify({
            "error": "Erreur lors de la prédiction batch",
            "message": str(e)
        }), 500


# Point d'entrée de l'application
if __name__ == "__main__":
    logging.info("Démarrage de l'application Flask")
    logging.info(f"Host: {API_HOST}, Port: {API_PORT}, Debug: {API_DEBUG}")

    app.run(
        host=API_HOST,
        port=API_PORT,
        debug=API_DEBUG
    )
