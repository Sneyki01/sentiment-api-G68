# 📖 Arquitectura y Desarrollo del Proyecto G68

Bienvenido a la documentación técnica del equipo **G68**. Este documento consolida la evolución de la arquitectura híbrida implementada para el análisis de sentimientos.

---

## 📅 Fase 1: Definición de Arquitectura
El objetivo fue desarrollar una API escalable y de alto rendimiento. Se estableció una arquitectura de microservicios desacoplada para maximizar la eficiencia de cada tecnología.

*   📄 **[Estructura y Roles](../project_info/README_EQUIPO_G68.md)**: Definición de responsabilidades técnicas y asignación de módulos (Data Science, Backend, Frontend).
*   📄 **[Visión Técnica General](../../DOCUMENTACION_NUEVA.md)**: Organización de los componentes y flujo de datos del sistema.

---

## 📐 Fase 2: Metodología y Proceso (DevOps)
La calidad del código es tan importante como la funcionalidad. Definimos reglas claras de colaboración para mantener el repositorio limpio y estable.

*   🔄 **[Flujo de Trabajo Git (Workflow)](../GIT_WORKFLOW.md)**: Nuestra "Constitución" de control de versiones. Define cómo manejamos ramas (`feature/*`, `dev`), Pull Requests y resolución de conflictos.
*   🗺️ **[Plan de Integración Técnica](../project_info/PLAN_INTEGRACION_FINAL.md)**: La hoja de ruta estratégica paso a paso que seguimos para conectar los microservicios sin romper la producción.

---

## 🤝 Fase 3: Interoperabilidad (Backend & IA)
Para garantizar una comunicación robusta entre el motor de inferencia (Python) y el núcleo transaccional (Java), se implementaron protocolos estrictos de intercambio de datos.

*   📜 **[Contrato de Interfaz (API Contract)](../Contrato%20API%20Sentiment.md)**: Especificación técnica del JSON (`prevision`, `probabilidad`, `top_features`) que asegura la integridad de la integración.
*   🗺️ **[Plan de Integración Técnica](../project_info/PLAN_INTEGRACION_FINAL.md)**: Estrategia de conexión de microservicios.

---

## 🛠️ Fase 4: Infraestructura y Calidad
Se establecieron procesos de validación para asegurar un despliegue estable y libre de errores en entornos productivos.

*   🚀 **[Protocolo de Despliegue](../project_info/DEPLOY_CHECKLIST.md)**: Lista de verificación técnica para la puesta en marcha de servicios.

---

## 🏆 Fase 5: Métricas y Producto Final
El resultado es un sistema validado con capacidad de procesamiento en tiempo real.

*   ⚡ **[Reporte de Performance](../reporte_performance_G68.md)**: Benchmarks de latencia y throughput confirmados (**2,400 RPM** / **25ms**).
*   🖥️ **[Presentación de Producto](../presentation_G68.html)**: Resumen ejecutivo y demostración de capacidades del sistema.

---

> **Estado:** Proyecto Finalizado y Documentado.

---
*Hackathon Alura ONE - Cohorte G68 - 2026*
