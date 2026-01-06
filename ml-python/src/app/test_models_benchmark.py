import joblib
import os
import time
import gc
import sys
from datetime import datetime

# =============================================================================
# CONFIGURACIÓN DE RUTAS
# =============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "..", "..", "data", "models", "candidates")
GOLD_DATA = os.path.join(BASE_DIR, "..", "..", "data", "raw", "gold_standard.txt")
REPORTS_DIR = os.path.join(BASE_DIR, "..", "..", "data", "results", "reports")

def inspect_architecture(model, file_name):
    """
    AUDITORÍA AUTOMÁTICA DE COMPONENTES:
    El script detecta componentes internos para validar la robustez técnica.
    """
    if file_name.endswith(('.h5', '.keras')):
        return "Deep Learning (Red Neuronal)"
    
    components = []
    if hasattr(model, 'named_steps'):
        for name, step in model.named_steps.items():
            step_str = str(step).lower()
            # Término neutral para evitar favoritismos: Balanceo de Clase
            if "smote" in step_str or "oversampling" in step_str: 
                components.append("Balanceo de Clase")
            elif "svc" in step_str or "linear" in step_str: 
                components.append("LinearSVC")
            elif "tfidf" in step_str: 
                components.append("TF-IDF")
    
    return ", ".join(components) if components else "Configuración Estándar"

def run_benchmark():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    report_name = f"audit_detail_report_{timestamp}.txt"
    report_path = os.path.join(REPORTS_DIR, report_name)

    os.makedirs(REPORTS_DIR, exist_ok=True)

    report_lines = []
    def log(message):
        print(message)
        report_lines.append(message)

    log(f"--- REPORTE DE AUDITORÍA TÉCNICA E IMPARCIAL ---")
    log(f"Fecha de evaluación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 1. CARGA DEL EXAMEN CON DETALLE DE AUTORÍA (Anti-Sesgo)
    cases = []
    if os.path.exists(GOLD_DATA):
        with open(GOLD_DATA, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 4:
                    # Formato esperado: ID|Etiqueta|Texto|SugeridoPor
                    cases.append({"id": parts[0], "exp": parts[1], "txt": parts[2], "autor": parts[3]})
    
    if not cases:
        log("[-] ERROR: Formato de gold_standard.txt incorrecto o archivo no encontrado.")
        log("Use el formato: ID|Etiqueta|Texto|Autor")
        return

    # 2. IDENTIFICACIÓN DE CANDIDATOS
    model_files = [f for f in os.listdir(MODELS_DIR) if f.endswith(('.pkl', '.h5', '.keras'))]
    results = []

    for file_name in model_files:
        log(f"\n>>> Evaluando candidato: {file_name}")
        try:
            # Limpieza de RAM vital para la instancia de 1GB
            gc.collect() 
            path = os.path.join(MODELS_DIR, file_name)
            
            start_load = time.time()
            if file_name.endswith('.pkl'):
                model = joblib.load(path)
            else:
                import tensorflow as tf
                model = tf.keras.models.load_model(path)
            load_time = time.time() - start_load
            
            # Auditoría de aciertos y detección de procedencia
            hits = 0
            mapa_aciertos = []
            for c in cases:
                pred = model.predict([c["txt"]])[0]
                if not isinstance(pred, str):
                    pred = "Positivo" if pred > 0.5 else "Negativo"
                
                es_acierto = str(pred).strip().lower() == c["exp"].strip().lower()
                if es_acierto:
                    hits += 1
                    # Marcamos acierto con el nombre de quien sugirió la frase
                    mapa_aciertos.append(f"#{c['id']}({c['autor']})")
                else:
                    # Marcamos fallo con una X
                    mapa_aciertos.append(f"#{c['id']}(X)")

            acc = (hits / len(cases)) * 100
            
            results.append({
                "Modelo": file_name[:15],
                "Exito": f"{acc:.0f}%",
                "Mapa": " ".join(mapa_aciertos),
                "Tech": inspect_architecture(model, file_name),
                "Estado": "Operativo",
                "Score": acc
            })

            del model
            if 'tf' in sys.modules:
                import tensorflow as tf
                tf.keras.backend.clear_session()
            gc.collect()

        except MemoryError:
            log(f"    [!] AVISO: La instancia no soportó la gestión de {file_name} (RAM Insuficiente)")
            results.append({"Modelo": file_name[:15], "Exito": "N/A", "Mapa": "N/A", "Tech": "N/A", "Estado": "FALLO (RAM)", "Score": -1})
        except Exception as e:
            log(f"    [!] Error técnico con {file_name}: {e}")
            results.append({"Modelo": file_name[:15], "Exito": "Error", "Mapa": "N/A", "Tech": "N/A", "Estado": "Incompatible", "Score": -1})

    # 3. GENERACIÓN DEL CUADRO COMPARATIVO FINAL
    results.sort(key=lambda x: x['Score'], reverse=True)
    
    table_header = "\n" + "="*115 + "\n"
    table_header += f"{'ARCHIVO':<15} | {'ÉXITO':<7} | {'ARQUITECTURA':<25} | {'MAPA DE ACIERTOS (Frase/Autor)'}\n"
    table_header += "-" * 115
    log(table_header)

    for r in results:
        log(f"{r['Modelo']:<15} | {r['Exito']:<7} | {r['Tech']:<25} | {r['Mapa']}")
    
    log("="*115)
    log("\nLEYENDA DEL MAPA: #ID(Nombre) = Acierto en frase de ese autor | #ID(X) = Fallo en la frase.")
    log("\n💡 CONCLUSIÓN TÉCNICA:")
    log(f"El mejor balance entre precisión y generalización lo ofrece: {results[0]['Modelo'] if results else 'N/A'}")

    # 4. EXPORTAR REPORTE
    try:
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(report_lines))
        print(f"\n[✓] REPORTE AUDITABLE GENERADO: {report_name}")
    except Exception as e:
        print(f"\n[!] Error al guardar reporte: {e}")

if __name__ == "__main__":
    run_benchmark()