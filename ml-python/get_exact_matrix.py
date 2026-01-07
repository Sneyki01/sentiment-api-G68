import pandas as pd
import joblib
import re
import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import confusion_matrix
from sklearn.utils import resample

# --- CONFIG ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "Big_AHR.csv")

def limpieza_pro(texto):
    texto = str(texto).lower()
    texto = re.sub(r'[^a-zñáéíóúü\s]', '', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto

def categorizar_sentimiento(r):
    if r <= 2: return 'Negativo'
    elif r == 3: return 'Neutro'
    else: return 'Positivo'

# 1. Load and Clean
try:
    df = pd.read_csv(DATA_PATH)
except FileNotFoundError:
    print(f"Error: No se encontró el archivo {DATA_PATH}")
    exit()

df['text_cleaned'] = df['review_text'].apply(limpieza_pro)
df['sentiment'] = df['rating'].apply(categorizar_sentimiento)

# 2. Upsample
df_majority = df[df.sentiment=='Positivo']
df_minority_neg = df[df.sentiment=='Negativo']
df_minority_neu = df[df.sentiment=='Neutro']

df_minority_neg_upsampled = resample(df_minority_neg, replace=True, n_samples=len(df_majority), random_state=42) 
df_minority_neu_upsampled = resample(df_minority_neu, replace=True, n_samples=len(df_majority), random_state=42) 

df_upsampled = pd.concat([df_majority, df_minority_neg_upsampled, df_minority_neu_upsampled])

# 3. Split
X_train, X_test, y_train, y_test = train_test_split(
    df_upsampled['text_cleaned'], df_upsampled['sentiment'], 
    test_size=0.2, random_state=42
)

# 4. Train Vectorizer
vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
X_train_vec = vectorizer.fit_transform(X_train)

# 5. Train Model
base_model = LinearSVC(class_weight='balanced', max_iter=2000, random_state=42)
model_final = CalibratedClassifierCV(base_model, method='sigmoid', cv=5)
model_final.fit(X_train_vec, y_train)

# --- HYBRID LOGIC ---
disparadores_negativos = ["suci", "asc", "mugr", "pelos", "cucarach", "chinch", "hedor", "podrid", "pésim", "rot", "viej", "rob", "estaf"]
cebos_positivos = ["excelente", "increíble", "maravilla", "perfecto", "genial", "recomiendo", "fantástico"]

def predict_hybrid(text):
    # 1. Filtro longitud (simplificado para test)
    if len(text) < 3: return "Neutro"
    
    # 2. Inferencia ML
    vec = vectorizer.transform([text])
    probs = model_final.predict_proba(vec)[0]
    
    # Mapping based on alphabetical order: Negativo, Neutro, Positivo
    idx_neg, idx_neu, idx_pos = 0, 1, 2
    
    conf_neg = probs[idx_neg]
    conf_pos = probs[idx_pos]
    
    # 3. Lógica Neutros
    if abs(conf_pos - conf_neg) < 0.22:
        return "Neutro"
    
    # 4. Motor Sarcasmo
    pred = "Positivo" if conf_pos > conf_neg else "Negativo"
    
    if pred == "Positivo":
        if any(w in text for w in cebos_positivos) and any(w in text for w in disparadores_negativos):
            return "Negativo" 
            
    return pred

print("Calculando Híbrido...")
y_pred_hybrid = [predict_hybrid(t) for t in X_test]

labels = ["Negativo", "Neutro", "Positivo"]
cm_hybrid = confusion_matrix(y_test, y_pred_hybrid, labels=labels)

print("CONFUSION MATRIX ROW 0 (Negativos Reales) - HIBRIDO:")
print(cm_hybrid[0])
