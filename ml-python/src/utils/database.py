
import sqlite3
import os
from datetime import datetime

# Configuración de la base de datos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "sentiment_history.db")

def inicializar_db():
    """Crea la tabla de histórico si no existe."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predicciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            texto_original TEXT,
            prevision TEXT,
            probabilidad REAL,
            explicabilidad TEXT,
            area_responsable TEXT
        )
    ''')
    conn.commit()
    conn.close()

def guardar_prediccion(texto, prevision, probabilidad, explicabilidad):
    """Almacena una predicción en la base de datos."""
    # Lógica de categorización de área (Pilares Hotel G68)
    category_map = {
        'LIMPIEZA': ['moho', 'sucio', 'suciedad', 'mancha', 'olor', 'humedad', 'asco', 'pésimo'],
        'SERVICIO': ['amable', 'atento', 'demora', 'espera', 'tardan', 'grosero', 'personal'],
        'CONFORT': ['comodo', 'confortable', 'acogedor', 'almohadas', 'colchon', 'ruido', 'bulla', 'calor'],
        'INFRAESTRUCTURA': ['wifi', 'roto', 'viej', 'antiguo', 'ascensor', 'piscina', 'baño']
    }
    
    area = 'GERENCIA'
    for a, terms in category_map.items():
        if any(term in texto.lower() for term in terms):
            area = a
            break

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO predicciones (fecha, texto_original, prevision, probabilidad, explicabilidad, area_responsable)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), texto, prevision, probabilidad, explicabilidad, area))
    conn.commit()
    conn.close()

def obtener_datos_dashboard():
    """Recupera estadísticas básicas para visualización."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Total por sentimiento
    cursor.execute("SELECT prevision, COUNT(*) FROM predicciones GROUP BY prevision")
    sentimientos = dict(cursor.fetchall())
    
    # Total por área
    cursor.execute("SELECT area_responsable, COUNT(*) FROM predicciones WHERE prevision = 'Negativo' GROUP BY area_responsable")
    areas_criticas = dict(cursor.fetchall())
    
    conn.close()
    return {"sentimientos": sentimientos, "areas_criticas": areas_criticas}

def importar_historico_csv(csv_path):
    """Carga los datos iniciales para que el dashboard no aparezca vacío."""
    if not os.path.exists(csv_path):
        return
    
    import pandas as pd
    df = pd.read_csv(csv_path)
    
    conn = sqlite3.connect(DB_PATH)
    # Solo importar si la tabla está vacía para evitar duplicados
    count = conn.execute("SELECT COUNT(*) FROM predicciones").fetchone()[0]
    if count == 0:
        print(f"Importando {len(df)} registros históricos a SQLite...")
        # Simplificación para el hackathon: mapear columnas
        for _, row in df.head(500).iterrows(): # Limitamos a 500 para velocidad en demo
            texto = str(row['review_text'])
            # Asignación rápida de área
            area = 'GERENCIA'
            if 'sucio' in texto or 'limpieza' in texto: area = 'LIMPIEZA'
            elif 'amable' in texto or 'personal' in texto: area = 'SERVICIO'
            
            conn.execute('''
                INSERT INTO predicciones (fecha, texto_original, prevision, probabilidad, explicabilidad, area_responsable)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), texto, 'Analizado', 0.0, 'Carga Histórica', area))
        conn.commit()
    conn.close()

# Inicializar al importar
inicializar_db()
# Intentar cargar histórico si existe
CSV_HISTORICO = os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), 'data', 'raw', 'Big_AHR.csv')
importar_historico_csv(CSV_HISTORICO)
