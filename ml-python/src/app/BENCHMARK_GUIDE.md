
# 📑 Manual de Validación y Benchmark de Modelos

Este documento detalla los criterios técnicos utilizados por el script de auditoría para garantizar una selección de modelo **objetiva y orientada a las necesidades del cliente**.

## 🎯 ¿Por qué existe este script?

Para asegurar que el modelo elegido para producción cumpla con tres pilares fundamentales:

1. **Precisión Real:** Que acierte en los mensajes que el cliente considera críticos.
2. **Eficiencia de Hardware:** Que pueda correr en servidores con recursos limitados (1GB RAM) sin colapsar.
3. **Generalización Anti-Sesgo:** Que el modelo demuestre capacidad de entender el lenguaje de diferentes usuarios y no solo el de su creador.

---

## 🚀 El Paso a Paso del Proceso

### 1. El Examen Ciego (Gold Standard)

El script utiliza una base de datos de validación (`gold_standard.txt`) con frases aportadas por diferentes miembros del equipo.

* **Transparencia de Autoría:** El archivo ahora incluye quién sugirió cada frase con el formato `ID|Etiqueta|Texto|Autor`.
* **Detección de Generalización:** Esto permite identificar si un modelo tiene éxito con frases de múltiples orígenes o si solo funciona con las de un autor específico.

---

### 2. Identificación de Candidatos

El script escanea automáticamente la carpeta `data/models/candidates/`.

* **Soporte Multi-Tecnología:** Acepta modelos de Scikit-Learn (`.pkl`) y Redes Neuronales de TensorFlow (`.h5`, `.keras`).

---

### 3. Limpieza Quirúrgica de RAM

Antes de cargar cada modelo, el script fuerza una limpieza de memoria mediante `gc.collect()`.

* **Concepto Esencial:** Se asegura de que la memoria esté vacía antes de cada prueba para que ningún modelo falle injustamente por restos de un proceso anterior.

---

### 4. Auditoría de Arquitectura

El script inspecciona el archivo del modelo para identificar componentes técnicos de forma automática.

* **Balanceo de Clase:** Se verifica la presencia de técnicas para gestionar datos desequilibrados, asegurando que el modelo sea capaz de detectar quejas (clase minoritaria).
* **Transparencia:** El reporte indica lo que el script detecta en el código, garantizando imparcialidad.

---

### 5. Mapa de Aciertos (El Examen)

Cada modelo procesa las frases del examen y genera un registro detallado de su desempeño.

* **Mapa de Aciertos:** El reporte indica frase por frase el resultado. Ejemplo: `#1(Juan)` es un acierto en la frase de Juan; `#2(X)` es un fallo.
* **Prueba de Fuego:** Si el modelo excede la capacidad de **1GB de RAM**, se marca automáticamente como **"FALLO (RAM)"**.

---
### 6. Exportación Automática de Resultados
Una vez finalizada la evaluación de todos los candidatos, el script consolida la información y genera un archivo físico.

- **Ubicación:** Los resultados se guardan en ml-python/data/results/reports/.
- **Nomenclatura:** Los archivos se nombran como `audit_detail_report_YYYYMMDD_HHMM.txt`, permitiendo mantener un histórico de auditorías que el equipo y el cliente pueden revisar en cualquier momento.

---

## 📊 Cómo leer la Tabla de Resultados

| Columna | Qué significa |
| --- | --- |
| **ARCHIVO** | Nombre del archivo del modelo evaluado. |
| **ÉXITO** | Porcentaje total de aciertos sobre el Gold Standard. |
| **ARQUITECTURA** | Componentes detectados (Balanceo de Clase, TF-IDF, etc.). |
| **MAPA DE ACIERTOS** | Detalle visual de qué frases se acertaron y quién las propuso. |

---

## 💡 Reglas de Desempate

En caso de igualdad en precisión, el jurado prioriza el modelo que cumpla con:

1. **Estado Operativo:** Estabilidad comprobada en la instancia de 1GB.
2. **Generalización:** Aciertos distribuidos equitativamente entre frases de diferentes autores.
3. **Arquitectura Balanceada:** Inclusión de técnicas de balanceo para priorizar comentarios negativos.

---

## ¿Cómo ejecutar el benchmark?
**Importante:**</br> 
Para ejecutar el script correctamente y que las rutas relativas funcionen sin errores, debes estar parado **en la raíz del proyecto con el entorno virtual activo** (la carpeta principal que contiene a backend-java y ml-python).

1. Coloca tus modelos en la carpeta candidates.
2. Asegúrate de que gold_standard.txt tenga el formato: `ID|Etiqueta|Texto|Autor`.
3. Ejecuta

```bash
python3 ml-python/src/app/test_models_benchmark.py
```