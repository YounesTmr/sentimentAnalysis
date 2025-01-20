import streamlit as st
import requests

# URL de votre API Flask
API_PREDICT_URL = "http://testapp-env.eba-xsg2a8c5.eu-west-3.elasticbeanstalk.com/predict"  # Endpoint pour les prédictions
API_VALIDATE_URL = "http://testapp-env.eba-xsg2a8c5.eu-west-3.elasticbeanstalk.com/validate"  # Endpoint pour les validations

st.title("Analyse de Sentiment") 

# Initialiser les variables d'état
if "prediction" not in st.session_state:
    st.session_state.prediction = None
if "feedback_given" not in st.session_state:
    st.session_state.feedback_given = False

# Formulaire pour envoyer un texte
text_input = st.text_area("Entrez un texte à analyser :", "")

# Bouton pour effectuer une prédiction
if st.button("Prédire"):
    if text_input.strip() == "":
        st.error("Veuillez entrer un texte avant de soumettre.")
    else:
        # Réinitialiser les états
        st.session_state.prediction = None
        st.session_state.feedback_given = False

        # Envoi des données à l'API pour prédiction
        response = requests.post(API_PREDICT_URL, json={"text": text_input})

        if response.status_code == 200:
            st.session_state.prediction = response.json().get("prediction")
            st.success(f"Prédiction : {st.session_state.prediction}")
        else:
            st.error(f"Erreur API : {response.status_code}")

# Afficher les options de validation uniquement après une prédiction réussie
if st.session_state.prediction and not st.session_state.feedback_given:
    st.markdown("### Donnez votre feedback sur la prédiction :")
    user_feedback = st.radio(
        "Est-ce que cette prédiction est correcte ?",
        ("Oui", "Non"),
        key="user_feedback_choice"
    )

    if st.button("Envoyer le feedback"):
        # Préparer le feedback utilisateur
        is_feedback_positive = st.session_state.user_feedback_choice == "Oui"

        # Envoi des données de validation à l'API
        feedback_response = requests.post(
            API_VALIDATE_URL,
            json={
                "text": text_input,
                "predicted_sentiment": st.session_state.prediction,
                "user_feedback": is_feedback_positive
            }
        )

        if feedback_response.status_code == 200:
            st.success("Merci pour votre feedback !")
            st.session_state.feedback_given = True
        else:
            st.error(f"Erreur lors de l'envoi du feedback : {feedback_response.status_code}")

# Si le feedback a déjà été donné, afficher un message
if st.session_state.feedback_given:
    st.info("Votre feedback a déjà été enregistré. Merci !")
