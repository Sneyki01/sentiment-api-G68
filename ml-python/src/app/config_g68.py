import os
# Prioridad: 1. Variable de entorno 'G68_AUDIT' | 2. Valor manual (True/False)
DEBUG_AUDIT = os.getenv("G68_AUDIT", "True").lower() == "true"




DICCIONARIO_PESOS = {
    # --- NIVEL CRÍTICO: VETOS Y RIESGO REPUTACIONAL ---
    "estafa": -1.0, "robo": -1.0, "engaño": -0.9, "fraude": -1.0,
    "peligro": -0.9, "asco": -0.8, "chinches": -1.0, "cucaracha": -0.9,
    "sangre": -0.9, "moho": -0.8, "veneno": -0.8, "terror": -1.0, "horror": -1.0,
    "maltrato": -0.9, "inundacion": -0.9, "ignoro": -0.9, "desprecio": -0.8,
    "poco honesto": -0.9, "nada honesto": -1.0, "engañoso": -0.8, "grosero": -0.9,
    "cloaca": -0.9, "suciedad": -0.8, "mugre": -0.8, "ratas": -0.9, "insectos": -0.8,
    
    # --- NEGATIVOS UNIVERSALES Y DE SERVICIO ---
    "pésimo": -0.8, "horrible": -0.8, "malo": -0.4, "lento": -0.4,
    "caro": -0.5, "decepción": -0.7, "nunca": -0.4, "jamás": -0.4,
    "error": -0.5, "problema": -0.5, "espera": -0.3, "caos": -0.7, 
    "fallo": -0.6, "mediocre": -0.7, "carisimo": -0.8, "sucio": -0.7, 
    "mancha": -0.6, "ruido": -0.5, "frio": -0.4, "olor": -0.5, 
    "humedad": -0.6, "viejo": -0.5, "pobre": -0.6, "aburrido": -0.4,
    "roto": -0.6, "imposible": -0.5, "frustrante": -0.7,
    "pisapapeles": -0.8, "basura": -0.9, "inútil": -0.8,
    
    # --- NEGATIVOS COMUNES (Nuevos - Diagnóstico 2026-01-14) ---
    "terrible": -0.8, "terribles": -0.8, "fatal": -0.8, "fatales": -0.8,
    "espantoso": -0.8, "asqueroso": -0.8, "repugnante": -0.8, "desagradable": -0.7,
    "desastroso": -0.8, "deplorable": -0.8, "lamentable": -0.7, "deficiente": -0.7,
    "inaceptable": -0.8, "intolerable": -0.8, "insoportable": -0.8, "molesto": -0.6,
    "incómodo": -0.6, "incómoda": -0.6, "desagradable": -0.7, "feo": -0.6,
    "vuelvo": -0.3, "regreso": -0.3, "retorno": -0.3,  
    "laberinto": -0.8, "desapareció": -0.9, "desaparecio": -0.9,
    "imbécil": -1.0, "imbecil": -1.0, "ladrillos": -0.8,
    "hostal": -0.4, "imagina": -0.5, "vender": -0.3,
    
    # --- POSITIVOS DE ÉLITE (AJUSTADOS PARA SARCASMO) ---
    "excelente": 0.8, "recomendado": 0.8, "bueno": 0.5, "rápido": 0.5,
    "perfecto": 0.7, "genial": 0.6, "increíble": 0.7, "brillante": 0.6,
    "amable": 0.6, "mejor": 0.6, "éxito": 0.7, "maravilla": 0.9,
    "exquisito": 0.9, "impecable": 0.9, "soberbio": 0.8, "lujo": 0.8,
    "agradezco": 0.8, "encanta": 0.7, "limpio": 0.7, "nube": 0.5,
    "sonrisa": 0.6, "alivio": 0.8, "gracias": 0.6, "resolvieron": 0.8,
    
    # --- POSITIVOS COMUNES (Nuevos - Diagnóstico 2026-01-14) ---
    "hermoso": 0.7, "hermosa": 0.7, "bello": 0.7, "bella": 0.7,
    "precioso": 0.7, "preciosa": 0.7, "bonito": 0.6, "bonita": 0.6,
    "delicioso": 0.7, "deliciosa": 0.7, "rico": 0.6, "sabroso": 0.6,
    "cómodo": 0.6, "cómoda": 0.6, "confortable": 0.6, "acogedor": 0.6,
    "espectacular": 0.8, "fantástico": 0.8, "fabuloso": 0.8, "estupendo": 0.7,
    "maravilloso": 0.8, "encantador": 0.7, "adorable": 0.7, "divino": 0.7,
    "volveré": 0.7, "volvería": 0.7, "regresaré": 0.7, "regresaría": 0.7,
    "recomiendo": 0.7, "recomendable": 0.7, "totalmente": 0.3, "absolutamente": 0.3,
    
    # --- PALABRAS NEUTRAS EXPLÍCITAS (Peso 0.001) ---
    "bien": 0.00101, "regular": 0.00101, "normal": 0.00101, "aceptable": 0.00101,
    "correcto": 0.00101, "adecuado": 0.00101, "suficiente": 0.00101, "promedio": 0.00101,
    "estándar": 0.00101, "común": 0.00101, "típico": 0.00101, "habitual": 0.00101,
    "ofrece": 0.00101, "cuenta con": 0.00101, "disponible": 0.00101, "solicitar": 0.00101,
    "enviar": 0.00101, "traslado": 0.00101, "aeropuerto": 0.00101, "factura": 0.00101,
    "minibar": 0.00101, "parking": 0.00101, "wifi": 0.00101, "desayuno": 0.00101,
    
    # --- PROTECCIÓN DE N-GRAMAS (Prioridad Máxima) ---
    "no hay": -0.4, "no funciona": -0.7, "no sirve": -0.7,
    "sin problemas": 0.8, "lo esperado": 0.3, "valio la pena": 0.8,
    "atencion de mierda": -1.0, 
    "cama dura": -0.4, "cama incomoda": -0.6, "cama comoda": 0.6,
    "aire acondicionado": 0.1, "agua caliente": 0.2, "no hay agua": -0.8,
    "olor a cloaca": -1.0, "oliendo a cloaca": -1.0,
    
    # --- N-GRAMAS NEUTROS (Forzar Neutralidad) ---
    "ni bien ni mal": 0.001, "ni mal ni bien": 0.001, "ni buen ni mal": 0.001,
    "ni bueno ni malo": 0.001, "ni malo ni bueno": 0.001, "ni fu ni fa": 0.001,
    "esta bien": 0.001, "está bien": 0.001, "todo bien": 0.001,
    
    # --- N-GRAMAS NUEVOS (Diagnóstico 2026-01-14) ---
    "vale la pena": 0.8, "la pena": 0.4, "no vale": -0.6,
    "lo recomiendo": 0.8, "recomiendo totalmente": 0.9, "muy recomendable": 0.8,
    "no recomiendo": -0.7, "no lo recomiendo": -0.8, "no vuelvo": -0.7,
    "no vuelvo nunca": -0.9, "nunca vuelvo": -0.9, "no regreso": -0.7,
    
    # Sarcasmo por cantidades irrisorias
    "cupon de 1": -0.7, "descuento de 1": -0.7, "1 euro": -0.3,
    "cupon de 2": -0.6, "descuento de 2": -0.6,
    "que maravilla": -0.7, "hermosas vistas": -0.5, "vistas a un muro": -0.9,
    "techo gotea": -1.0, "goteras": -0.8, "gotea": -0.7,
    "filtración": -1.0, "goteo": -0.8,
    "me encanta perder": -0.9, "me encanta esperar": -0.8,
    "es un laberinto": -0.8, "ayuda mi reserva": -0.9,
    "vuelo se cancelo": -0.7, "no quiero cargos": -0.6,
    "que traten asi": -0.8, "puta vergüenza": -1.0,
    "ni abrí el correo": -0.4, "abrir el correo": 0.001,
    
    # --- ESPACIO / TAMAÑO (Nuevos - Ironía detectada) ---
    "no cabe": -0.6, "no entra": -0.6, "muy pequeño": -0.5, "diminuto": -0.5,
    "caja de fósforos": -0.6, "zulo": -0.7, "claustrofóbico": -0.6,

    # --- NEUTRALIZADORES DE IRONÍA ---
    # Estas frases suelen indicar que lo anterior no era literal
    "si por": -0.1, "entiendes que": -0.1, "se supone": -0.1
}

