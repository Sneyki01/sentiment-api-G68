import os
import sys
import joblib

# Asegurar que encuentre la carpeta src
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, "src"))

from engine.sentiment_engine import analizar_sentimiento_hibrido

def exportar_estado_modelo():
    MODEL_PATH = os.path.join(BASE_DIR, "data", "models", "sentiment_model.pkl")
    VECTOR_PATH = os.path.join(BASE_DIR, "data", "models", "tfidf_vectorizer.pkl")
    
    if os.path.exists(MODEL_PATH) and os.path.exists(VECTOR_PATH):
        print("✅ Modelos encontrados y listos para produccion.")
        return True
    else:
        print("❌ Modelos no encontrados en data/models/")
        return False

if __name__ == "__main__":
    exportar_estado_modelo()