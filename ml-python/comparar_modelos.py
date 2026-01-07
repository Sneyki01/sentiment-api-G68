import pandas as pd
import joblib
import re
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.utils import resample

# Este script asume que se ejecuta desde la raíz de 'ml-python'.
# Python encontrará el directorio 'src' automáticamente.
from src.engine.sentiment_engine import analizar_sentimiento_hibrido

# --- Configuración ---
print("--- Script de Comparación de Métricas ---")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "Big_AHR.csv")
MODEL_PATH = os.path.join(BASE_DIR, "data", "models", "sentiment_model.pkl")
VECTOR_PATH = os.path.join(BASE_DIR, "data", "models", "tfidf_vectorizer.pkl")

# --- Funciones de Preparación de Datos ---
def limpieza_pro(texto):
    """Función de limpieza consistente con el pipeline de entrenamiento."""
    texto = str(texto).lower()
    texto = re.sub(r'[^a-zñáéíóúü\s]', '', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto

def categorizar_sentimiento(r):
    """Categoriza el sentimiento basado en el rating."""
    if r <= 2: return 'Negativo'
    elif r == 3: return 'Neutro'
    else: return 'Positivo'

# --- 1. Cargar y Preparar Datos ---
print(f"Cargando datos desde {DATA_PATH}...")
try:
    df = pd.read_csv(DATA_PATH)
    print(f"✅ Datos cargados: {df.shape[0]} registros.")
except FileNotFoundError:
    print(f"❌ Error: No se encontró el archivo en {DATA_PATH}")
    print("Asegúrate de ejecutar este script desde la carpeta 'ml-python'.")
    exit()

# Aplicar limpieza y categorización como en el entrenamiento
df['text_cleaned'] = df['review_text'].apply(limpieza_pro)
df['sentiment'] = df['rating'].apply(categorizar_sentimiento)
print("Limpieza y categorización completadas.")

# Balancear el dataset para igualar las condiciones de entrenamiento
df_majority = df[df.sentiment=='Positivo']
df_minority_neg = df[df.sentiment=='Negativo']
df_minority_neu = df[df.sentiment=='Neutro']
n_samples = len(df_majority)

df_minority_neg_upsampled = resample(df_minority_neg, replace=True, n_samples=n_samples, random_state=42)
df_minority_neu_upsampled = resample(df_minority_neu, replace=True, n_samples=n_samples, random_state=42)

df_upsampled = pd.concat([df_majority, df_minority_neg_upsampled, df_minority_neu_upsampled])
print(f"Dataset balanceado a {len(df_upsampled)} registros.")

# --- Dividir los datos en sets de entrenamiento/prueba ---
# Usamos el 'review_text' original para el modelo híbrido y el 'text_cleaned' para el de ML.
# El set de prueba 'y_test' será el mismo para ambos.
X_train, X_test, y_train, y_test = train_test_split(
    df_upsampled[['review_text', 'text_cleaned']], 
    df_upsampled['sentiment'],
    test_size=0.2, 
    random_state=42
)
print(f"Datos divididos: {len(X_test)} registros de prueba.")

# --- 2. Cargar Modelo Pre-entrenado y Vectorizador ---
print(f"Cargando modelo desde {MODEL_PATH}...")
try:
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTOR_PATH)
    print("✅ Modelo y Vectorizador cargados exitosamente.")
except FileNotFoundError:
    print(f"❌ Error: No se encontraron los archivos del modelo en {MODEL_PATH} o {VECTOR_PATH}.")
    print("Asegúrate de haber ejecutado 'train_pipeline.py' primero.")
    exit()

# --- 3. Evaluar Modelo ML-Only ---
print("\n" + "="*50)
print("📊 MÉTRICAS: MODELO MACHINE LEARNING (SVM CALIBRADO)")
print("="*50)

# Vectorizar el texto de prueba limpio
X_test_vec = vectorizer.transform(X_test['text_cleaned'])
# Predecir usando el modelo cargado
y_pred_ml = model.predict(X_test_vec)

# Imprimir reporte de clasificación
labels = ['Positivo', 'Neutro', 'Negativo']
print(classification_report(y_test, y_pred_ml, labels=labels, digits=4))


# --- 4. Evaluar Modelo Híbrido ---
print("\n" + "="*50)
print("🧠 MÉTRICAS: MODELO HÍBRIDO (ML + CAPA SEMÁNTICA G68)")
print("="*50)

y_pred_hybrid = []
# Iterar sobre el texto original (sin limpiar) para el motor híbrido
for text in X_test['review_text']:
    # El motor híbrido realiza su propia limpieza interna
    prevision, _, _ = analizar_sentimiento_hibrido(text, model, vectorizer)
    y_pred_hybrid.append(prevision)

# Imprimir reporte de clasificación
print(classification_report(y_test, y_pred_hybrid, labels=labels, digits=4))
print("\n--- Fin del Script ---")