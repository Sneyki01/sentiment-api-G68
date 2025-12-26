from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import os

app = FastAPI(title="API Sentimientos Hotel - Alexis v1.0 (SVM)")

# --- CARGAR MODELO ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'data', 'models', 'modelo_sentimiento_pipeline.pkl')
model = joblib.load(MODEL_PATH)

class Request(BaseModel):
    text: str

def detectar_motivo_api(text):
    text = text.lower()
    categorías = {
        "Habitación": ["habitación", "habitaciones", "cuarto", "cama", "baño", "ducha", "calurosa", "caluroso", "aire", "ruido"],
        "Personal": ["atención", "servicio", "personal", "recepción", "amabilidad", "mesero", "atender", "empleados"],
        "Instalaciones": ["piscina", "wifi", "internet", "desayuno", "comida", "ascensor", "ambiente", "gym"],
        "Ubicación": ["ubicación", "cerca", "lejos", "centro", "zona", "playa"]
    }
    for motivo, palabras in categorías.items():
        if any(p in text for p in palabras):
            return motivo
    return "General"

@app.post("/predict/sentiment")
async def predict(data: Request):
    # 1. Predicción base
    pred = model.predict([data.text])[0]
    
    # 2. Lógica de Seguridad (Override)
    # Si detectamos estas palabras, forzamos Negativo aunque el modelo dude
    criticas = ["mala", "malo", "pésimo", "terrible", "deficiente", "sucio", "asco"]
    texto_lower = data.text.lower()
    
    resultado_final = int(pred)
    if any(p in texto_lower for p in criticas):
        resultado_final = 0
    
    nombres = {0: "Negativo", 1: "Positivo", 3: "Neutral"}
    motivo = detectar_motivo_api(data.text)
    
    return {
        "prevision": nombres.get(resultado_final),
        "motivo": motivo,
        "status": "Procesado con motor SVM + Heurística",
        "modelo_version": "1.1-svm-hybrid"
    }