import joblib
import os
import time
import gc
import json
import sys
import numpy as np
import psutil
import random
from datetime import datetime

# =============================================================================
# --- CONFIGURACIÓN DE ENTORNO Y LOGGING ---
# =============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Ajuste de rutas para subir a la raíz del proyecto
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "..")) 
BASE_REPORTS_DIR = os.path.join(ROOT_DIR, "data", "results", "reports")
AUDIT_SUBDIR = os.path.join(BASE_REPORTS_DIR, "models_audit_evaluation")
RELATIVE_ROUTE = os.path.relpath(AUDIT_SUBDIR, ROOT_DIR)

if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# Crear carpeta de reportes si no existe
os.makedirs(AUDIT_SUBDIR, exist_ok=True)
timestamp_file = datetime.now().strftime("%Y%m%d_%H%M%S")
ARCHIVO_LOG_ACTUAL = os.path.join(AUDIT_SUBDIR, f"auditoria_{timestamp_file}.log")

def log(msg):
    """Escribe en consola y en el archivo de log simultáneamente."""
    print(msg)
    with open(ARCHIVO_LOG_ACTUAL, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

# Registro de clase para Alexis (evita errores de deserialización)
try:
    from engine.test_review import SentimentLabG68
except ImportError:
    log("[SISTEMA] Advertencia: No se encontró la clase SentimentLabG68 en engine.test_review")

# Silenciar TensorFlow para un log limpio
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import logging
logging.getLogger('tensorflow').setLevel(logging.ERROR)

try:
    import tensorflow as tf
    from tensorflow.keras.preprocessing.sequence import pad_sequences
    from tensorflow.keras.preprocessing.text import tokenizer_from_json
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False

def get_memory_usage():
    """Devuelve el uso de RAM del proceso actual en Kilobytes (KB)."""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 

# =============================================================================
# --- CORE DEL BENCHMARK ---
# =============================================================================

def run_benchmark():
    log(f"=== INICIANDO AUDITORÍA JUSTA: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
    
    # 1. Cargar Gold Standard
    gs_path = os.path.join(ROOT_DIR, "data", "raw", "gold_standard.txt")
    test_cases = []
    if os.path.exists(gs_path):
        with open(gs_path, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) >= 4:
                    test_cases.append({
                        "id": parts[0], "label": parts[1].lower(),
                        "text": parts[2], "author": parts[3]
                    })
    log(f"[SISTEMA] {len(test_cases)} casos cargados para evaluación.\n")

    # 2. Localizar Candidatos
    models_dir = os.path.join(ROOT_DIR, "data", "models", "candidates")
    candidatos = [d for d in os.listdir(models_dir) if os.path.isdir(os.path.join(models_dir, d))]
    
    # Shuffle para evitar ventaja por orden de ejecución
    random.shuffle(candidatos)
    
    modelos_stats = []

    # --- FASE 1: CARGA Y MEDICIÓN DE RAM AISLADA ---
    for cand_name in candidatos:
        path = os.path.join(models_dir, cand_name)
        
        # Limpieza profunda antes de medir cada modelo
        gc.collect()
        time.sleep(1) # Estabilización
        ram_antes = get_memory_usage()
        
        m_data = {
            "nombre": cand_name, "modelo": None, "tokenizer": None, 
            "mapping": None, "tech": "N/A", "ram_uso": 0,
            "aciertos": 0, "neg_totales": 0, "neg_identificados": 0,
            "tiempos": [], "preds_list": []
        }

        try:
            files = os.listdir(path)
            # Carga PKL (Alexis / Diego)
            if any(f.endswith('.pkl') for f in files):
                pkl_file = next(f for f in files if f.endswith('.pkl'))
                m_data["modelo"] = joblib.load(os.path.join(path, pkl_file))
                m_data["tech"] = "PKL"
            # Carga Keras (Fernando)
            elif any(f.endswith('.h5') or f.endswith('.keras') for f in files):
                h5_file = next(f for f in files if f.endswith(('.h5', '.keras')))
                m_data["modelo"] = tf.keras.models.load_model(os.path.join(path, h5_file))
                m_data["tech"] = "Keras"
                with open(os.path.join(path, "tokenizer.json"), "r") as f:
                    m_data["tokenizer"] = tokenizer_from_json(json.load(f))
                with open(os.path.join(path, "label_mapping.json"), "r") as f:
                    m_data["mapping"] = json.load(f)

            ram_despues = get_memory_usage()
            m_data["ram_uso"] = max(0, ram_despues - ram_antes)
            modelos_stats.append(m_data)
            log(f"[+] '{cand_name}' cargado. Impacto neto: {m_data['ram_uso']:.1f} KB")
        except Exception as e:
            log(f"[!] Error cargando {cand_name}: {e}")

    # --- FASE 2: CALENTAMIENTO (WARM-UP) ---
    log("\n[SISTEMA] Iniciando fase de Warm-up (Calentamiento de CPU)...")
    warmup_text = "El servicio es aceptable y la atencion normal."
    for m in modelos_stats:
        for _ in range(3):
            try:
                if m["tech"] == "PKL":
                    # Detectar si es Alexis o Diego para el formato de entrada
                    if "SentimentLab" in str(type(m["modelo"])):
                        m["modelo"].predict(warmup_text)
                    else:
                        m["modelo"].predict([warmup_text])
                elif m["tech"] == "Keras":
                    seq = m["tokenizer"].texts_to_sequences([warmup_text])
                    m["modelo"].predict(pad_sequences(seq, maxlen=m["modelo"].input_shape[1]), verbose=0)
            except: pass

    # --- FASE 3: EVALUACIÓN REAL (ENTRADA CRUDA) ---
    log(f"[SISTEMA] Procesando {len(test_cases)} frases en orden aleatorio...")
    
    for case in test_cases:
        real_label = case["label"]
        raw_text = case["text"]

        for m in modelos_stats:
            if real_label == "negativo": m["neg_totales"] += 1
            
            start_t = time.perf_counter() # Mayor precisión que time.time()
            try:
                if m["tech"] == "PKL":
                    if "SentimentLab" in str(type(m["modelo"])):
                        p = m["modelo"].predict(raw_text)
                    else:
                        p = m["modelo"].predict([raw_text])[0]
                else:
                    seq = m["tokenizer"].texts_to_sequences([raw_text])
                    padded = pad_sequences(seq, maxlen=m["modelo"].input_shape[1])
                    res = m["modelo"].predict(padded, verbose=0)
                    idx = np.argmax(res, axis=1)[0]
                    p = m["mapping"].get(str(idx), str(idx))

                prediction = str(p).lower().strip()
            except:
                prediction = "error"

            m["tiempos"].append(time.perf_counter() - start_t)
            m["preds_list"].append(prediction)
            
            if prediction == real_label:
                m["aciertos"] += 1
                if real_label == "negativo": m["neg_identificados"] += 1

    # =============================================================================
    # 3. REPORTES FINALES
    # =============================================================================
    
    # --- TABLA 1: RESUMEN GENERAL (Métricas de Hardware y Éxito) ---
    log("\n" + "="*125)
    header = f"{'CANDIDATO':<20} | {'ÉXITO':<7} | {'NEGATIVOS':<10} | {'LATENCIA':<12} | {'RAM':<10} | {'TECH'}"
    log(header)
    log("-" * 125)
    for m in modelos_stats:
        exito = (m["aciertos"] / len(test_cases)) * 100
        latencia = (sum(m["tiempos"]) / len(test_cases)) * 1000
        log(f"{m['nombre']:<20} | {exito:>5.1f}% | {m['neg_identificados']}/{m['neg_totales']:<8} | {latencia:>7.2f} ms | {m['ram_uso']:>6.1f} KB | {m['tech']}")
    log("-" * 125)
    log(f"LEYENDA: [ OK ] = Acierto | [!!!!] = Fallo. \nLogs en: {RELATIVE_ROUTE}\n")

    # --- TABLA 2: DETALLE COMPARATIVO CON ALERTAS Y TOTALES ---
    log("DETALLE DE EJECUCIÓN COMPARATIVO (POR FRASE):")
    
    # Configuración de anchos para consistencia
    w_cand = 12
    w_pred = 12
    w_res = 10
    
    # Encabezado dinámico
    head_det = f"{'NRO':<4}| {'REAL':<10} | {'COMENTARIO':<15} | {'SUGIRIÓ':<10} |"
    for m in modelos_stats:
        head_det += f" {'CANDIDATO':<{w_cand}} | {'PREDICHO':<{w_pred}} | {'RESULTADO':<{w_res}} |"
    
    separador = "-" * len(head_det)
    log(separador)
    log(head_det)
    log(separador)

    # Filas de datos (Frase por Frase)
    for i, case in enumerate(test_cases):
        fila = f"{case['id']:<4}| {case['label'][:10].upper():<10} | {case['text'][:12]+'...':<15} | {case['author'][:10].upper():<10} |"
        
        for m in modelos_stats:
            p = m["preds_list"][i]
            # Sistema de alertas visuales
            res_txt = "[ OK ]" if p == case["label"].lower() else "[!!!!]"
            fila += f" {m['nombre'][:w_cand]:<{w_cand}} | {p.upper()[:w_pred]:<{w_pred}} | {res_txt:<{w_res}} |"
        log(fila)

    # --- NUEVA FILA: TOTAL DE ACIERTOS DEBAJO DE LAS COLUMNAS ---
    log(separador)
    fila_totales = f"{'TOTAL':<4}| {'':<10} | {'':<15} | {'':<10} |"
    for m in modelos_stats:
        # Sumamos el total de aciertos acumulado durante la evaluación
        total_aciertos = f"{m['aciertos']}/{len(test_cases)}"
        fila_totales += f" {'SUMA FINAL':<{w_cand}} | {'ACIERTOS:':<{w_pred}} | {total_aciertos:<{w_res}} |"
    
    log(fila_totales)
    log(separador)

if __name__ == "__main__":
    run_benchmark()