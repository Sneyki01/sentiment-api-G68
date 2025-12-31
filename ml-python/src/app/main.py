from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
import tensorflow as tf
from tensorflow.keras.preprocessing.text import tokenizer_from_json
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import json
import os
from .utils import clean_text_optimized # Usamos tu limpieza

app = FastAPI(title="G68 - Hotel Sentiment API (LSTM)", version="2.0.0")

# --- CARGA DE MODELO Y TOKENIZER ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Ajustamos rutas para que funcionen tanto local como en Docker
MODEL_PATH = os.path.join(BASE_DIR, "../../data/models/modelo_lstm_v2.keras")
TOKENIZER_PATH = os.path.join(BASE_DIR, "../../data/models/tokenizer.json")
MAPPING_PATH = os.path.join(BASE_DIR, "../../data/models/label_mapping.json")

# Cargamos en memoria al iniciar
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    with open(TOKENIZER_PATH, 'r') as f:
        tokenizer = tokenizer_from_json(json.load(f))
    with open(MAPPING_PATH, 'r') as f:
        labels_map = {int(k): v for k, v in json.load(f).items()}
except Exception as e:
    print(f"❌ Error al cargar artefactos: {e}")
    model = None

class SentimentRequest(BaseModel):
    text: str = Field(..., min_length=1, example="Excelente atención y ubicación.")

    @validator('text')
    def validate_content(cls, v):
        if v.strip().isdigit():
            raise ValueError('El texto no puede ser solo números.')
        return v

@app.post("/predict/sentiment")
async def predict(request: SentimentRequest):
    if model is None:
        raise HTTPException(status_code=503, detail="Modelo no disponible")

    # 1. Limpieza con tu lógica optimizada
    clean_text = clean_text_optimized(request.text)
    
    if not clean_text:
        raise HTTPException(status_code=422, detail="Texto sin contenido útil tras limpieza.")

    # 2. Tokenización y Padding (Igual que en el entrenamiento)
    seq = tokenizer.texts_to_sequences([clean_text])
    padded = pad_sequences(seq, maxlen=200, padding="post")

    # 3. Inferencia (Probabilidades Reales Softmax)
    predictions = model.predict(padded)[0]
    idx = np.argmax(predictions)
    
    return {
        "text_original": request.text,
        "prevision": labels_map[idx],
        "probabilidad": round(float(predictions[idx]), 4),
        "metodo": "Deep Learning (Bi-LSTM)"
    }