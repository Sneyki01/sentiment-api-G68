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
# Usamos el nombre exacto de tu archivo

# Busca la línea 11 aproximadamente y cámbiala por esta:
try:
    # Ruta relativa desde la raíz del proyecto
    df = pd.read_csv("ml-python/data/raw/Big_AHR.csv") 
    print(f"✅ Datos cargados: {df.shape[0]} registros encontrados.")
except FileNotFoundError:
    print(f"❌ Error: No se encontró el archivo en ml-python/data/raw/Big_AHR.csv")
    exit()

# 2. LIMPIEZA Y PREPARACIÓN (Manejando ñ y acentos)
def limpieza_pro(texto):
    texto = str(texto).lower()
    texto = re.sub(r'[^a-zñáéíóúü\s]', '', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto

print("Limpiando textos...")
df['text_cleaned'] = df['review_text'].apply(limpieza_pro)

# Lógica de sentimientos basada en el rating (1-5)
def categorizar_sentimiento(r):
    if r <= 2: return 'Negativo'
    elif r == 3: return 'Neutro'
    else: return 'Positivo'

df['sentiment'] = df['rating'].apply(categorizar_sentimiento)

# Balance the dataset
df_majority = df[df.sentiment=='Positivo']
df_minority_neg = df[df.sentiment=='Negativo']
df_minority_neu = df[df.sentiment=='Neutro']
 
# Upsample minority class
df_minority_neg_upsampled = resample(df_minority_neg, 
                                 replace=True,     # sample with replacement
                                 n_samples=len(df_majority),    # to match majority class
                                 random_state=42) # reproducible results
 
df_minority_neu_upsampled = resample(df_minority_neu, 
                                 replace=True,     # sample with replacement
                                 n_samples=len(df_majority),    # to match majority class
                                 random_state=42) # reproducible results
 
# Combine majority class with upsampled minority class
df_upsampled = pd.concat([df_majority, df_minority_neg_upsampled, df_minority_neu_upsampled])


# 3. DIVISIÓN DE DATOS
X_train, X_test, y_train, y_test = train_test_split(
    df_upsampled['text_cleaned'], df_upsampled['sentiment'], 
    test_size=0.2, random_state=42
)

# 4. VECTORIZACIÓN (TF-IDF con Bigramas)
vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# 5. ENTRENAMIENTO CALIBRADO (Para la variabilidad de probabilidad)
print("Entrenando modelo con soporte para probabilidades reales...")
base_model = LinearSVC(class_weight='balanced', max_iter=2000, random_state=42)
model_final = CalibratedClassifierCV(base_model, method='sigmoid', cv=5)
model_final.fit(X_train_vec, y_train)

# 6. MÉTRICAS PARA EL ENTREGABLE
y_pred = model_final.predict(X_test_vec)
print("\n--- REPORTE DE RENDIMIENTO ---")
print(classification_report(y_test, y_pred))

# 7. GUARDAR ARCHIVOS PARA LA API
import os
os.makedirs("ml-python/data/models", exist_ok=True)
joblib.dump(model_final, "ml-python/data/models/sentiment_model.pkl")
joblib.dump(vectorizer, "ml-python/data/models/tfidf_vectorizer.pkl")

print("\n🚀 ¡Archivos .pkl actualizados! Ahora tu API devolverá probabilidades reales.")