
#Script para generar dataset con frases largas de reseñas

import pandas as pd
import random
import os
import unicodedata

def quitar_acentos(texto):
    """Elimina acentos y caracteres especiales para evitar errores de codificación."""
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    ).replace('ñ', 'n').replace('Ñ', 'N')

def generar_dataset_limpio(n=100):
    # 1. Asegurar que la carpeta de destino exista
    os.makedirs("data/processed", exist_ok=True)
    
    # 2. Componentes de las reseñas
    intro = ["Mi estancia fue mixta.", "No se como calificarlo.", "Llegamos con expectativas."]
    cuerpo_pos = ["la vista era increible y el diseno excelente,", "el personal fue sumamente profesional,"]
    cuerpo_neg = ["pero el bano era un asco,", "aunque el mantenimiento es mediocre,", "pero hay mucha suciedad,"]
    conclusion = ["el precio es normal.", "es aceptable para una noche.", "experiencia terrible."]

    datos = []
    for i in range(1, n + 1):
        # Construir la frase
        parrafo = f"{random.choice(intro)} {random.choice(cuerpo_pos)} {random.choice(cuerpo_neg)} {random.choice(conclusion)}"
        # Limpiar caracteres especiales
        parrafo_limpio = quitar_acentos(parrafo)
        datos.append([i, parrafo_limpio])

    # 3. CREAR EL DATAFRAME (Aquí es donde se define 'df')
    df = pd.DataFrame(datos, columns=['id', 'review_text_clean'])
    
    # 4. GUARDAR EL ARCHIVO
    ruta_salida = "data/processed/mensajes_nuevos_largos.csv"
    df.to_csv(ruta_salida, index=False, encoding='utf-8-sig')
    
    print(f"✅ ¡Éxito! Se han generado {n} reseñas en: {ruta_salida}")

# Iniciar la ejecución
if __name__ == "__main__":
    generar_dataset_limpio()