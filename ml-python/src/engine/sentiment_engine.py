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
    # Limpieza profunda: Solo nos quedamos con letras y espacios para la detección
    # Esto asegura que "%&$/Cucarachas" sea detectado como "cucarachas"
    texto_limpio = re.sub(r'[^a-zñáéíóúü\s]', ' ', texto.lower())
    tokens = [t.strip() for t in texto_limpio.split() if t.strip()]
    
    if len(tokens) < 2: # Bajamos un poco el umbral para permitir quejas cortas útiles
        return "Neutro", 0.5, {"explicabilidad": {"triggers": ["Texto muy corto"], "areas": []}}

    is_short = len(tokens) < 15

    # --- 2. CAPA BASE (ML DE HOY) ---
    vector = vectorizador.transform([texto_limpio])
    probs = modelo.predict_proba(vector)[0]
    conf_pos_ml = probs[2]

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
        'superficial': -0.6, 'minuscul': -0.7, 'calcetin': -0.8, 'arqueologi': -0.7,
        'terror': -1.0, 'horror': -1.0
    }

    ajuste_semantico = 0.0
    palabras_detectadas = []
    current_multiplier = 1.0
    anclaje_negativo = False
    es_veto_critico_global = False # Variable global para la decisión final
    
    LISTA_NEGRA = {
        'suci', 'asc', 'cucarach', 'chinch', 'sangr', 'moh', 'rob', 'estaf', 
        'peligr', 'mied', 'inund', 'desastr', 'pesadill', 'manch', 'pelos', 
        'humed', 'rancio', 'tabac', 'maltrat', 'ignor', 'ignorart',
        'inexistent', 'caotic', 'caos', 'dolor', 'engañ', 'ruid', 'fri', 'ausenci', 
        'mediocr', 'carisim', 'fall', 'superficial', 'minuscul', 'calcetin', 'arqueologi',
        'terror', 'horror'
    }

    # --- 3. ESCANEO INVERSO CON ANCLAJE G68 REFINADO ---
    neg_actions = {'funcion', 'limpi', 'hay', 'cumpl', 'serv', 'exist', 'respond', 'atend', 'ayud', 'pued', 'tien', 'encontr'}
    fillers = {'hay', 'esta', 'está', 'es', 'son', 'estan', 'están', 'tiene', 'tienen', 'existe', 'existen', 'parece', 'resulta', 'seria', 'sería', 'era'}
    entities = {'habitación', 'habitacion', 'hotel', 'experiencia', 'cama', 'personal', 'recepción', 'recepcion', 'wifi', 'baño', 'bano', 'comida', 'desayuno', 'atención', 'atencion', 'precio', 'ubicación', 'ubicacion', 'aire', 'ruido', 'limpieza', 'piscina', 'instalaciones', 'servicio', 'desayuno', 'pelicula', 'película', 'maravilla'}
    
    for i in reversed(range(len(tokens))):
        word = tokens[i]
        # Skip negations, intensifiers and contrast markers from being primary triggers
        if word in negations or word == "pero" or word in intensifiers:
            if word in contrastes: current_multiplier = 0.35
            continue

        root = stemmer.stem(word)
        es_esta_palabra_veto = False 
        
        # REGLA DE MODIFICADORES G68: Detecta Negaciones y Magnificadores cercanos
        pfx_temp = ""
        found_modifier = False
        
        # 1. Mirar atrás inmediato (ej: "no limpia", "muy buena")
        if i > 0 and (tokens[i-1] in negations or tokens[i-1] in intensifiers):
            pfx_temp = f"{tokens[i-1]} "
            found_modifier = True
        # 2. Mirar atrás con puente (ej: "no esta limpia", "muy es buena")
        elif i > 1 and (tokens[i-2] in negations or tokens[i-2] in intensifiers) and tokens[i-1] in fillers:
            pfx_temp = f"{tokens[i-2]} " # Saltamos el filler (hay/esta)
            found_modifier = True
            
        # Si es una falta o alerta detectada por patrón (Usamos la lista entities global del motor)
        if found_modifier and (root in neg_actions or word in entities):
            ajuste_semantico -= 0.8
            # Solo añadimos si no es redundante
            label = "FALTA" if pfx_temp.strip() in negations else "ALERTA"
            if f"{label}({pfx_temp}{word})" not in palabras_detectadas:
                palabras_detectadas.append(f"{label}({pfx_temp}{word})")
            if root not in ELITE_LEX and root not in LEXICON_G68:
                continue

        if root in ELITE_LEX: base_score = ELITE_LEX[root]
        elif root in LEXICON_G68: base_score = float(LEXICON_G68[root][0])
        else: continue
        
        # --- CÁLCULO DE MODIFICADORES ---
        modifier = 1.0
        if i > 0 and tokens[i-1] in negations: modifier = -1.6
        elif i > 1 and tokens[i-2] in negations and tokens[i-1] in fillers: modifier = -1.5
        elif i > 0 and tokens[i-1] in intensifiers: modifier = 2.0 
        elif i > 1 and tokens[i-2] in intensifiers and tokens[i-1] in fillers: modifier = 1.8
        
        word_score_raw = (base_score * modifier)
        word_score = word_score_raw * current_multiplier
        
        # DETECTOR DE ANCLAJE G68 (Prioridad Términos Críticos)
        if word_score_raw < -0.30: # Usamos el score raw para el veto
            anclaje_negativo = True
            if root in LISTA_NEGRA or word in LISTA_NEGRA:
                es_veto_critico_global = True
                es_esta_palabra_veto = True

        # PENALIZACIÓN SUAVIZADA (Balance de Neutros)
        if word_score > 0 and anclaje_negativo:
            word_score *= 0.6 # Reducido a 0.6 para ser más estricto con falsos positivos
            palabras_detectadas.append(f"FAKE({word})")
            
        ajuste_semantico += word_score
        
        # IMPACTO MINIMO PARA EXPLICABILIDAD (FILTRO RUIDO)
        stopwords_g68 = {'una', 'uno', 'unas', 'unos', 'el', 'la', 'los', 'las', 'un', 'con', 'por', 'para', 'del', 'al', 'de'}
        
        if word in stopwords_g68 and not es_esta_palabra_veto:
            continue

        is_relevant = abs(word_score) > 0.25 or es_esta_palabra_veto
        if is_relevant:
            phrase = word
            phrase_detected = False
            
            # --- VINCULADOR DE TRIGRAMAS G68 (Contexto + Modificador + Palabra) ---
            entity_near = ""
            import unicodedata
            
            def clean_txt(t):
                return "".join(c for c in unicodedata.normalize('NFD', t.lower()) if unicodedata.category(c) != 'Mn')
            
            ENTITIES_CLEAN = {clean_txt(e) for e in entities}
            
            idx_entity = -1
            for offset in [-1, 1, -2, 2, -3, 3]:
                idx = i + offset
                if 0 <= idx < len(tokens):
                    if clean_txt(tokens[idx]) in ENTITIES_CLEAN:
                        entity_near = tokens[idx]
                        idx_entity = idx
                        break
            
            if entity_near:
                # REGLA DE CONECTOR G68: Si hay un "de" en medio, lo incluimos
                has_de = False
                low = min(i, idx_entity)
                high = max(i, idx_entity)
                if high - low == 2 and tokens[low+1].lower() == 'de':
                    has_de = True
                
                # Construcción inteligente de la frase
                if pfx_temp:
                    if idx_entity < i: 
                        phrase = f"{entity_near} {pfx_temp}{word}"
                    else:
                        conn = " de " if has_de else " "
                        phrase = f"{pfx_temp}{word}{conn}{entity_near}"
                else:
                    if idx_entity < i:
                        conn = " de " if has_de else " "
                        phrase = f"{entity_near}{conn}{word}"
                    else:
                        conn = " de " if has_de else " "
                        phrase = f"{word}{conn}{entity_near}"
                phrase_detected = True
            elif pfx_temp:
                phrase = f"{pfx_temp}{word}"
            
            # BOOST DE CONTEXTO
            if phrase_detected:
                word_score *= 1.3
                ajuste_semantico += (word_score * 0.3)
            
            tag = "VETO" if es_esta_palabra_veto else ("FALTA" if "FALTA" in str(palabras_detectadas[-1:]) else "")
            if tag:
                palabras_detectadas.append(f"{tag}({phrase})")
            else:
                palabras_detectadas.append(f"{phrase}({word_score:.1f})")

    # --- 4. FUSIÓN EXPLOSIVA G68 (PRIORIDAD RECALL NEGATIVO) ---
    # Priorizamos seguridad sobre precisión: las reglas mandan si son negativas.
    if ajuste_semantico < -0.1 and es_veto_critico_global:
        impacto_reglas = 0.8
    elif ajuste_semantico < 0:
        impacto_reglas = 0.5
    else:
        impacto_reglas = 0.35

    p_base = conf_pos_ml + (ajuste_semantico * impacto_reglas)
    p_final = max(0.0, min(1.0, p_base))

    if es_veto_critico_global:
        # VETO SOBERANO: Si el usuario dice algo crítico (sucio, asco, robo), es Negativo.
        # No importa que el ML crea que es positivo.
        p_final = 0.10 # Forzar Negativo Extremo
    
    # --- 5. RED DE SEGURIDAD (Sarcasmo) ---
    fake_pos_start = {'gracias', 'lujo', 'genial', 'excelente', 'aplauso', 'encanta', 'idea', 'habilidad'}
    if tokens and tokens[0] in fake_pos_start and (ajuste_semantico < 0.5 or es_veto_critico_global or "FALTA" in str(palabras_detectadas)):
        p_final = 0.15
        palabras_detectadas.append("Red Sarcasmo")

    # --- 6. CLASIFICADOR FINAL PREMIUM (Zonas de Confort) ---
    if p_final < 0.36: prevision = "Negativo"
    elif p_final > 0.60: prevision = "Positivo"
    else: prevision = "Neutro"

    # --- 7. CONSTRUCCIÓN DE METADATA ESTRUCTURADA ---
    print(f"DEBUG: palabras_detectadas = {palabras_detectadas}")
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

