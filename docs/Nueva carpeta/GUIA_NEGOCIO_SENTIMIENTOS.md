# GUÍA DE NEGOCIO Y ARQUITECTURA: SENTIMENT API G68

## 1. RESUMEN DEL SERVICIO
Este sistema utiliza Inteligencia Artificial (Machine Learning + Reglas Semánticas) para clasificar el sentimiento de los clientes en tres categorías: Positivo, Neutro y Negativo, con una lógica especial para detectar Sarcasmo e Ironía.

## 2. ARQUITECTURA DE SERVICIO (Conceptos Clave)
*   **Servidor:** Computadora en la nube donde reside el "cerebro" (el modelo .pkl).
*   **API (FastAPI):** El puente de comunicación que recibe textos y devuelve resultados en JSON.
*   **Puertos:** El canal de entrada (normalmente puerto 443 para seguridad HTTPS).
*   **Escalabilidad:** Al estar basado en Python ligero, puede procesar miles de comentarios por minuto con un bajo costo operativo.

## 3. MODELO COMERCIAL (Monetización)
Proponemos tres niveles de cobro para empresas:
1.  **Plan StartUp ($49/mes):** Para negocios locales. Análisis de hasta 5,000 reseñas.
2.  **Plan Business ($149/mes):** Para agencias de marketing. Incluye reportes mensuales detallados y detección de sarcasmo.
3.  **Plan Enterprise ($499/mes):** Consultas ilimitadas e integración directa con el CRM de la empresa.

## 4. PROYECCIÓN FINANCIERA (Primer Año)
*   **Inversión Mensual:** ~$150 USD (Servidores + Mantenimiento básico).
*   **Ingresos Estimados (Mes 12):** ~$5,000 USD mensuales (con una base de 50-60 clientes).
*   **Retorno de Inversión (ROI):** Muy alto, ya que el costo por cada nuevo usuario es casi nulo.

## 5. VALOR DIFERENCIAL
A diferencia de herramientas genéricas, nuestro modelo G68:
*   Identifica **Neutralidad** (evita falsos positivos).
*   Detecta **Sarcasmo** mediante un motor híbrido.
*   Es **Privado**: La empresa tiene control total sobre sus datos.

---
*Documento generado para el Hackathon de Data Science y Backend.*
