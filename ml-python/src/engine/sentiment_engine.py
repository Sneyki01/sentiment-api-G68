import numpy as np
import re

def analizar_sentimiento_hibrido(texto, modelo, vectorizador):
    """
    Motor Híbrido G68: ML + Reglas de Negación + Intensificadores + Atenuadores
    Calibración Final: Pesos (Pos 0.7 / Neg 1.5) - Umbrales (0.45 / 0.60)
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
        return "Neutro", 0.5, {"nota": "Texto insuficiente para análisis"}

    # 3. CONFIGURACION DE REGLAS SEMANTICAS
    negaciones = {'no', 'sin', 'nunca', 'jamas', 'tampoco', 'ni', 'nada'}
    intensificadores = {'muy', 'sumamente', 'totalmente', 'extremadamente', 'super', 'bastante'}
    atenuadores = {'algo', 'poco', 'ligeramente'}
    
    # LEXICON CON PESOS DECIMALES (Optimizado para Hoteles)
    lexicon_pesos = {
        # POSITIVOS (Elogios Hoteleros)
        "excelente": 0.65, "perfecto": 0.65, "increible": 0.60, "maravilloso": 0.60,
        "impecable": 0.65, "pulcro": 0.60, "reluciente": 0.55,
        "amable": 0.50, "atento": 0.50, "hospitalidad": 0.50, "gentil": 0.45,
        "comodo": 0.40, "confortable": 0.40, "acogedor": 0.45, "almohadas": 0.35, "colchon": 0.35,
        "bien": 0.25, "limpio": 0.35, "limpia": 0.35, "amplio": 0.25, "wifi": 0.30,
        
        # NEUTROS/AMBIGUOS (Tendencia Negativa en Servicio)
        "normal": -0.45, "regular": -0.40, "aceptable": -0.25, "pasable": -0.30,
        
        # NEGATIVOS (Alertas y Quejas)
        "asco": -0.95, "sucio": -0.85, "suciedad": -0.85, "pesimo": -0.90, "terrible": -0.90,
        "moho": -0.85, "mancha": -0.80, "olor": -0.75, "humedad": -0.80, "humedo": -0.70,
        "ruido": -0.70, "bulla": -0.65, "calor": -0.50, "frio": -0.50,
        "roto": -0.75, "viej": -0.60, "antiguo": -0.40, "mal": -0.60,
        "demora": -0.70, "espera": -0.55, "tardan": -0.65, "grosero": -0.85,
        "caro": -0.45, "estafa": -0.95, "robo": -0.95, "lejos": -0.45, "lejano": -0.45
    }

    # 4. PREDICCION BASE DEL MODELO MACHINE LEARNING
    # Usamos el texto con limpieza simple para el vectorizador
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
            
            # Aplicar Lógica de Contexto (Negación, Intensidad, Atenuación)
            # Buscamos hacia atrás, saltando preposiciones cortas (como 'de', 'del')
            modifier = 1.0
            contexto = ""
            idx_prev = i - 1
            if idx_prev >= 0 and tokens[idx_prev] in {'de', 'del', 'la', 'el'}:
                idx_prev -= 1 # Saltamos la preposición
                
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

    # 7. CLASIFICACION POR UMBRALES (CENTRO DESPLAZADO A 0.55)
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