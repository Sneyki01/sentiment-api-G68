
#Procesamiento por lotes de reseñas usando lógica híbrida

import pandas as pd
import os
import joblib
import unicodedata
from src.engine.sentiment_engine import analizar_sentimiento_hibrido

def limpiar_texto_vuelo(texto):
    """Limpia caracteres raros si se filtran por el encoding"""
    if not isinstance(texto, str): return ""
    # Normaliza y elimina acentos para evitar símbolos como 'Ã©'
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    ).replace('ñ', 'n').replace('Ñ', 'N')

def run_batch_process():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, 'data', 'models', 'sentiment_model.pkl')
    vectorizer_path = os.path.join(base_dir, 'data', 'models', 'tfidf_vectorizer.pkl')
    input_csv = os.path.join(base_dir, 'data', 'processed', 'mensajes_nuevos_largos.csv')
    output_csv = os.path.join(base_dir, 'data', 'processed', 'resultados_lote.csv')

    # 1. CARGA DE MODELOS
    print("⏳ Cargando modelos...")
    try:
        modelo = joblib.load(model_path)
        vectorizador = joblib.load(vectorizer_path)
    except Exception as e:
        return print(f"❌ Error de carga: {e}")

    # 2. CARGA DE DATOS CON ENCODING DE SEGURIDAD
    if not os.path.exists(input_csv):
        return print("❌ No existe el archivo de entrada.")

    # Usamos utf-8-sig para leer correctamente lo generado por el otro script
    df = pd.read_csv(input_csv, encoding='utf-8-sig')
    
    print(f"🚀 Procesando {len(df)} mensajes limpios...")

    # 3. LIMPIEZA Y ANÁLISIS
    # Primero limpiamos visualmente el texto antes de analizarlo
    df['review_text_clean'] = df['review_text_clean'].apply(limpiar_texto_vuelo)
    
    resultados = df['review_text_clean'].apply(
        lambda x: analizar_sentimiento_hibrido(x, modelo, vectorizador)
    )

    # 4. EXTRACCIÓN DE RESULTADOS
    df['prevision'] = [r[0] for r in resultados]
    df['probabilidad'] = [r[1] for r in resultados]
    df['probabilidad_ml_puro'] = [r[2].get('ml_original', 0.0) for r in resultados]
    df['nota'] = [r[2].get('nota_tecnica', 'Sin nota') for r in resultados]

    # 5. GUARDAR RESULTADO FINAL LIMPIO
    df.to_csv(output_csv, index=False, encoding='utf-8-sig')
    
    print("\n--- ✅ PROCESO COMPLETADO ---")
    print(df['prevision'].value_counts())

if __name__ == "__main__":
    run_batch_process()