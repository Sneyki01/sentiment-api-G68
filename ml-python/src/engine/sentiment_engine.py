import numpy as np
import re
import json
import os
import math
from nltk.stem import SnowballStemmer

# 1. Configuración del Motor y Rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LEXICON_PATH = os.path.join(BASE_DIR, "data", "raw", "lexicon_final_optimizado.json")

# 2. El "Cerebro" de raíces (Snowball para Español)
stemmer = SnowballStemmer('spanish')

def load_and_stem_lexicon(path):
    """Carga el lexicón de 1385 palabras y lo pre-procesa con raíces."""
    if not os.path.exists(path):
        print(f"⚠️ Error: Lexicón no encontrado en {path}.")
        return {}
    try:
        # Cargamos con utf-8-sig para evitar problemas de BOM
        with open(path, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
            # Portamos la lógica de la rama personal: raíz -> [peso, area, subarea, ...]
            # Esto permite que 'increíbles' coincida con 'increíble'
            return {stemmer.stem(k): v for k, v in data.items()}
    except Exception as e:
        print(f"⚠️ Error al procesar léxico: {e}")
        return {}

# 3. Cargar Léxico y Reglas G68
LEXICON_STEMMED = load_and_stem_lexicon(LEXICON_PATH)
print(f"✅ Lógica G68 Activa: {len(LEXICON_STEMMED)} raíces cargadas para análisis.")

# Palabras que deben ser neutrales (No deben aportar sentimiento por sí solas)
# Esto corrige el error donde 'una' o 'el' tenían pesos negativos en el JSON
STOPWORDS_G68 = {
    'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas', 
    'de', 'del', 'al', 'y', 'en', 'para', 'con', 'por', 'que',
    'habitacion', 'estancia', 'hotel', 'servicio', 'atencion', 'comida'
}
STOPWORDS_ROOTS = {stemmer.stem(w) for w in STOPWORDS_G68}

def analizar_sentimiento_hibrido(texto, modelo, vectorizador):
    """
    Motor Híbrido G68 - Versión Definitiva
    Lógica: ML Calibrado + Stemming + Reglas Semánticas Alexis-Personal
    """
    # 1. LIMPIEZA Y TOKENIZACIÓN
    if not isinstance(texto, str): texto = ""
    texto_limpio = texto.lower().strip()
    # Separar signos de puntuación
    texto_limpio = re.sub(r'([.,!?])', r' \1 ', texto_limpio)
    tokens = texto_limpio.split()
    
    # Validador de longitud mínima (Requisito de negocio)
    palabras_reales = [t for t in tokens if t not in {'.', ',', '!', '?'}]
    if len(palabras_reales) < 3:
        return "Neutro", 0.5, {"nota": "Texto muy corto", "explicabilidad": "Insuficiente"}

    # 2. REGLAS SEMÁNTICAS (Lógica de Polaridad y Intensidad)
    negaciones = {'no', 'sin', 'nunca', 'jamas', 'nada', 'tampoco', 'ni'}
    intensificadores = {'muy', 'super', 'bastante', 'extremadamente', 'totalmente', 'increible', 'perfectamente'}
    
    neg_roots = {stemmer.stem(w) for w in negaciones}
    int_roots = {stemmer.stem(w) for w in intensificadores}

    # 3. PREDICCIÓN BASE (Machine Learning)
    # Limpieza específica para el vectorizador (manejo de ñ y acentos)
    texto_ml = re.sub(r'[^a-zñáéíóúü\s]', '', texto.lower())
    X_vec = vectorizador.transform([texto_ml])
    
    # Obtenemos la probabilidad de la clase 'Positivo' (índice 2 en labels G68)
    # Clases: ['Negativo', 'Neutro', 'Positivo']
    prob_ml = modelo.predict_proba(X_vec)[0][2] 

    # 4. PROCESAMIENTO SEMÁNTICO (Lógica G68)
    score_acumulado = 0.0
    palabras_match = []
    area_detectada = "General"

    for i, word in enumerate(tokens):
        if word in {'.', ',', '!', '?'}: continue
        
        root = stemmer.stem(word)
        
        # Saltamos si es una palabra de ruido (artículo/conector neutro)
        if root in STOPWORDS_ROOTS and root not in neg_roots and root not in int_roots:
            continue

        if root in LEXICON_STEMMED:
            datos_lex = LEXICON_STEMMED[root]
            peso_base = float(datos_lex[0])
            
            # Detección de Área (Si el léxico tiene el dato en la posición 3)
            if len(datos_lex) >= 4 and datos_lex[3] != "General":
                area_detectada = datos_lex[3]

            # Lógica de CONTEXTO (Bigramas)
            modifier = 1.0
            etiqueta = "directo"
            
            if i > 0:
                prev_word = tokens[i-1]
                prev_root = stemmer.stem(prev_word)
                
                # Regla de Inversión de Polaridad
                if prev_root in neg_roots:
                    modifier = -1.2
                    etiqueta = f"negado por '{prev_word}'"
                # Regla de Intensificación
                elif prev_root in int_roots:
                    modifier = 1.6
                    etiqueta = f"potenciado por '{prev_word}'"

            # Aplicar modificador
            valor_intermedio = peso_base * modifier
            
            # --- CALIBRACIÓN G68: BALANZA DE JUSTICIA ---
            if valor_intermedio > 0:
                # Castigo a positivos (x0.7) - Evita el sesgo de "todo es genial"
                peso_final = valor_intermedio * 0.7
                etiqueta += " [G68-Pos-x0.7]"
            elif valor_intermedio < 0:
                # Ampliación de negativos (x1.4) - Prioriza la queja
                peso_final = valor_intermedio * 1.4
                etiqueta += " [G68-Neg-x1.4]"
            else:
                peso_final = 0.0

            score_acumulado += peso_final
            if peso_final != 0:
                palabras_match.append(f"{word} ({etiqueta})")

    # 5. FUSIÓN HÍBRIDA
    # La probabilidad final es la suma del ML + el empuje semántico
    # El ajuste semántico tiene un valor alfa de diseño 0.15 para no romper la escala
    p_final = max(0.0001, min(0.9999, prob_ml + score_acumulado))

    # 6. CATEGORIZACIÓN (Umbrales de Decisión G68)
    # Negativo < 0.45 | Neutro 0.45-0.60 | Positivo > 0.60
    if p_final < 0.45:
        prevision = "Negativo"
    elif p_final > 0.60:
        prevision = "Positivo"
    else:
        prevision = "Neutro"

    # 7. RESPUESTA FINAL
    prefijo_area = f"Área: {area_detectada} | " if area_detectada != "General" else ""
    info_explicabilidad = prefijo_area + (" | ".join(palabras_match) if palabras_match else "Análisis estadístico basado en patrones ML")

    return prevision, round(p_final, 4), {
        "explicabilidad": info_explicabilidad,
        "score_semantico": round(score_acumulado, 4),
        "ml_base": round(prob_ml, 4)
    }