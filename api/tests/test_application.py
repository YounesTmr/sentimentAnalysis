import pytest
import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from application import app
 

@pytest.fixture
def client():
    app.config['TESTING'] = True  # Activer le mode test
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to the Sentiment Analysis API ! Corrected" in response.data

def test_predict_positive(client):
    response = client.post('/predict', json={"text": "I love this product!"})
    data = json.loads(response.data)
    assert response.status_code == 200
    assert 'prediction' in data
    assert data['prediction'] == "positive"

def test_predict_negative(client):
    response = client.post('/predict', json={"text": "This is a bad product!"})
    data = json.loads(response.data)
    assert response.status_code == 200
    assert 'prediction' in data
    assert data['prediction'] == "negative"


# def test_validate(client):
#     response = client.post('/validate', json={
#         "text": "I love this product!",
#         "predicted_sentiment": "positive",
#         "user_feedback": True
#     })
#     data = json.loads(response.data)
#     assert response.status_code == 200
#     assert "message" in data
# does not work now because instrumentation_key of azure is no more available