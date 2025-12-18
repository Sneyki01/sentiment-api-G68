# SentimentAPI – Frontend Demo

Proyecto demo de análisis de sentimiento desarrollado para Oracle Next Education.

Este README explica cómo levantar la **interfaz de usuario** del proyecto **SentimentAPI** usando Docker.  
Este frontend es un **demo funcional** que simula la interacción con la API de análisis de sentimientos.

---

## Componentes

- **Backend:** API REST en Spring Boot
- **Frontend:** Interfaz web simple
- **Docker:** Contenerización para demo rápida

---

## Estructura del frontend

- `index.html` → Página principal con input de texto y botón "Analizar"
- `style.css` → Estilos de la página
- `app.js` → Lógica del frontend (mock de análisis de sentimientos o conexión a la API real)
- `Dockerfile` → Contenerización del frontend para demo rápida

---

## Levantar el frontend con Docker

Desde la raíz del proyecto o dentro de la carpeta `frontend/`:

```bash
docker compose up --build
