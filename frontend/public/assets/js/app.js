/**
 * ============================================================================
 * SentimentalIA — Front-End (MVP) — app.js
 * ============================================================================
 * 
 * PROPÓSITO PARA JUECES:
 * Este archivo implementa el Front-End completo del MVP de SentimentalIA.
 * El FE se conecta ÚNICAMENTE al Backend (BE) vía HTTP REST API.
 * 
 * ARQUITECTURA:
 * - El FE NO calcula sentimientos, NO hace heurísticas, NO usa datos mock.
 * - El FE consume endpoints reales del Backend Java Spring Boot.
 * - El Backend se comunica con el servicio ML (Python) internamente.
 * - El FE solo necesita conocer la API pública del Backend.
 * 
 * ENDPOINTS UTILIZADOS:
 * - POST /sentiment     → Analizar sentimiento de un texto
 * - GET  /dashboard    → Obtener datos agregados del dashboard
 * - GET  /dashboard/*  → Endpoints granulares (fallback)
 * 
 * AUTOR: Equipo Front-End (Hackathon NoCountry + AluraLatam)
 * FECHA: 2025-01-XX
 * ============================================================================
 */

/* ============================================================================
 * 1) CONFIGURACIÓN DE API
 * ============================================================================
 * Define la URL base del Backend y todos los endpoints disponibles.
 * Estos valores pueden ser inyectados desde el HTML si es necesario.
 */

/**
 * URL base del Backend Java Spring Boot.
 * 
 * Prioridad:
 * 1. Variable global inyectada desde HTML: window.__SENTIMENTAL_API_BASE__
 * 2. Fallback: localhost:8000 (puerto estándar del Backend)
 * 
 * @type {string}
 */
const API_BASE_URL =
  (window && window.__SENTIMENTAL_API_BASE__) || "http://localhost:8000";

/**
 * Endpoints del Backend según el contrato de la rama DEV.
 * 
 * CONTRATO PÚBLICO (FE ↔ BE):
 * - POST /sentiment: Analiza sentimiento de un texto
 *   Request:  { "text": "..." }
 *   Response: { "prevision": "Positivo|Neutro|Negativo", "probabilidad": 0.87 }
 * 
 * CONTRATO DASHBOARD (FE ↔ BE):
 * - GET /dashboard: Endpoint agregado (ideal para MVP)
 * - GET /dashboard/*: Endpoints granulares (fallback si el agregado no existe)
 * 
 * @type {Object<string, string>}
 */
const ENDPOINTS = {
  // Endpoint principal para análisis de sentimiento
  SENTIMENT: "/sentiment",
  
  // Dashboard: endpoint agregado (preferido)
  DASHBOARD_ALL: "/dashboard",

  // Dashboard: endpoints granulares (fallback automático)
  DASHBOARD_KPIS: "/dashboard/kpis",
  DASHBOARD_TRENDS_7D: "/dashboard/trends?days=7",
  DASHBOARD_TOP_DEPTS: "/dashboard/top-departments?limit=6",
  DASHBOARD_RECENT: "/dashboard/recent?limit=10",
  DASHBOARD_DISTRIBUTION: "/dashboard/distribution",
};

/* ============================================================================
 * 2) UTILIDADES: Funciones auxiliares para HTTP y manipulación de datos
 * ============================================================================
 */

/**
 * Une una URL base con un path, manejando correctamente las barras.
 * 
 * @param {string} base - URL base (ej: "http://localhost:8000")
 * @param {string} path - Path del endpoint (ej: "/sentiment")
 * @returns {string} URL completa
 * 
 * @example
 * joinUrl("http://localhost:8000", "/sentiment") // → "http://localhost:8000/sentiment"
 */
function joinUrl(base, path) {
  const b = String(base || "").replace(/\/+$/, "");
  const p = String(path || "").replace(/^\/+/, "");
  return `${b}/${p}`;
}

/**
 * Realiza una petición HTTP con manejo robusto de errores y timeout.
 * 
 * CARACTERÍSTICAS:
 * - Timeout configurable (por defecto 12 segundos)
 * - Manejo de errores HTTP (400, 500, 503, etc.)
 * - Detección automática de JSON vs texto
 * - Mensajes de error descriptivos
 * 
 * @param {string} path - Path del endpoint (ej: "/sentiment")
 * @param {Object} options - Opciones de la petición
 * @param {string} options.method - Método HTTP (GET, POST, etc.)
 * @param {Object} options.body - Cuerpo de la petición (se serializa a JSON)
 * @param {number} options.timeoutMs - Timeout en milisegundos (default: 12000)
 * @returns {Promise<Object>} Respuesta parseada como JSON
 * @throws {Error} Si la petición falla (timeout, error HTTP, red, etc.)
 * 
 * @example
 * // GET request
 * const data = await fetchJSON("/dashboard");
 * 
 * @example
 * // POST request
 * const result = await fetchJSON("/sentiment", {
 *   method: "POST",
 *   body: { text: "Me encantó el servicio" }
 * });
 */
