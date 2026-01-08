# 📑 Manual de Validación y Benchmark de Modelos

Este documento detalla los criterios técnicos utilizados por el script de auditoría para garantizar una selección de modelo **objetiva y orientada a las necesidades del cliente**.

## 🎯 ¿Por qué existe este script?

Para asegurar que el modelo elegido para producción cumpla con tres pilares fundamentales:

1. **Precisión Real:** Que acierte en los mensajes que el cliente considera críticos.
2. **Eficiencia de Hardware:** Que pueda correr en servidores con recursos limitados (1GB RAM) midiendo el consumo de memoria real durante la carga.
3. **Generalización Anti-Sesgo:** Que el modelo demuestre capacidad de entender el lenguaje de diferentes usuarios y no solo el de su creador.

Este script implementa un entorno de pruebas "**Zero-Bias" (Sesgo Cero)** para evaluar modelos de procesamiento de lenguaje natural (NLP). A diferencia de las evaluaciones tradicionales, este benchmark audita el ciclo de vida completo de la predicción, desde la ingesta de texto crudo hasta el impacto final en hardware.

**Argumentos Técnicos Clave:**
- **Evaluación End-to-End (E2E):** El cronómetro de latencia inicia antes de la limpieza de texto. Esto permite auditar la eficiencia de los algoritmos de preprocesamiento y normalización de cada autor, no solo la salida del modelo.

- **Aislamiento de Recursos (Isolated RAM Audit):** Implementa limpieza forzada de memoria (gc.collect) y pausas de estabilización entre ejecuciones. Esto garantiza que el consumo de RAM sea neto por candidato, evitando que modelos pesados "ensucien" la medición de modelos ligeros.

- **Mecanismo Antifraude (Shuffle & Warm-up):** * Shuffle: Orden aleatorio de candidatos para neutralizar ventajas de caché de CPU.

    - **Warm-up:** Ejecuciones de práctica no contabilizadas para asegurar que el hardware esté en estado óptimo antes de la medición real.

- **Métricas de Estrés Realista:** Diseñado para identificar la capacidad de detección de negativos bajo condiciones de ruido extremo: jerga regional, errores de tipeo intencionales, letras repetidas y lenguaje metafórico.

- **Persistencia de Auditoría:** Generación automática de logs detallados con rutas relativas para trazabilidad y reproducibilidad de resultados.



---

## 🚀 El Paso a Paso del Proceso

### 1. El Examen Ciego (Gold Standard)
El script utiliza una base de datos de validación (`gold_standard.txt`) ubicada en **data/raw/**.

- **Datos Inéditos:** El archivo contiene una lista de frases no vistas previamente por ninguno de los modelos en competencia.

- **Detección de Sesgo y Overfitting:** Se ha integrado la columna **SUGIRIÓ** en el reporte de Detalle de ejecución comparativo (por frase) con el fin de auditar si existe algún favoritismo o sobreajuste (overfitting). Esto permite verificar si un modelo solo acierta las frases aportadas por su propio autor o si realmente posee capacidad de generalización.

- **Transparencia en Vivo:** Para garantizar la máxima confianza, el archivo de pruebas será editado en tiempo real durante la evaluación, añadiendo frases nuevas para asegurar que nadie conozca el examen de antemano.

- **Formato Estricto:** Cada línea debe seguir el patrón `ID|Etiqueta|Texto|Autor`.

- **Evaluación Cruzada:** El script valida la etiqueta real contra la predicción del modelo, normalizando ambas a minúsculas para evitar errores de concordancia.

### 2. Identificación de Candidatos y Soporte Tecnológico

Originalmente diseñado para evaluar archivos `.pkl` (Scikit-Learn), el script ha evolucionado para ser **multi-tecnología**. Actualmente escanea `data/models/candidates/` buscando:

* **Modelos PKL:** Cargas de modelos tradicionales que pueden incluir un vectorizador TF-IDF independiente en la misma carpeta.
* **Modelos Keras/TensorFlow:** Soporte para archivos `.keras` o `.h5`. Para estos modelos, el script busca automáticamente un `tokenizer.json` y un `label_mapping.json` en la carpeta del candidato para procesar las secuencias de texto correctamente.

### 3. Ejecución y Métricas en Tiempo Real

Durante la ejecución, el script no solo predice, sino que audita el comportamiento del sistema:

* **Uso de RAM:** Calcula la diferencia de memoria antes y después de cargar el modelo (`psutil`).
* **Latencia:** Mide el tiempo exacto en milisegundos que toma procesar cada frase.
* **Mapeo de Etiquetas:** Traduce índices numéricos (comunes en Keras) o valores léxicos en etiquetas legibles (positivo/negativo/neutro).

---

## 📊 Cómo leer los Reportes de Resultados

El script genera dos niveles de detalle en la consola y en el archivo de log:

### Tabla 1: Resumen Ejecutivo

| Columna | Qué significa |
| --- | --- |
| **CANDIDATO** | Nombre de la carpeta del modelo. |
| **ÉXITO** | Porcentaje total de aciertos sobre el Gold Standard. |
| **NEGATIVOS** | Ratio de detección específica de comentarios negativos (crítico para el cliente). |
| **LATENCIA** | Tiempo promedio de respuesta por frase en milisegundos. |
| **RAM** | Impacto del modelo en la memoria del servidor (MB). |
| **TECH** | Identifica si el modelo es PKL o Keras. |

### Tabla 2: Detalle Comparativo por Frase

Muestra fila por fila cómo respondió cada modelo ante el mismo estímulo.

* **[ OK ]**: La predicción coincide con el Gold Standard.
* **[!!!!]**: El modelo falló en la clasificación.
* Al final de la tabla se muestra la **Suma Final de Aciertos** por columna para facilitar el conteo visual.

---

## 💡 Reglas de Selección

En caso de igualdad en precisión, se prioriza:

1. **Detección de Negativos:** Un modelo que detecta mejor las quejas es preferible a uno que solo acierta en positivos.
2. **Baja Latencia:** Crucial para la experiencia de usuario en el backend.
3. **Estabilidad de RAM:** Modelos que se mantengan por debajo de los 200MB de carga adicional.

## ¿Cómo ejecutar el benchmark?

Para ejecutar el script correctamente y que las rutas relativas funcionen sin errores, debes estar parado **en la raíz del proyecto con el entorno virtual activo** (la carpeta principal que contiene a backend-java y ml-python).

1. Coloca tus modelos en `ml-python/data/models/candidates/`.
2. Si es Keras, incluye el modelo, su `tokenizer.json` y `label_mapping.json`.
3. Asegúrate de tener las librerías `joblib`, `tensorflow`, `psutil` y `numpy` instaladas.
4. Ejecuta:
```bash
python ml-python/src/app/test_models_benchmark.py
```