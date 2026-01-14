import os
import sys
from fastapi import FastAPI
from pydantic import BaseModel

# --- CONFIGURACIÓN DE RUTAS ---
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
if src_dir not in sys.path:
    sys.path.append(src_dir)

from engine.sentiment_engine import SentimentEngine
from motor_hibrido import enriquecer_respuesta

app = FastAPI(
    title="G68 Sentiment API - FULL INTELLIGENCE",
    description="Motor Híbrido con Explicabilidad, Sarcasmo y Clasificación de Departamentos"
)

# Inicializamos el motor de IA
ai_engine = SentimentEngine()

class SentimentRequest(BaseModel):
    text: str

@app.get("/")
def home():
    return {"status": "G68 Online", "mode": "FULL_INTELLIGENCE"}

@app.post("/predict/sentiment")
async def predict(request: SentimentRequest):
    """
    Endpoint FULL. Devuelve prevision, probabilidad, hallazgos y departamentos.
    """
    if not request.text or len(request.text.strip()) < 3:
        return {"error": "Text too short", "status": 400}

    pred_ia, prob_ia = ai_engine.predict_raw(request.text)
    resultado_full = enriquecer_respuesta(request.text, pred_ia, prob_ia)
    
    # En esta rama NO filtramos, entregamos todo el valor de G68
    return resultado_full

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)