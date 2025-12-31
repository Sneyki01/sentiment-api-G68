from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field
import joblib
import re
import os

# 1. Configuración de la App con Metadatos Profesionales
app = FastAPI(
    title="Análisis de Sentimiento Pro - Grupo 68",
    description="Sistema híbrido: ML (LinearSVC) + Motor Semántico de Sarcasmo (+200 variantes)",
    version="2.1.0"
)

# 2. Estructura de la Petición
class PeticionSentiment(BaseModel):
    # Dejamos el min_length en 3 para que Pydantic haga un primer filtro de longitud bruta
    text: str = Field(..., min_length=3, description="Texto de la reseña")

# 3. Carga de Modelos (Solo una vez al inicio)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "data", "models", "sentiment_model.pkl")
VECTOR_PATH = os.path.join(BASE_DIR, "data", "models", "tfidf_vectorizer.pkl")

try:
    modelo = joblib.load(MODEL_PATH)
    vectorizador = joblib.load(VECTOR_PATH)
    print("✅ Motor de ML y Vectorizador cargados exitosamente")
except Exception as e:
    print(f"❌ Error crítico al cargar archivos .pkl: {e}")

# 4. Función de Limpieza Pro
def limpieza_pro(texto):
    texto = str(texto).lower()
    # Mantiene solo letras y espacios, eliminando símbolos y números
    texto = re.sub(r'[^a-zñáéíóúü\s]', '', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto

# 5. Manejador de Errores de Validación (Español)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={
            "status": "error",
            "mensaje": "El texto enviado es demasiado corto o inválido."
        }
    )

# 6. ENDPOINT PRINCIPAL (Cerebro del Proyecto)
@app.post("/predict/sentiment", tags=["Análisis de Cliente"])
async def predecir_sentimiento(data: PeticionSentiment):
    try:
        texto_original = data.text.strip()
        texto_min = texto_original.lower()
        
        # A. Limpieza para el análisis
        texto_limpio = limpieza_pro(texto_original)
        
        # 🛡️ FILTRO DE SEGURIDAD PARA SÍMBOLOS Y RUIDO
        # Si después de limpiar (quitar !!!, ???) quedan menos de 2 letras
        if len(texto_limpio.replace(" ", "")) < 2:
            return {
                "prevision": "Neutro / Solo Símbolos",
                "probabilidad_ml": 0.0,
                "meta": {
                    "deteccion_ironia": False,
                    "nota": "El mensaje no contiene texto analizable."
                }
            }

        # B. Inferencia de Machine Learning (Solo si hay texto real)
        vector = vectorizador.transform([texto_limpio])
        prediccion_ml = modelo.predict(vector)[0]
        probabilidades = modelo.predict_proba(vector)[0]
        max_prob = float(max(probabilidades))
        
        # C. MOTOR DE REGLAS DE SARCASMO (+200 variantes mediante raíces)
        disparadores = {
            "higiene": ["suci", "asc", "mugr", "pelos", "cucarach", "chinch", "hedor", "podrid", "manch", "limpiez", "basur", "moho", "apest", "pestil", "insect", "plag", "polv", "usad", "gras", "infect", "olía", "nause", "vomit", "fetid"],
            "servicio": ["grit", "gros", "maltrat", "prepotent", "humill", "ignor", "educac", "antip", "insult", "pésim", "inefic", "lent", "tard", "demor", "neglig", "mala gan", "descort", "burl", "atención", "espera", "filas", "tosco", "brut", "malhumor", "arrog", "groser"],
            "infraestructura": ["rot", "viej", "sin agua", "aire dañ", "ruid", "pared", "frí", "calor", "ascensor", "wifi", "internet", "enchufe", "luz", "ilumin", "incóm", "piedra", "humed", "goter", "clima", "ventan", "cortin", "tv", "televis", "control", "baño", "duch", "cañer", "toall"],
            "seguridad_dinero": ["rob", "estaf", "enga", "fals", "fraud", "peligros", "peor", "caro", "preci", "cobro", "extra", "abus", "factur", "tarjeta", "dinero", "pagu", "gast", "perdí", "segurid", "mied", "oscur", "asust", "ladron", "rater", "excesiv", "carisim", "publicid"],
            "lexico_negativo": ["chist", "brom", "joda", "vacil", "burla", "ironi", "desastr", "decepc", "horror", "terrib", "espant", "fatal", "asco", "deplor", "vergon", "pena", "lástim", "miser", "pobr", "fatal"]
        }

        cebos_positivos = [
            "excelente", "increíble", "maravilla", "perfecto", "genial", "recomiendo", 
            "fantástico", "encant", "buenis", "magnif", "estupend", "lindo", "bello", 
            "hermos", "amable", "limpio", "joya", "maravill"
        ]
        
        todas_las_quejas = [word for sublist in disparadores.values() for word in sublist]
        
        # D. Lógica de Re-Clasificación Semántica (Sarcasmo)
        es_sarcasmo = False
        
        if prediccion_ml == "Positivo":
            # Regla 1: Contradicción (Palabra positiva + Queja crítica)
            if any(pos in texto_min for pos in cebos_positivos) and any(queja in texto_min for queja in todas_las_quejas):
                es_sarcasmo = True
            
            # Regla 2: Conectores de contraste
            elif any(con in texto_min for con in [" pero ", " aunque ", " sin embargo "]) and any(q in texto_min for q in todas_las_quejas):
                es_sarcasmo = True
            
            # Regla 3: Temas Críticos (Higiene, Seguridad o Maltrato anulan el positivo automáticamente)
            elif any(q in texto_min for q in disparadores["higiene"] + disparadores["seguridad_dinero"] + ["grit"]):
                es_sarcasmo = True

        # E. Resultado Final
        resultado_final = "Negativo (Sarcasmo)" if es_sarcasmo else str(prediccion_ml)

        return {
            "prevision": resultado_final,
            "probabilidad_ml": round(max_prob, 4),
            "meta": {
                "deteccion_ironia": es_sarcasmo,
                "modelo_base": "LinearSVC",
                "version_motor": "v2.1-robusta"
            }
        }
        
    except Exception as e:
        # Registro detallado del error en consola para debugging
        print(f"Error interno detectado: {str(e)}")
        raise HTTPException(status_code=500, detail="Error en el motor semántico.")