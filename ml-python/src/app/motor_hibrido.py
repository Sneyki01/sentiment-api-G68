import re
import os
import sys
from nltk.stem import SnowballStemmer

# Blindaje de rutas
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from config_g68 import DICCIONARIO_PESOS, KEYWORDS_DEPT, DEBUG_AUDIT
    from utils_hibrido import (clean_text, get_stopwords, get_sustantivos_neutros, 
                               es_ngram_valido, tiene_carga_emocional)
except ImportError:
    from .config_g68 import DICCIONARIO_PESOS, KEYWORDS_DEPT, DEBUG_AUDIT
    from .utils_hibrido import (clean_text, get_stopwords, get_sustantivos_neutros, 
                                es_ngram_valido, tiene_carga_emocional)

stemmer = SnowballStemmer('spanish')
STOPWORDS = get_stopwords()
SUSTANTIVOS_NEUTROS = get_sustantivos_neutros()

# Pre-procesamiento del diccionario para mayor velocidad
DICCIONARIO_STEMMED = {
    " ".join([stemmer.stem(k) for k in key.split()]): val 
    for key, val in DICCIONARIO_PESOS.items()
}
print(f"📦 [G68 DICC] Cargadas {len(DICCIONARIO_STEMMED)} reglas semánticas.")

def enriquecer_respuesta(texto, pred_ia, prob_ia, engine=None):
    """
    Función principal del Motor Híbrido G68.
    Combina predicción de IA con análisis semántico local y veto crítico.
    """
    tokens = clean_text(texto)
    txt_normalizado = " ".join(tokens)
    
    # Herramientas de análisis lingüístico
    negations = {'no', 'sin', 'ni', 'nunca', 'jamás', 'jamas', 'tampoco'}
    intensifiers = {'muy', 'sumamente', 'totalmente', 'completamente', 'bastante', 'extremadamente', 'demasiado', 'realmente'}
    contrast_markers = {'pero', 'aunque', 'mientras', 'excepto', 'lástima', 'lastima', 'sin embargo'}
    
    ajuste_semantico = 0.0
    hallazgos, deptos = set(), set()
    hallazgo_critico = False
    hits = []
    
    # 1. Detección temprana de neutralidad idiomática
    patrones_neutrales = ["ni bien ni mal", "ni mal ni bien", "ni bueno ni malo", "esta bien", "está bien", "todo bien"]
    es_neutral_forzado = any(patron in txt_normalizado for patron in patrones_neutrales)
    
    # 2. Escaneo de tokens (n-gramas)
    n = len(tokens)
    i = n - 1
    while i >= 0:
        found = False
        for size in [4, 3, 2, 1]:
            if i - size + 1 >= 0:
                ngram_tokens = tokens[i - size + 1 : i + 1]
                ngram_stemmed = " ".join([stemmer.stem(t) for t in ngram_tokens])
                peso = DICCIONARIO_STEMMED.get(ngram_stemmed, 0)
                
                if peso != 0:
                    mult = 1.0
                    # Intensificadores
                    if i - size >= 0 and tokens[i - size] in intensifiers:
                        mult = 1.3
                    
                    # Negaciones (ventana 3)
                    for j in range(1, 4):
                        if i - size + 1 - j >= 0 and tokens[i - size + 1 - j] in negations:
                            mult = -1.2 if peso > 0 else 0.0
                            break
                    
                    peso_adj = peso * mult
                    hits.append({'peso': peso_adj, 'word': " ".join(ngram_tokens), 'original_peso': peso})
                    if peso_adj <= -0.8: hallazgo_critico = True
                    
                    # Mapeo Departamental
                    for depto, mapeo in KEYWORDS_DEPT.items():
                        for k_map, v_map in mapeo.items():
                            if " ".join([stemmer.stem(x) for x in k_map.split()]) == ngram_stemmed:
                                hallazgos.add(f"{v_map} ({' '.join(ngram_tokens)})")
                                deptos.add(depto)
                    
                    i -= size
                    found = True
                    break
        if not found: i -= 1

    # 3. Auditoría de ironía y sarcasmo
    match_ironia = re.search(r"si por (\w+) entiendes", txt_normalizado)
    stem_ironia = stemmer.stem(match_ironia.group(1)) if match_ironia else None
    
    tiene_neg_fuerte = any(h['peso'] < -0.4 for h in hits)
    tiene_contraste = any(t in contrast_markers for t in tokens)

    for h in hits:
        p = h['peso']
        if stem_ironia and stemmer.stem(h['word']) == stem_ironia:
            if p > 0: p = -0.5 # Inversión por ironía
        elif p > 0 and (tiene_neg_fuerte or tiene_contraste):
            p *= 0.2 # Atenuación por sarcasmo
        ajuste_semantico += p

    # 4. Lógica de Decisión Final
    prob_ia_val = float(prob_ia)
    solo_neutras = len(hits) > 0 and all(abs(h['original_peso']) < 0.01 for h in hits)
    
    if es_neutral_forzado or solo_neutras:
        final_pred, prob_final, motivo = "Neutro", 0.5, "Neutralidad Forzada"
    elif hallazgo_critico:
        final_pred, prob_final, motivo = "Negativo", 0.99, "Veto Crítico"
    elif ajuste_semantico <= -0.4:
        final_pred, prob_final, motivo = "Negativo", (0.95 if pred_ia == "Negativo" else 0.85), "Semántica Negativa"
    elif ajuste_semantico >= 0.4:
        final_pred, prob_final, motivo = "Positivo", (0.95 if pred_ia == "Positivo" else 0.85), "Semántica Positiva"
    elif abs(ajuste_semantico) < 0.25:
        # Fallback IA Inteligente: Usamos la predicción del modelo ML si no hay señales fuertes locales
        if solo_neutras:
            final_pred, prob_final, motivo = "Neutro", 0.5, "Info Neutra"
        else:
            mapa = {0: "Negativo", 1: "Positivo", 3: "Neutro"}
            # Aseguramos que pred_ia sea tratado como entero para el mapeo
            try:
                clase_id = int(pred_ia)
                final_pred = mapa.get(clase_id, "Neutro")
            except:
                final_pred = "Neutro"
            
            prob_final = prob_ia_val
            motivo = f"IA Fallback ({final_pred})"
    else:
        # Zona Gris
        final_pred = "Positivo" if ajuste_semantico > 0 else "Negativo"
        prob_final, motivo = 0.65, "Zona Gris"

    # Mapeo de seguridad final
    if str(final_pred).isdigit():
        mapa = {0: "Negativo", 1: "Positivo", 3: "Neutro"}
        final_pred = mapa.get(int(final_pred), "Negativo")

    if DEBUG_AUDIT:
        _audit_console(texto, pred_ia, prob_ia_val, ajuste_semantico, hits, deptos, final_pred, prob_final)

    # 5. Generación de Top Features
    top_features = _generar_top_features(texto, hits, engine)

    return {
        "prevision": final_pred,
        "probabilidad": round(prob_final, 4),
        "top_features": top_features,
        "explicabilidad_interna": {  # Propuesta para mañana
            "motivo": motivo,
            "ajuste": round(ajuste_semantico, 2),
            "deptos": list(deptos)
        }
    }

