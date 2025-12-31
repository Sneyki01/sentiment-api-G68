import os
import re
import sys
import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator # <--- Importante para los Schemas integrados

# 1. CONFIGURACIÓN DE RUTAS 
# Añadimos la carpeta actual al path para asegurar que encuentre utils.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils import clean_text

# =============================================================================
# SCHEMAS (Modelos de datos integrados)
# =============================================================================

class TextIn(BaseModel):
    """Estructura de entrada para la reseña"""
    # Validamos que sea string y tenga longitud mínima de 1 (no vacío)
    text: str = Field(..., min_length=1, example="La comida estuvo excelente.")

    @field_validator('text')
    @classmethod
    def validate_content(cls, v):
        # 1. Quitar espacios en blanco extremos y verificar si queda vacío
        content = v.strip()
        if not content:
            raise ValueError('El texto no puede estar vacío o contener solo espacios.')
        
        # 2. Verificar si es solo números
        if content.isdigit():
            raise ValueError('El texto no puede ser únicamente numérico.')
        
        # 3. Verificar si contiene demasiados números (opcional, pero recomendado)
        # Si quieres rechazar cualquier cosa que tenga números mezclados, usa:
        # if any(char.isdigit() for char in content):
        #     raise ValueError('No se permiten números en la reseña.')

        return content

class PredictionOut(BaseModel):
    """Estructura de salida de la API"""
    prevision: str
    probabilidad: float

# =============================================================================
# CONFIGURACIÓN GENERAL Y RUTAS DE ARCHIVOS
# =============================================================================

# Localizamos el archivo .pkl subiendo niveles desde src/app hasta ml-python/data/models
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_PATH = os.path.join(BASE_DIR, 'data', 'models', 'modelo_sentimiento_pipeline.pkl')

app = FastAPI(
    title="Sentiment Analysis API",
    description=(
        "Microservicio de inferencia para análisis de sentimiento. "
        "El modelo fue entrenado priorizando el recall de la clase NEGATIVO."
    ),
    version="1.1.0"
)

# Singleton para el modelo
model_pipeline = None

# =============================================================================
# EVENTOS DE SERVIDOR
# =============================================================================

@app.on_event("startup")
async def load_model():
    """Carga el pipeline al iniciar el servicio (Fail-fast)"""
    global model_pipeline
    try:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"No se encontró el archivo .pkl en: {MODEL_PATH}")

        model_pipeline = joblib.load(MODEL_PATH)
        print("✅ MODELO CARGADO: Pipeline listo para inferencia.")
    except Exception as e:
        print(f"❌ ERROR CRÍTICO: {e}")
        # El servidor no arrancará si esto falla
        raise RuntimeError("No se pudo inicializar el modelo de IA.")

# =============================================================================
# ENDPOINTS
# =============================================================================

@app.get("/")
async def root():
    return {
        "message": "API de Análisis de Sentimiento activa",
        "docs": "/docs",
        "status": "OK"
    }

@app.post("/predict/sentiment", response_model=PredictionOut)
async def predict_sentiment(payload: TextIn):
    """
    Endpoint principal. Realiza limpieza, predicción y cálculo de confianza.
    """
    if model_pipeline is None:
        raise HTTPException(status_code=503, detail="Modelo no disponible")

    try:
        # Limpieza (utils.py)
        cleaned_text = clean_text(payload.text)

        # Validación extra: Si tras limpiar el texto (quitar stop words, etc) queda vacío
        if not cleaned_text or cleaned_text.isspace():
            raise HTTPException(
                status_code=422, 
                detail="El texto procesado no contiene palabras válidas para analizar."
            )

        # Inferencia
        prediction = model_pipeline.predict([cleaned_text])[0]
        decision_score = model_pipeline.decision_function([cleaned_text])
        probability = 1 / (1 + np.exp(-np.max(decision_score)))

        return PredictionOut(
            prevision=str(prediction),
            probabilidad=round(float(probability), 3)
        )

    except ValueError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error en el procesamiento")

# --- PUNTO DE ENTRADA LOCAL ---
# Permite ejecutar con 'python main.py' además de 'uvicorn main:app'
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080) # 0.0.0.0 es necesario para despliegues en la nube/Docker.