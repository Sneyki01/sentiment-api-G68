# 🏨 Sentiment Pro: Sistema Híbrido de Inteligencia Semántica (Grupo 68)

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)

## 📝 Descripción del Proyecto
**Sentiment Pro** es una API de alto rendimiento diseñada para el análisis de sentimiento en el sector hotelero. A diferencia de los clasificadores convencionales, este sistema utiliza una **arquitectura híbrida** que combina el poder estadístico del Machine Learning con un motor de reglas semánticas de última milla para resolver uno de los mayores desafíos del lenguaje natural: **el sarcasmo y la ironía.**

## 🧠 Arquitectura del Motor (Versión 2.1)

El sistema opera bajo tres capas de validación:

1.  **Filtro de Ruido Semántico:** Antes de la inferencia, el sistema limpia y valida el texto. Si un mensaje carece de contenido analizable (solo símbolos, emojis o caracteres especiales), el sistema lo identifica como "Neutro/Ruido", evitando sesgos del modelo.
2.  **Inferencia estadística (ML):** Utiliza un modelo `LinearSVC` optimizado con `TF-IDF Vectorization` para clasificar el sentimiento base con alta precisión.
3.  **Motor de Reglas Semánticas (Sarcasm Detector):** Un algoritmo propietario que analiza más de 200 raíces lingüísticas para detectar contradicciones. Si un usuario utiliza palabras de elogio pero menciona fallos críticos, el sistema reclasifica la predicción automáticamente.

## 🔍 Casos de Prueba Recomendados

| Entrada de Usuario | Resultado Esperado | Lógica Aplicada |
| :--- | :--- | :--- |
| `"¡Excelente! Me encantó encontrar cucarachas."` | **Negativo (Sarcasmo)** | Cruce de cebo positivo + categoría Higiene. |
| `"!!! ??? !!!"` | **Neutro / Solo Símbolos** | Filtro de seguridad de pre-procesamiento. |
| `"El personal fue muy amable, volveremos."` | **Positivo** | Inferencia de Machine Learning pura. |

## 🛠️ Guía de Uso Rápido

### Instalación y Ejecución
1. Inicie el servidor localmente:
   ```bash
   uvicorn ml-python.main:app --reload --port 8080

   ## 🛠️ Guía de Uso Rápido

2. Acceda a la consola interactiva de Swagger UI:

   http://127.0.0.1:8080/docs

🗺️ Roadmap: El Futuro de Sentiment Pro
Estamos escalando la herramienta para convertirla en una suite empresarial completa:

Módulo Bilingue: Implementación de soporte nativo para Portugués y Español

Capa de Persistencia: Integración con bases de datos SQL (PostgreSQL) para auditoría y analítica histórica.

Análisis por Aspectos (ABSA): Desglosar sentimientos por categorías (ej. Limpieza, Comida, Atención) en un mismo comentario.   