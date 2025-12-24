import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
import os

# --- CONFIGURACIÓN DE RUTAS ---
# Se utiliza una ruta relativa al archivo para asegurar portabilidad en contenedores Docker o servidores Linux.
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'data', 'models', 'modelo_sentimiento_pipeline.pkl')

app = FastAPI(
    title="Análisis de Sentimiento - Hotel Reviews",
    version="1.1.0",
    description="API de clasificación de texto. Requiere scikit-learn e imbalanced-learn para cargar el Pipeline."
)

# Variable global para mantener el modelo en memoria (Singleton pattern) y evitar recargas costosas.
model_pipeline = None

@app.on_event("startup")
async def load_artifacts():
    """
    Carga de artefactos al iniciar el servidor. 
    Es crítico que el archivo .pkl exista en la ruta especificada antes de recibir peticiones.
    """
    global model_pipeline
    try:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Archivo de modelo no encontrado en: {MODEL_PATH}")
            
        # IMPORTANTE: joblib requiere que las librerías con las que se entrenó (imblearn) estén instaladas.
        model_pipeline = joblib.load(MODEL_PATH)
        print("✅ Pipeline de producción cargado correctamente.")
    except Exception as e:
        print(f"❌ ERROR CRÍTICO: No se pudo inicializar el modelo. Detalle: {e}")
        # En producción, si el modelo no carga, el servicio debe fallar (fail-fast).
        raise RuntimeError("Fallo en la carga del modelo de IA.")

# --- ESQUEMAS DE VALIDACIÓN (Pydantic) ---
class TextIn(BaseModel):
    """Estructura de entrada esperada por el endpoint."""
    # min_length=1 asegura que no sea un string vacío a nivel de esquema
    text: str = Field(..., min_length=1, example="La ubicación es perfecta, pero el ruido era excesivo.")

    @field_validator('text')
    @classmethod
    def validate_content(cls, v: str) -> str:
        # 1. Verificación de tipo estricta (opcional, Pydantic suele manejarlo)
        if not isinstance(v, str):
            raise ValueError('El valor debe ser una cadena de texto (string).')

        # 2. .strip() elimina espacios al inicio y final
        cleaned_text = v.strip()
        
        # 3. Validar que no esté vacío después de limpiar
        if not cleaned_text:
            raise ValueError('El texto no puede estar vacío o contener solo espacios.')
        
        # 4. Validar que no sea solo un número
        # Esto evita que envíen "12345" y el modelo intente predecirlo
        if cleaned_text.isdigit():
            raise ValueError('El texto no puede ser únicamente numérico; debe ser una reseña real.')

        return cleaned_text

class PredictionOut(BaseModel):
    """Contrato de salida JSON para el cliente/frontend."""
    prevision: str
    probabilidad: float

@app.get("/")
async def root():
    return {
        "message": "API de Análisis de Sentimiento Activa",
        "puerto": 8080,
        "docs": "/docs"
    }

# --- ENDPOINTS ---
@app.post("/predict/sentiment", response_model=PredictionOut)
async def predict_sentiment(data: TextIn):
    """
    Endpoint principal. El Pipeline realiza:
    1. Preprocesamiento (limpieza).
    2. Vectorización (TF-IDF).
    3. Clasificación (LinearSVC).
    """
    if model_pipeline is None:
        raise HTTPException(status_code=503, detail="Modelo no cargado en el servidor.")

    try:
        # Predicción de clase (Positivo/Negativo/Neutro)
        prevision = model_pipeline.predict([data.text])[0]

        # Cálculo de confianza: LinearSVC no posee predict_proba nativo.
        # Se aplica una función sigmoide sobre el decision_function para normalizar el score.
        decision_score = model_pipeline.decision_function([data.text])
        probabilidad = 1 / (1 + np.exp(-np.max(decision_score)))

        return PredictionOut(
            prevision=str(prevision),
            probabilidad=round(float(probabilidad), 3)
        )
    except Exception as e:
        # Registro de errores internos para monitoreo
        print(f"Error en inferencia: {e}")
        raise HTTPException(status_code=500, detail="Error interno al procesar la predicción.")

# --- PUNTO DE ENTRADA LOCAL ---
# Permite ejecutar con 'python main.py' además de 'uvicorn main:app'
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080) # 0.0.0.0 es necesario para despliegues en la nube/Docker.

# ==============================================================================
# 📋 GUÍA DE EJECUCIÓN Y PRUEBAS LOCALES
# ==============================================================================
#
# 1. INSTALACIÓN DE DEPENDENCIAS (Si es la primera vez):
#    pip install fastapi uvicorn joblib scikit-learn imbalanced-learn numpy
#
# 2. ARRANCAR LA API:
#    Desde la terminal, ubicado en la carpeta 'datascience', ejecuta:
#    uvicorn main:app --reload --port 8080
#
# 3. CÓMO VER LA INFORMACIÓN:
#    - Raíz (Estado): http://127.0.0.1:8080/
#    - Documentación Interactiva (Probar modelo): http://127.0.0.1:8080/docs
#    - Esquema Técnico: http://127.0.0.1:8080/openapi.json
#
# 4. PASOS PARA PROBAR UNA RESEÑA:
#    a. Entra a http://127.0.0.1:8080/docs
#    b. Haz clic en el botón verde 'POST /predict/sentiment'
#    c. Haz clic en 'Try it out'
#    d. Cambia el texto en el JSON y presiona 'Execute'
#
# 5. DETENER EL SERVIDOR:
#    Presiona Ctrl + C en la terminal.
# ==============================================================================