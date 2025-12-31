import re
import string

# Stopwords controladas
# IMPORTANTE: se EXCLUYEN negaciones y modificadores de intensidad
STOPWORDS_ES = {
    "de", "la", "que", "el", "en", "y", "a", "los", "del",
    "las", "por", "un", "para", "con", "una", "su", "al",
    "lo", "como", "más", "sus", "le", "ya", "o", "este",
    "sí", "porque", "esta", "entre", "cuando"
}

# Negaciones que NO deben eliminarse
NEGATIONS = {"no", "nunca", "jamás", "nada", "sin"}

# Intensificadores que aportan señal
INTENSIFIERS = {"muy", "poco", "bastante", "demasiado", "peor", "mal"}

def clean_text(text: str) -> str:
    """
    Limpieza conservadora para minimizar falsos negativos del estado NEGATIVO.

    Principios:
    - Mantener negaciones
    - Mantener intensidad
    - No lematizar
    - No normalizar en exceso
    """
    text = text.lower()

    # Eliminar URLs
    text = re.sub(r"http\S+", "", text)

    text = re.sub(f"[{re.escape(string.punctuation)}]", " ", text)

    # Mantener letras y acentos
    text = re.sub(r"[^a-záéíóúñ\s]", "", text)

    

    tokens = []
    for word in text.split():
        if (
            word in NEGATIONS
            or word in INTENSIFIERS
            or (word not in STOPWORDS_ES and len(word) > 2)
        ):
            tokens.append(word)

    return " ".join(tokens)
