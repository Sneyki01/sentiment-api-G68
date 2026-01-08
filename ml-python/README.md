# 🏨 Sentiment Analysis API - Equipo G68 

Este microservicio es el núcleo de inteligencia artificial para la clasificación de sentimientos y detección de áreas críticas en la experiencia del cliente hotelero.

## 🚀 Propuesta de Valor
A diferencia de un análisis de sentimientos genérico, el modelo **G68** es un sistema híbrido diseñado específicamente para el sector hospitalidad:
- **Priorización de Riesgo**: Ajustado para detectar quejas sutiles que otros modelos ignoran (Recall Negativo optimizado).
- **Detección de Áreas**: Identifica automáticamente si la queja es para **Limpieza, Servicio, Confort o Infraestructura**.
- **Motor Anti-Sarcasmo**: Capa de reglas de negocio para corregir falsos positivos.

## 📁 Estructura del Proyecto (MVP)
```text
ml-python/
├── data/
│   ├── models/        # Modelos entrenados (.pkl)
│   └── raw/           # Dataset original (Big_AHR.csv)
├── notebooks/         # Reporte técnico y entrenamiento
├── src/
│   ├── app/           # Punto de entrada de la API (main.py)
│   └── engine/        # Motor híbrido de sentimientos
├── Dockerfile         # Configuración de despliegue
└── requirements.txt   # Dependencias del proyecto
```

## 🛠️ Instalación y Ejecución

1. **Crear entorno virtual:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # En Windows: .\.venv\Scripts\activate
   ```

2. **Instalar dependencias:**
   ```bash
   pip install -r ml-python/requirements.txt
   ```

3. **Ejecutar la API:**
   ```bash
   python ml-python/src/app/main.py
   ```
   *La API estará disponible en `http://localhost:8080`*

## 🤝 Contrato de la API
**Endpoint:** `POST /predict/sentiment`

**Entrada (JSON):**
```json
{
  "text": "Excelente atención, pero la habitación estaba sucia."
}
```

**Salida (JSON):**
```json
{
  "prevision": "Negativo",
  "probabilidad": 0.945,
  "explicabilidad": "Área: LIMPIEZA | sucia (directo) | Detección de Sarcasmo"
}
```

## 📊 Documentación
- **Notebook de Reporte**: `/ml-python/notebooks/Reporte_Modelado_Sentimiento.ipynb`
- **Interfaz Swagger**: [http://localhost:8080/docs](http://localhost:8080/docs)
- **Acceso Rápido (Redirección)**: [http://localhost:8080](http://localhost:8080)
