from fastapi.testclient import TestClient
import sys
import os

# Ajustar rutas para encontrar la app
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert "status" in response.json()

def test_predict_positive():
    response = client.post("/predict/sentiment", json={"text": "El hotel es excelente y muy limpio"})
    assert response.status_code == 200
    assert response.json()["prevision"] == "Positivo"

def test_predict_negative():
    response = client.post("/predict/sentiment", json={"text": "La habitación está sucia"})
    assert response.status_code == 200
    assert response.json()["prevision"] == "Negativo"

def test_empty_text():
    response = client.post("/predict/sentiment", json={"text": ""})
    assert response.status_code == 422 # Pydantic min_length error
