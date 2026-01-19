import re
from nltk.stem import SnowballStemmer

def clean_text(text):
    """Limpia el texto para análisis, eliminando puntuación pero manteniendo tildes y ñ."""
    txt_lower = (text or "").lower()
    return [t.strip() for t in re.sub(r'[^a-zñáéíóúü\s]', ' ', txt_lower).split() if t.strip()]

def get_stopwords():
    """Retorna el set de stopwords informativas para filtrado de features."""
    return {
        'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'ser', 'se', 'no', 'haber',
        'por', 'con', 'su', 'para', 'como', 'estar', 'tener', 'le', 'lo', 'todo',
        'pero', 'más', 'hacer', 'o', 'poder', 'decir', 'este', 'ir', 'otro', 'ese',
        'si', 'me', 'ya', 'ver', 'porque', 'dar', 'cuando', 'él', 'muy', 'sin',
        'vez', 'mucho', 'saber', 'qué', 'sobre', 'mi', 'alguno', 'mismo', 'yo',
        'también', 'hasta', 'año', 'dos', 'querer', 'entre', 'así', 'primero',
        'desde', 'grande', 'eso', 'ni', 'nos', 'llegar', 'pasar', 'tiempo', 'ella',
        'sí', 'día', 'uno', 'poco', 'deber', 'entonces', 'poner', 'cosa',
        'tanto', 'hombre', 'parecer', 'nuestro', 'tan', 'donde', 'ahora', 'parte',
        'después', 'vida', 'quedar', 'siempre', 'creer', 'hablar', 'llevar', 'dejar',
        'nada', 'cada', 'seguir', 'menos', 'nuevo', 'encontrar', 'algo', 'solo',
        'salir', 'tomar', 'conocer', 'vivir', 'sentir', 'tratar',
        'mirar', 'contar', 'empezar', 'esperar', 'buscar', 'existir', 'entrar',
        'trabajar', 'escribir', 'perder', 'producir', 'ocurrir', 'entender', 'pedir',
        'recibir', 'recordar', 'terminar', 'permitir', 'aparecer', 'conseguir',
        'comenzar', 'servir', 'sacar', 'necesitar', 'mantener', 'resultar', 'leer',
        'caer', 'cambiar', 'presentar', 'crear', 'abrir', 'considerar', 'oír',
        'acabar', 'mil', 'contra', 'cual', 'durante', 'ellos', 'arriba', 'grupo',
        'manera', 'tal', 'aquí', 'allí', 'fue', 'era', 'son', 'está',
        'estaba', 'fueron', 'eran', 'estaban', 'sido', 'siendo', 'sea', 'seas',
        'seamos', 'sean', 'fuera', 'fueras', 'fuéramos', 'fueran', 'fuese', 'fueses',
        'fuésemos', 'fuesen', 'he', 'has', 'ha', 'hemos', 'habéis', 'han', 'había',
        'habías', 'habíamos', 'habíais', 'habían', 'hube', 'hubiste', 'hubo',
        'hubimos', 'hubisteis', 'hubieron', 'habré', 'habrás', 'habrá', 'habremos',
        'habréis', 'habrán', 'habría', 'habrías', 'habríamos', 'habríais', 'habrían',
        'haya', 'hayas', 'hayamos', 'hayáis', 'hayan', 'hubiera', 'hubieras',
        'hubiéramos', 'hubierais', 'hubieran', 'hubiese', 'hubieses', 'hubiésemos',
        'hubieseis', 'hubiesen', 'al', 'del', 'los', 'las', 'unos', 'unas'
    }

def get_sustantivos_neutros():
    """Identifica sustantivos comunes que no suelen aportar carga emocional por sí solos."""
    return {
        'agua', 'hotel', 'habitación', 'habitacion', 'ducha', 'baño', 'bano',
        'cama', 'cuarto', 'piso', 'edificio', 'lugar', 'sitio', 'zona',
        'área', 'area', 'espacio', 'sala', 'comedor', 'cocina', 'puerta',
        'ventana', 'pared', 'techo', 'suelo', 'mesa', 'silla', 'mueble',
        'televisión', 'television', 'tv', 'aire', 'luz', 'día', 'dia',
        'noche', 'mañana', 'tarde', 'hora', 'minuto', 'momento', 'vez',
        'persona', 'gente', 'cliente', 'huésped', 'huesped', 'empleado',
        'recepción', 'recepcion', 'entrada', 'salida', 'pasillo', 'escalera',
        'ascensor', 'parking', 'estacionamiento', 'piscina', 'gimnasio',
        'restaurante', 'bar', 'cafetería', 'cafeteria', 'desayuno', 'comida',
        'cena', 'plato', 'bebida', 'café', 'cafe', 'té', 'te', 'vino',
        'cerveza', 'precio', 'costo', 'tarifa', 'reserva', 'booking',
        'check', 'checkout', 'wifi', 'internet', 'teléfono', 'telefono',
        'servicio', 'atención', 'atencion', 'personal', 'equipo', 'staff',
        'ciudad', 'centro', 'playa', 'mar', 'montaña', 'montana', 'vista',
        'ubicación', 'ubicacion', 'distancia', 'metro', 'bus', 'taxi',
        'aeropuerto', 'estación', 'estacion', 'parada', 'calle', 'avenida',
        'barrio', 'vecindario', 'alrededores', 'cercanía', 'cercania'
    }

def es_ngram_valido(ngram, stopwords):
    """Filtra n-gramas que solo contienen stopwords."""
    palabras = ngram.split()
    if len(palabras) == 1:
        return palabras[0] not in stopwords
    if len(palabras) == 2 and all(p in stopwords for p in palabras):
        return False
    return any(p not in stopwords for p in palabras)

def tiene_carga_emocional(palabra, diccionario_stemmed, sustantivos_neutros, stemmer):
    """Heurística para determinar si una palabra tiene carga emocional."""
    if stemmer.stem(palabra) in diccionario_stemmed:
        return True
    if palabra in sustantivos_neutros:
        return False
    
    term_adj = ['oso', 'osa', 'ble', 'nte', 'ivo', 'iva', 'ado', 'ada', 'ido', 'ida', 'ante', 'ente', 'al', 'ar', 'il']
    term_verb = ['aron', 'ieron', 'ó', 'ió', 'é', 'í', 'aste', 'iste']
    
    for term in term_adj + term_verb:
        if palabra.endswith(term) and len(palabra) > len(term) + 2:
            return True
    return False
