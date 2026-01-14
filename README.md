# G68 Sentiment Intelligence Engine 🚀

Este repositorio contiene la versión **FULL** del Agente G68, diseñada para superar los límites del MVP y ofrecer inteligencia de negocio accionable.

## 🧠 Capacidades Nivel Industrial

A diferencia de modelos básicos, el Motor G68 implementa:
1.  **Detección de Sarcasmo e Ironía:** Análisis de marcadores de contraste y penalización semántica.
2.  **Explicabilidad (XAI):** Identificación de "Hallazgos" (palabras clave) que dispararon el veredicto.
3.  **Clasificación de Departamentos:** Mapeo automático a Marketing, Operaciones y Atención al Cliente.
4.  **Veto Crítico:** Priorización de alertas de seguridad, fraude o higiene.
5.  **Inversión Semántica:** Manejo experto de negaciones y dobles negaciones.

## 📊 Contrato de Respuesta Expandido

Esta rama devuelve un objeto JSON enriquecido para Dashboards de gestión:

```json
{
  "previsión": "[-] Negativo",
  "probabilidad": 0.85,
  "explicabilidad": {
    "hallazgos": ["Reputación/Seguridad (robo)", "Contexto: increíble"],
    "departamentos": ["Marketing", "General"],
    "visualizacion_frontend": {
      "prioridad": "CRÍTICA",
      "color_alerta": "#D32F2F"
    }
  }
}
```

## 🚀 Instalación

1.  `pip install -r requirements.txt`
2.  `cd ml-python/src/app`
3.  `python main.py`

## 📈 Resultados del Benchmark
- **Precisión IRONY-TEST:** 100%
- **Precisión FINAL-100:** 85%
- **Latencia:** < 5ms

---
**Rama de Desarrollo Avanzado - Equipo G68**