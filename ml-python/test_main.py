import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_predict_sentiment_positive():
    response = client.post("/predict/sentiment", json={"text": "El servicio fue excelente"})
    assert response.status_code == 200
    data = response.json()
    assert "prevision" in data
    assert "probabilidad" in data
    assert "explicabilidad" in data
    assert data["prevision"] in ["Positivo", "Negativo", "Neutro"]

def test_predict_sentiment_negativo():
    response = client.post("/predict/sentiment", json={"text": "El servicio fue terrible"})
    assert response.status_code == 200
    data = response.json()
    assert "prevision" in data
    assert "probabilidad" in data
    assert "explicabilidad" in data
    assert data["prevision"] == "Negativo"

def test_predict_sentiment_empty_text():
    response = client.post("/predict/sentiment", json={"text": ""})
    assert response.status_code == 400
    assert response.json()["detail"] == "El texto no puede estar vacío"

def test_predict_sentiment_short_text():
    response = client.post("/predict/sentiment", json={"text": "No"})
    assert response.status_code == 200
    data = response.json()
    assert data["prevision"] == "Neutro"
    assert "explicabilidad" in data
    assert data["explicabilidad"] == "Texto muy corto para análisis"

def test_invalid_payload():
    response = client.post("/predict/sentiment", json={"text_field": "some text"})
    assert response.status_code == 422