async function fetchJSON(path, { method = "GET", body = null, timeoutMs = 12000 } = {}) {
  const url = joinUrl(API_BASE_URL, path);

  // Configurar AbortController para timeout
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

  try {
    // Configurar headers y body
    const headers = { Accept: "application/json" };
    let requestBody = null;

    if (body && (method === "POST" || method === "PUT" || method === "PATCH")) {
      headers["Content-Type"] = "application/json";
      requestBody = JSON.stringify(body);
    }

    // Realizar petición
    const res = await fetch(url, {
      method,
      headers,
      body: requestBody,
      signal: controller.signal,
    });

    // Detectar tipo de contenido
    const contentType = (res.headers.get("content-type") || "").toLowerCase();
    const isJSON = contentType.includes("application/json");

    // Parsear respuesta
    let responseBody = null;
    if (isJSON) {
      try {
        responseBody = await res.json();
      } catch (_) {
        // JSON inválido, intentar leer como texto
        responseBody = await res.text().catch(() => null);
      }
    } else {
      responseBody = await res.text().catch(() => null);
    }

    // Verificar si la respuesta es exitosa
    if (!res.ok) {
      // Extraer mensaje de error del body
      const errorMessage =
        (responseBody && responseBody.error) ||
        (responseBody && responseBody.message) ||
        (typeof responseBody === "string" ? responseBody : null) ||
        `Error HTTP ${res.status}`;

      const error = new Error(errorMessage);
      error.status = res.status;
      error.url = url;
      error.body = responseBody;
      throw error;
    }

    return responseBody;
  } catch (e) {
    // Manejar timeout
    if (e.name === "AbortError") {
      const timeoutError = new Error("Timeout al consultar el Backend");
      timeoutError.isTimeout = true;
      throw timeoutError;
    }
    
    // Re-lanzar errores conocidos
    if (e instanceof Error) {
      throw e;
    }
    
    // Error desconocido
    throw new Error("Error de red al comunicarse con el Backend");
  } finally {
    clearTimeout(timeoutId);
  }
}

/**
 * Escapa caracteres HTML para prevenir XSS.
 * 
 * @param {string} str - String a escapar
 * @returns {string} String escapado
 */
