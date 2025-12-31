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

## Arquitectura general
```mermaid
 flowchart TD
    A[texto de cliente] --> B[Back-End API]
    B -->C[Servicio ML] 
    C -->D[Modelo de sentimiento]
    D --> E[Respuesta]
```
- **Backend (Java)**: expone la API publica, valida request, maneja errores
y consume el servicio de ML
- **Data Science (Python)**: entrena el modelo y expone un microservicio
para realizar predicciones

---
## Contrato de la API (Publico)
**Endpoint**
```yaml
POST: /sentiment
```

**Request**
```json
{
  "text" : "El servicio fue excelente"
}
```

**Validaciones**

- Text es obligatorio
- Longitud minima: 3 caracteres
- Longitud maxima: 2000 Caracteres

**Response (200 OK)**

```json
{
  "prevision": "positivo",
  "probabilidad" : "0.87"
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

cd backend-java
mvn spring-boot:run
```

La API estara disponible en:
```yaml
http://localhost:8000
```
---

**Data science**

Requisitos:
*Por definir

Ejemplos de arranque:
*Por definir

---

## Stack tecnologico

**Backend**
- java 17
- Spring boot
- Bean validation
- REST API

**Data Science**

*Por definir

---

## Estado del proyecto
Backend: ![Static Badge](https://img.shields.io/badge/In%20Progress-yellow)


Data Science ![Static Badge](https://img.shields.io/badge/In%20Progress-yellow)

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
-[ ] Integracion de ML
- [ ] Persistencia
- [ ] Docker

Por definir*

---

## Aprendizajes

*Por definir

---

## Limitaciones conocidas

*Por definir

---
## Nota final

Este README es un documento **vivo** y se ira ampliando conforme el
proyecto evolucione.