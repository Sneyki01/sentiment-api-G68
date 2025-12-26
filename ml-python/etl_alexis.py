import pandas as pd
import re
import os

def clean_text_expert(text):
    if not isinstance(text, str): return ""
    # 1. Normalización básica
    text = text.lower()
    # 2. Limpieza de caracteres (mantenemos ñ y tildes para el contexto español)
    text = re.sub(r'[^a-zñáéíóú\s]', '', text)
    # 3. Eliminar espacios extra
    text = re.sub(r'\s+', ' ', text).strip()
    return text

print("🚀 Iniciando ETL de nivel experto...")

# Carga del dataset original
df = pd.read_csv('data/raw/Big_AHR.csv')

# --- TRATAMIENTO DE NULOS ---
# Eliminamos cualquier fila que no tenga texto o etiqueta (son inservibles para ML)
antes_nulos = len(df)
df = df.dropna(subset=['review_text', 'label'])
print(f"🗑️ Nulos eliminados: {antes_nulos - len(df)}")

# --- TRATAMIENTO DE DUPLICADOS ---
# A veces la misma reseña aparece varias veces con la misma o diferente etiqueta
antes_duplicados = len(df)
df = df.drop_duplicates(subset=['review_text'], keep='first')
print(f"🗑️ Duplicados eliminados: {antes_duplicados - len(df)}")

# --- LIMPIEZA DE ETIQUETAS (LABEL) ---
# Nos aseguramos de que solo queden las etiquetas del contrato: 0, 1 y 3
# Si hay algún valor extraño, lo eliminamos
df = df[df['label'].isin([0, 1, 3])]
df['label'] = df['label'].astype(int)

# --- NORMALIZACIÓN DE TEXTO ---
print("🧹 Normalizando texto (esto toma un momento)...")
df['clean_text'] = df['review_text'].apply(clean_text_expert)

# --- FILTRO POST-LIMPIEZA ---
# Si después de limpiar el texto quedó vacío (solo eran emojis o símbolos), lo borramos
df = df[df['clean_text'].str.len() > 2]

# --- GUARDADO ---
os.makedirs('data/processed', exist_ok=True)
ruta_final = 'data/processed/dataset_master.csv'
df.to_csv(ruta_final, index=False)

print("-" * 30)
print(f"✅ ETL FINALIZADO CON ÉXITO")
print(f"📊 Registros finales: {len(df)}")
print(f"📂 Archivo maestro creado en: {ruta_final}")
print("-" * 30)