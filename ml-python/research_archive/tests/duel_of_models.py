import os
import sys
import joblib
import pandas as pd
from tqdm import tqdm

# Configurar rutas para importar el motor
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, "src"))

from engine.sentiment_engine import analizar_sentimiento_hibrido

def run_benchmark():
    # 1. Cargar Datos y Modelos
    csv_path = os.path.join(BASE_DIR, "data", "raw", "golden_benchmark_325.csv")
    model_path = os.path.join(BASE_DIR, "data", "models", "sentiment_model.pkl")
    vectorizer_path = os.path.join(BASE_DIR, "data", "models", "tfidf_vectorizer.pkl")

    if not os.path.exists(csv_path):
        print(f"Error: No se encuentra el archivo {csv_path}")
        return

    df = pd.read_csv(csv_path)
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)

    # 2. Definir Bloques (Basado en la estructura de consolidación)
    # Se asume el orden en que fueron inyectados
    blocks = {
        "1. Spa y Bienestar": (0, 50),
        "2. Hospitalidad": (50, 100),
        "3. Sarcasmo (Lab)": (100, 150),
        "4. Ambigüedad": (150, 200),
        "5. Reseñas Largas": (200, 225),
        "6. Temas Cortos": (225, 325),
        "7. Sarcasmo/Estrés (Real)": (325, 375),
        "8. Largas Complejas": (375, 395)
    }

    results = []

    print(f"--- DUELO DE MODELOS G68: ML PURO VS HÍBRIDO SUPREME ---")
    print(f"Total de frases a evaluar: {len(df)}\n")

    for block_name, (start, end) in blocks.items():
        block_df = df.iloc[start:end]
        if block_df.empty: continue

        ml_correct = 0
        hybrid_correct = 0
        total = len(block_df)

        for _, row in block_df.iterrows():
            texto = row['text']
            esperado = row['sentiment'].lower()

            # Predicción ML Puro
            X = vectorizer.transform([texto])
            ml_pred = model.predict(X)[0].lower()
            if ml_pred == esperado: ml_correct += 1

            # Predicción Híbrida
            hybrid_pred, _, _ = analizar_sentimiento_hibrido(texto, model, vectorizer)
            if hybrid_pred.lower() == esperado: hybrid_correct += 1

        ml_acc = (ml_correct / total) * 100
        hybrid_acc = (hybrid_correct / total) * 100
        
        results.append({
            "Bloque": block_name,
            "Total": total,
            "ML Acc": f"{ml_acc:.2f}%",
            "Hybrid Acc": f"{hybrid_acc:.2f}%",
            "Gana": "Híbrido 🚀" if hybrid_acc > ml_acc else ("ML 🤖" if ml_acc > hybrid_acc else "Empate 🤝")
        })

    # 3. Mostrar Resultados
    report_df = pd.DataFrame(results)
    print(report_df.to_string(index=False))

    # Totales Globales
    all_ml_correct = 0
    all_hybrid_correct = 0
    total_global = len(df)

    for _, row in df.iterrows():
        texto = row['text']
        esperado = row['sentiment'].lower()
        
        # ML
        ml_pred = model.predict(vectorizer.transform([texto]))[0].lower()
        if ml_pred == esperado: all_ml_correct += 1
        
        # Híbrido
        hybrid_pred, _, _ = analizar_sentimiento_hibrido(texto, model, vectorizer)
        if hybrid_pred.lower() == esperado: all_hybrid_correct += 1

    print(f"\n--- RENDIMIENTO GLOBAL ---")
    print(f"ML PURO ACCURACY: {(all_ml_correct/total_global)*100:.2f}%")
    print(f"HÍBRIDO SUPREME ACCURACY: {(all_hybrid_correct/total_global)*100:.2f}%")

if __name__ == "__main__":
    run_benchmark()
