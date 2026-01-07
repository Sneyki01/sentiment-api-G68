
import joblib
import os
import sys
import re

# Asegurar rutas absolutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, 'src'))
from engine.sentiment_engine import analizar_sentimiento_hibrido

model_path = os.path.join(BASE_DIR, 'data', 'models', 'sentiment_model.pkl')
vector_path = os.path.join(BASE_DIR, 'data', 'models', 'tfidf_vectorizer.pkl')

model = joblib.load(model_path)
vectorizer = joblib.load(vector_path)

texto = 'Es algo tonto dejar de mencionar un servicio como el que recibimos en el hotel., personal decepte, bien presentado, la comida normal bien sasonada, algo lejanos del centro de la ciudad, las habitaciones con algo de moho en las paredes, buen servicio de internet y wifi, enn general como sitio de paso por cuestiones laborales es un buen lugar ya que no se permanece durante el dia.'

print("--- ANALIZANDO CON EXPLICABILIDAD G68 ---")
prevision, prob, meta = analizar_sentimiento_hibrido(texto, model, vectorizer)

print(f'\nRESULTADO FINAL: {prevision}')
print(f'CONFIANZA HIBRIDA: {prob}')
print(f'EXPLICABILIDAD: {meta.get("explicabilidad")}')
print(f'NOTA TECNICA: {meta.get("nota_tecnica")}')
print("-" * 40)
print(f'ML PURA: {meta.get("ml_original")}')
print(f'AJUSTE SEMANTICO: {meta.get("ajuste_semantico")}')
