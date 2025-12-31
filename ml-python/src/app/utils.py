import re
import nltk
from nltk.corpus import stopwords

# --- CONFIGURACIÓN DE RECURSOS ---
# Descargamos las stopwords solo si no están presentes para optimizar velocidad en la nube
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

SPANISH_STOPWORDS = set(stopwords.words('spanish'))

def clean_text_optimized(text: str) -> str:
    """
    Realiza una limpieza profunda y optimizada para modelos de Deep Learning.
    Mantiene la estructura semántica necesaria para redes neuronales (LSTM).
    """
    if not isinstance(text, str):
        return ""

    # 1. Normalización a minúsculas
    text = text.lower()

    # 2. Eliminación de ruido (URLs y correos electrónicos)
    text = re.sub(r"http\S+|www\S+|\S+@\S+", "", text)

    # 3. Limpieza de caracteres: Mantiene letras, tildes y la 'ñ'
    # Eliminamos números y puntuación que no aportan sentimiento
    text = re.sub(r"[^a-záéíóúñü\s]", " ", text)

    # 4. Normalización de espacios
    text = re.sub(r"\s+", " ", text).strip()

    # 5. Tokenización y remoción de Stopwords
    tokens = text.split()
    tokens_filtros = [word for word in tokens if word not in SPANISH_STOPWORDS]

    return " ".join(tokens_filtros)