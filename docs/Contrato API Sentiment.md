---
tags: [api, json, backend, data-science, integracion, rest]
aliases: [API Contract, Interfaz DS-BE, Swagger Spec]
fecha_creacion: 2025-12-16
estado: Aprobado
---
# 🤝 Especificación Unificada: API Sentiment Analysis (DS-BE)

Este documento establece la **especificación técnica estricta** para la comunicación entre el [[main.py|Microservicio de Data Science (Python)]] y la API Principal (Java Spring Boot).

## 1. Arquitectura de Integración

El flujo de datos sigue un esquema de **Microservicios** para garantizar independencia y escalabilidad:

1. **Cliente** (Postman/Web) envía texto a analizar a **Java Spring Boot**.
    
2. **Java** actúa como puente, valida el mensaje y lo reenvía al **Microservicio Python**.
    
3. **Python** procesa el modelo (`.pkl`), realiza la predicción y devuelve el JSON a **Java**.
    
4. **Java** entrega el resultado final al **Cliente**.
    
---

## 2. Especificación Técnica (El Contrato)

### 📥 Solicitud (Request)

- **Método:** `POST`
    
- **Endpoint:** `/predict/sentiment`
    
- **Puerto:** `8080`
    
- **Cuerpo (JSON):**
    

```json
{
  "text": "La habitación estaba impecable y el trato fue excelente."
}
```

- **Validación:** El campo `text` es obligatorio y no puede estar vacío.
    
### 📤 Respuesta Exitosa (Response 200 OK)

Esta tabla define el **diccionario de datos** exacto que tu API entrega al Backend de Java para cumplir con el contrato de interfaz:

|**Campo**|**Tipo**|**Valores permitidos**|**Descripción**|
|---|---|---|---|
|**`prevision`**|**String**|`"Positivo"`, `"Neutro"`, `"Negativo"`|Representa la etiqueta categórica asignada por el modelo de IA tras analizar el texto.|
|**`probabilidad`**|**Float**|`0.0` a `1.0`|Indica el nivel de confianza del modelo en su predicción, expresado en formato decimal (ej: 0.945).|

---

## 3. Guía de Testing para el Equipo

1.  Inicia tu servidor: `uvicorn main:app --reload --port 8080`
2. Ejecutar este comando en una nueva terminal

```bash
curl -X POST http://localhost:8080/predict/sentiment \
     -H "Content-Type: application/json" \
     -d '{"text": "Estoy muy feliz con el servicio"}'
```

### Prueba con Swagger (Navegador)

1. Inicia tu servidor: `uvicorn main:app --reload --port 8080`
    
2. Accede a: `http://localhost:8080/docs` e interactúa con el endpoint.
---
## 4. Gestión de Logs y Manejo de Errores (Resiliencia)

Para garantizar la estabilidad del microservicio y facilitar el "debugging" (depuración) entre los equipos de DS y Backend, se establecen las siguientes reglas de respuesta y registro:

### 🚩 Códigos de Estado HTTP

El microservicio utilizará códigos estándar para informar al Backend de Java sobre el resultado de la petición:

| **Código** | **Estado**                | **Escenario en el que ocurre** (registro en `main.py`)                                                                                                                                                 |
| ---------- | ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **200**    | **OK**                    | La predicción se realizó exitosamente y se entrega el JSON de salida.                                                                                                                                  |
| **422**    | **Bad Request**           | Se activa automáticamente si el JSON está mal, pero requiere `min_length=1` en la clase `TextIn` para detectar textos vacíos o entradas numéricas.<br> → `El texto no puede estar vacío o contener solo espacios.` </br> → `El texto no puede ser únicamente numérico.` |
| **405**    | **Method Not Allowed**    | FastAPI lo genera solo si se intenta acceder al endpoint mediante un método distinto a `POST` (ej: `GET`).                                                                                             |
| **500**    | **Internal Server Error** | Fallo crítico en el servidor, como la imposibilidad de cargar el modelo `.pkl`.<br> → `Error interno al procesar la predicción.`                                                              |
| **503**    | **Service Unavailable**   | El servidor está activo pero el modelo de IA no ha terminado de cargarse en memoria.<br> →`Modelo no cargado en el servidor`                                                                      |

### 📝 Registro de Logs (Trazabilidad)

El archivo **`main.py`** generará registros automáticos en la consola para monitorear el flujo de trabajo:

