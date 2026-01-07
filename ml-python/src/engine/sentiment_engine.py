import numpy as np

def analizar_sentimiento_hibrido(texto, modelo, vectorizador):
    """
    Motor Híbrido G68: ML + Reglas de Negación + Intensificadores + Lexicón Decimal
    Calibración Final: Pesos (Pos 0.7 / Neg 1.5) - Umbrales (0.45 / 0.60)
    """
    # 1. LIMPIEZA BÁSICA Y TOKENIZACIÓN
    texto_limpio = texto.lower().strip()
    tokens = texto_limpio.split()
    
    # 2. REGLA DE LONGITUD (CONTRATO)
    if len(tokens) < 3:
        return "Neutro", 0.5, {"nota": "Texto insuficiente para análisis"}

    # 3. CONFIGURACIÓN DE REGLAS SEMÁNTICAS
    negaciones = {'no', 'sin', 'nunca', 'jamas', 'tampoco', 'ni', 'nada'}
    intensificadores = {'muy', 'sumamente', 'totalmente', 'extremadamente', 'super', 'bastante'}
    
    # LEXICÓN CON PESOS DECIMALES
    lexicon_pesos = {
        "excelente": 0.60, "increible": 0.55, "perfecto": 0.65, "bien": 0.25,
        "limpio": 0.30, "limpia": 0.30, "comodo": 0.30, "amplio": 0.20,
        "normal": -0.45, "regular": -0.40, "aceptable": -0.25,
        "asco": -0.90, "sucio": -0.80, "suciedad": -0.80, "pesimo": -0.85, 
        "malo": -0.60, "mediocre": -0.50, "terrible": -0.90, "ruido": -0.40
    }

    # 4. PREDICCIÓN BASE DEL MODELO MACHINE LEARNING
    vector = vectorizador.transform([texto_limpio])
    probabilidades = modelo.predict_proba(vector)[0]
    conf_pos_ml = probabilidades[1]  # Probabilidad de la clase positiva

    # 5. PROCESAMIENTO DE LA CAPA SEMÁNTICA (AJUSTE)
    ajuste_semantico = 0.0
    for i, word in enumerate(tokens):
        if word in lexicon_pesos:
            base_score = lexicon_pesos[word]
            modifier = 1.0
            
            # Aplicar Lógica de Contexto (Negación e Intensidad)
            if i > 0 and tokens[i-1] in negaciones:
                modifier = -0.8  # Invierte el sentido del sentimiento
            elif i > 0 and tokens[i-1] in intensificadores:
                modifier = 1.5   # Aumenta la intensidad
            
            word_score = base_score * modifier
            
            # --- REGLA DE PESOS CALIBRADA POR ALEXIS ---
            if word_score < 0:
                word_score *= 1.5  # Castigo firme a lo negativo
            elif word_score > 0:
                word_score *= 0.7  # Filtro de calidad a lo positivo
            
            ajuste_semantico += word_score

    # 6. CÁLCULO DE PROBABILIDAD HÍBRIDA FINAL (p_final)
    p_final = max(0.0, min(1.0, conf_pos_ml + ajuste_semantico))

    # 7. CLASIFICACIÓN POR UMBRALES (CENTRO DESPLAZADO A 0.55)
    # Calibrado para compensar el sesgo positivo del entrenamiento
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
    return prevision, round(p_final, 4), {
        "ml_original": round(conf_pos_ml, 4),
        "ajuste_semantico": round(ajuste_semantico, 4),
        "nota_tecnica": nota
    }