function escapeHtml(str) {
  return String(str ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

/**
 * Normaliza un valor numérico al rango [0, 1].
 * 
 * @param {number} n - Valor a normalizar
 * @returns {number} Valor entre 0 y 1
 */
function clamp01(n) {
  const x = Number(n);
  if (!Number.isFinite(x)) return 0;
  return Math.max(0, Math.min(1, x));
}

/**
 * Normaliza un valor de sentimiento a formato estándar.
 * 
 * @param {string} value - Valor de sentimiento (puede ser "Positivo", "positivo", etc.)
 * @returns {string} "positivo", "negativo" o "neutro"
 */
function toSentimentLower(value) {
  const normalized = String(value || "").trim().toLowerCase();
  if (normalized.includes("posit")) return "positivo";
  if (normalized.includes("negat")) return "negativo";
  return "neutro";
}

/**
 * Formatea una fecha/timestamp a formato legible.
 * 
 * @param {number|string} timestamp - Timestamp en milisegundos
 * @returns {string} Fecha formateada (YYYY-MM-DD HH:MM)
 */
function formatDateShort(timestamp) {
  const d = new Date(timestamp);
  const yyyy = d.getFullYear();
  const mm = String(d.getMonth() + 1).padStart(2, "0");
  const dd = String(d.getDate()).padStart(2, "0");
  const hh = String(d.getHours()).padStart(2, "0");
  const mi = String(d.getMinutes()).padStart(2, "0");
  return `${yyyy}-${mm}-${dd} ${hh}:${mi}`;
}

/**
 * Asegura que un valor sea un array.
 * 
 * @param {*} value - Valor a verificar
 * @returns {Array} Array (vacío si el valor no es un array)
 */
function safeArray(value) {
  return Array.isArray(value) ? value : [];
}

/**
 * Actualiza el texto de un elemento por su ID.
 * 
 * @param {string} id - ID del elemento
 * @param {string} value - Nuevo texto
 */
function setText(id, value) {
  const el = document.getElementById(id);
  if (el) el.textContent = value;
}

/* ============================================================================
 * 3) GESTIÓN DE TEMA (OS + toggle persistente)
 * ============================================================================
 */

const THEME_STORAGE_KEY = "sentimental_theme_preference";
let mqTheme = null;

/**
 * Obtiene el tema guardado en localStorage.
 * 
 * @returns {string|null} "light", "dark" o null
 */
function getSavedTheme() {
  try {
    const v = localStorage.getItem(THEME_STORAGE_KEY);
    if (v === "light" || v === "dark") return v;
  } catch (_) {}
  return null;
}

/**
 * Guarda la preferencia de tema en localStorage.
 * 
 * @param {string} value - "light" o "dark"
 */
function saveTheme(value) {
  try {
    localStorage.setItem(THEME_STORAGE_KEY, value);
  } catch (_) {}
}

/**
 * Aplica un tema al documento.
 * 
 * @param {string} mode - "light" o "dark"
 */
function applyTheme(mode) {
  document.body.classList.remove("theme-light", "theme-dark");
  document.body.classList.add(mode === "light" ? "theme-light" : "theme-dark");
  updateThemeToggleUI();
}

/**
 * Aplica el tema según la preferencia del sistema operativo.
 */
function applyThemeFromOS() {
  const prefersDark = mqTheme ? mqTheme.matches : true;
  applyTheme(prefersDark ? "dark" : "light");
}

/**
 * Actualiza la UI del botón de toggle de tema.
 */
function updateThemeToggleUI() {
  const btn = document.getElementById("themeToggle");
  if (!btn) return;

  const isLight = document.body.classList.contains("theme-light");
  btn.textContent = isLight ? "☾" : "☀";
  btn.title = isLight ? "Cambiar a tema oscuro" : "Cambiar a tema claro";
  btn.setAttribute("aria-label", btn.title);
}

/**
 * Configura el tema inicial desde el OS y escucha cambios.
 */
function setupThemeFromOS() {
  mqTheme = window.matchMedia("(prefers-color-scheme: dark)");

  const saved = getSavedTheme();
  if (saved) {
    applyTheme(saved);
  } else {
    applyThemeFromOS();
  }

  const onOSChange = () => {
    const savedNow = getSavedTheme();
    if (!savedNow) applyThemeFromOS();
    else updateThemeToggleUI();
  };

  if (typeof mqTheme.addEventListener === "function") {
    mqTheme.addEventListener("change", onOSChange);
  } else if (typeof mqTheme.addListener === "function") {
    mqTheme.addListener(onOSChange);
  }
}

/**
 * Configura el botón de toggle de tema.
 */
function setupThemeToggleButton() {
  const btn = document.getElementById("themeToggle");
  if (!btn) return;

  btn.addEventListener("click", () => {
    const isLight = document.body.classList.contains("theme-light");
    const next = isLight ? "dark" : "light";
    saveTheme(next);
    applyTheme(next);
  });

  updateThemeToggleUI();
}

/* ============================================================================
 * 4) NAVEGACIÓN: Resaltado de página activa
 * ============================================================================
 */

/**
 * Asegura que el link de navegación activo esté resaltado.
 */
function ensureActiveNav() {
  const links = document.querySelectorAll(".nav-link");
  if (!links || !links.length) return;

  const path = (window.location.pathname || "").toLowerCase();
  links.forEach((a) => a.classList.remove("active"));

  let active = "inicio";
  if (path.includes("dashboard")) active = "dashboard";
  else if (path.includes("estadisticas")) active = "estadisticas";
  else if (path.includes("docs")) active = "docs";
  else if (path.includes("recursos")) active = "recursos";

  links.forEach((a) => {
    const v = (a.getAttribute("data-nav") || "").toLowerCase();
    if (v === active) a.classList.add("active");
  });
}

/* ============================================================================
 * 5) ANÁLISIS DE SENTIMIENTO (Página Inicio - index.html)
 * ============================================================================
 * 
 * Esta sección maneja:
 * - Input de texto del usuario
 * - Botones de enviar/eliminar (visibilidad dinámica)
 * - Llamada al endpoint POST /sentiment
 * - Renderizado de resultados en el historial
 * - Manejo de errores y estados de carga
 */

/**
 * Estado global del análisis de sentimiento.
 */
const SentimentState = {
  isLoading: false,
  history: [],
};

/**
 * Obtiene el historial guardado en localStorage.
 * 
 * @returns {Array} Array de análisis previos
 */
function loadHistory() {
  try {
    const stored = localStorage.getItem("sentiment_history");
    if (stored) {
      return JSON.parse(stored);
    }
  } catch (_) {}
  return [];
}

/**
 * Guarda el historial en localStorage.
 * 
 * @param {Array} history - Array de análisis
 */
function saveHistory(history) {
  try {
    localStorage.setItem("sentiment_history", JSON.stringify(history));
  } catch (_) {}
}

/**
 * Analiza el sentimiento de un texto llamando al Backend.
 * 
 * CONTRATO:
 * - Request:  POST /sentiment { "text": "..." }
 * - Response: { "prevision": "Positivo|Neutro|Negativo", "probabilidad": 0.87 }
 * - Error:    { "error": "mensaje" } (400, 503, etc.)
 * 
 * @param {string} text - Texto a analizar
 * @returns {Promise<Object>} Resultado del análisis
 * @throws {Error} Si la petición falla
 */
async function analyzeSentiment(text) {
  return await fetchJSON(ENDPOINTS.SENTIMENT, {
    method: "POST",
    body: { text },
    timeoutMs: 15000, // 15 segundos para análisis ML
  });
}

/**
 * Actualiza la visibilidad de los botones según el estado del input.
 */
function updateInputButtons() {
  const textInput = document.getElementById("textInput");
  const clearButton = document.getElementById("clearButton");
  const sendButton = document.getElementById("sendButton");

  if (!textInput || !clearButton || !sendButton) return;

  const hasText = textInput.value.trim().length > 0;

  // Mostrar/ocultar botones según si hay texto
  if (hasText) {
    clearButton.classList.remove("hidden");
    sendButton.classList.remove("hidden");
  } else {
    clearButton.classList.add("hidden");
    sendButton.classList.add("hidden");
  }
}

/**
 * Limpia el input de texto y oculta los botones.
 */
function clearInput() {
  const textInput = document.getElementById("textInput");
  if (textInput) {
    textInput.value = "";
    updateInputButtons();
    textInput.focus();
  }
}

/**
 * Renderiza un análisis en el historial.
 * 
 * @param {Object} analysis - Objeto con: text, sentiment, probability, timestamp
 */
function renderAnalysis(analysis) {
  const historyContainer = document.getElementById("history");
  if (!historyContainer) return;

  const sentiment = toSentimentLower(analysis.sentiment || analysis.prevision || "neutro");
  const probability = clamp01(analysis.probability || analysis.probabilidad || 0);
  const text = analysis.text || "";
  const timestamp = analysis.timestamp || Date.now();

  // Determinar color según sentimiento
  let sentimentColor = "#9ca3af"; // neutro
  if (sentiment === "positivo") {
    sentimentColor = isLightTheme() ? "#16a34a" : "#4ade80";
  } else if (sentiment === "negativo") {
    sentimentColor = isLightTheme() ? "#b91c1c" : "#f97373";
  }

  // Crear elemento del historial
  const item = document.createElement("div");
  item.className = "history-item";
  item.innerHTML = `
    <div class="history-item-header">
      <span class="history-sentiment" style="color: ${sentimentColor}">
        ${escapeHtml(sentiment.toUpperCase())}
      </span>
      <span class="history-probability">${(probability * 100).toFixed(1)}%</span>
      <button class="history-delete" data-timestamp="${timestamp}" aria-label="Eliminar análisis">
        ×
      </button>
    </div>
    <div class="history-text">${escapeHtml(text)}</div>
    <div class="history-meta">${escapeHtml(formatDateShort(timestamp))}</div>
  `;

  // Agregar listener al botón eliminar
  const deleteBtn = item.querySelector(".history-delete");
  if (deleteBtn) {
    deleteBtn.addEventListener("click", () => {
      deleteAnalysis(timestamp);
    });
  }

  // Insertar al inicio del historial
  historyContainer.insertBefore(item, historyContainer.firstChild);
}

/**
 * Elimina un análisis del historial.
 * 
 * @param {number} timestamp - Timestamp del análisis a eliminar
 */
function deleteAnalysis(timestamp) {
  SentimentState.history = SentimentState.history.filter(
    (a) => a.timestamp !== timestamp
  );
  saveHistory(SentimentState.history);
  renderHistory();
}

/**
 * Renderiza todo el historial.
 */
function renderHistory() {
  const historyContainer = document.getElementById("history");
  if (!historyContainer) return;

  if (SentimentState.history.length === 0) {
    historyContainer.innerHTML = `
      <div class="history-empty">
        <p>No hay análisis aún. Escribe un comentario y analiza su sentimiento.</p>
      </div>
    `;
    return;
  }

  historyContainer.innerHTML = "";
  SentimentState.history.forEach((analysis) => {
    renderAnalysis(analysis);
  });
}

/**
 * Maneja el envío del formulario de análisis.
 */
async function handleSubmit() {
  const textInput = document.getElementById("textInput");
  if (!textInput) return;

  const text = textInput.value.trim();

  // Validación básica (el Backend también valida, pero mejor UX)
  if (text.length < 3) {
    alert("El texto debe tener al menos 3 caracteres.");
    return;
  }

  if (text.length > 2000) {
    alert("El texto no puede exceder 2000 caracteres.");
    return;
  }

  // Evitar múltiples envíos simultáneos
  if (SentimentState.isLoading) return;
  SentimentState.isLoading = true;

  // Deshabilitar botones durante la carga
  const sendButton = document.getElementById("sendButton");
  if (sendButton) {
    sendButton.disabled = true;
    sendButton.textContent = "⏳";
  }

  try {
    // Llamar al Backend
    const result = await analyzeSentiment(text);

    // Crear objeto de análisis
    const analysis = {
      text,
      sentiment: result.prevision || "Neutro",
      probability: result.probabilidad || 0,
      timestamp: Date.now(),
    };

    // Agregar al historial
    SentimentState.history.unshift(analysis);
    saveHistory(SentimentState.history);

    // Renderizar
    renderHistory();

    // Limpiar input
    clearInput();
  } catch (error) {
    // Mostrar error al usuario
    const errorMessage =
      error.message ||
      "No se pudo analizar el sentimiento. Verifica que el Backend esté disponible.";
    alert(`Error: ${errorMessage}`);
    console.error("[Sentiment] Error:", error);
  } finally {
    // Restaurar estado
    SentimentState.isLoading = false;
    if (sendButton) {
      sendButton.disabled = false;
      sendButton.textContent = "↑";
    }
  }
}

/**
 * Verifica si el tema actual es claro.
 * 
 * @returns {boolean}
 */
function isLightTheme() {
  return document.body.classList.contains("theme-light");
}

/**
 * Configura la página de inicio (análisis de sentimiento).
 */
function setupSentimentPage() {
  const textInput = document.getElementById("textInput");
  const clearButton = document.getElementById("clearButton");
  const sendButton = document.getElementById("sendButton");

  if (!textInput) return;

  // Cargar historial
  SentimentState.history = loadHistory();
  renderHistory();

  // Listener para mostrar/ocultar botones al escribir
  textInput.addEventListener("input", updateInputButtons);

  // Listener para limpiar
  if (clearButton) {
    clearButton.addEventListener("click", clearInput);
  }

  // Listener para enviar (botón)
  if (sendButton) {
    sendButton.addEventListener("click", handleSubmit);
  }

  // Listener para enviar (Enter, pero no Shift+Enter)
  textInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      if (textInput.value.trim().length > 0) {
        handleSubmit();
      }
    }
  });

  // Inicializar visibilidad de botones
  updateInputButtons();
}

