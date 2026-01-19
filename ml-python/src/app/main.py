from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import os
import sys

# Blindaje de rutas para imports locales
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # ml-python/src
sys.path.append(BASE_DIR)

from engine.sentiment_engine import SentimentEngine
from motor_hibrido import enriquecer_respuesta

app = FastAPI(
    title="Modelo Integral para el Análisis de Sentimientos",
    description="API Híbrida de Análisis de Sentimiento con Refinamiento Semántico (G68 Supreme).",
    version="2.1.0"
)

# Inicialización de motores
try:
    # Ajustamos la ruta para que encuentre los modelos en ../../data/models
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    model_path = os.path.join(base_path, "data", "models")
    ai_engine = SentimentEngine(model_dir=model_path)
    print(f"✅ Modelos ML cargados exitosamente desde: {model_path}")
except Exception as e:
    print(f"❌ Error crítico cargando modelos: {e}")
    ai_engine = None

class SentimentRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2500)

class SentimentResponse(BaseModel):
    prevision: str
    probabilidad: float
    top_features: str

@app.post("/sentiment", response_model=SentimentResponse)
async def analyze_sentiment(request: SentimentRequest):
    """
    Endpoint principal de análisis.
    Recibe texto y devuelve sentimiento, probabilidad y explicabilidad (top features).
    """
    if not request.text or len(request.text.strip()) < 3:
        return {
            "prevision": "Neutral",
            "probabilidad": 0.5,
            "top_features": "texto insuficiente"
        }

    if not ai_engine:
        raise HTTPException(status_code=500, detail="Motor de IA no inicializado")

    # 1. Obtener predicción base de la IA
    pred_ia, prob_ia = ai_engine.predict_raw(request.text)
    
    # 2. Refinar con el Motor Híbrido G68
    res = enriquecer_respuesta(request.text, pred_ia, prob_ia, ai_engine)
    
    # 3. Normalización final según contrato estricto
    label = res["prevision"]
    if label == "Neutro":
        label = "Neutral"
        
    return {
        "prevision": label,
        "probabilidad": res["probabilidad"],
        "top_features": res["top_features"]
    }

@app.get("/health")
async def health_check():
    return {"status": "online", "engine": "G68-Supreme"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
