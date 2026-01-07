# SentimentAPI - Clasificacion de sentimientos
![Java](https://img.shields.io/badge/Java-17-orange)
![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3-green)
![Python](https://img.shields.io/badge/Python-3.9-blue)
![Status](https://img.shields.io/badge/Status-MVP-yellow)
## Descripcion
**SentimentAPI** es una API REST que permite clasificar el 
sentimiento de texos (comentarios, reseñas o mensajes) 
como **Positivo, Neutro o Negativo**, devolviendo ademas la 
**Probabilidad/Confianza** de la prediccion.

El objetivo del proyecto es demostrar la **integracion entre
Data Science y Back-End**, entregando una MVP funcional capaz de
recibir texto, procesarlo mediante un modelo de Machine Learning
y responder de forma automatica a traves de una API.

---
## Caso de uso
Empresas que reciben grandes volumenes de feedback (reseñas, encuestas,
redes sociales) pueden usar esta API para: 

- identificar rapidamente comentarios negativos
- priorizar respuesta en atencion al cliente
- medir satisfaccion del cliente a lo largo del tiempo
- analizar campañas de marketing

---

## Arquitectura G68 (Híbrida)
```mermaid
 flowchart TD
    A[Texto de Cliente] --> B[Back-End Java]
    B --> C[Microservicio Python]
    C --> D[Motor Semántico G68]
    D --> E[Modelo Machine Learning]
    E --> F[Respuesta con Explicabilidad]
```
- **Backend (Java)**: Expone la API pública, maneja la persistencia (en desarrollo) y consume el servicio de ML.
- **Data Science (Python)**: Implementa un **Motor Híbrido** que combina un clasificador `LinearSVC` calibrado con un motor de reglas semánticas que detecta intensificadores, atenuadores y casos específicos del sector hotelero.

---
## Contrato de la API (Público)
**Endpoint**
```yaml
POST: /sentiment
```

**Request**
```json
{
  "text" : "Las habitaciones tenían algo de moho pero el wifi es muy bueno."
}
```

**Validaciones**

- Text es obligatorio
- Longitud minima: 3 caracteres
- Longitud maxima: 2000 Caracteres

**Response (200 OK)**
```json
{
  "prevision": "Negativo",
  "probabilidad" : "0.42",
  "explicabilidad": "moho (atenuado por 'algo') | wifi (intensificado por 'muy')"
}
```
**Posibles valores de Prevision**

- Positivo
- Neutro
- Negativo

---
## Respuestas de error
**Error de validacion (400 Bad Request)**
```json
{
  "error" : "El campo text es obligatorio"
}
```

**JSON mal formado (400 Bad Request)**

```json
{
  "error": "JSON invalido"
}
```

**Servicio ML no disponible (503 Service Unavailable)**

```json
{
  "error": "Servicio de prediccion no disponible"
}
```

---

## Contrato interno (Backend ↔ Data Science)

**Endpoint**
```yaml
POST: /predict/sentiment
```

**Request**
```json
{
  "text" : "El servicio fue excelente"
}
```

**Response**
```json
{
  "prevision" : "Positivo | Neutral | Negativo",
  "probabilidad" : "0.87"
}
```
- Prevision: Clase predicha por el modelo
- Probabilidad: Confianza de la clase ganadora (0-1)

---
## Puertos y servicios
| Servicio                  | Puerto |
|---------------------------|--------|
| Backend Java (SpringBoot) | 8000   |
| Servicio ML (Python)      | 8080   |

---

## Como ejecutar el proyecto (Local)

**Backend (Java)**

Requisitos:
- Java 17+
- Maven

```bash 

cd backend-java/api
mvn spring-boot:run
```

La API estará disponible en:
```yaml
http://localhost:8000
```
---

**Data Science (Python)**

Requisitos:
- Python 3.9+
- Un entorno virtual (recomendado)

1.  **Navega a la carpeta de Machine Learning:**
    ```bash
    cd ml-python
    ```

2.  **Crea y activa un entorno virtual:**
    ```bash
    # En Windows
    python -m venv venv
    .\venv\Scripts\activate
    
    # En macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Ejecuta el servicio de ML:**
    ```bash
    # Desde la carpeta raíz del proyecto
    uvicorn ml-python.main:app --host 0.0.0.0 --port 8080
    ```
    El servicio de ML estará disponible en `http://localhost:8080`.

---

## Stack tecnológico

**Backend**
- Java 17
- Spring Boot 3
- Maven
- Bean Validation
- REST API

**Data Science**
- Python 3.9
- FastAPI: Para construir la API de inferencia.
- Uvicorn: Como servidor ASGI para FastAPI.
- Scikit-learn: Para el modelo (LinearSVC) y vectorización (TfidfVectorizer).
- Joblib: Para cargar los modelos pre-entrenados.
- NLTK y RegEx: Para la limpieza de texto y el motor de reglas semánticas.

---

## Estado del proyecto
Backend: ![Static Badge](https://img.shields.io/badge/Completed-green)


Data Science ![Static Badge](https://img.shields.io/badge/Completed-green)

---

## Equipo

Proyecto desarrollado por estudiantes de Backend 
y Data Science como parte de un Hackathon de **NoCountry** junto
con **AluraLatam**, con enfoque en integración real entre disciplinas y buenas prácticas de desarrollo

**Integrantes**:

⚙️ **Backend Team**

<table>
  <tr>
    <!-- Backend 1 -->
    <td align="center" width="200">
      <a href="https://github.com/TinusLopez">
        <img src="https://avatars.githubusercontent.com/u/73755236?v=4" width="120" style="border-radius:50%;" />
        <br />
        <strong>Florentino Lopez</strong>
      </a>
      <br/>
      <sub>Backend Developer</sub>
    </td>
    <!-- Backend 2 -->
    <td align="center" width="200">
      <a href="https://github.com/lorenaraygoza09">
        <img src="https://avatars.githubusercontent.com/u/181152882?v=4" width="120" style="border-radius:50%;" />
        <br />
        <strong>Lorena Raygoza</strong>
      </a>
      <br />
      <sub>Backend Developer</sub>
    </td>
    <!-- Backend 3 -->
    <td align="center" width="200">
      <a href="https://github.com/Sneyki01">
        <img src="https://avatars.githubusercontent.com/u/156740507?v=4" width="120" style="border-radius:50%;" />
        <br />
        <strong>Edwing Herrera</strong>
      </a>
      <br />
      <sub>Backend Developer</sub>
    </td>
    <!-- Backend 4
    <td align="center" width="200">
      <a href="https://github.com/backend4">
        <img src="https://avatars.githubusercontent.com/u/ID4?v=4" width="120" style="border-radius:50%;" />
        <br />
        <strong>Nombre Apellido</strong>
      </a>
      <br />
      <sub>Backend Developer · Integrations</sub>
    </td>-->
  </tr>
</table>


📊 **Data Science Team**

<table>
  <tr>
    <!-- Data 1 -->
    <td align="center" width="200">
      <a href="https://github.com/dzapatasal">
        <img src="https://avatars.githubusercontent.com/u/182231593?v=4" width="120" style="border-radius:50%;" />
        <br />
        <strong>Diego Zapata</strong>
      </a>
      <br />
      <sub>Data Scientist</sub>
    </td>
    <!-- Data 2 -->
    <td align="center" width="200">
      <a href="https://github.com/Fernando-Falla">
        <img src="https://avatars.githubusercontent.com/u/203438966?v=4" width="120" style="border-radius:50%;" />
        <br />
        <strong>Fernando Falla</strong>
      </a>
      <br />
      <sub>Data Scientist</sub>
    </td>
    <!-- Data 3 -->
    <td align="center" width="200">
      <a href="https://github.com/ADRIAN-GP84">
        <img src="https://avatars.githubusercontent.com/u/198021746?v=4" width="120" style="border-radius:50%;" />
        <br />
        <strong>Adrian Galán</strong>
      </a>
      <br />
      <sub>Data Scientist</sub>
    </td>
    <!-- Data 4 
    <td align="center" width="200">
      <a href="https://github.com/data4">
        <img src="https://avatars.githubusercontent.com/u/ID8?v=4" width="120" style="border-radius:50%;" />
        <br />
        <strong>Nombre Apellido</strong>
      </a>
      <br />
      <sub>Data Scientist · Pipelines</sub>
    </td>-->
  </tr>
</table>

### ❤️ Gracias
Este proyecto existe porque personas reales dedican tiempo real.

---

## Proximas mejoras (roadmap)
-[x] API REST basica
-[x] Validaciones y manejo de errores
-[x] Motor Híbrido G68 (ML + Semántica)
-[x] Exportación y despliegue de modelos
-[ ] Persistencia en Base de Datos
-[ ] Dockerización y Orquestación

---
## Aprendizajes
- **Integración Multidisciplinaria:** Logramos conectar la precisión estadística de Python con la robustez de Java.
- **Ingeniería Semántica:** Aprendimos que en sectores críticos como el hotelero, el Machine Learning puro no es suficiente; las reglas de negocio (lexicones especializados) son el factor diferencial.
- **Explicabilidad (XAI):** La importancia de que una IA sea transparente ("caja abierta") para que el usuario final confíe en los resultados.

---

## Limitaciones conocidas

*Por definir

---
## Nota final

Este README es un documento **vivo** y se ira ampliando conforme el
proyecto evolucione.