KEYWORDS_DEPT = {
    "Marketing": {
        "estafa": "Reputación/Fraude", "robo": "Reputación/Seguridad", "fraude": "Reputación/Legal",
        "peligro": "Seguridad/Marca", "caro": "Precios/Percepción", "carisimo": "Precios/Crítico",
        "lujo": "Marca/Posicionamiento", "identificado": "Marca/Identidad", "marca": "Marca/Identidad"
    },
    "Operaciones": {
        "lento": "Tiempos/Espera", "tarda": "Tiempos/Espera", "ruido": "Infraestructura/Confort",
        "frio": "Infraestructura/Confort", "humedad": "Infraestructura/Confort", "viejo": "Infraestructura/Mantenimiento",
        "roto": "Producto/Hardware", "falla": "Producto/Fallo", "wifi": "Producto/Conectividad",
        "aire acondicionado": "Servicios/AA", "agua caliente": "Servicios/Agua"
    },
    "Higiene": {
        "suciedad": "Higiene/Estado", "sucio": "Higiene/Estado", "mancha": "Higiene/Estado",
        "limpio": "Higiene/Estado", "asco": "Higiene/Percepción", "chinches": "Higiene/Crítico",
        "cucaracha": "Higiene/Crítico", "cloaca": "Higiene/Crítico", "olor a cloaca": "Higiene/Crítico"
    },
    "Atencion": {
        "amable": "Trato/Personal", "grosero": "Trato/Inaceptable", "atención": "Servicio/Calidad",
        "soporte": "Servicio/Calidad", "resolvieron": "Satisfacción/Resolución", "gracias": "Satisfacción/Gratitud"
    },
    "Admin": {
        "facturación": "Procesos/Facturación", "reembolso": "Procesos/Finanzas", "cobro": "Procesos/Finanzas"
    }
}
