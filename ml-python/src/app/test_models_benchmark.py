import joblib      # Librería para cargar modelos de Scikit-Learn (.pkl)
import os          # Permite navegar por las carpetas de tu computadora
import time        # Para medir cuánto tarda el modelo en responder
import gc          # "Garbage Collector": Limpia la memoria RAM para que no explote
import json        # Para leer archivos de texto tipo diccionario (como el tokenizer)
import sys         # Proporciona acceso a variables del sistema
import numpy as np # Para manejo de números y matrices (necesario para Deep Learning)
from datetime import datetime # Para ponerle fecha y hora al reporte final

import os
# Silencia avisos de TensorFlow (0=todo, 1=no info, 2=no warnings, 3=no errors)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

import logging
# Silencia avisos de Python
logging.getLogger('tensorflow').setLevel(logging.ERROR)

# Intentamos activar el "Modo Inteligente" para Redes Neuronales
try:
    import tensorflow as tf
    from tensorflow.keras.preprocessing.text import tokenizer_from_json
    from tensorflow.keras.preprocessing.sequence import pad_sequences
    TF_AVAILABLE = True # Si tenemos TensorFlow instalado
except ImportError:
    TF_AVAILABLE = False # Si no está instalado, el script seguirá pero saltará esos modelos

# =============================================================================
# 1. CONFIGURACIÓN DE RUTAS Y SISTEMA DE AUDITORÍA
# =============================================================================
# Buscamos la carpeta donde está este script parado
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ruta a los modelos y datos
MODELS_DIR = os.path.join(BASE_DIR, "..", "..", "data", "models", "candidates")
GOLD_DATA = os.path.join(BASE_DIR, "..", "..", "data", "raw", "gold_standard.txt")

# --- NUEVA LÓGICA DE REPORTES ---
# Definimos la carpeta base de resultados
BASE_REPORTS_DIR = os.path.join(BASE_DIR, "..", "..", "data", "results", "reports")

# Subcarpeta específica para evaluaciones de modelos
AUDIT_SUBDIR = os.path.join(BASE_REPORTS_DIR, "models_audit_evaluation")

# Si la carpeta de reportes o la subcarpeta no existen, las creamos
os.makedirs(AUDIT_SUBDIR, exist_ok=True)

# Generamos un nombre único para este archivo basado en el momento exacto de la ejecución
# Formato: auditoria_20260106_014530.log (Año-Mes-Dia_Hora-Min-Seg)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
ARCHIVO_LOG_ACTUAL = os.path.join(AUDIT_SUBDIR, f"auditoria_{timestamp}.log")

