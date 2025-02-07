# API de Prédiction de Sentiment

## Objectif du projet

Cette API permet d'analyser le sentiment des tweets en temps réel. Elle a été développée pour la compagnie aérienne fictive "Air Paradis" et fait partie d'un projet OpenClassrooms intégrant les principes MLOps.

## Structure de l'API

- `application.py` : Code principal de l'API avec Flask.
- `test/` : Contient les tests unitaires de l'API.
- `requirements.txt` : Liste des dépendances nécessaires.
- `Dockerfile` : Fichier pour le déploiement via Docker.
- `README.md` : Documentation de l'API.
- `.platform` : Contient la configuration de serveur nginx installé dans le conteneur docker de deploiement.

## Endpoints

- **POST /predict** : Prend un tweet en entrée et retourne le sentiment prédit.
- **POST /validate** : Permet d'envoyer un feedback utilisateur sur la prédiction.

## Déploiement

L'API est déployée sur AWS Elastic Beanstalk et intègre un pipeline CI/CD via AWS CodePipeline.