/* ============================================================================
 * 6) GRÁFICAS Canvas (UI) — Donut / Línea / Barras
 * ============================================================================
 */

/**
 * Obtiene el color para un sentimiento según el tema actual.
 * 
 * @param {string} sentiment - "positivo", "negativo" o "neutro"
 * @returns {string} Color en formato hexadecimal
 */
function colorForSentiment(sentiment) {
  if (sentiment === "positivo") {
    return isLightTheme() ? "#16a34a" : "#4ade80";
  }
  if (sentiment === "negativo") {
    return isLightTheme() ? "#b91c1c" : "#f97373";
  }
  return isLightTheme() ? "#6b7280" : "#9ca3af";
}

/**
 * Dibuja un rectángulo redondeado en un canvas.
 * 
 * @param {CanvasRenderingContext2D} ctx - Contexto del canvas
 * @param {number} x - Posición X
 * @param {number} y - Posición Y
 * @param {number} w - Ancho
 * @param {number} h - Alto
 * @param {number} r - Radio de las esquinas
 */
function roundRect(ctx, x, y, w, h, r) {
  const rr = Math.min(r, w / 2, h / 2);
  ctx.beginPath();
  ctx.moveTo(x + rr, y);
  ctx.arcTo(x + w, y, x + w, y + h, rr);
  ctx.arcTo(x + w, y + h, x, y + h, rr);
  ctx.arcTo(x, y + h, x, y, rr);
  ctx.arcTo(x, y, x + w, y, rr);
  ctx.closePath();
}

