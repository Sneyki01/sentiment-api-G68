import os
import sys
import joblib

# Setup paths
PROJECT_ROOT = os.getcwd()
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
sys.path.append(SRC_DIR)

from engine.sentiment_engine import analizar_sentimiento_hibrido

# Paths to models
MODEL_PATH = os.path.join(PROJECT_ROOT, "data", "models", "sentiment_model.pkl")
VECTOR_PATH = os.path.join(PROJECT_ROOT, "data", "models", "tfidf_vectorizer.pkl")

print(f"Cargando modelos desde {MODEL_PATH}...")
model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTOR_PATH)

def test(text):
    print(f"\n--- Probando: '{text}' ---")
    res, prob, meta = analizar_sentimiento_hibrido(text, model, vectorizer)
    print(f"RESULTADO: {res} ({prob})")
    print(f"DETALLES: {meta['explicabilidad']}")

if __name__ == "__main__":
    test("Excelente servicio y habitación muy limpia.")
    test("Había cucarachas en el baño y el personal fue grosero.")
    test("El hotel es regular, nada del otro mundo.")
