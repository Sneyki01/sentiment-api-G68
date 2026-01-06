from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import re
import os

# 1. Definimos la estructura de la petición (ESTO DEBE IR PRIMERO)
class SentimentRequest(BaseModel):
    text: str

app = FastAPI(
    title="Sentiment Pro API - G68", 
    description="Sistema Híbrido ML + Reglas",
    version="2.1"
)

# 2. Configuración de rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
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

    # A. Filtro de 3 caracteres (Regla de negocio)
    if len(request.text.strip()) < 3:
        return {
            "prevision": "Neutro",
            "probabilidad_ml": 0.0,
            "meta": {"nota": "Rechazado: Mínimo 3 caracteres requerido."}
        }

    texto_limpio = limpieza_texto(request.text)

    # B. Inferencia ML
    vectorizado = vectorizer.transform([texto_limpio])
    probs = model.predict_proba(vectorizado)[0]
    conf_neg, conf_pos = probs[0], probs[1]

    # C. Lógica de Neutros (Umbral 0.22)
    diferencia = abs(conf_pos - conf_neg)
    if diferencia < 0.22:
        return {
            "prevision": "Neutro",
            "probabilidad_ml": round(float(np.max(probs)), 4),
            "meta": {"nota": "Opinión informativa o ambigua."}
        }

    # D. Motor de Sarcasmo
    resultado = "Positivo" if conf_pos > conf_neg else "Negativo"
    es_sarcasmo = False

    if resultado == "Positivo":
        if any(pos in texto_limpio for pos in cebos_positivos) and \
           any(neg in texto_limpio for neg in disparadores_negativos):
            resultado = "Negativo (Sarcasmo)"
            es_sarcasmo = True

    return {
        "prevision": resultado,
        "probabilidad_ml": round(float(np.max(probs)), 4),
        "meta": {
            "deteccion_sarcasmo": es_sarcasmo,
            "confianza_positiva": round(float(conf_pos), 4),
            "confianza_negativa": round(float(conf_neg), 4)
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)