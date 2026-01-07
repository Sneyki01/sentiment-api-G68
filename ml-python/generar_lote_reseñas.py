
#Script para generar dataset con frases largas de reseñas

import pandas as pd
import random
import os

def generar_dataset_largo(n=100):
    # Asegurar que la carpeta exista
    os.makedirs("data/processed", exist_ok=True)
    
    intro = ["Mi estancia fue mixta.", "Sinceramente no sé cómo calificarlo.", "Llegamos con expectativas."]
    cuerpo_pos = ["la vista era increíble y el diseño excelente,", "el personal fue sumamente profesional,"]
    cuerpo_neg = ["pero el baño era un asco,", "aunque el mantenimiento es mediocre,", "pero hay mucha suciedad,"]
    conclusion = ["el precio es normal.", "es aceptable para una noche.", "experiencia terrible."]

    datos = []
    for i in range(1, n + 1):
        párrafo = f"{random.choice(intro)} {random.choice(cuerpo_pos)} {random.choice(cuerpo_neg)} {random.choice(conclusion)}"
        datos.append([i, párrafo])

    df = pd.DataFrame(datos, columns=['id', 'review_text_clean'])
    df.to_csv("data/processed/mensajes_nuevos_largos.csv", index=False, encoding='utf-8')
    print("✅ 100 Reseñas largas generadas en data/processed/")

if __name__ == "__main__":
    generar_dataset_largo()