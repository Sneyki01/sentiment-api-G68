import joblib
import os
import time
import gc
import json
import sys
import numpy as np
import psutil
from datetime import datetime

# Silenciamos avisos de TensorFlow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import logging
logging.getLogger('tensorflow').setLevel(logging.ERROR)

try:
    import tensorflow as tf
    from tensorflow.keras.preprocessing.text import tokenizer_from_json
    from tensorflow.keras.preprocessing.sequence import pad_sequences
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False

# --- FUNCIONES DE UTILIDAD ---
def get_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)

def load_keras_assets(folder_path):
    tokenizer_obj = None
    mapping_obj = None
    tok_path = os.path.join(folder_path, "tokenizer.json")
    map_path = os.path.join(folder_path, "label_mapping.json")
    
    if os.path.exists(tok_path):
        with open(tok_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
            tokenizer_obj = tokenizer_from_json(raw_data if isinstance(raw_data, str) else json.dumps(raw_data))

    if os.path.exists(map_path):
        with open(map_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            mapping_obj = json.loads(data) if isinstance(data, str) else data
            
    return tokenizer_obj, mapping_obj

# =============================================================================
# 1. CONFIGURACIÓN DE RUTAS
# =============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "..", "..", "data", "models", "candidates")
GOLD_DATA = os.path.join(BASE_DIR, "..", "..", "data", "raw", "gold_standard.txt")
BASE_REPORTS_DIR = os.path.join(BASE_DIR, "..", "..", "data", "results", "reports")
AUDIT_SUBDIR = os.path.join(BASE_REPORTS_DIR, "models_audit_evaluation")

os.makedirs(AUDIT_SUBDIR, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
ARCHIVO_LOG_ACTUAL = os.path.join(AUDIT_SUBDIR, f"auditoria_{timestamp}.log")

def log(msg):
    print(msg)
    with open(ARCHIVO_LOG_ACTUAL, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

# =============================================================================
# 2. PROCESO PRINCIPAL
# =============================================================================
def run_benchmark():
    # Cargar frases de prueba (Examen)
    if not os.path.exists(GOLD_DATA):
        print(f"[!] No existe: {GOLD_DATA}")
        return

    test_cases = []
    with open(GOLD_DATA, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) == 4:
                test_cases.append({"id": parts[0], "label": parts[1], "text": parts[2], "author": parts[3]})

    log(f"=== INICIANDO BENCHMARK: {datetime.now().strftime('%d/%m/%Y %H:%M')} ===")
    log(f"Total de frases a evaluar: {len(test_cases)}")
    log("="*60)

    # --- PASO A: PRE-CARGAR TODOS LOS MODELOS ---
    # Esto es necesario para poder comparar frase por frase en una sola tabla
    modelos_vivos = []
    for candidate_name in os.listdir(MODELS_DIR):
        folder_path = os.path.join(MODELS_DIR, candidate_name)
        if not os.path.isdir(folder_path): continue

        try:
            model_file = next((f for f in os.listdir(folder_path) if f.endswith(('.pkl', '.keras', '.h5'))), None)
            if not model_file: continue

            full_path = os.path.join(folder_path, model_file)
            ram_antes = get_memory_usage()
            
            # Carga según tecnología
            obj_modelo = None
            tokenizer = None
            mapping = None
            tech = ""

            if model_file.endswith('.pkl'):
                obj_modelo = joblib.load(full_path)
                tech = "PKL"
            else:
                obj_modelo = tf.keras.models.load_model(full_path)
                tokenizer, mapping = load_keras_assets(folder_path)
                tech = "Keras"

            ram_despues = get_memory_usage()
            
            modelos_vivos.append({
                "nombre": candidate_name,
                "modelo": obj_modelo,
                "tokenizer": tokenizer,
                "mapping": mapping,
                "tech": tech,
                "ram_uso": max(0, ram_despues - ram_antes),
                "preds_list": [], # Aquí guardaremos cada respuesta
                "aciertos": 0,
                "neg_identificados": 0,
                "neg_totales": 0,
                "tiempos": []
            })
            log(f"[+] Modelo '{candidate_name}' cargado exitosamente.")
        except Exception as e:
            log(f"[!] Error cargando {candidate_name}: {e}")

    # --- PASO B: EVALUACIÓN CRUZADA (Frase por Frase) ---
    for case in test_cases:
        real_label = case["label"].lower()
        es_negativo = (real_label == "negativo")

        for m in modelos_vivos:
            if es_negativo: m["neg_totales"] += 1
            
            start_p = time.time()
            # PREDICCIÓN
            try:
                if m["tech"] == "PKL":
                    p = m["modelo"].predict([case["text"]])[0]
                else:
                    seq = m["tokenizer"].texts_to_sequences([case["text"]])
                    padded = pad_sequences(seq, maxlen=m["modelo"].input_shape[1])
                    res = m["modelo"].predict(padded, verbose=0)
                    idx = np.argmax(res, axis=1)[0]
                    print(f"DEBUG Fernando: Probabilidades brutas: {res} -> Indice elegido: {idx}")
                    p = m["mapping"].get(str(idx), str(idx)) if m["mapping"] else str(idx)
                
                prediction = str(p).lower()
            except:
                prediction = "error"

            m["tiempos"].append(time.time() - start_p)
            m["preds_list"].append(prediction)

            # Validar acierto
            if prediction == real_label:
                m["aciertos"] += 1
                if es_negativo: m["neg_identificados"] += 1

    # =============================================================================
    # 3. REPORTES FINALES
    # =============================================================================
    
    # --- TABLA 1: RESUMEN GENERAL (Métricas de Hardware y Éxito) ---
    log("\n" + "="*125)
    header = f"{'CANDIDATO':<20} | {'ÉXITO':<7} | {'NEGATIVOS':<10} | {'LATENCIA':<12} | {'RAM':<10} | {'TECH'}"
    log(header)
    log("-" * 125)
    for m in modelos_vivos:
        exito = (m["aciertos"] / len(test_cases)) * 100
        latencia = (sum(m["tiempos"]) / len(test_cases)) * 1000
        log(f"{m['nombre']:<20} | {exito:>5.1f}% | {m['neg_identificados']}/{m['neg_totales']:<8} | {latencia:>7.2f} ms | {m['ram_uso']:>6.1f} MB | {m['tech']}")
    log("-" * 125)
    log(f"LEYENDA: [ OK ] = Acierto | [!!!!] = Fallo. Logs en: {AUDIT_SUBDIR}\n")

    # --- TABLA 2: DETALLE COMPARATIVO CON ALERTAS Y TOTALES ---
    log("DETALLE DE EJECUCIÓN COMPARATIVO (POR FRASE):")
    
    # Configuración de anchos para consistencia
    w_cand = 12
    w_pred = 12
    w_res = 10
    
    # Encabezado dinámico
    head_det = f"{'NRO':<4}| {'REAL':<10} | {'COMENTARIO':<15} | {'SUGIRIÓ':<10} |"
    for m in modelos_vivos:
        head_det += f" {'CANDIDATO':<{w_cand}} | {'PREDICHO':<{w_pred}} | {'RESULTADO':<{w_res}} |"
    
    separador = "-" * len(head_det)
    log(separador)
    log(head_det)
    log(separador)

    # Filas de datos (Frase por Frase)
    for i, case in enumerate(test_cases):
        fila = f"{case['id']:<4}| {case['label'][:10].upper():<10} | {case['text'][:12]+'...':<15} | {case['author'][:10].upper():<10} |"
        
        for m in modelos_vivos:
            p = m["preds_list"][i]
            # Sistema de alertas visuales
            res_txt = "[ OK ]" if p == case["label"].lower() else "[!!!!]"
            fila += f" {m['nombre'][:w_cand]:<{w_cand}} | {p.upper()[:w_pred]:<{w_pred}} | {res_txt:<{w_res}} |"
        log(fila)

    # --- NUEVA FILA: TOTAL DE ACIERTOS DEBAJO DE LAS COLUMNAS ---
    log(separador)
    fila_totales = f"{'TOTAL':<4}| {'':<10} | {'':<15} | {'':<10} |"
    for m in modelos_vivos:
        # Sumamos el total de aciertos acumulado durante la evaluación
        total_aciertos = f"{m['aciertos']}/{len(test_cases)}"
        fila_totales += f" {'SUMA FINAL':<{w_cand}} | {'ACIERTOS:':<{w_pred}} | {total_aciertos:<{w_res}} |"
    
    log(fila_totales)
    log(separador)

if __name__ == "__main__":
    run_benchmark()