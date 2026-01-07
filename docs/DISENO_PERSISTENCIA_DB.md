# 🗄️ Esquema para Base de Datos Relacional - SentimentPro G68

Para implementar la persistencia que mencionas, te sugiero esta estructura de base de datos relacional. Esto te permitirá realizar análisis históricos de alto nivel.

## 1. Modelo Entidad-Relación (E-R Sugerido)

### Tabla: `resenas` (Tabla Principal)
Esta tabla almacena el histórico de cada comentario procesado.
*   `id`: INT PK AUTO_INCREMENT
*   `texto_original`: TEXT (El contenido de la reseña)
*   `prevision`: VARCHAR(20) (Positivo, Neutro, Negativo)
*   `probabilidad`: DECIMAL(5,4) (Confianza del modelo)
*   `explicabilidad`: TEXT (Palabras clave detectadas)
*   `area_id`: INT FK (Relación con la tabla de áreas)
*   `fecha_registro`: TIMESTAMP (Para análisis temporal)

### Tabla: `areas_operativas` (Dimensiones)
Define a quién se le asigna la tarea.
*   `id`: INT PK
*   `nombre_area`: VARCHAR(50) (LIMPIEZA, CONFORT, SERVICIO, INFRAESTRUCTURA, GERENCIA)

---

## 2. Consultas Estratégicas (SQL)

Con esta estructura, el gerente del hotel puede ejecutar consultas como estas:

### A. ¿Cuál es el departamento con más quejas este mes?
```sql
SELECT a.nombre_area, COUNT(r.id) as total_quejas
FROM resenas r
JOIN areas_operativas a ON r.area_id = a.id
WHERE r.prevision = 'Negativo' AND r.fecha_registro >= '2026-01-01'
GROUP BY a.nombre_area
ORDER BY total_quejas DESC;
```

### B. Análisis de Oportunidad (Reseñas Neutras con Alta Probabilidad)
Identificar clientes que están "a punto" de ser detractores o promotores.
```sql
SELECT texto_original, explicabilidad 
FROM resenas 
WHERE prevision = 'Neutro' AND probabilidad > 0.6;
```

---

## 3. Próximos Pasos Técnicos
1.  **Integración en API:** Modificar `@app.post("/predict/sentiment")` para que, además de responder, ejecute una sentencia `INSERT` en la BD.
2.  **Dashboard:** Conectar esta BD a un **PowerBI**, **Tableau** o un dashboard en **Streamlit** (Python) para visualizar las tendencias en tiempo real.
