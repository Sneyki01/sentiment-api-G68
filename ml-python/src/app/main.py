from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import re
import os
import sys

# Asegurar que encuentre la carpeta raíz de src
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(BASE_DIR, "src"))

from engine.sentiment_engine import analizar_sentimiento_hibrido
from app.utils import guardar_prediccion, obtener_datos_dashboard

# 1. Definimos la estructura de la petición (ESTO DEBE IR PRIMERO)
class SentimentRequest(BaseModel):
    text: str

app = FastAPI(
    title="Sentiment Pro API - G68", 
    description="Sistema Híbrido ML + Reglas",
    version="2.1"
)

# 2. Configuración de rutas (relativas a la raíz ml-python)
MODEL_PATH = os.path.join(BASE_DIR, "data", "models", "sentiment_model.pkl")
VECTOR_PATH = os.path.join(BASE_DIR, "data", "models", "tfidf_vectorizer.pkl")

# 3. Carga de archivos
try:
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTOR_PATH)
    print("✅ Modelo y Vectorizador G68 cargados exitosamente")
except Exception as e:
    print(f"❌ Error crítico al cargar: {e}")
    model = None
    vectorizer = None

# 4. Diccionarios para Sarcasmo
disparadores_negativos = ["suci", "asc", "mugr", "pelos", "cucarach", "chinch", "hedor", "podrid", "pésim", "rot", "viej", "rob", "estaf"]
cebos_positivos = ["excelente", "increíble", "maravilla", "perfecto", "genial", "recomiendo", "fantástico"]

# 5. Utilidades
def limpieza_texto(texto: str):
    texto = texto.lower()
    texto = re.sub(r'[^a-zñáéíóúü\s]', '', texto)
    return texto.strip()

# 6. Endpoints
@app.get("/")
def home():
    return {"status": "API G68 Online", "modelo": "Cargado"}

@app.post("/predict/sentiment")
async def predict_sentiment(request: SentimentRequest):
    if not request.text:
        raise HTTPException(status_code=400, detail="El texto no puede estar vacío")
    
    if model is None or vectorizer is None:
        raise HTTPException(status_code=500, detail="Modelo no disponible")

    # A. Filtro de longitud (Regla de negocio unificada)
    if len(request.text.strip()) < 3:
        return {
            "prevision": "Neutro",
            "probabilidad": 0.5,
            "explicabilidad": "Texto muy corto para análisis"
        }

    # B. Uso del Motor Híbrido Centralizado
    resultado, prob, meta = analizar_sentimiento_hibrido(request.text, model, vectorizer)

    # C. Lógica de Sarcasmo (Mantenida como capa superior)
    texto_limpio = request.text.lower()
    if resultado == "Positivo":
        if any(pos in texto_limpio for pos in cebos_positivos) and \
           any(neg in texto_limpio for neg in disparadores_negativos):
            resultado = "Negativo"
            meta["explicabilidad"] += " | Detección de Sarcasmo"

    # D. Persistencia en Base de Datos
    guardar_prediccion(request.text, resultado, prob, meta.get("explicabilidad", ""))

    # RETORNO ESTRICTO SEGÚN CONTRATO CONGELADO (3 CAMPOS)
    return {
        "prevision": resultado,
        "probabilidad": prob,
        "explicabilidad": meta.get("explicabilidad", "Análisis basado en patrones")
    }

@app.get("/dashboard/stats")
def get_stats():
    """Endpoint para alimentar dashboards externos o internos."""
    return obtener_datos_dashboard()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)