def log(msg):
    """Escribe en consola y en el archivo de auditoría único de esta sesión."""
    print(msg)
    # Usamos ARCHIVO_LOG_ACTUAL para que todas las líneas del benchmark 
    # se guarden en el mismo archivo con fecha y hora
    with open(ARCHIVO_LOG_ACTUAL, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

# También mantenemos una copia en "ultima_auditoria.log" por comodidad
# pero el archivo principal será el que tiene la fecha.
def actualizar_puntero_ultimo_log(msg):
    ruta_ultimo = os.path.join(BASE_REPORTS_DIR, "ultima_auditoria.log")
    with open(ruta_ultimo, "w", encoding="utf-8") as f:
        f.write(f"Ultima auditoria generada en: {ARCHIVO_LOG_ACTUAL}\n")


def load_keras_assets(folder_path):
    """
    Las Redes Neuronales (LSTM) necesitan un 'traductor' (tokenizer) 
    y un 'mapa' (label_mapping) para entender las palabras. 
    Esta función los busca dentro de la carpeta del candidato.
    """
    tokenizer = None
    mapping = None
    
    tok_path = os.path.join(folder_path, "tokenizer.json")
    map_path = os.path.join(folder_path, "label_mapping.json")
    
    # 1. CARGA DEL TOKENIZER
    if os.path.exists(tok_path):
        with open(tok_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
            # Si el archivo viene con doble comilla (como el tuyo), raw_data es un string
            if isinstance(raw_data, str):
                tokenizer_obj = tokenizer_from_json(raw_data)
            else:
                # Si viene como JSON directo, necesitamos convertir el dict a string para Keras
                tokenizer_obj = tokenizer_from_json(json.dumps(raw_data))

    # 2. CARGA DEL MAPPING (Aquí es donde rompe Fernando)
    if os.path.exists(map_path):
        with open(map_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # TRUCO: Si data es un string, lo volvemos a cargar como JSON
            if isinstance(data, str):
                mapping_obj = json.loads(data)
            else:
                mapping_obj = data
            
    return tokenizer_obj, mapping_obj

def run_benchmark():
    # Verificamos que el examen (Gold Standard) exista
    if not os.path.exists(GOLD_DATA):
        log(f"[-] ERROR CRÍTICO: No se encontró el archivo de examen en {GOLD_DATA}")
        return

    # -------------------------------------------------------------------------
    # 2. PREPARACIÓN DEL EXAMEN (Cargar frases del Gold Standard)
    # -------------------------------------------------------------------------
    test_cases = []
    with open(GOLD_DATA, "r", encoding="utf-8") as f:
        for line in f:
            if "|" in line:
                parts = line.strip().split("|")
                # Formato esperado: ID | Etiqueta | Texto | Autor
                if len(parts) == 4:
                    test_cases.append({
                        "id": parts[0], 
                        "label": parts[1], 
                        "text": parts[2], 
                        "author": parts[3]
                    })

    results = []
    log(f"\n=== INICIANDO BENCHMARK: {datetime.now().strftime('%d/%m/%Y %H:%M')} ===")
    log(f"Total de frases a evaluar: {len(test_cases)}")

    # -------------------------------------------------------------------------
    # 3. RECORRIDO DE CANDIDATOS (Entrar a cada subcarpeta)
    # -------------------------------------------------------------------------
    # Listamos todas las carpetas dentro de 'candidates/'
    for candidate_name in os.listdir(MODELS_DIR):
        folder_path = os.path.join(MODELS_DIR, candidate_name)
        
        # Solo entramos si es una carpeta (no archivos sueltos)
        if not os.path.isdir(folder_path): continue

        # Buscamos el archivo principal del modelo (.pkl o .keras) dentro de esa carpeta
        model_file = None
        for f in os.listdir(folder_path):
            if f.endswith(('.pkl', '.h5', '.keras')):
                model_file = f
                break
        
        if not model_file:
            log(f"[!] Aviso: No se encontró archivo de modelo en la carpeta {candidate_name}")
            continue

        full_model_path = os.path.join(folder_path, model_file)
        log(f"\n[+] Evaluando Candidato: {candidate_name}")

        try:
            # LIMPIEZA DE RAM: Antes de cargar un modelo, vaciamos la memoria
            gc.collect()
            success_count = 0
            mapa_aciertos = []

            # CASO A: MODELO DE SCIKIT-LEARN (.pkl)
            if model_file.endswith('.pkl'):
                model = joblib.load(full_model_path)
                tech = "Scikit-Learn (Pipeline)"
                
                # Pasamos frase por frase
                for case in test_cases:
                    # Estos modelos suelen aceptar el texto crudo directamente
                    pred = model.predict([case["text"]])[0]
                    
                    if str(pred).lower() == case["label"].lower():
                        success_count += 1
                        mapa_aciertos.append(f"#{case['id']}({case['author']})")
                    else:
                        mapa_aciertos.append(f"#{case['id']}(X)")

            # CASO B: RED NEURONAL (.h5 o .keras)
            elif model_file.endswith(('.h5', '.keras')):
                if not TF_AVAILABLE:
                    log("    [!] Error: TensorFlow no está instalado en este entorno.")
                    continue
                
                # NOTA TÉCNICA: Al cargar modelos .keras, pueden aparecer avisos (Warnings) en rojo.
                # 1. 'cuInit: UNKNOWN ERROR (303)': Es solo TensorFlow indicando que usará el CPU 
                #    en lugar de la tarjeta de video (GPU). No afecta la precisión del modelo.
                # 2. 'UserWarning: Skipping variable loading for optimizer': Indica que no se carga 
                #    el modo de entrenamiento. Como solo estamos evaluando (inferencia), esto es correcto
                #    y no altera las predicciones finales.    

                model = tf.keras.models.load_model(full_model_path)

                # Cargamos assets con doble validación para asegurar la integridad de los datos
                tokenizer, mapping = load_keras_assets(folder_path)
                tech = "Deep Learning (Keras)"
                
                for case in test_cases:
                    if tokenizer:
                        # Preprocesamiento de texto (Tokenización y Padding)
                        seq = tokenizer.texts_to_sequences([case["text"]])
                        
                        # Ajustamos el tamaño para que la Red Neuronal lo acepte
                        padded = pad_sequences(seq, maxlen=model.input_shape[1])
                        
                        # Ejecución de la inferencia (Predicción pura)
                        # verbose=0 evita que el log se llene de barras de progreso innecesarias
                        pred_raw = model.predict(padded, verbose=0)
                        
                        # --- INICIO DEL CAMBIO ---
                        # Mapeo de resultados: Convertimos la salida numérica a etiqueta textual
                        pred_idx_num = np.argmax(pred_raw, axis=1)[0]

                        if mapping and isinstance(mapping, dict):
                            # Buscamos en el diccionario. 'Desconocido' es un fallback de seguridad
                            # para evitar que el script se detenga si el modelo predice una clase no listada.
                            pred = mapping.get(str(pred_idx_num), "Desconocido")
                        else:
                            pred = str(pred_idx_num)
                        # --- FIN DEL CAMBIO ---
                        
                    else:
                        pred = "ERROR_SIN_TOKENIZER"

                    # Comparamos el resultado con la etiqueta real del Gold Standard
                    if str(pred).lower() == case["label"].lower():
                        success_count += 1
                        mapa_aciertos.append(f"#{case['id']}({case['author']})")
                    else:
                        mapa_aciertos.append(f"#{case['id']}(X)")

            # CALCULAMOS EL PUNTAJE FINAL
            accuracy = (success_count / len(test_cases)) * 100
            results.append({
                "Modelo": candidate_name,
                "Exito": f"{accuracy:.1f}%",
                "Mapa": " ".join(mapa_aciertos),
                "Tech": tech,
                "Score": accuracy
            })

        except Exception as e:
            log(f"    [!] Error al procesar {candidate_name}: {e}")

    # -------------------------------------------------------------------------
    # 4. GENERACIÓN DEL REPORTE FINAL (Cuadro comparativo)
    # -------------------------------------------------------------------------
    # Ordenamos de mayor a menor puntaje
    results.sort(key=lambda x: x['Score'], reverse=True)
    
    report_header = "\n" + "="*120 + "\n"
    report_header += f"{'CANDIDATO (Carpeta)':<25} | {'ÉXITO':<7} | {'TECNOLOGÍA':<20} | {'MAPA DE ACIERTOS'}\n"
    report_header += "-" * 120
    log(report_header)

    for r in results:
        log(f"{r['Modelo']:<25} | {r['Exito']:<7} | {r['Tech']:<20} | {r['Mapa']}")
    
    log("="*120)
    log("\nLEYENDA: #ID(Autor) = Acierto | #ID(X) = Fallo. Los reportes se guardan en data/results/reports/")

if __name__ == "__main__":
    run_benchmark()