/**
 * Dibuja un gráfico de dona (distribución de sentimientos).
 * 
 * @param {HTMLCanvasElement} canvas - Elemento canvas
 * @param {Array<number>} values - Valores [positivo, negativo, neutro]
 * @param {Array<string>} labels - Etiquetas ["positivo", "negativo", "neutro"]
 */
function drawDonut(canvas, values, labels) {
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  const w = (canvas.width = canvas.clientWidth);
  const h = (canvas.height = canvas.height || 260);

  ctx.clearRect(0, 0, w, h);

  const total = values.reduce((a, b) => a + b, 0);
  const cx = w / 2,
    cy = h / 2;
  const radius = Math.min(w, h) * 0.32;
  const inner = radius * 0.62;

  // Base ring
  ctx.beginPath();
  ctx.arc(cx, cy, radius, 0, Math.PI * 2);
  ctx.arc(cx, cy, inner, 0, Math.PI * 2, true);
  ctx.closePath();
  ctx.fillStyle = isLightTheme() ? "rgba(17,24,39,.06)" : "rgba(229,231,235,.06)";
  ctx.fill();

  if (!total) return;

  let start = -Math.PI / 2;
  for (let i = 0; i < values.length; i++) {
    const v = values[i];
    const ang = (v / total) * Math.PI * 2;

    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.arc(cx, cy, radius, start, start + ang);
    ctx.closePath();

    ctx.globalCompositeOperation = "source-over";
    ctx.fillStyle = colorForSentiment(labels[i]);
    ctx.fill();

    start += ang;
  }

  // Punch hole
  ctx.globalCompositeOperation = "destination-out";
  ctx.beginPath();
  ctx.arc(cx, cy, inner, 0, Math.PI * 2);
  ctx.closePath();
  ctx.fill();

  ctx.globalCompositeOperation = "source-over";

  // Center text
  ctx.fillStyle = isLightTheme() ? "#111827" : "#e5e7eb";
  ctx.font = "800 18px system-ui, -apple-system, Segoe UI, sans-serif";
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.fillText(`${total}`, cx, cy - 8);

  ctx.fillStyle = isLightTheme() ? "#4b5563" : "#9ca3af";
  ctx.font = "600 12px system-ui, -apple-system, Segoe UI, sans-serif";
  ctx.fillText("análisis", cx, cy + 12);
}

/**
 * Dibuja un gráfico de línea (tendencias temporales).
 * 
 * @param {HTMLCanvasElement} canvas - Elemento canvas
 * @param {Array<number>} points - Valores Y
 * @param {Array<string>} labels - Etiquetas X
 * @param {number|null} yMax - Valor máximo del eje Y (null = auto)
 */
function drawLine(canvas, points, labels, yMax = null) {
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  const w = (canvas.width = canvas.clientWidth);
  const h = (canvas.height = canvas.height || 260);

  ctx.clearRect(0, 0, w, h);

  const pad = 26;
  const max = yMax != null ? yMax : Math.max(1, ...points);
  const min = 0;

  // Grid
  ctx.strokeStyle = isLightTheme() ? "rgba(17,24,39,.10)" : "rgba(229,231,235,.10)";
  ctx.lineWidth = 1;
  for (let i = 0; i < 4; i++) {
    const y = pad + (i * (h - pad * 2)) / 3;
    ctx.beginPath();
    ctx.moveTo(pad, y);
    ctx.lineTo(w - pad, y);
    ctx.stroke();
  }

  const stepX = (w - pad * 2) / Math.max(1, points.length - 1);

  // Line
  ctx.strokeStyle = isLightTheme() ? "#2563eb" : "#6366f1";
  ctx.lineWidth = 2.25;
  ctx.beginPath();
  for (let i = 0; i < points.length; i++) {
    const x = pad + i * stepX;
    const y = h - pad - ((points[i] - min) / (max - min)) * (h - pad * 2);
    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  }
  ctx.stroke();

  // Dots
  ctx.fillStyle = isLightTheme() ? "#2563eb" : "#6366f1";
  for (let i = 0; i < points.length; i++) {
    const x = pad + i * stepX;
    const y = h - pad - ((points[i] - min) / (max - min)) * (h - pad * 2);
    ctx.beginPath();
    ctx.arc(x, y, 3.5, 0, Math.PI * 2);
    ctx.fill();
  }

  // X labels
  ctx.fillStyle = isLightTheme() ? "#4b5563" : "#9ca3af";
  ctx.font = "600 11px system-ui, -apple-system, Segoe UI, sans-serif";
  ctx.textAlign = "center";
  ctx.textBaseline = "top";
  for (let i = 0; i < labels.length; i++) {
    const x = pad + i * stepX;
    ctx.fillText(labels[i], x, h - pad + 6);
  }
}

