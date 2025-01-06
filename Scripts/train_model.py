import mlflow
import mlflow.sklearn  # ou mlflow.keras/tensorflow pour des modèles spécifiques

# Configurer MLFlow pour suivre localement
mlflow.set_tracking_uri("file:./mlruns")
mlflow.set_experiment("sentiment_analysis_project")

with mlflow.start_run(run_name="baseline_model"):
    # Exemple de suivi d'un paramètre
    mlflow.log_param("model_type", "Logistic Regression")

    # Exemple de suivi d'une métrique
    accuracy = 0.85
    mlflow.log_metric("accuracy", accuracy)

    # Exemple de sauvegarde d'un modèle
    # Remplacez cela par le modèle entraîné
    dummy_model = {"coef": [0.5], "intercept": 0.1}
    mlflow.log_artifact("dummy_model.pkl")

