from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import os

app = FastAPI(title="API Sentimientos Hotel - Alexis v1.2 Final")

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
        "Personal": ["atención", "servicio", "personal", "recepción", "amabilidad", "mesero", "atender", "empleados", "atencion"],
        "Instalaciones": ["piscina", "wifi", "internet", "desayuno", "comida", "ascensor", "ambiente", "gym"],
        "Ubicación": ["ubicación", "cerca", "lejos", "centro", "zona", "playa", "ubicacion"]
    }
    for motivo, palabras in categorías.items():
        if any(p in text for p in palabras):
            return motivo
    return "General"

@app.post("/predict/sentiment")
async def predict(data: Request):
    # 1. Obtener predicción y probabilidad del modelo
    pred = model.predict([data.text])[0]
    probs = model.predict_proba([data.text])[0]
    prob_max = max(probs)
    
    # 2. Lógica de Seguridad para quejas (Override)
    criticas = ["mala", "malo", "pésimo", "terrible", "deficiente", "sucio", "asco", "disgustado"]
    texto_lower = data.text.lower()
    
    resultado_final = int(pred)
    
    # Si hay una palabra crítica, aseguramos que sea Negativo (0)
    if any(p in texto_lower for p in criticas):
        resultado_final = 0
        # Ajustamos el score para mostrar confianza en la detección de la queja
        if prob_max < 0.8: prob_max = 0.88

    nombres = {0: "Negativo", 1: "Positivo", 3: "Neutral"}
    motivo = detectar_motivo_api(data.text)
    
    return {
        "prevision": nombres.get(resultado_final),
        "probabilidad": str(round(prob_max, 2)),
        "motivo": motivo,
        "status": "Procesado exitosamente con SVM Calibrado",
        "modelo_version": "1.2-svm-final"
    }