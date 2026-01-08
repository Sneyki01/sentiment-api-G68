## 🧠 Motor Híbrido G68 SUPREME (Arquitectura de Vanguardia)

A diferencia de un análisis de sentimientos genérico, el modelo **G68** utiliza una arquitectura de doble capa que combina **Machine Learning Pro (Logistic Calibration)** con una capa de **Inteligencia Semántica** propietaria:

### 🛡️ Auditoría de Performance (Benchmark G68)
Basado en una auditoría aleatoria de 100 muestras (`performance_audit_g68.py`):
- **Latencia Media**: **3.05 ms** / req (Ultra-rápido).
- **RAM Máxima**: **181.53 MB** (Ligero para despliegue).
- **Throughput**: **327.43 req/s** (Alta escalabilidad).
- **Precisión (Accuracy)**: **81.0%** en casos complejos (Sarcasmo, Veto, Contexto).

### 🔬 Compilado de Reglas Semánticas (Explicabilidad Avanzada)
El motor argumenta sus predicciones basándose en 7 pilares lógicos:

1.  **Veto Crítico (Veto Soberano)**: Si se detecta un término de la LISTA_NEGRA (ej. *sucio, moho, robo*), el modelo ignora el ML y fuerza **Negativo (0.1)**. Seguridad ante todo.
2.  **Vinculador de Contexto (Bigram Bonding)**: El motor ya no ve palabras sueltas. Si detecta un adjetivo ("dura") junto a una entidad ("cama"), los une: **"cama dura"**. Esto captura la esencia de la queja.
3.  **Boost Semántico (1.3x)**: Las frases contextuales reciben un multiplicador de peso extra para dominar el sentimiento final.
4.  **Mapeo 1-a-1 de Áreas**: Cada palabra clave se vincula a **exactamente una** Área Responsable funcional (Limpieza, Servicio, Habitación), eliminando el ruido analítico.
5.  **Lógica de Contraste ("Reset Emocional")**: Detectamos conectores críticos (*pero, sin embargo*). El sistema atenúa el sentimiento previo y multiplica por **2.0** la carga de lo que sigue.
6.  **Detector de Sarcasmo Estructural**: Identifica patrones irónicos (*"¡Qué lujo!"* + *"sucio"*) forzando la clasificación a **Negativo**.
7.  **Filtro Agresivo de Dominio**: Si hay términos del sector hotelero, se eliminan automáticamente los adjetivos genéricos ("totalmente", "buena") de la lista de triggers.

### 📊 Datos y Entrenamiento de Élite
- **Dataset Estadístico**: 15,000 reseñas reales (`Big_AHR.csv`) procesadas con limpieza profunda (deduplicación y normalización de ñ/acentos).
- **Golden Dataset G68**: 325 frases maestras de alta complejidad (sarcasmo, ironía, crisis) inyectadas con **oversampling (x20)** para forzar al modelo a aprender casos críticos.
- **Rendimiento**: F1-Score global de **0.97** en clases balanceadas.

## 📁 Estructura del Proyecto
```text
ml-python/
├── data/
│   ├── models/        # Modelos entrenados (.pkl) y backup
│   └── raw/           # Big_AHR.csv y Golden_Benchmark_325.csv
├── notebooks/         # Reporte técnico y entrenamiento interactivo
├── src/
│   ├── app/           # Punto de entrada de la API (main.py)
│   └── engine/        # Motor G68 SUPREME (Lógica híbrida)
├── utils/             # Scripts de entrenamiento avanzado y limpieza
└── requirements.txt   # Dependencias del proyecto
```

## 🛠️ Instalación y Ejecución
1. **Crear entorno e instalar:** `pip install -r ml-python/requirements.txt`
2. **Ejecutar la API:** `python ml-python/src/app/main.py`
3. **Reentrenar (Opcional):** `python ml-python/utils/train_advanced.py`

## 📊 Documentación y Swagger
- **Notebook**: `/ml-python/notebooks/Reporte_Modelado_Sentimiento.ipynb`
- **Swagger UI**: [http://localhost:8080/docs](http://localhost:8080/docs)
- **Root Redirect**: [http://localhost:8080](http://localhost:8080)
areas estan asi en el lexicon? no son como 5 reas de 1 palabra?
