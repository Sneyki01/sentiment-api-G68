import numpy as np
import re
import json
import os
import math
from nltk.stem import SnowballStemmer

# 1. Configuración del Motor G68 SUPREME-ULTIMATE
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LEXICON_PATH = os.path.join(BASE_DIR, "data", "raw", "lexicon_final_optimizado.json")
stemmer = SnowballStemmer('spanish')

def load_and_stem_lexicon(path):
    if not os.path.exists(path): return {}
    try:
        with open(path, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
            # Todo el léxico de hoy indexado por raíces para precisión máxima
            return {stemmer.stem(k): v for k, v in data.items()}
    except: return {}

LEXICON_G68 = load_and_stem_lexicon(LEXICON_PATH)

def analizar_sentimiento_hibrido(texto, modelo, vectorizador):
    """
    Motor G68 SUPREME-ULTIMATE: Lo mejor de ayer (Suma Directa) + Lo mejor de hoy (Capa Semántica).
    """
    # --- 1. LIMPIEZA Y TOKENIZACIÓN ---
    if not isinstance(texto, str): texto = ""
    texto_p = texto.lower()
    texto_p = re.sub(r'([.,!?])', r' \1 ', texto_p)
    tokens = [t.strip() for t in texto_p.split() if t.strip()]
    
    if len(tokens) < 3:
        return "Neutro", 0.5, {"explicabilidad": "Texto muy corto"}

    is_short = len(tokens) < 15

    # --- 2. CAPA BASE (ML DE HOY - 93.5% ACC) ---
    texto_vector = re.sub(r'[^a-zñáéíóúü\s]', '', texto.lower())
    vector = vectorizador.transform([texto_vector])
    probs = modelo.predict_proba(vector)[0]
    conf_pos_ml = probs[2] # Clase Positiva

    # --- 3. CAPA SEMÁNTICA (AJUSTADA GOLD) ---
    negations = {'no', 'sin', 'nunca', 'jamas', 'tampoco', 'ni', 'nada', 'ningun', 'ninguna'}
    intensifiers = {'muy', 'super', 'bastante', 'extremadamente', 'totalmente', 'increiblemente', 'realmente'}
    contrastes = {'pero', 'aunque', 'sin embargo', 'pena', 'malo', 'lastima', 'fallo', 'problema', 'pésimo', 'horror'}
    excepciones_olor = {'gel', 'jabón', 'flores', 'perfume', 'desayuno', 'café'}
    
    # LÉXICO DE ÉLITE G68
    ELITE_LEX = {
        'rompedor': 0.8, 'exquisit': 0.9, 'soberbi': 0.8, 'impecabl': 0.9,
        'bunker': -0.7, 'moho': -0.8, 'sangre': -0.9, 'cucaracha': -0.9,
        'estaf': -0.9, 'rob': -0.9, 'inundacion': -0.9, 'venen': -0.8,
        'ignor': -0.9, 'ignorart': -0.9, 'despreci': -0.8, 'indiferent': -0.7, 'lent': -0.6,
        'pobr': -0.7, 'viej': -0.6, 'sucio': -0.8, 'asco': -0.8, 'manch': -0.7, 'maltrat': -0.9,
        'caos': -0.8, 'caotic': -0.8, 'inexistent': -0.9, 'dolor': -0.7, 'engañ': -0.9, 'ruid': -0.6,
        'fri': -0.5, 'ausenci': -0.7, 'mediocr': -0.8, 'carisim': -0.8, 'fall': -0.7,
        'superficial': -0.6, 'minuscul': -0.7, 'calcetin': -0.8, 'arqueologi': -0.7
    }

    ajuste_semantico = 0.0
    palabras_detectadas = []
    current_multiplier = 1.0
    anclaje_negativo = False
    es_veto_critico = False
    
    LISTA_NEGRA = {
        'suci', 'asc', 'cucarach', 'chinch', 'sangr', 'moh', 'rob', 'estaf', 
        'peligr', 'mied', 'inund', 'desastr', 'pesadill', 'manch', 'pelos', 
        'humed', 'rancio', 'tabac', 'maltrat', 'ignor', 'ignorart',
        'inexistent', 'caotic', 'caos', 'dolor', 'engañ', 'ruid', 'fri', 'ausenci', 
        'mediocr', 'carisim', 'fall', 'superficial', 'minuscul', 'calcetin', 'arqueologi'
    }

    # --- 3. ESCANEO INVERSO CON ANCLAJE G68 REFINADO ---
    neg_actions = {'funcion', 'limpi', 'hay', 'cumpl', 'serv', 'exist', 'respond', 'atend', 'ayud', 'pued', 'tien', 'encontr'}
    
    for i in reversed(range(len(tokens))):
        word = tokens[i]
        
        # 'no' y similares no puntúan por sí mismos, son modificadores
        if word in negations or word == "pero":
            if word in contrastes: current_multiplier = 0.35
            continue

        root = stemmer.stem(word)
        
        # Regla: no + verbo_acción (ej: 'no funciona', 'no hay')
        if i > 0 and tokens[i-1] in negations:
            if root in neg_actions:
                ajuste_semantico -= 0.8 # Castigo por falta de servicio/acción
                palabras_detectadas.append(f"FALTA({word})")
                continue # Ya procesado como patrón

        if root in ELITE_LEX: base_score = ELITE_LEX[root]
        elif root in LEXICON_G68: base_score = float(LEXICON_G68[root][0])
        else: continue
        
        modifier = 1.0
        # Modificador de negación estándar (ej: 'no excelente' -> negativo)
        if i > 0 and tokens[i-1] in negations: 
            modifier = -1.6
        elif i > 0 and tokens[i-1] in intensifiers: 
            modifier = 1.8
        
        word_score_raw = (base_score * modifier)
        word_score = word_score_raw * current_multiplier
        
        # DETECTOR DE ANCLAJE G68 (Prioridad Términos Críticos)
        if word_score_raw < -0.30: # Usamos el score raw para el veto
            anclaje_negativo = True
            if root in LISTA_NEGRA or word in LISTA_NEGRA:
                es_veto_critico = True
                palabras_detectadas.append(f"VETO({word})")

        # PENALIZACIÓN SUAVIZADA (Balance de Neutros)
        if word_score > 0 and anclaje_negativo:
            word_score *= 0.6 # Reducido a 0.6 para ser más estricto con falsos positivos
            palabras_detectadas.append(f"FAKE({word})")
            
        ajuste_semantico += word_score
        
        # IMPACTO MINIMO PARA EXPLICABILIDAD (FILTRO RUIDO)
        stopwords_g68 = {'una', 'uno', 'unas', 'unos', 'el', 'la', 'los', 'las', 'un', 'con', 'por', 'para', 'del', 'al'}
        
        # Si es stopword y NO es veto crítico, ignorar siempre
        if word in stopwords_g68 and not es_veto_critico:
            continue

        is_relevant = abs(word_score) > 0.25 and len(word) > 2
        if is_relevant or es_veto_critico or (word_score < 0 and anclaje_negativo):
            # --- VINCULADOR DE CONTEXTO G68 REFINADO ---
            # Si detectamos una palabra clave, miramos si hay un sustantivo al lado
            phrase = word
            # Lista extendida de entidades críticas del sector
            entities = {'habitación', 'habitacion', 'cama', 'personal', 'recepción', 'recepcion', 'wifi', 'baño', 'bano', 'comida', 'desayuno', 'atención', 'atencion', 'precio', 'ubicación', 'ubicacion', 'aire', 'ruido', 'limpieza', 'piscina', 'instalaciones', 'servicio', 'desayuno'}
            
            phrase_detected = False
            # Mirar atrás (ej: "cama dura")
            if i > 0 and tokens[i-1].lower() in entities:
                phrase = f"{tokens[i-1]} {word}"
                phrase_detected = True
            # Mirar adelante (ej: "sucia habitación")
            elif i < len(tokens) - 1 and tokens[i+1].lower() in entities:
                phrase = f"{word} {tokens[i+1]}"
                phrase_detected = True
            
            # BOOST DE CONTEXTO: Las frases pesan un 30% más que las palabras sueltas
            if phrase_detected:
                word_score *= 1.3
                ajuste_semantico += (word_score * 0.3) # Sumamos el excedente del boost
            
            tag = "VETO" if es_veto_critico else ("FALTA" if "FALTA" in str(palabras_detectadas[-1:]) else "")
            if tag:
                palabras_detectadas.append(f"{tag}({phrase})")
            else:
                palabras_detectadas.append(f"{phrase}({word_score:.1f})")

    # --- 4. FUSIÓN EXPLOSIVA G68 (PRIORIDAD RECALL NEGATIVO) ---
    # Priorizamos seguridad sobre precisión: las reglas mandan si son negativas.
    impacto_reglas = 0.60 if ajuste_semantico < 0 else 0.30
    p_base = conf_pos_ml + (ajuste_semantico * impacto_reglas)
    p_final = max(0.0, min(1.0, p_base))

    if es_veto_critico:
        # VETO SOBERANO: Si el usuario dice algo crítico (sucio, asco, robo), es Negativo.
        # No importa que el ML crea que es positivo.
        p_final = 0.10 # Forzar Negativo Extremo
    
    # --- 5. RED DE SEGURIDAD (Sarcasmo) ---
    fake_pos_start = {'gracias', 'lujo', 'genial', 'excelente', 'aplauso', 'encanta', 'idea', 'habilidad'}
    if tokens[0] in fake_pos_start and (ajuste_semantico < 0.3 or es_veto_critico):
        p_final = 0.15
        palabras_detectadas.append("Red Sarcasmo")

    # --- 6. CLASIFICADOR FINAL PREMIUM (Zonas de Confort) ---
    if p_final < 0.36: prevision = "Negativo"
    elif p_final > 0.60: prevision = "Positivo"
    else: prevision = "Neutro"

    # --- 7. CONSTRUCCIÓN DE METADATA ESTRUCTURADA ---
    # Procesamos los resultados internos para devolver listas limpias directamente
    candidates = []
    
    # Extraemos palabras de los marcadores internos (ej: "sucio(-0.8)", "VETO(sucio)")
    for item in palabras_detectadas:
        # item formato: "PALABRA(SCORE)" o "TAG(PALABRA)"
        if '(' in item:
            parts = item.split('(')
            tag_or_word = parts[0]
            content = parts[1].replace(')', '')
            
            # Si es tag, el score es implícito alto o necesitamos buscalo
            # Simplicidad: si es tag, usamos un score dummy alto (1.0) para que salga primero
            if tag_or_word in ["VETO", "FAKE", "FALTA"]:
                final_word = content
                abs_score = 1.0 
            else:
                final_word = tag_or_word
                try:
                    # content debería ser el score float str
                    abs_score = abs(float(content))
                except:
                    abs_score = 0.0

            # Deduplicación básica al añadir
            if final_word:
                # Chequear si ya existe
                exists = False
                for c in candidates:
                    if c['word'] == final_word:
                        exists = True
                        break
                if not exists:
                    # CÁLCULO DE PRIORIDAD DE DOMINIO
                    priority_score = abs_score
                    
                    # Para frases, intentamos sacar el stem de la palabra principal (adjetivo/veto)
                    # o probamos con la frase completa.
                    found_area = False
                    for part in final_word.split():
                        p_root = stemmer.stem(part)
                        if p_root in LEXICON_G68 and len(LEXICON_G68[p_root]) > 1:
                            found_area = True
                            break
                    
                    root = stemmer.stem(final_word.split()[-1]) # Stem de la última palabra suele ser el adjetivo
                    
                    # 1. Boost Máximo: Veto, Elite, o Falta grave
                    if root in ELITE_LEX or root in LISTA_NEGRA or tag_or_word in ["VETO", "FALTA"]:
                        priority_score *= 2.0
                    # 2. Boost Medio: Palabras con Área definida (Contexto Hotelero)
                    elif found_area:
                        priority_score *= 1.5
                    
                    # FILTRO FINAL DE STOPWORDS (Incluso si pasaron el filtro inicial)
                    if final_word.lower() in stopwords_g68:
                        continue
                        
                    candidates.append({
                        'word': final_word, 
                        'score': abs_score,
                        'priority': priority_score
                    })

    # FILTRADO AGRESIVO DE DOMINIO (Solo Sectores Críticos)
    # Si hay al menos una palabra de dominio (Priority > 1.2), matamos las genéricas.
    has_domain_word = any(c['priority'] > 1.2 for c in candidates)
    
    if has_domain_word:
         candidates = [c for c in candidates if c['priority'] > 1.2]

    # ORDENAMIENTO POR PRIORIDAD (Mayor a menor)
    candidates.sort(key=lambda x: x['priority'], reverse=True)
    
    # TOP 3 STRICT (Focus Absoluto)
    top_candidates = candidates[:3]
    
    triggers_clean = []
    areas_clean = set()

    # WHITELIST DE ÁREAS RESPONSABLES (Sectorización Hotelera)
    AREAS_RELEVANTES = {
        "Habitación", "Habitacion", "Limpieza", "Servicio", "Personal", 
        "Gastronomía", "Gastronomia", "Instalaciones", "Ubicación", "Ubicacion", 
        "Economía", "Economico", "Conectividad", "Gestión", "Gestion", "Alojamiento",
        "Atención", "Atencion"
    }

    for cand in top_candidates:
        w = cand['word']
        triggers_clean.append(w)
        
        # Buscamos áreas
        stem = stemmer.stem(w)
        if stem in LEXICON_G68:
            # LEXICON_G68[stem] = [score, area1, area2...]
            areas_found = LEXICON_G68[stem][1:]
            for area in areas_found:
                # SOLO EL PRIMER ÁREA RELEVANTE POR PALABRA (Mapeo 1-a-1)
                if area in AREAS_RELEVANTES:
                    areas_clean.add(area)
                    break # Salir al encontrar la primera área válida para esta palabra

    return prevision, round(p_final, 4), {
        "votos": "Veto/Ancla" if anclaje_negativo else "Balance",
        "score_reglas": round(ajuste_semantico, 4),
        "explicabilidad": {
            "triggers": triggers_clean,
            "areas": list(areas_clean)
        }
    }

