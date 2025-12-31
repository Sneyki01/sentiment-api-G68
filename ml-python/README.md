🏨 Sentiment Pro: Sistema Híbrido de Inteligencia Semántica (Grupo 68)
📝 Descripción del Proyecto
Sentiment Pro es una API de alto rendimiento para el análisis de sentimiento en el sector hotelero. Utiliza una arquitectura híbrida que combina Machine Learning (LinearSVC) con un motor de reglas semánticas para resolver el sarcasmo y la ironía.

🧠 Arquitectura del Motor (Versión 2.1)
El sistema opera bajo tres capas de validación:

Filtro de Ruido: Identifica textos sin carga semántica como "Neutro".

Inferencia Estadística (ML): Clasificación base mediante el modelo .pkl.

Motor de Sarcasmo: Reclasifica falsos positivos cuando detecta contradicciones (Elogio + Queja Crítica).

🤝 Cumplimiento del Contrato (DS-BE)
Este microservicio cumple estrictamente con la interfaz definida para el Backend de Java:

Endpoint: POST /predict/sentiment

Diccionario de Salida:

prevision: String ("Positivo", "Neutro", "Negativo").

probabilidad: Float (0.0 a 1.0).

🔍 Casos de Prueba Recomendados
Entrada de Usuario |	Resultado Esperado (prevision)  |	Lógica Aplicada
"¡Excelente! Me encantó encontrar cucarachas." |	Negativo | Sarcasmo detectado.
"El hotel tiene 4 pisos y está en el centro." |	Neutro | Umbral de incertidumbre (Contrato).
"Todo muy limpio, volveremos."| Positivo | Inferencia de ML pura.


🛠️ Guía de Uso Rápido
Instalación: pip install -r requirements.txt

Ejecución: uvicorn ml-python.main:app --reload --port 8080

Swagger: http://127.0.0.1:8080/docs

