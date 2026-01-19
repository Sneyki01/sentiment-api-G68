import sys
import os
import time
import tracemalloc
import statistics
import random

# --- Configuration ---
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
# Correct path navigating from ml-python/notebooks to ml-python/src
SRC_PATH = os.path.abspath(os.path.join(ROOT_PATH, '..', 'src'))

if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)

from engine.sentiment_engine import SentimentEngine

TEST_PHRASES = [
    "La habitación estaba increíblemente sucia, un desastre.",
    "El desayuno fue maravilloso, me encantó.",
    "No estuvo mal, pero el precio es un poco alto.",
    "Excelente servicio, aunque el aire acondicionado fallaba.",
    "Terrible experiencia, nunca volveré.",
    "Me encanta que las sábanas tengan manchas, qué toque rústico.", # Ironía
    "El personal de recepción fue muy amable.",
    "La ubicación es perfecta para turistas.",
    "Ruido insoportable toda la noche.",
    "Todo correcto, sin quejas."
]

def measure_performance():
    print("🚀 Iniciando Test de Performance G68...\n")
    
    # --- 1. Memory & Load Time ---
    tracemalloc.start()
    start_load = time.perf_counter()
    
    # Models path relative to ml-python/notebooks -> ../data/models
    MODELS_PATH = os.path.abspath(os.path.join(ROOT_PATH, '..', 'data', 'models'))
    try:
        engine = SentimentEngine(model_dir=MODELS_PATH)
    except Exception as e:
        print(f"❌ Error al cargar el motor: {e}")
        return

    load_time = time.perf_counter() - start_load
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    print(f"✅ Motor cargado en {load_time:.4f} segundos")
    print(f"🧠 Pico de Memoria durante carga: {peak / 1024 / 1024:.2f} MB\n")

    # --- 2. Warm-up ---
    print("🔥 Calentando motores (10 inferencias)...")
    for _ in range(10):
        engine.predict_raw(random.choice(TEST_PHRASES))

    # --- 3. Stress Test ---
    ITERATIONS = 100
    latencies = []
    
    print(f"⚡ Ejecutando Stress Test ({ITERATIONS} iteraciones)...")
    
    start_stress = time.perf_counter()
    
    for i in range(ITERATIONS):
        text = random.choice(TEST_PHRASES)
        
        t_start = time.perf_counter_ns()
        engine.predict_raw(text)
        t_end = time.perf_counter_ns()
        
        latencies.append((t_end - t_start) / 1_000_000) # Convert to ms

    total_stress_time = time.perf_counter() - start_stress
    
    # --- 4. Report ---
    avg_latency = statistics.mean(latencies)
    p95_latency = statistics.quantiles(latencies, n=20)[18] # 95th percentile
    p99_latency = statistics.quantiles(latencies, n=100)[98] # 99th percentile
    throughput = ITERATIONS / total_stress_time

    print("\n" + "="*40)
    print("📊 REPORTE DE RENDIMIENTO G68")
    print("="*40)
    print(f"| Métrica | Valor |")
    print(f"|---|---|")
    print(f"| **Carga del Modelo** | {load_time:.4f} s |")
    print(f"| **Uso de RAM (Pico)** | {peak / 1024 / 1024:.2f} MB |")
    print(f"| **Latencia Promedio** | {avg_latency:.2f} ms |")
    print(f"| **Latencia P95** | {p95_latency:.2f} ms |")
    print(f"| **Latencia P99** | {p99_latency:.2f} ms |")
    print(f"| **Throughput** | {throughput:.2f} req/s |")
    print("="*40)

if __name__ == "__main__":
    measure_performance()
