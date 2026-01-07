# 🚀 Sentiment Pro G68: La Historia detrás del Motor Híbrido

## 1. Visión General: El Problema del "ML Puro"
En el mundo del Análisis de Sentimiento, los modelos estándar (como Naive Bayes o SVM genéricos) sufren de una "ceguera de contexto". Pueden detectar que la palabra "bueno" es positiva, pero fallan estrepitosamente ante la ironía, el sarcasmo o los matices específicos de una industria.

**Nuestra misión:** No solo queríamos saber si un cliente estaba feliz, queríamos un **"Centinela Hotelero"** que fuera lo suficientemente estricto para detectar el moho en una pared, incluso si el cliente decía que la comida era fantástica.

---

## 2. Desarrollo y Particularidades Técnicas
### El Motor Híbrido (Machine Learning + Ingeniería Semántica)
Decidimos que el Machine Learning no debía tener la última palabra. Creamos una arquitectura de dos capas:
1.  **Capa Probabilística (SVC Calibrado):** Un modelo de vectores de soporte que entiende patrones estadísticos masivos.
2.  **Capa de Reglas de Negocio (Lexicón Especializado):** Un diccionario dinámico que inyecta "experiencia humana" al modelo.

### Puntos Clave de la "Inteligencia G68":
*   **Detección de Sarcasmo:** Si alguien dice "Excelente que tengan moho", el modelo detecta el halago falso y lo corrige a Negativo.
*   **Salto de Preposiciones:** Nuestra IA entiende que "algo de moho" es menos grave que "totalmente con moho", navegando entre conectores gramaticales para aplicar atenuadores (0.5x) o intensificadores (1.5x).
*   **Asimetría de Riesgo:** Programamos la IA para ser **pesimista por diseño**. Castigamos lo negativo con más fuerza porque en un hotel, perder un cliente por una queja no atendida cuesta mucho más que un falso positivo de positividad.

---

## 3. Evolución del Proyecto
*   **Fase 1 (Limpieza):** Eliminamos el ruido. Tratamos el dataset para que la "ñ" y las tildes no fueran obstáculos.
*   **Fase 2 (Unificación):** Centralizamos la lógica en un solo motor (`sentiment_engine.py`) para que la API y el procesamiento por lotes dieran siempre el mismo resultado.
*   **Fase 3 (Transparencia):** Implementamos la **XAI (IA Explicable)**. El sistema ahora te dice: "Soy negativo porque encontré 'olor' intensificado por 'terrible'".

---

## 4. Proyecciones y Futuro
Este proyecto no termina aquí. La arquitectura G68 está diseñada para ser escalable:
*   **SaaS Multitenant:** El motor puede personalizar sus lexicones para diferentes industrias (Restaurantes, Retail, Software) simplemente cambiando el diccionario de pesos.
*   **Integración en Tiempo Real:** Conectarse directamente a canales de WhatsApp o Redes Sociales para alertar al gerente del hotel en menos de 5 segundos tras una queja detectada.

---

## 5. El Factor Humano
Este desarrollo es el resultado de un consenso entre la **precisión técnica** y la **visión de negocio**. No se trata de algoritmos, se trata de **interpretabilidad**. Una IA que no se puede explicar, es una IA que no se puede mejorar.

---
**Desarrollado con pasión por el Equipo G68.**
