from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field
import joblib
import os
import sys
import datetime
import traceback

# Asegurar que encuentre la carpeta raíz de src
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC_DIR = os.path.join(BASE_DIR, "src")
sys.path.append(SRC_DIR)

try:
    from engine.sentiment_engine import analizar_sentimiento_hibrido, LEXICON_G68
except ModuleNotFoundError as e:
    print(f"❌ Error de Importación: No se encuentra el módulo 'engine'.")
    print(f"   Ruta buscada: {SRC_DIR}")
    print(f"   Detalle: {e}")
    sys.exit(1)

# 1. Definimos la estructura de la petición (Modelo TextIn según contrato)
class TextIn(BaseModel):
    text: str = Field(min_length=1, max_length=5000, description="El texto no puede estar vacío")

app = FastAPI(
    title="Sentiment Pro API - G68", 
    description="Sistema Híbrido ML + Reglas (MVP)",
    version="2.4"
)

# 2. Configuración de rutas
MODEL_PATH = os.path.join(BASE_DIR, "data", "models", "sentiment_model.pkl")
VECTOR_PATH = os.path.join(BASE_DIR, "data", "models", "tfidf_vectorizer.pkl")

# 3. Carga de archivos (Gestión de 503 Service Unavailable)
try:
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTOR_PATH)
    print(f"✅ Pipeline de producción cargado correctamente desde: {MODEL_PATH}")
except Exception as e:
    print(f"❌ Error crítico al cargar modelo: {e}")
    model = None
    vectorizer = None

# 4. Endpoints
@app.get("/", include_in_schema=False)
def home():
    """Redirige automáticamente a la documentación Swagger."""
    return RedirectResponse(url="/docs")

@app.post("/predict/sentiment")
async def predict_sentiment(request: TextIn):
    # Log de Petición (Trazabilidad)
    hora_peticion = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{hora_peticion}] 📩 Petición recibida: POST /predict/sentiment")

    # Validación de longitud mínima (400 Bad Request)
    if not request.text or len(request.text.strip()) < 3:
        raise HTTPException(
            status_code=400, 
            detail="Solicitud Incorrecta: El mensaje es demasiado corto (mínimo 3 caracteres)."
        )
    
    # Validación de carga de modelo (503 Service Unavailable)
    if model is None or vectorizer is None:
        raise HTTPException(
            status_code=503, 
            detail="Modelo no cargado en el servidor"
        )

    # Garantizamos que `meta` exista aunque falle el motor
    meta = {}
    try:
        # Uso del Motor Híbrido Centralizado G68
        resultado, prob, meta = analizar_sentimiento_hibrido(request.text, model, vectorizer)

        # Construir explicabilidad basada en léxico (Optimizada G68)
        # Ahora el motor devuelve directamente la estructura limpia
        explicabilidad = meta.get("explicabilidad", {"triggers": [], "areas": []})
        return {
            "prevision": resultado,
            "probabilidad": prob,
            "explicabilidad": explicabilidad
        }
    except Exception as e:
        # Error log (Resiliencia - Error 500)
        print(f"❌ Error interno al procesar la predicción: {e}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail="Error interno al procesar la predicción"
        )

if __name__ == "__main__":
    import uvicorn
    print("🚀 Servidor iniciando...")
    print("👉 Abre esta URL para verificar: http://localhost:8080/docs")
    uvicorn.run(app, host="0.0.0.0", port=8080)
