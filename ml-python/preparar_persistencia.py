
import pandas as pd
import joblib
import os
import sys
import re

# 1. Rutas y carga de motor G68
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, 'src'))
from engine.sentiment_engine import analizar_sentimiento_hibrido

# Carga de modelos
model = joblib.load(os.path.join(BASE_DIR, 'data', 'models', 'sentiment_model.pkl'))
vectorizer = joblib.load(os.path.join(BASE_DIR, 'data', 'models', 'tfidf_vectorizer.pkl'))

# 2. Mapa de Áreas Operativas G68
category_map = {
    'LIMPIEZA': ['moho', 'sucio', 'suciedad', 'mancha', 'olor', 'humedad', 'asco', 'pésimo', 'mugre', 'pelos'],
    'SERVICIO': ['amable', 'atento', 'demora', 'espera', 'tardan', 'grosero', 'personal', 'recepción', 'atención'],
    'CONFORT': ['comodo', 'almohadas', 'colchon', 'ruido', 'bulla', 'calor', 'frio', 'aire', 'dormir', 'cama'],
    'INFRAESTRUCTURA': ['wifi', 'roto', 'viej', 'antiguo', 'ascensor', 'piscina', 'baño', 'internet', 'ducha']
}

def get_area_responsable(text):
    text = text.lower()
    for area, terms in category_map.items():
        if any(term in text for term in terms):
            return area
    return 'GERENCIA' # Categoría por defecto para casos generales

# 3. Procesamiento del Dataset para Persistencia
def preparar_dataset_persistente(path_input, path_output):
    print(f"--- Iniciando Transformación de Datos para Persistencia ---")
    df = pd.read_csv(path_input)
    
    # Limpieza inicial
    df.dropna(subset=['review_text'], inplace=True)
    
    # Aplicar Motor Híbrido y Enriquecimiento
    print("Analizando sentimientos y extrayendo explicabilidad...")
    resultados = df['review_text'].apply(lambda x: analizar_sentimiento_hibrido(x, model, vectorizer))
    
    df['prevision'] = [r[0] for r in resultados]
    df['probabilidad'] = [r[1] for r in resultados]
    df['palabras_clave'] = [r[2].get('explicabilidad') for r in resultados]
    
    print("Categorizando áreas responsables...")
    df['area_responsable'] = df['review_text'].apply(get_area_responsable)
    
    # Agregar timestamp simulado para históricos (opcional pero recomendado para DB)
    df['fecha_registro'] = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Guardar Dataset Enriquecido
    df.to_csv(path_output, index=False)
    print(f"✅ Dataset para BD guardado en: {path_output}")
    print(f"--- Columnas creadas: prevision, probabilidad, palabras_clave, area_responsable, fecha_registro ---")

if __name__ == "__main__":
    input_csv = os.path.join(BASE_DIR, 'data', 'raw', 'Big_AHR.csv')
    output_csv = os.path.join(BASE_DIR, 'data', 'processed', 'Dataset_Persistencia_G68.csv')
    preparar_dataset_persistente(input_csv, output_csv)
