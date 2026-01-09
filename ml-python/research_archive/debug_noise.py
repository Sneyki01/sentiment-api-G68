import os
import sys
import re
from nltk.stem import SnowballStemmer
import joblib

# Setup paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, "src"))

from engine.sentiment_engine import analizar_sentimiento_hibrido

# Mock model and vectorizer
class MockModel:
    def predict_proba(self, v):
        return [[0.1, 0.4, 0.5]]

class MockVec:
    def transform(self, t):
        return None

# Load actual model to be sure
model_path = os.path.join(BASE_DIR, "data", "models", "sentiment_model.pkl")
vector_path = os.path.join(BASE_DIR, "data", "models", "tfidf_vectorizer.pkl")
modelo = joblib.load(model_path)
vectorizador = joblib.load(vector_path)

text = "%&$/Cucarachas en la camacc¡?=)(/%"
print(f"Testing text: {text}")

pred, prob, meta = analizar_sentimiento_hibrido(text, modelo, vectorizador)

print(f"Result: {pred}")
print(f"Prob: {prob}")
print(f"Meta: {meta}")
