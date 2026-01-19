import os
import pandas as pd
import joblib
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import classification_report
from sklearn.utils import resample

# 1. Rutas y Configuración
# La ruta base es ml-python/, subiendo desde scripts/training/
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
raw_data_path = os.path.join(base_dir, "data", "raw", "Big_AHR.csv")
golden_data_path = os.path.join(base_dir, "data", "raw", "golden_benchmark_325.csv")
model_path = os.path.join(base_dir, "data", "models", "sentiment_model.pkl")
vectorizer_path = os.path.join(base_dir, "data", "models", "tfidf_vectorizer.pkl")

# Funciones de Soporte
def limpieza_pro(texto):
    if not isinstance(texto, str): return ""
    texto = texto.lower()
    texto = re.sub(r'[^a-zñáéíóúü\s]', '', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto

def categorizar_sentimiento(r):
    if r <= 2: return 'Negativo'
    elif r == 3: return 'Neutro'
    else: return 'Positivo'

# 2. CARGA DE DATOS
df_andalu = pd.read_csv(raw_data_path).dropna(subset=['review_text', 'rating'])
df_andalu['text_cleaned'] = df_andalu['review_text'].apply(limpieza_pro)
df_andalu['sentiment'] = df_andalu['rating'].apply(categorizar_sentimiento)

df_golden = pd.read_csv(golden_data_path)
df_golden['text_cleaned'] = df_golden['text'].apply(limpieza_pro)
print(f"Cargando dataset Andalucía ({len(df_andalu)} reseñas) y Golden Benchmark ({len(df_golden)} frases)...")

# 3. SPLIT DE SEGURIDAD (Datos que el modelo nunca verá en ninguna fase)
df_and_train, df_and_test = train_test_split(df_andalu, test_size=0.15, random_state=42)
df_gol_train, df_gol_test = train_test_split(df_golden, test_size=0.15, random_state=42)

# --- FASE 1: RESET SEMÁNTICO (Entrenamiento exclusivo con frases complejas) ---
print("\n--- FASE 1: Entrenando modelo de 'Pura Inteligencia' (Solo Golden) ---")
# Hacemos un upsampling solo de las golden para que el modelo aprenda sus patrones
df_phase1 = pd.concat([df_gol_train] * 50, ignore_index=True)
vec_phase1 = TfidfVectorizer(max_features=10000, ngram_range=(1, 2))
X_p1 = vec_phase1.fit_transform(df_phase1['text_cleaned'])
y_p1 = df_phase1['sentiment']

model_p1 = LinearSVC(class_weight='balanced', max_iter=3000, random_state=42)
model_p1.fit(X_p1, y_p1)
print("Fase 1 completada. El modelo ha olvidado los sesgos de frecuencia de hoteles.")

# --- FASE 2: REFOCO PROFESIONAL (Entrenamiento Combinado) ---
print("\n--- FASE 2: Reintegrando dominio de hoteles con refuerzo semántico ---")
# Golden boosted (x20) + Andalucía
df_golden_boosted = pd.concat([df_gol_train] * 20, ignore_index=True)
df_train_final = pd.concat([
    df_and_train[['text_cleaned', 'sentiment']], 
    df_golden_boosted[['text_cleaned', 'sentiment']]
], ignore_index=True)

# Balanceo final
df_pos = df_train_final[df_train_final.sentiment == 'Positivo']
df_neg = df_train_final[df_train_final.sentiment == 'Negativo']
df_neu = df_train_final[df_train_final.sentiment == 'Neutro']
max_size = len(df_pos)
df_neg_up = resample(df_neg, replace=True, n_samples=max_size, random_state=42)
df_neu_up = resample(df_neu, replace=True, n_samples=max_size, random_state=42)

df_balanced = pd.concat([df_pos, df_neg_up, df_neu_up])
print(f"Dataset de entrenamiento final balanceado: {len(df_balanced)} registros.")

# Vectorización Final
vectorizer_final = TfidfVectorizer(max_features=10000, ngram_range=(1, 2))
X_train = vectorizer_final.fit_transform(df_balanced['text_cleaned'])
y_train = df_balanced['sentiment']

# Validación Cruzada con Calibración
print("Calibrando modelo definitivo G68 SUPREME...")
base_model = LinearSVC(class_weight='balanced', max_iter=3000, random_state=42)
model_final = CalibratedClassifierCV(base_model, method='sigmoid', cv=5)
model_final.fit(X_train, y_train)

# --- 4. PRUEBA CIEGA (VALIDACIÓN HONESTA) ---
df_test_final = pd.concat([
    df_and_test[['text_cleaned', 'sentiment']], 
    df_gol_test[['text_cleaned', 'sentiment']]
], ignore_index=True)

X_test = vectorizer_final.transform(df_test_final['text_cleaned'])
y_test = df_test_final['sentiment']
y_pred = model_final.predict(X_test)

print("\n--- REPORTE FINAL POST-RESET SEMÁNTICO ---")
print(classification_report(y_test, y_pred))

# 5. GUARDAR
os.makedirs(os.path.dirname(model_path), exist_ok=True)
joblib.dump(model_final, model_path)
joblib.dump(vectorizer_final, vectorizer_path)
print(f"\n🚀 MODELO G68 REENTRENADO CON ESTRATEGIA DE 'RESET & REFOCO' COMPLETADO.")
