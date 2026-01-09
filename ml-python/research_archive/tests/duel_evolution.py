import os
import sys
import joblib
import pandas as pd

# Configurar rutas para importar los motores
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, "src"))

from engine.sentiment_engine import analizar_sentimiento_hibrido as motor_hoy
from engine.sentiment_engine_ayer import analizar_sentimiento_hibrido_ayer as motor_ayer

def run_evolution_duel():
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

    # 2. Definir Bloques
    blocks = {
        "1. Spa/Bienestar": (0, 50),
        "2. Hospitalidad": (50, 100),
        "3. Sarcasmo (Lab)": (100, 150),
        "4. Ambigüedad": (150, 200),
        "5. Reseñas Largas": (200, 225),
        "6. Temas Cortos": (225, 325),
        "7. Sarcasmo/Estrés": (325, 375),
        "8. Largas Complejas": (375, 395),
        "9. Élite G68 🔥": (395, 485),
        "10. Validación G68 ✨": (485, 580)
    }

    results = []

    print(f"--- ⚔️ DUELO DE EVOLUCIÓN G68: AYER VS HOY ⚔️ ---")
    print(f"Dataset Maestro: {len(df)} frases\n")

    for block_name, (start, end) in blocks.items():
        block_df = df.iloc[start:end]
        if block_df.empty: continue

        ayer_correct = 0
        hoy_correct = 0
        ml_correct = 0
        total = len(block_df)

        for _, row in block_df.iterrows():
            texto = row['text']
            esperado = row['sentiment'].lower()

            # 1. Ayer
            res_ayer, _, _ = motor_ayer(texto, model, vectorizer)
            if res_ayer.lower() == esperado: ayer_correct += 1

            # 2. Hoy
            res_hoy, _, _ = motor_hoy(texto, model, vectorizer)
            if res_hoy.lower() == esperado: hoy_correct += 1

            # 3. ML Puro
            X = vectorizer.transform([texto])
            res_ml = model.predict(X)[0].lower()
            if res_ml == esperado: ml_correct += 1

        results.append({
            "Bloque": block_name,
            "Ayer 🕒": f"{(ayer_correct/total)*100:.1f}%",
            "Hoy 🚀": f"{(hoy_correct/total)*100:.1f}%",
            "ML 🤖": f"{(ml_correct/total)*100:.1f}%"
        })

    # Mostrar Resultados
    report_df = pd.DataFrame(results)
    print(report_df.to_string(index=False))

    # Totales Globales
    all_ayer = sum([float(r['Ayer 🕒'].replace('%','')) for r in results]) / len(results)
    all_hoy = sum([float(r['Hoy 🚀'].replace('%','')) for r in results]) / len(results)
    all_ml = sum([float(r['ML 🤖'].replace('%','')) for r in results]) / len(results)

    print(f"\n--- RENDIMIENTO PROMEDIO FINAL ---")
    print(f"VERSIÓN AYER  : {all_ayer:.2f}%")
    print(f"VERSIÓN HOY   : {all_hoy:.2f}%")
    print(f"ML PURO       : {all_ml:.2f}%")
    print(f"\nNota: El ML Puro tiene ventaja por haber sido entrenado con estos datos.")

if __name__ == "__main__":
    run_evolution_duel()
