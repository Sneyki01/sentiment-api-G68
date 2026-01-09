import os
import time
import pandas as pd
import joblib
import psutil
from src.engine.sentiment_engine import analizar_sentimiento_hibrido

def get_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)  # MB

def run_audit():
    print("🚀 Iniciando Auditoría de Performance G68...")
    
    # 1. Carga de Datos
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, "data", "raw", "golden_benchmark_325.csv")
    df = pd.read_csv(data_path)
    
    # Muestreo aleatorio de 100 mensajes
    sample_df = df.sample(n=100, random_state=42)
    
    # 2. Carga de Modelos y Medición de RAM
    start_mem = get_memory_usage()
    model_path = os.path.join(base_dir, "data", "models", "sentiment_model.pkl")
    vector_path = os.path.join(base_dir, "data", "models", "tfidf_vectorizer.pkl")
    
    print(f"📦 RAM Inicial: {start_mem:.2f} MB")
    
    modelo = joblib.load(model_path)
    vectorizador = joblib.load(vector_path)
    
    post_load_mem = get_memory_usage()
    print(f"📦 RAM Post-Carga Modelos: {post_load_mem:.2f} MB (Delta: {post_load_mem - start_mem:.2f} MB)")
    
    # 3. Ejecución de Benchmarks (Latencia y Precisión)
    correct = 0
    latencies = []
    
    print(f"🧪 Procesando 100 muestras...")
    
    for _, row in sample_df.iterrows():
        text = row['text']
        true_label = row['sentiment']
        
        start_time = time.perf_counter()
        pred_label, prob, meta = analizar_sentimiento_hibrido(text, modelo, vectorizador)
        end_time = time.perf_counter()
        
        latencies.append(end_time - start_time)
        
        if pred_label == true_label:
            correct += 1
            
    # 4. Resultados Finales
    avg_latency = (sum(latencies) / len(latencies)) * 1000 # ms
    total_time = sum(latencies)
    accuracy = (correct / len(sample_df)) * 100
    peak_mem = get_memory_usage()
    
    print("\n" + "="*40)
    print("📊 RESULTADOS DE LA AUDITORÍA G68")
    print("="*40)
    print(f"⏱️  Latencia Media: {avg_latency:.2f} ms / req")
    print(f"⏱️  Tiempo Total (100 req): {total_time:.2f} s")
    print(f"🧠 Consumo RAM Máximo: {peak_mem:.2f} MB")
    print(f"🎯 Precisión (Accuracy): {accuracy:.1f} %")
    print("="*40)
    
    # Detalle de performance por tipo
    print(f"⚡ Throughput: {1.0 / (avg_latency/1000):.2f} req/s")

if __name__ == "__main__":
    run_audit()