- **Startup Log:** Confirmación visual de que el modelo `.pkl` se cargó correctamente al arrancar el servidor pudiendo visualizar en consola: `✅ Pipeline de producción cargado correctamente.`
    
- **Request Log:** Registro de cada petición recibida. Cada vez que llegue una "servilleta" (JSON), se registrará la hora y el tipo de petición para medir la latencia.
    
- **Error log:** Ante un error 500, el sistema imprimirá el "Traceback" completo en la consola de Python para identificar si el fallo es de memoria, de versión de librería o de datos.
    
---

## 🧠 La Analogía: "El Sommelier de Mensajes"

Imagina el proyecto como un **Restaurante de Alta Cocina**:

1. **El Cliente:** Es el **Usuario final** (o el sistema de Frontend/Postman). Es quien origina la acción porque tiene una necesidad o una opinión que expresar.
    
2. **La Reseña:** Es el **Dato crudo** o el mensaje de texto. Es la información que el cliente quiere comunicar ("Me gustó el hotel" o "Pésimo servicio").
    
3. **La Servilleta (JSON de entrada):** Es el formato donde se escribe la reseña (el campo `"text"`) para que pueda ser transportada.
    
4. **El Contrato API:** Es el **Manual de Procedimientos** pegado en la pared de la cocina. Dicta que el mesero debe usar la ventanilla (Puerto 8080) y que el Sommelier debe responder con un Post-it específico.
    
5. **El Backend de Java (El Mesero):** Toma la servilleta. Sabe gestionar la mesa y cobrar, pero no entiende de sentimientos científicos; por eso, sigue el manual (Contrato) y corre a buscar al experto.
    
6. **`main.py` (La Estación de Trabajo):** Es el espacio físico del Sommelier. Aquí están sus herramientas (FastAPI), sus copas y el acceso a la ventanilla (Endpoints) para recibir pedidos.
    
7. **El Sommelier (Tu API de Python):** Vive dentro de `main.py`. Recibe la servilleta por la ventanilla, usa su "olfato" (**Modelo .pkl**) y redacta el resultado.
    
8. **El Post-it (JSON de salida):** **(El objeto)** Es el **formato físico** del mensaje. Representa la estructura técnica que acordaron en el contrato: un papelito pequeño donde solo caben dos datos: `prevision` y `probabilidad`. No es una carta larga, es una respuesta rápida y estandarizada.
    
9. **El Diagnóstico (La Respuesta):** **(El contenido):** Es la **conclusión** que el Sommelier (tu IA) escribió en ese papel. Es el valor del resultado (por ejemplo: "Positivo") tras haber analizado la reseña.

### El Sistema de Alarmas

- **Gestión de Errores (El Rechazo):** Si el **Mesero (Java)** le entrega al **Sommelier (Python)** una servilleta manchada de café o totalmente en blanco, el Sommelier no intenta adivinar; inmediatamente le devuelve la servilleta con una nota roja (**Error 400**) diciendo: "Esto no se puede leer, tráeme una nueva".
    
- **Logs (La Bitácora):** El Sommelier tiene un cuaderno en su estación de trabajo (**`main.py`**). Allí anota cada vez que analiza una reseña y si hubo algún problema con su herramienta de trabajo (el sacacorchos o **modelo .pkl**). Si el Sommelier se enferma y no puede trabajar (**Error 500**), el dueño del restaurante puede leer la bitácora para saber exactamente qué falló.

---

## 🏆 Resumen:

Este contrato cumple con tres funciones estratégicas que los evaluadores valoran críticamente:

1. **Estandarización y Consistencia:** Elimina cualquier ambigüedad sobre los nombres de los campos. Al fijar términos como `prevision`, aseguras que el equipo de Data Science y el de Backend no tengan errores de integración de último minuto por usar palabras distintas (como "resultado" o "etiqueta").
    
2. **Garantía de Calidad (Validación):** Define qué ocurre ante datos erróneos, como un texto vacío (Error 400). Esto demuestra a los jueces que el equipo consideró la "robustez" del sistema y que la API no se caerá si un usuario comete un error, cumpliendo con las funcionalidades exigidas del MVP.
    
3. **Facilidad de Integración y Escalabilidad:** Al incluir ejemplos claros y un snippet de código, permites que cualquier compañero, aunque no sepa Python, pueda conectar su parte del proyecto en minutos. Esto acelera el desarrollo y permite que el sistema crezca como una arquitectura de microservicios moderna.