/**
 * Dibuja un gráfico de barras.
 * 
 * @param {HTMLCanvasElement} canvas - Elemento canvas
 * @param {Array<Object>} items - Items con {label, value}
 */
function drawBars(canvas, items) {
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  const w = (canvas.width = canvas.clientWidth);
  const h = (canvas.height = canvas.height || 260);

  ctx.clearRect(0, 0, w, h);

  const pad = 26;
  const max = Math.max(1, ...items.map((x) => x.value));
  const barW = ((w - pad * 2) / Math.max(1, items.length)) * 0.72;
  const gap = ((w - pad * 2) / Math.max(1, items.length)) * 0.28;

  // Grid
  ctx.strokeStyle = isLightTheme() ? "rgba(17,24,39,.10)" : "rgba(229,231,235,.10)";
  ctx.lineWidth = 1;
  for (let i = 0; i < 4; i++) {
    const y = pad + (i * (h - pad * 2)) / 3;
    ctx.beginPath();
    ctx.moveTo(pad, y);
    ctx.lineTo(w - pad, y);
    ctx.stroke();
  }

  for (let i = 0; i < items.length; i++) {
    const x0 = pad + i * (barW + gap) + gap * 0.5;
    const val = items[i].value;
    const bh = (val / max) * (h - pad * 2);
    const y0 = h - pad - bh;

    ctx.fillStyle = isLightTheme() ? "rgba(37,99,235,.55)" : "rgba(99,102,241,.55)";
    ctx.strokeStyle = isLightTheme() ? "rgba(37,99,235,.90)" : "rgba(99,102,241,.90)";
    ctx.lineWidth = 1;

    roundRect(ctx, x0, y0, barW, bh, 10);
    ctx.fill();
    ctx.stroke();

    ctx.fillStyle = isLightTheme() ? "#4b5563" : "#9ca3af";
    ctx.font = "600 11px system-ui, -apple-system, Segoe UI, sans-serif";
    ctx.textAlign = "center";
    ctx.textBaseline = "top";
    ctx.fillText(items[i].label, x0 + barW / 2, h - pad + 6);
  }
}

/* ============================================================================
 * 7) DASHBOARD (dashboard.html) — Consumo real del Backend
 * ============================================================================
 */

/**
 * Normaliza el payload del dashboard del Backend a formato interno.
 * 
 * El Backend puede devolver datos en diferentes formatos, esta función
 * los normaliza a un formato estándar para el FE.
 * 
 * @param {Object} raw - Payload crudo del Backend
 * @returns {Object} Datos normalizados
 */
function normalizeDashboardPayload(raw) {
  const r = raw && typeof raw === "object" ? raw : {};

  // KPIs
  const total =
    Number(r.total ?? r.total_analisis ?? r.totalAnalisis ?? r.kpis?.total) || 0;
  const pos =
    Number(r.positivo ?? r.pos ?? r.kpis?.positivo ?? r.kpis?.pos) || 0;
  const neg =
    Number(r.negativo ?? r.neg ?? r.kpis?.negativo ?? r.kpis?.neg) || 0;
  const neu =
    Number(r.neutro ?? r.neu ?? r.kpis?.neutro ?? r.kpis?.neutral) || 0;
  const probAvg = clamp01(
    r.prob_avg ?? r.probAvg ?? r.kpis?.prob_avg ?? r.kpis?.probAvg ?? 0
  );
  const last7d = Number(r.last7d ?? r.ultimos_7_dias ?? r.kpis?.last7d) || 0;

  // Distribución
  const dist = r.distribution || r.distribucion || r.sentiment_distribution || {};
  const distPos = Number(dist.positivo ?? dist.pos ?? dist.positive) || pos;
  const distNeg = Number(dist.negativo ?? dist.neg ?? dist.negative) || neg;
  const distNeu = Number(dist.neutro ?? dist.neu ?? dist.neutral) || neu;

  // Tendencias
  const trendsRaw =
    safeArray(r.trends7d || r.trends || r.serie_7d || r.last7days || []);
  const trends7d = trendsRaw.slice(0, 7).map((x) => {
    const obj = x && typeof x === "object" ? x : {};
    const label =
      String(
        obj.label ??
          obj.day ??
          obj.fecha ??
          obj.date ??
          obj.x ??
          ""
      ) || "";
    const value = Number(obj.value ?? obj.count ?? obj.total ?? obj.y ?? 0) || 0;
    return { label, value };
  });

  // Top departamentos
  const topRaw =
    safeArray(r.topDepartments || r.top_departments || r.departamentos || []);
  const topDepartments = topRaw.slice(0, 6).map((x) => {
    const obj = x && typeof x === "object" ? x : {};
    const full = String(obj.full ?? obj.departamento ?? obj.name ?? obj.label ?? "General");
    const value = Number(obj.value ?? obj.count ?? obj.total ?? 0) || 0;
    return {
      full,
      label: full.length > 10 ? full.slice(0, 10) + "…" : full,
      value,
    };
  });

  // Recientes
  const recentRaw =
    safeArray(r.recent || r.recientes || r.latest || r.history || []);
  const recent = recentRaw.slice(0, 10).map((x) => {
    const obj = x && typeof x === "object" ? x : {};
    const ts = Number(obj.ts ?? obj.timestamp ?? obj.fecha_ts ?? obj.created_at ?? 0) || 0;
    const sentiment = toSentimentLower(obj.sentiment ?? obj.previsibilidad ?? obj.prevision ?? obj.label);
    const prob = clamp01(obj.prob ?? obj.probabilidad ?? obj.score ?? 0);
    const departamentos = safeArray(obj.departamentos ?? obj.depts ?? obj.departments);
    const hallazgos = safeArray(obj.hallazgos ?? obj.findings ?? obj.insights);
    return { ts, sentiment, prob, departamentos, hallazgos };
  });

  // Si el BE manda "kpis" como objeto:
  const k = r.kpis && typeof r.kpis === "object" ? r.kpis : null;
  const kTotal = Number(k?.total ?? 0) || total;
  const kPos = Number(k?.positivo ?? k?.pos ?? 0) || pos;
  const kNeg = Number(k?.negativo ?? k?.neg ?? 0) || neg;
  const kNeu = Number(k?.neutro ?? k?.neu ?? k?.neutral ?? 0) || neu;
  const kProbAvg = clamp01(k?.prob_avg ?? k?.probAvg ?? probAvg);
  const kLast7d = Number(k?.last7d ?? k?.ultimos_7_dias ?? 0) || last7d;

  return {
    kpis: {
      total: kTotal,
      pos: kPos,
      neg: kNeg,
      neu: kNeu,
      probAvg: kProbAvg,
      last7d: kLast7d,
    },
    distribution: {
      positivo: distPos,
      negativo: distNeg,
      neutro: distNeu,
    },
    trends7d,
    topDepartments,
    recent,
  };
}

