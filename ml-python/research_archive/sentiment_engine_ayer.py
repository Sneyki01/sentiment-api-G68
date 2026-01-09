import numpy as np
import re

def analizar_sentimiento_hibrido_ayer(texto, modelo, vectorizador):
    """
    Motor Híbrido G68 (VERSION AYER): ML + Reglas de Negación + Intensificadores + Atenuadores
    Calibración: Pesos (Pos 0.7 / Neg 1.5) - Umbrales (0.45 / 0.60)
    """
    # 1. LIMPIEZA
    if not isinstance(texto, str):
        texto = ""
    texto_limpio = texto.lower().strip()
    texto_limpio = re.sub(r'([.,!?])', r' \1 ', texto_limpio)
    tokens = texto_limpio.split()
    
    # 2. REGLA DE LONGITUD
    palabras_reales = [t for t in tokens if t not in {'.', ',', '!', '?'}]
    if len(palabras_reales) < 3:
        return "Neutro", 0.5, {"explicabilidad": "Texto muy corto"}

    # 3. CONFIGURACION DE REGLAS SEMANTICAS (Estatunidense ayer)
    negaciones = {'no', 'sin', 'nunca', 'jamas', 'tampoco', 'ni', 'nada'}
    intensificadores = {'muy', 'sumamente', 'totalmente', 'extremadamente', 'super', 'bastante'}
    atenuadores = {'algo', 'poco', 'ligeramente'}
    
    lexicon_pesos = {
        "excelente": 0.65, "perfecto": 0.65, "increible": 0.60, "maravilloso": 0.60,
        "impecable": 0.65, "pulcro": 0.60, "reluciente": 0.55,
        "amable": 0.50, "atento": 0.50, "hospitalidad": 0.50, "gentil": 0.45,
        "comodo": 0.40, "confortable": 0.40, "acogedor": 0.45, "wifi": 0.30,
        "limpio": 0.35, "limpia": 0.35, "amplio": 0.25, "bien": 0.25,
        "normal": -0.45, "regular": -0.40, "aceptable": -0.25, "pasable": -0.30,
        "asco": -0.95, "sucio": -0.85, "suciedad": -0.85, "pesimo": -0.90, "terrible": -0.90,
        "moho": -0.85, "mancha": -0.80, "olor": -0.75, "humedad": -0.80, "humedo": -0.70,
        "ruido": -0.70, "bulla": -0.65, "calor": -0.50, "frio": -0.50,
        "roto": -0.75, "viejo": -0.60, "antiguo": -0.40, "mal": -0.60,
        "demora": -0.70, "espera": -0.55, "tardan": -0.65, "grosero": -0.85,
        "caro": -0.45, "estafa": -0.95, "robo": -0.95, "lejos": -0.45, "lejano": -0.45,
        "cucarachas": -0.95, "bichos": -0.80, "chinches": -0.95
    }

    # 4. PREDICCION BASE ML
    texto_vector = re.sub(r'[^a-zñáéíóúü\s]', '', texto.lower())
    vector = vectorizador.transform([texto_vector])
    probabilidades = modelo.predict_proba(vector)[0]
    # OJO: Ayer se usaba el índice 1 para Positivo (dependiendo de como estaba el modelo ayer)
    # Para ser comparables hoy, usaremos el índice 2 que es el Positivo en el modelo actual [Neg, Neu, Pos]
    conf_pos_ml = probabilidades[2] 

    # 5. PROCESAMIENTO SEMÁNTICO
    ajuste_semantico = 0.0
    for i, word in enumerate(tokens):
        if word in lexicon_pesos:
            base_score = lexicon_pesos[word]
            modifier = 1.0
            idx_prev = i - 1
            if idx_prev >= 0 and tokens[idx_prev] in {'de', 'del', 'la', 'el'}:
                idx_prev -= 1
            if idx_prev >= 0:
                if tokens[idx_prev] in negaciones: modifier = -0.8
                elif tokens[idx_prev] in intensificadores: modifier = 1.5
                elif tokens[idx_prev] in atenuadores: modifier = 0.5
            
            word_score = base_score * modifier
            if word_score < 0: word_score *= 1.5
            elif word_score > 0: word_score *= 0.7
            ajuste_semantico += word_score

    # 6. CALCULO FINAL
    p_final = max(0.0, min(1.0, conf_pos_ml + ajuste_semantico))

    # 7. CLASIFICACION
    if p_final < 0.45: prevision = "Negativo"
    elif p_final > 0.60: prevision = "Positivo"
    else: prevision = "Neutro"

    return prevision, round(p_final, 4), {"score": round(ajuste_semantico, 4)}
