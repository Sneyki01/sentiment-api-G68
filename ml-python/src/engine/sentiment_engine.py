import numpy as np
import re
import json
import os

# Cargar léxico completo al inicio (solo una vez)
LEXICON_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "..", "data", "raw", "lexicon_final_optimizado.json")
try:
    with open(LEXICON_PATH, 'r', encoding='utf-8') as f:
        LEXICON_COMPLETO = json.load(f)
    print(f"✅ Léxico cargado: {len(LEXICON_COMPLETO)} palabras")
except Exception as e:
    print(f"⚠️ No se pudo cargar el léxico completo: {e}")
    LEXICON_COMPLETO = {}

def analizar_sentimiento_hibrido(texto, modelo, vectorizador):
    """
    Motor Híbrido G68: ML + Léxico Completo (1365 palabras) + Reglas de Negación
    Calibración Final: Pesos (Pos 0.7 / Neg 1.5) - Umbrales (0.45 / 0.60)
    Soporte: Hotelero Especializado | XAI (Explicabilidad)
    """
    # 1. LIMPIEZA MEJORADA (Manejo de signos de puntuación)
    if not isinstance(texto, str):
        texto = ""
    texto_limpio = texto.lower().strip()
    # Separamos puntos y comas con espacios para que no se peguen a las palabras
    texto_limpio = re.sub(r'([.,!?])', r' \1 ', texto_limpio)
    tokens = texto_limpio.split()
    
    # 2. REGLA DE LONGITUD (CONTRATO)
    # Filtramos los signos para contar solo palabras reales
    palabras_reales = [t for t in tokens if t not in {'.', ',', '!', '?'}]
    if len(palabras_reales) < 3:
        return "Neutro", 0.5, {"nota": "Texto insuficiente para análisis", "explicabilidad": "Texto muy corto"}

    # 3. CONFIGURACION DE REGLAS SEMANTICAS (Español Hotelero)
    negaciones = {'no', 'sin', 'nunca', 'jamas', 'tampoco', 'ni', 'nada'}
    intensificadores = {'muy', 'sumamente', 'totalmente', 'extremadamente', 'super', 'bastante'}
    atenuadores = {'algo', 'poco', 'ligeramente'}
    
    # 4. CONVERTIR LEXICON JSON A DICCIONARIO DE PESOS
    # Formato JSON: {"palabra": [peso, categoria, ...]}
    lexicon_pesos = {}
    for palabra, datos in LEXICON_COMPLETO.items():
        if isinstance(datos, list) and len(datos) > 0:
            try:
                lexicon_pesos[palabra] = float(datos[0])  # El peso está en la primera posición
            except (ValueError, TypeError):
                continue

    # 4. PREDICCION BASE DEL MODELO MACHINE LEARNING
    texto_vector = re.sub(r'[^a-zñáéíóúü\s]', '', texto.lower())
    vector = vectorizador.transform([texto_vector])
    probabilidades = modelo.predict_proba(vector)[0]
    conf_pos_ml = probabilidades[1]  # Probabilidad de la clase positiva

    # 5. PROCESAMIENTO DE LA CAPA SEMANTICA (AJUSTE)
    ajuste_semantico = 0.0
    palabras_detectadas = []
    
    for i, word in enumerate(tokens):
        if word in lexicon_pesos:
            base_score = lexicon_pesos[word]
            
            # Aplicar Lógica de Contexto
            modifier = 1.0
            contexto = ""
            idx_prev = i - 1
            if idx_prev >= 0 and tokens[idx_prev] in {'de', 'del', 'la', 'el'}:
                idx_prev -= 1
                
            if idx_prev >= 0:
                if tokens[idx_prev] in negaciones:
                    modifier = -0.8
                    contexto = f"negado por '{tokens[idx_prev]}'"
                elif tokens[idx_prev] in intensificadores:
                    modifier = 1.5
                    contexto = f"intensificado por '{tokens[idx_prev]}'"
                elif tokens[idx_prev] in atenuadores:
                    modifier = 0.5
                    contexto = f"atenuado por '{tokens[idx_prev]}'"
            
            word_score = base_score * modifier
            palabras_detectadas.append(f"{word} ({contexto if contexto else 'directo'})")
            
            # --- REGLA DE PESOS CALIBRADA POR EQUIPO G68 ---
            if word_score < 0:
                word_score *= 1.5  # Castigo firme a lo negativo
            elif word_score > 0:
                word_score *= 0.7  # Filtro de calidad a lo positivo
            
            ajuste_semantico += word_score

    # 6. CALCULO DE PROBABILIDAD HIBRIDA FINAL (p_final)
    p_final = max(0.0, min(1.0, conf_pos_ml + ajuste_semantico))

    # 7. CLASIFICACION POR UMBRALES
    umbral_negativo = 0.45  
    umbral_positivo = 0.60  

    if p_final < umbral_negativo:
        prevision = "Negativo"
        nota = "G68: Prioridad de queja detectada"
    elif p_final > umbral_positivo:
        prevision = "Positivo"
        nota = "G68: Satisfaccion validada por encima del sesgo"
    else:
        prevision = "Neutro"
        nota = "G68: Experiencia mixta o ambigua"

    # 8. RESPUESTA PARA LA API / LOTE
    explicabilidad = " | ".join(palabras_detectadas) if palabras_detectadas else "Análisis por patrones estadísticos (ML)"
    
    return prevision, round(p_final, 4), {
        "ml_original": round(conf_pos_ml, 4),
        "ajuste_semantico": round(ajuste_semantico, 4),
        "explicabilidad": explicabilidad,
        "nota_tecnica": nota
    }