/**
 * Carga datos del dashboard desde el Backend.
 * 
 * ESTRATEGIA:
 * 1. Intenta usar el endpoint agregado /dashboard (ideal para MVP)
 * 2. Si no existe (404), usa endpoints granulares y los compone
 * 
 * @returns {Promise<Object>} Datos normalizados del dashboard
 */
async function loadDashboardFromBE() {
  // Intento 1: endpoint agregado
  try {
    const all = await fetchJSON(ENDPOINTS.DASHBOARD_ALL);
    return normalizeDashboardPayload(all);
  } catch (e) {
    const status = e && typeof e === "object" ? e.status : null;
    if (status !== 404) {
      // Si es otro error, lo propagamos
      throw e;
    }
  }

  // Intento 2: endpoints granulares (fallback)
  const [kpis, distribution, trends7d, topDepartments, recent] = await Promise.all([
    fetchJSON(ENDPOINTS.DASHBOARD_KPIS).catch(() => ({})),
    fetchJSON(ENDPOINTS.DASHBOARD_DISTRIBUTION).catch(() => ({})),
    fetchJSON(ENDPOINTS.DASHBOARD_TRENDS_7D).catch(() => []),
    fetchJSON(ENDPOINTS.DASHBOARD_TOP_DEPTS).catch(() => []),
    fetchJSON(ENDPOINTS.DASHBOARD_RECENT).catch(() => []),
  ]);

  return normalizeDashboardPayload({
    kpis,
    distribution,
    trends7d,
    topDepartments,
    recent,
  });
}

/**
 * Actualiza el estado visual del dashboard (loading/error/ok).
 * 
 * @param {Object} options - Opciones
 * @param {boolean} options.loading - Si está cargando
 * @param {string|null} options.error - Mensaje de error (null si no hay error)
 */
function setDashboardStatus({ loading = false, error = null } = {}) {
  const badge = document.getElementById("biStatusBadge");
  if (!badge) return;

  if (loading) {
    badge.className = "bi-status loading";
    badge.textContent = "Cargando datos del Backend…";
    return;
  }
  if (error) {
    badge.className = "bi-status error";
    badge.textContent = `Error: ${error}`;
    return;
  }
  badge.className = "bi-status ok";
  badge.textContent = "Datos actualizados";
}

/**
 * Renderiza los datos del dashboard en la UI.
 * 
 * @param {Object} data - Datos normalizados del dashboard
 */
