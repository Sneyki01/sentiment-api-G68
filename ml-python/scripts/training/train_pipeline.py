import os
import pandas as pd
import joblib
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.utils import resample

# 1. CARGA DE DATOS
try:
    # La ruta base es ml-python/, subiendo desde scripts/training/
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    input_file = os.path.join(base_dir, "data", "raw", "Big_AHR.csv")
    golden_file = os.path.join(base_dir, "data", "raw", "golden_benchmark_325.csv")
    
    # 1.1 Dataset Principal
    df_main = pd.read_csv(input_file)
    df_main = df_main.rename(columns={'review_text': 'text'})
    
    def categorizar_sentimiento(r):
        if r <= 2: return 'Negativo'
        elif r == 3: return 'Neutro'
        else: return 'Positivo'
    
    df_main['sentiment'] = df_main['rating'].apply(categorizar_sentimiento)
    
    # 1.2 Golden Dataset
    df_golden = pd.read_csv(golden_file)
    
    # 1.3 Fusión
    df = pd.concat([
        df_main[['text', 'sentiment', 'rating']], 
        df_golden[['text', 'sentiment']]
    ], ignore_index=True)
    
    print(f"✅ Datos combinados: {df.shape[0]} registros.")

    # LIMPIEZA BÁSICA (Nulos y Duplicados)
    df.dropna(subset=['text', 'sentiment'], inplace=True)
    df.drop_duplicates(subset=['text'], inplace=True)
    print(f"📉 Datos tras limpiar nulos/duplicados: {df.shape[0]} registros únicos.")

except Exception as e:
    print(f"❌ Error crítico en carga: {e}")
    exit()

# 2. LIMPIEZA PRO
def limpieza_pro(texto):
    texto = str(texto).lower()
    texto = re.sub(r'[^a-zñáéíóúü\s]', '', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto

print("Limpiando textos...")
df['text_cleaned'] = df['text'].apply(limpieza_pro)

# Balance the dataset
df_majority = df[df.sentiment=='Positivo']
df_minority_neg = df[df.sentiment=='Negativo']
df_minority_neu = df[df.sentiment=='Neutro']
 
df_minority_neg_upsampled = resample(df_minority_neg, 
                                 replace=True, 
                                 n_samples=len(df_majority), 
                                 random_state=42)
 
df_minority_neu_upsampled = resample(df_minority_neu, 
                                 replace=True, 
                                 n_samples=len(df_majority), 
                                 random_state=42)
 
df_upsampled = pd.concat([df_majority, df_minority_neg_upsampled, df_minority_neu_upsampled])

# 3. DIVISIÓN DE DATOS
X_train, X_test, y_train, y_test = train_test_split(
    df_upsampled['text_cleaned'], df_upsampled['sentiment'], 
    test_size=0.2, random_state=42
)

# 4. VECTORIZACIÓN
vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# 5. ENTRENAMIENTO
print("Entrenando modelo con soporte para probabilidades reales...")
base_model = LinearSVC(class_weight='balanced', max_iter=2000, random_state=42, dual='auto')
model_final = CalibratedClassifierCV(base_model, method='sigmoid', cv=5)
model_final.fit(X_train_vec, y_train)

# 6. MÉTRICAS
y_pred = model_final.predict(X_test_vec)
print("\n--- REPORTE DE RENDIMIENTO ---")
print(classification_report(y_test, y_pred))

# 7. GUARDAR
os.makedirs(os.path.join(base_dir, "data", "models"), exist_ok=True)
joblib.dump(model_final, os.path.join(base_dir, "data", "models", "sentiment_model.pkl"))
joblib.dump(vectorizer, os.path.join(base_dir, "data", "models", "tfidf_vectorizer.pkl"))

print("\n🚀 ¡Archivos .pkl actualizados con el Golden Dataset!")