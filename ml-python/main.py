   
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import re
import os

app = FastAPI(
    title="Sentiment Pro API",
    description="Sistema Híbrido de Análisis de Sentimiento (ML + Reglas Semánticas)",
    version="2.1"
)

# --- CONFIGURACIÓN DE RUTAS Y MODELOS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "data", "models", "sentiment_model.pkl")
VECTOR_PATH = os.path.join(BASE_DIR, "data", "models", "tfidf_vectorizer.pkl")

try:
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTOR_PATH)
except Exception as e:
    print(f"Error crítico al cargar modelos: {e}")

# --- DICCIONARIOS PARA MOTOR DE REGLAS (Sarcasmo) ---
disparadores_negativos = [
    "suci", "asc", "mugr", "pelos", "cucarach", "chinch", "hedor", "podrid", 
    "grit", "gros", "maltrat", "prepotent", "humill", "ignor", "pésim", 
    "rot", "viej", "ruid", "rob", "estaf", "enga", "fals", "fraud", "caro"
]
cebos_positivos = [
    "excelente", "increíble", "maravilla", "perfecto", "genial", 
    "recomiendo", "fantástico", "encant", "buenis", "magnif"
]

# --- UTILIDADES ---
class SentimentRequest(BaseModel):
    text: str

def limpieza_texto(texto: str):
    texto = texto.lower()
    texto = re.sub(r'[^a-zñáéíóúü\s]', '', texto)
    return texto.strip()

# --- ENDPOINT PRINCIPAL ---
@app.post("/predict/sentiment")
async def predict_sentiment(request: SentimentRequest):
    if not request.text:
        raise HTTPException(status_code=400, detail="El texto no puede estar vacío")

    texto_original = request.text
    texto_limpio = limpieza_texto(texto_original)

    # 1. FILTRO DE SEGURIDAD (Neutro por ruido/brevedad)
    if len(texto_limpio.split()) < 3:
        return {
            "prevision": "Neutro",
            "probabilidad_ml": 0.0,
            "meta": {"nota": "Texto demasiado corto o sin carga semántica clara."}
        }

    # 2. INFERENCIA ML BINARIA
    vector = vectorizer.transform([texto_limpio])
    probs = model.predict_proba(vector)[0]  # [Prob_Neg, Prob_Pos]
    conf_neg, conf_pos = probs[0], probs[1]
    
    # 3. LÓGICA TERCIARIA (Detección de Neutros por Incertidumbre)
    # Si la diferencia es pequeña, el modelo no está seguro -> Neutro
    diferencia = abs(conf_pos - conf_neg)
    UMBRAL_NEUTRO = 0.22 

    if diferencia < UMBRAL_NEUTRO:
        return {
            "prevision": "Neutro",
            "probabilidad_ml": round(float(np.max(probs)), 4),
            "meta": {"nota": "Opinión informativa o ambigua detectada."}
        }

    # 4. MOTOR DE REGLAS (Detección de Sarcasmo)
    resultado = "Positivo" if conf_pos > conf_neg else "Negativo"
    es_sarcasmo = False

    if resultado == "Positivo":
        # Si dice algo "bueno" pero contiene una palabra de "queja crítica"
        if any(pos in texto_limpio for pos in cebos_positivos) and \
           any(neg in texto_limpio for neg in disparadores_negativos):
            resultado = "Negativo (Sarcasmo)"
            es_sarcasmo = True

    return {
        "prevision": resultado,
        "probabilidad_ml": round(float(np.max(probs)), 4),
        "meta": {
            "deteccion_sarcasmo": es_sarcasmo,
            "confianza_negativa": round(float(conf_neg), 4),
            "confianza_positiva": round(float(conf_pos), 4)
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080) 