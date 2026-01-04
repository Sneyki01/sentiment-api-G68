# SentimentAPI – Frontend Demo

Proyecto demo de análisis de sentimiento desarrollado para **Oracle Next Education**.

Este README explica cómo levantar la **interfaz de usuario** del proyecto **SentimentAPI** usando Docker.  
Este frontend es un **demo funcional** que simula la interacción con la API de análisis de sentimientos.

> ⚠️ Esta rama **no reemplaza** a `dev`. Es una rama de **trabajo especializado en frontend**.

---

## 🧩 Componentes del Proyecto

El ecosistema completo incluye:

- **Backend Java (API REST — puerto 8000)**
- **Microservicio de Machine Learning (puerto 8080)**
- **Frontend Web (puerto 3000)**
- **Contenedores Docker para ejecución demo**

### Modos de operación del frontend

| Estado del proyecto        | Comportamiento del Frontend              |
|---------------------------|------------------------------------------|
| ML / Backend en pruebas   | Puede devolver resultados neutros        |
| ML integrado en `dev`     | Muestra resultados reales                |
| Sin backend disponible    | Puede operar en modo mock temporal       |

> El frontend no define el modelo de ML ni sus resultados.  
> Se adapta al estado que el equipo **BE / DS** publique en `dev`.

---

## 📂 Estructura del módulo Frontend

```text
/frontend
├─ index.html    # Página principal con input de texto y botón "Analizar"
├─ style.css     # Estilos y diseño
├─ app.js        # Lógica del frontend + integración con API
├─ Dockerfile    # Contenedor del frontend
```

### Tecnologías utilizadas

- HTML + CSS + JavaScript (sin frameworks)
- Diseño ligero y portable
- Pensado para despliegue y demo rápida

---

## 🌐 Integración Frontend — Backend

### Puertos activos durante desarrollo

| Componente   | Puerto |
|-------------|--------|
| Frontend    | 3000   |
| Backend API | 8000   |
| ML Service  | 8080   |

### Endpoint actual de backend

**POST** `/sentiment`

### Ejemplo de request

```json
{
  "text": "comentario del usuario"
}
```

### Ejemplo de respuesta esperada

```json
{
  "prevision": "Positivo | Negativo | Neutro",
  "probabilidad": 0.87
}
```

### Colores aplicados en la UI

| Sentimiento | Color |
|-------------|-------|
| Positivo    | Verde |
| Negativo    | Rojo  |
| Neutro      | Gris  |

---

## 🧪 Validaciones de entrada

El campo de texto permite:

- Entre **3 y 2000 caracteres**

Incluye:

- Sanitización de espacios
- Mensajes de validación
- Estado de carga
- Elemento para limpiar texto
- Botón de envío contextual

---

## ▶️ Levantar el frontend con Docker

Desde la raíz del repositorio:

```bash
docker compose up --build
```

Abrir en el navegador:

```text
http://localhost:3000
```

Si la UI carga correctamente, el frontend está operativo.

---

## 🚦 Estados actuales de integración

El frontend soporta:

- Ejecución con backend local
- Integración futura con endpoint ML definitivo
- Despliegue piloto en OCI

### Notas de coordinación con el equipo

- El ML final será integrado vía backend
- Esta rama no fuerza mocks
- El comportamiento depende del estado publicado en `dev`
- Cuando se publique el endpoint productivo se actualizará `app.js`

---

## 👤 Responsable del módulo Frontend

**Desarrollo UI / UX**  
**Autor:** Florentino López  
**Rama activa:** `feature/frontend-demo`

Este módulo está diseñado para servir como:

- Demo de experiencia de usuario
- Punto de entrada para pruebas
- Base para integración con backend productivo