function renderDashboardData(data) {
  const root = document.getElementById("biRoot");
  if (!root) return;

  const k = data.kpis;

  // KPIs
  setText("kpiTotal", String(k.total || 0));
  setText("kpiTotalSub", k.total ? "Datos desde Backend" : "Sin datos");

  setText("kpiPos", String(k.pos || 0));
  setText("kpiNeg", String(k.neg || 0));
  setText("kpiNeu", String(k.neu || 0));

  const totalAll = (k.pos || 0) + (k.neg || 0) + (k.neu || 0);
  const pct = (n) => (totalAll ? `${Math.round((n / totalAll) * 100)}%` : "—");
  setText("kpiPosSub", `Participación: ${pct(k.pos || 0)}`);
  setText("kpiNegSub", `Participación: ${pct(k.neg || 0)}`);
  setText("kpiNeuSub", `Participación: ${pct(k.neu || 0)}`);

  setText("kpiProb", Number(k.probAvg || 0).toFixed(2));
  setText("kpiProbSub", totalAll ? "Promedio global" : "—");

  setText("kpi7d", String(k.last7d || 0));
  setText("kpi7dSub", "Conteo últimos 7 días");

  // Donut: distribución
  const donut = document.getElementById("chartDonut");
  drawDonut(
    donut,
    [data.distribution.positivo || 0, data.distribution.negativo || 0, data.distribution.neutro || 0],
    ["positivo", "negativo", "neutro"]
  );

  const legend = document.getElementById("legendDonut");
  if (legend) {
    legend.innerHTML = `
      <span class="item" style="color:${colorForSentiment("positivo")}"><span class="dot"></span> Positivo</span>
      <span class="item" style="color:${colorForSentiment("negativo")}"><span class="dot"></span> Negativo</span>
      <span class="item" style="color:${colorForSentiment("neutro")}"><span class="dot"></span> Neutro</span>
    `;
  }

  // Línea: últimos 7 días
  const line = document.getElementById("chartLine");
  const points = (data.trends7d || []).map((x) => Number(x.value || 0));
  const labels = (data.trends7d || []).map((x) => String(x.label || ""));
  drawLine(
    line,
    points.length ? points : [0, 0, 0, 0, 0, 0, 0],
    labels.length ? labels : ["", "", "", "", "", "", ""]
  );

  // Barras: top departamentos
  const bars = document.getElementById("chartBars");
  const deptItems = (data.topDepartments || []).length
    ? data.topDepartments
    : [{ label: "General", value: 0, full: "General" }];
  drawBars(bars, deptItems);

  // Tabla: actividad reciente
  const tbody = document.getElementById("biTableBody");
  if (tbody) {
    const recent = safeArray(data.recent);

    if (!recent.length) {
      tbody.innerHTML = `<tr><td colspan="5" class="bi-empty">Sin actividad reciente reportada por el Backend.</td></tr>`;
    } else {
      tbody.innerHTML = recent
        .map((it) => {
          const s = toSentimentLower(it.sentiment || "neutro");
          const prob = Number(it.prob || 0).toFixed(2);

          const depts = safeArray(it.departamentos)
            .slice(0, 2)
            .map((d) => `<span class="bi-pill">${escapeHtml(d)}</span>`)
            .join(" ");

          const halls = safeArray(it.hallazgos)
            .slice(0, 2)
            .map((h) => `<span class="bi-pill">${escapeHtml(h)}</span>`)
            .join(" ");

          const badgeColor = colorForSentiment(s);
          const badge = `<span class="bi-pill" style="color:${badgeColor}">${escapeHtml(s)}</span>`;

          return `
            <tr>
              <td>${escapeHtml(formatDateShort(it.ts || Date.now()))}</td>
              <td>${badge}</td>
              <td>${escapeHtml(prob)}</td>
              <td>${depts || `<span class="bi-pill">General</span>`}</td>
              <td>${halls || `<span class="bi-pill">Sin hallazgos</span>`}</td>
            </tr>
          `;
        })
        .join("");
    }
  }
}

/**
 * Orquestador del Dashboard: carga datos y renderiza.
 */
async function renderDashboard() {
  const root = document.getElementById("biRoot");
  if (!root) return;

  setDashboardStatus({ loading: true });

  try {
    const data = await loadDashboardFromBE();
    renderDashboardData(data);
    setDashboardStatus({ loading: false, error: null });
  } catch (e) {
    const msg =
      (e && e.message) ||
      "No fue posible obtener datos del Backend (revisa CORS / URL / endpoint)";
    setDashboardStatus({ loading: false, error: msg });
    console.error("[Dashboard] Error:", e);
  }
}

/**
 * Configura la página del dashboard.
 */
function setupDashboardBI() {
  const root = document.getElementById("biRoot");
  if (!root) return;

  const refreshBtn = document.getElementById("biRefreshBtn");
  if (refreshBtn) {
    refreshBtn.addEventListener("click", () => renderDashboard());
  }

  // Re-render de canvas al redimensionar
  window.addEventListener("resize", () => {
    renderDashboard();
  });

  renderDashboard();
}

/* ============================================================================
 * 8) ESTADÍSTICAS (estadisticas.html) — Similar a docs.html pero enfocado
 * ============================================================================
 */

/**
 * Configura la página de estadísticas.
 * Por ahora, muestra información similar a docs.html pero enfocada en estadísticas.
 */
function setupStatisticsPage() {
  const root = document.getElementById("statsRoot");
  if (!root) return;

  // Esta página puede mostrar estadísticas detalladas en el futuro
  // Por ahora, se mantiene la estructura HTML existente
  console.log("[Statistics] Página de estadísticas cargada");
}

/* ============================================================================
 * 9) INICIALIZACIÓN GLOBAL
 * ============================================================================
 */

/**
 * Inicializa la aplicación cuando el DOM está listo.
 */
document.addEventListener("DOMContentLoaded", () => {
  // Configurar tema
  setupThemeFromOS();
  setupThemeToggleButton();

  // Configurar navegación
  ensureActiveNav();

  // Configurar páginas según la ruta actual
  const path = (window.location.pathname || "").toLowerCase();

  if (path.includes("index.html") || path === "/" || path.endsWith("/")) {
    setupSentimentPage();
  } else if (path.includes("dashboard")) {
  setupDashboardBI();
  } else if (path.includes("estadisticas")) {
    setupStatisticsPage();
  }

  console.log("[SentimentalIA] Front-End inicializado. Backend:", API_BASE_URL);
});
