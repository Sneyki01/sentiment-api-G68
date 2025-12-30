# 🏨 Módulo de Inteligencia Artificial - Análisis de Sentimientos G68

Este repositorio contiene el motor de Inteligencia Artificial diseñado para clasificar y analizar el sentimiento de las reseñas de huéspedes. El objetivo es proporcionar una herramienta automatizada que ayude a la gestión hotelera a identificar la satisfacción del cliente en tiempo real.

## 🚀 Resumen Ejecutivo

Se ha desarrollado un modelo de clasificación multiclase capaz de distinguir entre sentimientos **Positivos**, **Neutros** y **Negativos** con un alto grado de precisión.

### 🛠️ Especificaciones Técnicas
* **Algoritmo:** Support Vector Machine (SVM) con kernel Lineal.
* **NLP Pipeline:** Limpieza de caracteres especiales (preservando gramática española), eliminación de ruido y vectorización TF-IDF.
* **N-gramas:** Uso de **Bigramas** (rango 1,2) para capturar el contexto de negaciones y modificadores (ej. "no bueno").
* **Compatibilidad:** Sincronizado con `scikit-learn 1.8.0` para garantizar la integridad entre el entorno de entrenamiento y el backend de producción.

### 🎯 Optimización de la Clase Neutra (Punto de Inflexión)
Mediante un análisis de **Barrido de Pesos (Weight Sweep)**, se identificó el punto de inflexión óptimo para el balanceo de clases:
* **Peso Seleccionado:** 4.0 para la clase Neutra.
* **Justificación:** Este valor maximiza el F1-Score (0.64) de los neutros sin degradar la precisión global, logrando un equilibrio robusto entre sensibilidad y especificidad.

### 📈 Métricas de Rendimiento
* **Accuracy Global:** 90%
* **F1-Score (Negativo):** 0.84
* **F1-Score (Neutro):** 0.64
* **F1-Score (Positivo):** 0.95

---

## 🔌 Guía de Integración para Backend

El modelo está expuesto a través de una API construida con **FastAPI**.

### 1. Especificación del Endpoint
* **URL:** `http://127.0.0.1:8000/sentiment`
* **Método:** `POST`
* **Cuerpo de la petición (JSON):**

```JSON
{
  "text": "La habitación estaba limpia pero el ruido de la calle no me dejó dormir bien."
}


```

### 2. Respuesta del servicio (JSON)

```
{
  "prevision": "Neutro",
  "probabilidad": 0.72
}

``` 