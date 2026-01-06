import pickle
import os
import sys
from nltk.stem import SnowballStemmer

# 1. Definimos la clase dentro del script para que el .pkl sea autosuficiente
class SentimentLabG68:
    def __init__(self, lexicon_path, alpha=0.15):
        self.stemmer = SnowballStemmer('spanish')
        self.alpha = alpha
        self.negations = {'no', 'sin', 'nunca', 'jamas', 'nada'}
        self.intensifiers = {'muy', 'super', 'bastante', 'demasiado'}
        with open(lexicon_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.lexicon = {self.stemmer.stem(k): v for k, v in data.items()}

# 2. Código de exportación
import json
ruta_lexicon = "data/lexicon/lexicon_final_optimizado.json"
ruta_destino = "data/models/modelo_sentimiento_pipeline.pkl"

if os.path.exists(ruta_lexicon):
    # Creamos la instancia con tus reglas de contrato
    modelo_final = SentimentLabG68(ruta_lexicon, alpha=0.15)
    
    # Creamos la carpeta si no existe
    os.makedirs(os.path.dirname(ruta_destino), exist_ok=True)
    
    # Sobreescribimos el archivo antiguo con el nuevo
    with open(ruta_destino, "wb") as f:
        pickle.dump(modelo_final, f)
    
    print(f"✅ ARCHIVO ACTUALIZADO: {ruta_destino}")
    print("🚀 Ahora estás 100% seguro de que entregas el modelo con Raíces y Balance G68.")
else:
    print("❌ No se encontró el Lexicón en la ruta especificada.")