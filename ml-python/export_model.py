import pickle
import os
import sys

# Aseguramos que Python encuentre tus clases
sys.path.append(os.path.abspath("src"))
from engine.sentiment_rule_engine import SentimentLabG68

def exportar():
    lexicon_path = "data/lexicon/lexicon_final_optimizado.json"
    
    if not os.path.exists(lexicon_path):
        print("❌ Error: No se encuentra el lexicon para exportar.")
        return

    # Instanciamos el modelo con tu configuración de contrato
    modelo_ganador = SentimentLabG68(lexicon_path, alpha=0.15)
    
    # Guardamos el objeto completo
    nombre_archivo = "modelo_sentiment_G68.pkl"
    with open(nombre_archivo, "wb") as f:
        pickle.dump(modelo_ganador, f)
    
    print(f"✅ ¡Éxito! '{nombre_archivo}' generado.")
    print("👉 Este es el archivo que debes entregar hoy 06/01.")

if __name__ == "__main__":
    exportar()