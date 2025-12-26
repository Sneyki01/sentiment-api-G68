import pandas as pd
import os
import joblib
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC # <--- Cambio de modelo
from sklearn.pipeline import Pipeline
from sklearn.utils import resample

# --- CONFIGURACIÓN DE RUTAS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'raw', 'Big_AHR.csv')
MODEL_DIR = os.path.join(BASE_DIR, 'data', 'models')
os.makedirs(MODEL_DIR, exist_ok=True)

def limpiar_texto(text):
    if not isinstance(text, str): return ""
    text = text.lower()
    text = re.sub(r'[^a-zñáéíóú\s]', '', text)
    return re.sub(r'\s+', ' ', text).strip()

print("⚖️ Entrenando con SVM (Support Vector Machine) para eliminar sesgos...")

# 1. CARGA Y LIMPIEZA
df = pd.read_csv(DATA_PATH).dropna(subset=['review_text', 'label'])
df['label'] = df['label'].astype(int)
df = df.drop_duplicates(subset=['review_text'])
df['clean_text'] = df['review_text'].apply(limpiar_texto)

# 2. BALANCEO ESTRATÉGICO
df_neg = df[df['label'] == 0]
df_pos = df[df['label'] == 1]
df_pos_bal = resample(df_pos, replace=False, n_samples=len(df_neg), random_state=42)
df_final = pd.concat([df_neg, df_pos_bal])

# 3. PIPELINE CON SVM
X_train, X_test, y_train, y_test = train_test_split(
    df_final['clean_text'], df_final['label'], test_size=0.2, random_state=42
)

# El LinearSVC es excelente para clasificación de texto
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(ngram_range=(1, 3), max_features=5000, min_df=2)),
    ('clf', LinearSVC(class_weight='balanced', C=1.0, random_state=42))
])

print("🧠 Entrenando el motor SVM...")
pipeline.fit(X_train, y_train)

# 4. GUARDADO
joblib.dump(pipeline, os.path.join(MODEL_DIR, 'modelo_sentimiento_pipeline.pkl'))
print(f"💾 Nuevo modelo SVM guardado en: {MODEL_DIR}")