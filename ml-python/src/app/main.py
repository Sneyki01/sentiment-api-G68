from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import numpy as np
import re
import os
import sys

# Asegurar que encuentre la carpeta raíz de src
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(BASE_DIR, "src"))

from engine.sentiment_engine import analizar_sentimiento_hibrido

# 1. Definimos la estructura de la petición (Modelo TextIn según contrato)
class TextIn(BaseModel):
    text: str = Field(min_length=1, max_length=5000, description="El texto no puede estar vacío")

app = FastAPI(
    title="Sentiment Pro API - G68", 
    description="Sistema Híbrido ML + Reglas (MVP)",
    version="2.3"
)

# 2. Configuración de rutas (relativas a la raíz ml-python)
MODEL_PATH = os.path.join(BASE_DIR, "data", "models", "sentiment_model.pkl")
VECTOR_PATH = os.path.join(BASE_DIR, "data", "models", "tfidf_vectorizer.pkl")

# 3. Carga de archivos
try:
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTOR_PATH)
    print("✅ Pipeline de producción cargado correctamente.")
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
    return {"status": "API G68 Online (MVP)", "modelo": "Cargado"}

@app.post("/predict/sentiment")
async def predict_sentiment(request: TextIn):
    # Validación de texto vacío o solo espacios (400 Bad Request)
    if not request.text or request.text.isspace():
        raise HTTPException(
            status_code=400, 
            detail="El texto no puede estar vacío o contener solo espacios."
        )
    
    # Validación de carga de modelo (503 Service Unavailable)
    if model is None or vectorizer is None:
        raise HTTPException(
            status_code=503, 
            detail="Modelo no cargado en el servidor"
        )

    # A. Filtro de longitud técnica (Regla de negocio adicional)
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

    # RETORNO ESTRICTO SEGÚN CONTRATO CONGELADO (3 CAMPOS)
    return {
        "prevision": resultado,
        "probabilidad": prob,
        "explicabilidad": meta.get("explicabilidad", "Análisis basado en patrones")
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
