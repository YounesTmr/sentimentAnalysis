from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
import numpy as np
import tensorflow_hub as hub
from opencensus.ext.azure.log_exporter import AzureLogHandler
import logging
from transformers import BertTokenizer, BertModel
import torch

# Initialiser Flask
application = app = Flask(__name__)

# Charger le modèle TensorFlow
model = load_model("sentiment_model.h5")

instrumentation_key = "3762cbd1-6a49-42ec-9653-d92a296d33de"  
logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(connection_string=f"InstrumentationKey={instrumentation_key}"))
logger.setLevel(logging.INFO)


# Route pour la page d'accueil
@app.route('/')
def home():
    return "Welcome to the Sentiment Analysis API ! Corrected"

# Function to get BERT embeddings for a single text
def get_bert_embeddings(text):
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')

    # Tokenize the input text
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    
    # Perform inference with the model
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Use the [CLS] token embedding as the sentence embedding
    embedding = outputs.last_hidden_state[:, 0, :].squeeze().numpy()

    # Ensure the embedding has the shape (1, 768) for the TensorFlow model
    return embedding.reshape(1, -1)  # Reshape to (1, 768)

# Endpoint pour effectuer une prédiction
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Récupérer les données JSON
        data = request.get_json()
        text = data.get("text", "")
        if not text:
            return jsonify({"error": "No text provided"}), 400

        # Générer les embeddings et effectuer la prédiction
        embedding = get_bert_embeddings(text)  # Pass text directly, not in a list
        prediction = model.predict(embedding)
        sentiment = "positive" if prediction[0] > 0.5 else "negative"

        # Retourner la réponse
        return jsonify({"text": text, "prediction": sentiment}), 200
    except Exception as e:
        logger.error(f"Erreur dans /predict : {e}")
        return jsonify({"error": "Erreur lors de la prédiction"}), 500


# Endpoint pour enregistrer une validation ou une invalidation
@app.route('/validate', methods=['POST'])
def validate():
    try:
        # Récupérer les données JSON
        data = request.get_json()
        text = data.get("text", "")
        predicted_sentiment = data.get("predicted_sentiment", "")
        user_feedback = data.get("user_feedback", None)  # True (validation), False (invalidation)

        if not text or not predicted_sentiment or user_feedback is None:
            return jsonify({"error": "Données incomplètes"}), 400

        # Journaliser les traces dans Azure Application Insights
        if user_feedback:
            logger.info(f"Validation réussie pour le texte : '{text}' avec le sentiment prédit : '{predicted_sentiment}'")
        else:
            logger.warning(f"Prédiction invalidée pour le texte : '{text}' avec le sentiment prédit : '{predicted_sentiment}'")

        return jsonify({"message": "Feedback enregistré avec succès"}), 200
    except Exception as e:
        logger.error(f"Erreur dans /validate : {e}")
        return jsonify({"error": "Erreur lors de l'enregistrement du feedback"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