def _audit_console(txt, p_ia, pr_ia, aj, hits, dp, f_p, f_pr):
    mapa = {0: "Negativo", 1: "Positivo", 3: "Neutro"}
    # Ensure we map the IA prediction to its label even if it arrives as a string
    try:
        p_ia_int = int(p_ia)
        p_ia_n = mapa.get(p_ia_int, p_ia)
    except (ValueError, TypeError):
        p_ia_n = p_ia  # fallback to original value if conversion fails
    print(f"\n🔍 [G68 AUDIT] '{txt[:50]}...'", flush=True)
    print(f"   ├─ IA: {p_ia_n} ({pr_ia:.2f}) | Ajuste: {aj:.2f}", flush=True)
    if hits: print(f"   ├─ Señales: {[h['word'] for h in hits[:5]]}", flush=True)
    print(f"   └─ FINAL: {f_p} ({f_pr:.2f})", flush=True)

def _generar_top_features(texto, hits, engine):
    """Extrae las 3 señales más importantes del texto."""
    feats = []
    # Prioridad 1: Críticos del diccionario
    if hits:
        ordenados = sorted(hits, key=lambda h: abs(h['original_peso']), reverse=True)
        # Tomamos los 3 más importantes si superan umbral o si son los únicos hallazgos relevantes
        candidatos = [h for h in ordenados if abs(h['original_peso']) >= 0.8]
        if not candidatos and ordenados:
             candidatos = ordenados[:3] # Fallback a los top encontrados
        
        for h in candidatos[:3]:
            feats.append(h['word'])
    
    # Prioridad 2: Features del modelo ML si faltan
    if len(feats) < 3 and engine:
        try:
            ml_feats = engine.get_top_features_from_model(texto, top_n=10)
            for f_name, _ in ml_feats:
                if es_ngram_valido(f_name, STOPWORDS) and f_name not in feats:
                    if any(tiene_carga_emocional(p, DICCIONARIO_STEMMED, SUSTANTIVOS_NEUTROS, stemmer) for p in f_name.split()):
                        feats.append(f_name)
                if len(feats) >= 3: break
        except: pass
        
    return " | ".join(feats) if feats else "análisis contextual"
