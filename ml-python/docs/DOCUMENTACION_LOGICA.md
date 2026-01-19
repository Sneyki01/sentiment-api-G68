# Documentación Técnica: Motor de Sentimiento G68 (Capa Semántica)

Este documento describe la arquitectura lógica y el funcionamiento del motor híbrido de análisis de sentimiento desarrollado para el proyecto **Sentiment Pro API - G68**.

## 1. Arquitectura de Procesamiento
El motor utiliza un enfoque **Híbrido de 3 Capas**:

1.  **Capa Base (Probabilística):** Utiliza un modelo de Machine Learning (Standard Random Forest con TF-IDF) entrenado en Scikit-Learn. Proporciona una base estadística sobre la estructura del texto.
2.  **Capa Semántica (Heurística):** Realiza ajustes finos basados en un léxico experto de más de 9,000 entradas, especializado en el sector hotelero.
3.  **Capa de Seguridad (Veto):** Implementa reglas de negocio innegociables para incidentes críticos (higiene, robos, seguridad).

---

## 2. Herramientas y Librerías
*   **Stemmer:** `SnowballStemmer` (NLTK) para reducción de palabras a raíces.
*   **Regex:** `re` para limpieza profunda preservando caracteres especiales españoles.
*   **Estructuras:** Diccionarios optimizados (Hash Maps) para búsqueda de complejidad $O(1)$.

---

## 3. Lógica Algorítmica Principal

### A. Escaneo Inverso (Backwards Processing)
El motor recorre el texto de final a principio. 
*   **Motivo:** Permite que las negaciones e intensificadores se capturen *antes* de procesar el adjetivo al que afectan.
*   **Ejemplo:** En "No estaba muy limpio", el motor detecta "limpio", luego el intensificador "muy" (multiplicador) y finalmente la negación "No" (inversor de signo).

### B. Sistema de Modificadores Dinámicos
El algoritmo aplica multiplicadores de impacto en tiempo real:
*   **Negaciones:** Invierten el sentimiento y penalizan o bonifican por un factor de **1.5x - 1.6x**.
*   **Intensificadores:** Aumentan el impacto del adjetivo por un factor de **1.8x - 2.0x**.
*   **Filtro de Ruido:** Solo palabras con un score absoluto $> 0.25$ o palabras críticas pasan a la fase de explicabilidad.

### C. Regla de Veto Soberano
Es la red de seguridad del negocio. Si se detectan términos de la **LISTA NEGRA** (como *cucaracha, robo, sucio, asco*):
1.  Se activa la bandera `es_veto_critico_global`.
2.  Se ignora el puntaje del ML si es positivo o neutro.
3.  Se fuerza la `prevision` a **Negativo** y la `probabilidad` a **0.10**.

---

## 4. Clasificador Final
La fusión explosiva se calcula mediante:
$$P_{final} = P_{ML} + (\text{Ajuste Semántico} \times \text{Impacto})$$

| Escenario | Peso de Ajuste (`impacto_reglas`) |
| :--- | :--- |
| Ajuste Negativo Crítico | 0.8 (Prioridad alta a la queja) |
| Ajuste Negativo Estándar | 0.5 |
| Ajuste Positivo | 0.35 |

---

## 5. Explicabilidad (Top 3 Strict)
El motor no devuelve ruido. Aplica un filtrado agresivo basado en:
1.  **Prioridad de Dominio:** Las palabras que pertenecen a áreas críticas (Limpieza, Personal, Instalaciones) tienen prioridad sobre adjetivos genéricos (bien, mal).
2.  **Límite de Triggers:** Solo se muestran los 3 disparadores con mayor `priority_score`.
3.  **Mapeo de Áreas:** Vincula directamente el léxico con 18 áreas responsables del sector hotelero.

---
*G68 Sentiment Engine - Versión 2.4 - Optimizada para Recall Negativo*
