# SentimentAPI – Frontend Demo

Frontend web del proyecto **SentimentAPI**, desarrollado como **demo funcional** para **Oracle Next Education (ONE)**.

Este módulo implementa una **interfaz BI ligera** para análisis de sentimiento, funcionando sobre **Nginx + Docker** y consumiendo datos reales o simulados almacenados en `localStorage`.

> ⚠️ Esta rama (`feature/frontend-demo`) es **exclusiva de frontend** y **no reemplaza** la rama `dev`.

---

## 🧩 Rol del Frontend dentro del ecosistema

El ecosistema completo del proyecto contempla:

- **Backend API (Java / REST)**  
- **Microservicio ML (modelos de sentimiento)**  
- **Frontend Web (este módulo)**  
- **Docker / Nginx para despliegue demo**

El frontend:

- No define modelos de ML
- No decide la lógica del sentimiento
- Visualiza resultados enviados por el backend **o** simulados en modo MOCK

---

## ⚙️ Modos de operación del Frontend

| Estado del entorno | Comportamiento |
|------------------|----------------|
| Backend + ML activos | Resultados reales |
| Backend parcial | Resultados mixtos |
| Sin backend | **Modo MOCK local (demo)** |

En modo MOCK:
- Los análisis se generan localmente
- Se almacenan en `localStorage`
- Alimentan **Dashboard** y **Estadísticas**

---

## 📂 Estructura real del módulo Frontend

```text
frontend
├── Dockerfile
├── README.md
└── public
    ├── index.html
    ├── dashboard.html
    ├── estadisticas.html
    ├── docs.html
    ├── recursos.html
    └── assets
        ├── css
        │   └── style.css
        └── js
            └── app.js
```

### Puntos clave

- **Nginx sirve todo desde `/public`**
- CSS y JS viven en `/assets`
- HTML enlaza recursos con rutas absolutas `/assets/...`

---

## 🎨 Funcionalidades implementadas

### Páginas

- **Inicio**: envío de comentarios y análisis
- **Dashboard**: BI resumido (KPIs, gráficas, tabla)
- **Estadísticas**: análisis histórico avanzado
- **Docs / Recursos**: secciones informativas

### UI / UX

- Tema claro / oscuro persistente
- Header global reutilizado
- Layout tipo BI
- Gráficas canvas (sin librerías externas)
- Diseño responsive

---

## 📊 Dashboard y Estadísticas

Ambas vistas consumen datos desde:

```text
localStorage:
- sentimental_history_v1
- sentimental_stats_totals_v1
```

Esto permite:

- KPIs acumulados
- Sentiment over time
- Distribución por categoría
- Historial detallado
- Nube de palabras (base)

---

## ▶️ Levantar el frontend con Docker

Desde la carpeta `frontend`:

```bash
docker build -t sentimental-frontend .
docker run -p 3000:80 sentimental-frontend
```

Abrir en el navegador:

```text
http://localhost:3000
```

> El contenedor usa **Nginx Alpine** y expone el puerto **80** internamente.

---

## 🔗 Integración con Backend

Cuando el backend esté disponible:

- Endpoint esperado: `POST /sentiment`
- El frontend enviará el texto del usuario
- El backend define sentimiento, probabilidad y explicabilidad

Mientras tanto, el frontend puede operar de forma autónoma (MOCK).

---

## 🚦 Estado actual

- ✔ Header unificado en todas las páginas
- ✔ Dashboard BI funcional
- ✔ Estadísticas conectadas a datos reales del historial
- ✔ Docker + Nginx estable
- ✔ Listo para demo técnica

---

## 👤 Responsable

**Frontend / UI / UX**  
**Autor:** Florentino López  
**Programa:** Oracle Next Education  
**Rama:** `feature/frontend-demo`

Este frontend está diseñado como:

- Demo profesional
- Base para integración productiva
- Evidencia técnica de arquitectura y UX
