from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import re

# 1. Cargar el "cerebro" (tus archivos descargados)
# Asegúrate de que los nombres de los archivos coincidan exactamente
modelo = joblib.load("ml-python/data/models/sentiment_model.pkl")
vectorizador = joblib.load("ml-python/data/models/tfidf_vectorizer.pkl")

# 2. Configurar la aplicación FastAPI
app = FastAPI(title="Servicio de Análisis de Sentimientos")

# 3. Definir el Contrato de Integración (lo que recibe la API)
class PeticionSentiment(BaseModel):
    text: str

# 4. Función de limpieza (IDÉNTICA a la de Colab)
def limpieza_pro(texto):
    texto = str(texto).lower()
    # Mantenemos letras, ñ y vocales con tilde. Borramos números y símbolos.
    texto = re.sub(r'[^a-zñáéíóúü\s]', '', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto

# 5. Endpoint de Predicción
@app.post("/sentiment")
async def predecir_sentimiento(data: PeticionSentiment):
    # Validación mínima exigida en los lineamientos
    if not data.text or len(data.text) < 3:
        raise HTTPException(status_code=400, detail="El texto es demasiado corto o inexistente")
    
    try:
        # Limpiar el texto que viene del Backend
        texto_limpio = limpieza_pro(data.text)
        
        # Convertir a vector numérico
        vector = vectorizador.transform([texto_limpio])
        
        # Realizar la predicción
        prediccion = modelo.predict(vector)[0]
        
        # Devolver el resultado según el contrato oficial
        return {
            "prevision": prediccion,
            "probabilidad": 1.0  # SVM Linear no da probabilidad directa, pero cumplimos el campo
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")

# Para ejecutar: uvicorn main:app --reload


