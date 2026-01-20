// =====================
// Configuración de APIs (compatibilidad)
// =====================

const API_ENDPOINTS = {
  DEV_BACKEND: "http://localhost:8000/sentiment",
  MODEL_LINEAR: "http://159.112.150.158:8080/predict",
  MODEL_BILSTM: "http://149.130.183.97:8080/predict",
};

let ACTIVE_API = API_ENDPOINTS.DEV_BACKEND;
let hasFirstMessageSent = false;

// =====================
// MOCK TOTAL
// =====================

const MOCK_ONLY = true;
const MOCK_LATENCY_MS = 650;
const MOCK_METHOD = "C68 Híbrido";

// Rangos de probabilidad por clase
const MOCK_PROB_RANGES = {
  positivo: [0.62, 0.93],
  negativo: [0.62, 0.93],
  neutro: [0.55, 0.85],
};

function clamp01(n) {
  const x = Number(n);
  if (!Number.isFinite(x)) return 0;
  return Math.max(0, Math.min(1, x));
}

function randBetween(min, max) {
  const a = Number(min);
  const b = Number(max);
  return a + Math.random() * (b - a);
}

function inferSentimentFromText(text) {
  const t = String(text || "").toLowerCase();

  const positiveWords = [
    "excelente",
    "increíble",
    "me encantó",
    "genial",
    "perfecto",
    "recomiendo",
    "gracias",
    "buen",
    "buena",
    "maravill",
  ];

  const negativeWords = [
    "horrible",
    "pésimo",
    "pesimo",
    "odio",
    "molesto",
    "ruido",
    "nunca",
    "mal",
    "queja",
    "terrible",
    "decepcion",
    "asqueros",
    "fatal",
  ];

  let score = 0;
  for (const w of positiveWords) if (t.includes(w)) score += 1;
  for (const w of negativeWords) if (t.includes(w)) score -= 1;

  // sarcasmo demo
  const sarcasm =
    t.includes("increíble") &&
    (t.includes("obra") || t.includes("martill") || t.includes("ruido"));
  if (sarcasm) score -= 2;

  if (score >= 1) return "positivo";
  if (score <= -1) return "negativo";
  return "neutro";
}

function buildMockResponseFromText(originalText) {
  const sentiment = inferSentimentFromText(originalText);

  const [pmin, pmax] = MOCK_PROB_RANGES[sentiment] || [0.55, 0.85];
  const prob = clamp01(randBetween(pmin, pmax));

  const texto_limpio = String(originalText || "").trim();

  const hallazgos = [];
  const t = texto_limpio.toLowerCase();

  if (t.includes("obra") || t.includes("martill") || t.includes("ruido"))
    hallazgos.push("Posible queja por ruido/obras");
  if (t.includes("servicio") || t.includes("atención") || t.includes("atencion"))
    hallazgos.push("Menciona servicio/atención");
  if (
    t.includes("precio") ||
    t.includes("caro") ||
    t.includes("barato") ||
    t.includes("costo")
  )
    hallazgos.push("Menciona precio/costo");
  if (hallazgos.length === 0) hallazgos.push("Sin hallazgos");

  const departamentos = [];
  if (t.includes("ruido") || t.includes("obra") || t.includes("martill"))
    departamentos.push("Mantenimiento");
  if (t.includes("servicio") || t.includes("atención") || t.includes("atencion"))
    departamentos.push("Atención al cliente");
  if (t.includes("precio") || t.includes("costo")) departamentos.push("Comercial");
  if (departamentos.length === 0) departamentos.push("General");

  return {
    previsibilidad:
      sentiment === "positivo"
        ? "Positivo"
        : sentiment === "negativo"
        ? "Negativo"
        : "Neutro",
    probabilidad: prob,
    explicabilidad: { texto_limpio, hallazgos, departamentos },
    metodo: MOCK_METHOD,
  };
}

// =====================
// Tema: OS + toggle manual persistente
// =====================

const THEME_STORAGE_KEY = "sentimental_theme_preference"; // "light" | "dark"
let mqTheme = null;

function getSavedTheme() {
  try {
    const v = localStorage.getItem(THEME_STORAGE_KEY);
    if (v === "light" || v === "dark") return v;
  } catch (e) {}
  return null;
}

function saveTheme(value) {
  try {
    localStorage.setItem(THEME_STORAGE_KEY, value);
  } catch (e) {}
}

function applyTheme(mode) {
  document.body.classList.remove("theme-light", "theme-dark");
  if (mode === "light") document.body.classList.add("theme-light");
  else document.body.classList.add("theme-dark");
  updateThemeToggleUI();
}

function applyThemeFromOS() {
  const prefersDark = mqTheme ? mqTheme.matches : true;
  applyTheme(prefersDark ? "dark" : "light");
}

function updateThemeToggleUI() {
  const btn = document.getElementById("themeToggle");
  if (!btn) return;

  const isLight = document.body.classList.contains("theme-light");
  btn.textContent = isLight ? "☾" : "☀";
  btn.title = isLight ? "Cambiar a tema oscuro" : "Cambiar a tema claro";
  btn.setAttribute("aria-label", btn.title);
}

function setupThemeFromOS() {
  mqTheme = window.matchMedia("(prefers-color-scheme: dark)");

  const saved = getSavedTheme();
  if (saved) applyTheme(saved);
  else applyThemeFromOS();

  const onOSChange = () => {
    const savedNow = getSavedTheme();
    if (!savedNow) applyThemeFromOS();
    else updateThemeToggleUI();
  };

  if (typeof mqTheme.addEventListener === "function")
    mqTheme.addEventListener("change", onOSChange);
  else if (typeof mqTheme.addListener === "function") mqTheme.addListener(onOSChange);
}

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

// =====================
// Totales (compatibilidad)
// =====================

const STATS_STORAGE_KEY = "sentimental_stats_totals_v1"; // {positive, negative, neutral}
let sentimentTotals = { positive: 0, negative: 0, neutral: 0 };

function loadTotals() {
  try {
    const raw = localStorage.getItem(STATS_STORAGE_KEY);
    if (!raw) return;
    const obj = JSON.parse(raw);
    if (obj && typeof obj === "object") {
      sentimentTotals = {
        positive: Number(obj.positive) || 0,
        negative: Number(obj.negative) || 0,
        neutral: Number(obj.neutral) || 0,
      };
    }
  } catch (e) {}
}

function saveTotals() {
  try {
    localStorage.setItem(STATS_STORAGE_KEY, JSON.stringify(sentimentTotals));
  } catch (e) {}
}

function bumpTotals(previsionLower) {
  if (previsionLower === "positivo") sentimentTotals.positive += 1;
  else if (previsionLower === "negativo") sentimentTotals.negative += 1;
  else sentimentTotals.neutral += 1;
  saveTotals();
}

// =====================
// NUEVO: historial de análisis (Dashboard/Estadísticas)
// =====================

const HISTORY_STORAGE_KEY = "sentimental_history_v1";
// cada item (v2):
// {
//   ts, sentiment, prob, metodo, departamentos[], hallazgos[], textLen, apiKey,
//   text, source, category, keywords[]
// }
function loadHistory() {
  try {
    const raw = localStorage.getItem(HISTORY_STORAGE_KEY);
    if (!raw) return [];
    const arr = JSON.parse(raw);
    return Array.isArray(arr) ? arr : [];
  } catch (e) {
    return [];
  }
}

function saveHistory(arr) {
  try {
    localStorage.setItem(HISTORY_STORAGE_KEY, JSON.stringify(arr));
  } catch (e) {}
}

function pushHistoryItem(item) {
  const arr = loadHistory();
  arr.push(item);
  const MAX = 300;
  const sliced = arr.length > MAX ? arr.slice(arr.length - MAX) : arr;
  saveHistory(sliced);
}

function toSentimentLower(previsibilidad) {
  const p = String(previsibilidad || "").trim().toLowerCase();
  if (p.includes("posit")) return "positivo";
  if (p.includes("negat")) return "negativo";
  return "neutro";
}

function formatDateShort(ts) {
  const d = new Date(ts);
  const yyyy = d.getFullYear();
  const mm = String(d.getMonth() + 1).padStart(2, "0");
  const dd = String(d.getDate()).padStart(2, "0");
  const hh = String(d.getHours()).padStart(2, "0");
  const mi = String(d.getMinutes()).padStart(2, "0");
  return `${yyyy}-${mm}-${dd} ${hh}:${mi}`;
}

// =====================
// Enriquecimiento: Categoría + Keywords
// =====================

const CATEGORY_LABELS = [
  "usabilidad",
  "funcionalidad",
  "precios",
  "soporte",
  "confiabilidad",
  "general",
];

function inferCategoryFromText(text) {
  const t = String(text || "").toLowerCase();

  const rules = [
    { cat: "soporte", hits: ["soporte", "atención", "atencion", "ticket", "ayuda", "call center"] },
    { cat: "precios", hits: ["precio", "caro", "barato", "costo", "tarifa", "cobro", "factura"] },
    { cat: "usabilidad", hits: ["interfaz", "botón", "boton", "difícil", "dificil", "confuso", "navegar", "menú", "menu", "ux"] },
    { cat: "funcionalidad", hits: ["funciona", "error", "bug", "falla", "no carga", "crash", "lento", "performance", "rendimiento"] },
    { cat: "confiabilidad", hits: ["cae", "caído", "caido", "intermitente", "seguro", "seguridad", "estable", "inestable", "confiable"] },
  ];

  for (const r of rules) {
    if (r.hits.some((w) => t.includes(w))) return r.cat;
  }
  return "general";
}

function normalizeSpanishWord(w) {
  return String(w || "")
    .toLowerCase()
    .trim()
    .replace(/[^\p{L}\p{N}]+/gu, ""); // letras/números unicode
}

const STOPWORDS_ES = new Set([
  "de","la","que","el","en","y","a","los","del","se","las","por","un","para","con","no","una","su","al","lo",
  "como","más","mas","pero","sus","le","ya","o","este","sí","si","porque","esta","entre","cuando","muy","sin",
  "sobre","también","tambien","me","hasta","hay","donde","quien","desde","todo","nos","durante","todos","uno",
  "les","ni","contra","otros","ese","eso","ante","ellos","e","esto","mí","mi","mis","tu","tus","te","yo","tú",
  "usted","ustedes","ustd","ustds","siempre","nunca","es","son","fue","eran","ser","estar","está","esta","estan",
  "están","muy","tan","un","una","unas","unos","the","and","to","of","in"
]);

function extractKeywords(text, max = 14) {
  const t = String(text || "").toLowerCase();
  const raw = t.split(/\s+/g).map(normalizeSpanishWord).filter(Boolean);

  const freq = new Map();
  for (const w of raw) {
    if (w.length < 4) continue;
    if (STOPWORDS_ES.has(w)) continue;
    freq.set(w, (freq.get(w) || 0) + 1);
  }

  return Array.from(freq.entries())
    .sort((a, b) => b[1] - a[1])
    .slice(0, max)
    .map(([k]) => k);
}

// =====================
// Modal: detalles (se queda)
// =====================

let lastModelDetails = null;

function escapeHtml(str) {
  return String(str ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function ensureDetailsModal() {
  if (document.getElementById("modelDetailsModal")) return;

  const style = document.createElement("style");
  style.id = "modelDetailsModalStyles";
  style.textContent = `
    .mdm-overlay{ position:fixed; inset:0; background: rgba(2,6,23,.72); backdrop-filter: blur(10px);
      display:none; align-items:center; justify-content:center; z-index:9999; padding: 1.25rem; }
    .mdm-overlay.open{ display:flex; }
    .mdm-modal{ width: min(860px, 96vw); max-height: min(78vh, 760px); overflow:auto;
      border-radius: 18px; border: 1px solid var(--border-subtle); background: rgba(2,6,23,.92);
      color: var(--text-primary); box-shadow: 0 22px 65px rgba(0,0,0,.55); padding: 1.05rem 1.05rem 1rem; }
    body.theme-light .mdm-modal{ background: rgba(255,255,255,.92); box-shadow: 0 18px 55px rgba(148,163,184,.35); }
    .mdm-header{ display:flex; align-items:flex-start; justify-content:space-between; gap: 0.75rem;
      padding-bottom: .75rem; border-bottom: 1px solid var(--border-subtle); margin-bottom: .85rem; }
    .mdm-title{ font-size: 1.05rem; font-weight: 700; letter-spacing: .01em; margin:0; }
    .mdm-sub{ margin:.25rem 0 0; font-size:.9rem; color: var(--text-secondary); }
    .mdm-close{ width: 38px; height: 38px; border-radius: 999px; border: 1px solid var(--border-subtle);
      background: var(--bg-surface-alt); color: var(--text-primary); cursor:pointer; display:inline-flex;
      align-items:center; justify-content:center; font-size: 1.15rem; transition: transform .1s ease-out, box-shadow .12s ease-out, border-color .15s ease-out; }
    .mdm-close:hover{ transform: translateY(-1px); border-color: var(--accent); box-shadow: 0 12px 24px rgba(37,99,235,.25); }
    .mdm-grid{ display:grid; grid-template-columns: 1fr 1fr; gap: .75rem; margin-bottom: .9rem; }
    @media (max-width: 720px){ .mdm-grid{ grid-template-columns: 1fr; } }
    .mdm-card{ border-radius: 14px; border: 1px solid var(--border-subtle); background: rgba(3,7,18,.55); padding: .75rem .8rem; }
    body.theme-light .mdm-card{ background: rgba(243,244,246,.75); }
    .mdm-k{ font-size:.78rem; color: var(--text-secondary); margin-bottom: .25rem; letter-spacing:.02em; text-transform: uppercase; }
    .mdm-v{ font-size: .98rem; line-height: 1.45; white-space: pre-wrap; word-break: break-word; }
    .mdm-list{ margin: .35rem 0 0; padding-left: 1.05rem; color: var(--text-primary); line-height:1.5; }
    .mdm-stats{ display:flex; gap: .5rem; flex-wrap: wrap; margin-top: .35rem; }
    .mdm-pill{ display:inline-flex; align-items:center; gap:.4rem; padding: .35rem .65rem; border-radius: 999px;
      border: 1px solid var(--border-subtle); background: rgba(15,23,42,.55); font-size: .85rem; color: var(--text-primary); }
    body.theme-light .mdm-pill{ background: rgba(255,255,255,.75); }
    .mdm-dot{ width: 9px; height: 9px; border-radius: 999px; background: currentColor; opacity: .85; }
  `;
  document.head.appendChild(style);

  const overlay = document.createElement("div");
  overlay.id = "modelDetailsModal";
  overlay.className = "mdm-overlay";
  overlay.setAttribute("role", "dialog");
  overlay.setAttribute("aria-modal", "true");
  overlay.setAttribute("aria-label", "Más detalles del modelo");

  overlay.innerHTML = `
    <div class="mdm-modal">
      <div class="mdm-header">
        <div>
          <h3 class="mdm-title">Más detalles del modelo</h3>
          <p class="mdm-sub">Explicabilidad y estadística acumulada del demo</p>
        </div>
        <button type="button" class="mdm-close" aria-label="Cerrar">×</button>
      </div>
      <div id="mdmBody"></div>
    </div>
  `;

  document.body.appendChild(overlay);

  overlay.querySelector(".mdm-close").addEventListener("click", closeDetailsModal);
  overlay.addEventListener("click", (e) => {
    if (e.target === overlay) closeDetailsModal();
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      const ov = document.getElementById("modelDetailsModal");
      if (ov && ov.classList.contains("open")) closeDetailsModal();
    }
  });
}

function closeDetailsModal() {
  const overlay = document.getElementById("modelDetailsModal");
  if (overlay) overlay.classList.remove("open");
}

function normalizeModelDetails(data) {
  const rawPrev = (data.previsibilidad ?? data.prevision ?? "Neutro")
    .toString()
    .trim();
  const rawProb = data.probabilidad;

  const probabilidad =
    typeof rawProb === "number"
      ? rawProb
      : Number.parseFloat((rawProb ?? "0").toString());

  const exp =
    data.explicabilidad && typeof data.explicabilidad === "object"
      ? data.explicabilidad
      : {};
  const texto_limpio = exp.texto_limpio ?? exp.textoLimpio ?? "";
  const hallazgos = Array.isArray(exp.hallazgos) ? exp.hallazgos : [];
  const departamentos = Array.isArray(exp.departamentos) ? exp.departamentos : [];
  const metodo = (data.metodo ?? MOCK_METHOD).toString();

  return {
    previsibilidad: rawPrev,
    probabilidad: Number.isFinite(probabilidad) ? probabilidad : 0,
    explicabilidad: {
      texto_limpio: texto_limpio || "Sin texto limpio",
      hallazgos: hallazgos.length ? hallazgos : ["Sin hallazgos"],
      departamentos: departamentos.length ? departamentos : ["General"],
    },
    metodo,
  };
}

function openDetailsModal() {
  ensureDetailsModal();

  const overlay = document.getElementById("modelDetailsModal");
  const body = document.getElementById("mdmBody");

  if (!lastModelDetails) {
    body.innerHTML = `
      <div class="mdm-card">
        <div class="mdm-k">Estado</div>
        <div class="mdm-v">Aún no hay detalles del modelo. Envía un comentario primero.</div>
      </div>
    `;
    overlay.classList.add("open");
    return;
  }

  const d = lastModelDetails;

  body.innerHTML = `
    <div class="mdm-card" style="margin-bottom:.75rem;">
      <div class="mdm-k">Estadística acumulada (totales)</div>
      <div class="mdm-stats">
        <span class="mdm-pill" style="color: var(--success);"><span class="mdm-dot"></span> Positivos: ${sentimentTotals.positive}</span>
        <span class="mdm-pill" style="color: var(--danger);"><span class="mdm-dot"></span> Negativos: ${sentimentTotals.negative}</span>
        <span class="mdm-pill" style="color: var(--text-secondary);"><span class="mdm-dot"></span> Neutros: ${sentimentTotals.neutral}</span>
      </div>
    </div>

    <div class="mdm-grid">
      <div class="mdm-card"><div class="mdm-k">Previsibilidad</div><div class="mdm-v">${escapeHtml(
        d.previsibilidad
      )}</div></div>
      <div class="mdm-card"><div class="mdm-k">Probabilidad</div><div class="mdm-v">${Number(
        d.probabilidad || 0
      ).toFixed(2)}</div></div>
      <div class="mdm-card"><div class="mdm-k">Método</div><div class="mdm-v">${escapeHtml(
        d.metodo
      )}</div></div>
      <div class="mdm-card"><div class="mdm-k">Texto limpio</div><div class="mdm-v">${escapeHtml(
        d.explicabilidad.texto_limpio
      )}</div></div>
    </div>

    <div class="mdm-card">
      <div class="mdm-k">Hallazgos</div>
      <ul class="mdm-list">
        ${d.explicabilidad.hallazgos
          .map((h) => `<li>${escapeHtml(String(h))}</li>`)
          .join("")}
      </ul>
    </div>

    <div class="mdm-card" style="margin-top:.75rem;">
      <div class="mdm-k">Departamentos</div>
      <ul class="mdm-list">
        ${d.explicabilidad.departamentos
          .map((x) => `<li>${escapeHtml(String(x))}</li>`)
          .join("")}
      </ul>
    </div>
  `;

  overlay.classList.add("open");
}

// =====================
// UI helpers (Index)
// =====================

function autoResize(textarea) {
  if (!textarea) return;
  textarea.style.height = "auto";
  textarea.style.height = Math.min(textarea.scrollHeight, 260) + "px";
}

function updateInputIcons() {
  const textarea = document.getElementById("textInput");
  const clearBtn = document.getElementById("clearButton");
  const sendBtn = document.getElementById("sendButton");

  if (!textarea) return;

  const hasText = textarea.value.trim().length > 0;
  const isValidLength = textarea.value.trim().length >= 3;

  if (clearBtn) clearBtn.classList.toggle("hidden", !hasText);

  if (sendBtn) {
    sendBtn.classList.toggle("hidden", !hasText);
    sendBtn.disabled = !isValidLength;
  }
}

function enterChatModeOnce() {
  if (hasFirstMessageSent) return;
  hasFirstMessageSent = true;

  const hero = document.querySelector(".hero");
  if (hero && !hero.classList.contains("hidden")) hero.classList.add("hidden");

  document.body.classList.add("chat-mode");
}

function showInputAndModel() {
  const inputArea = document.querySelector(".input-area");
  const apiSelector = document.querySelector(".api-selector");

  if (inputArea) inputArea.classList.remove("hidden");
  if (apiSelector) apiSelector.classList.remove("hidden");

  const mainTextarea = document.getElementById("textInput");
  if (mainTextarea) {
    mainTextarea.value = "";
    autoResize(mainTextarea);
    updateInputIcons();
    mainTextarea.focus();
  }
}

// =====================
// Core: analyze() (Index)
// =====================

function analyze() {
  const textarea = document.getElementById("textInput");
  const history = document.getElementById("history");
  const btnSend = document.getElementById("sendButton");
  const apiSelect = document.getElementById("apiSelect");

  if (!textarea) return; // si estás en dashboard u otra página
  const text = textarea.value.trim();

  if (text.length < 3) {
    alert("el texto debe tener al menos 3 caracteres.");
    return;
  }
  if (text.length > 2000) {
    alert("el texto no puede superar los 2000 caracteres.");
    return;
  }

  enterChatModeOnce();
  if (history) history.innerHTML = "";

  const item = document.createElement("div");
  item.className = "history-item";

  const userBlock = document.createElement("div");
  userBlock.className = "history-user";

  const userBubble = document.createElement("div");
  userBubble.className = "history-user-bubble";
  userBubble.textContent = text;
  userBlock.appendChild(userBubble);

  const responseWrapper = document.createElement("div");
  responseWrapper.className = "history-response";

  const resultDiv = document.createElement("div");
  resultDiv.className = "result loading";
  resultDiv.innerHTML = `
    <div class="skeleton-line"></div>
    <div class="skeleton-line"></div>
  `;

  const actionsDiv = document.createElement("div");
  actionsDiv.className = "result-actions";

  const moreBtn = document.createElement("button");
  moreBtn.type = "button";
  moreBtn.className = "action-btn more-details";
  moreBtn.innerHTML = `<span class="action-icon-circle"><span>•••</span></span>`;
  moreBtn.addEventListener("click", () => openDetailsModal());

  const shareBtn = document.createElement("button");
  shareBtn.type = "button";
  shareBtn.className = "action-btn";
  shareBtn.innerHTML = `<span class="action-icon-circle"><span>⤴</span></span>`;
  shareBtn.addEventListener("click", () =>
    alert("funcionalidad de compartir (en desarrollo).")
  );

  const likeBtn = document.createElement("button");
  likeBtn.type = "button";
  likeBtn.className = "action-btn";
  likeBtn.innerHTML = `<span class="action-icon-circle"><span class="icon-heart-like">♥</span></span>`;
  likeBtn.addEventListener("click", () =>
    alert("feedback positivo registrado (en desarrollo).")
  );

  const dislikeBtn = document.createElement("button");
  dislikeBtn.type = "button";
  dislikeBtn.className = "action-btn";
  dislikeBtn.innerHTML = `<span class="action-icon-circle"><span class="icon-heart-dislike">♥</span></span>`;
  dislikeBtn.addEventListener("click", () =>
    alert("feedback negativo registrado (en desarrollo).")
  );

  actionsDiv.appendChild(moreBtn);
  actionsDiv.appendChild(shareBtn);
  actionsDiv.appendChild(likeBtn);
  actionsDiv.appendChild(dislikeBtn);

  const newCommentBtn = document.createElement("button");
  newCommentBtn.type = "button";
  newCommentBtn.className = "action-btn new-comment-btn";
  newCommentBtn.title = "Nuevo sentimiento";
  newCommentBtn.innerHTML = `<span class="action-icon-circle"><span class="icon-new-comment">⟳</span></span>`;
  newCommentBtn.addEventListener("click", () => showInputAndModel());

  const actionsRow = document.createElement("div");
  actionsRow.className = "result-actions-row";
  actionsRow.appendChild(actionsDiv);
  actionsRow.appendChild(newCommentBtn);

  responseWrapper.appendChild(resultDiv);
  responseWrapper.appendChild(actionsRow);

  item.appendChild(userBlock);
  item.appendChild(responseWrapper);

  if (history) history.appendChild(item);

  // Limpieza input
  textarea.value = "";
  autoResize(textarea);
  updateInputIcons();

  if (btnSend) {
    btnSend.disabled = true;
    btnSend.classList.add("loading");
  }

  // Ocultar input/modelo activo tras enviar
  const inputArea = document.querySelector(".input-area");
  const apiSelector = document.querySelector(".api-selector");
  if (inputArea) inputArea.classList.add("hidden");
  if (apiSelector) apiSelector.classList.add("hidden");

  const apiKey = apiSelect ? apiSelect.value : "DEV_BACKEND";

  window.setTimeout(() => {
    const mock = buildMockResponseFromText(text);

    resultDiv.classList.remove("loading", "positive", "negative", "neutral");

    const previsionNorm = toSentimentLower(mock.previsibilidad);
    const probNum = clamp01(mock.probabilidad);

    if (previsionNorm === "positivo") resultDiv.classList.add("positive");
    else if (previsionNorm === "negativo") resultDiv.classList.add("negative");
    else resultDiv.classList.add("neutral");

    resultDiv.innerHTML = `
      <div>
        <span class="sentiment-label">previsibilidad:</span>
        <span class="sentiment-value">${previsionNorm}</span>
      </div>
      <div class="probability">probabilidad: ${probNum.toFixed(2)}</div>
    `;

    lastModelDetails = normalizeModelDetails(mock);

    bumpTotals(previsionNorm);

    // NUEVO: guardar en historial enriquecido para Dashboard/Estadísticas
    const exp = mock.explicabilidad || {};
    const category = inferCategoryFromText(text);
    const keywords = extractKeywords(text, 14);

    pushHistoryItem({
      ts: Date.now(),
      sentiment: previsionNorm,
      prob: probNum,
      metodo: String(mock.metodo || MOCK_METHOD),
      departamentos: Array.isArray(exp.departamentos) ? exp.departamentos : ["General"],
      hallazgos: Array.isArray(exp.hallazgos) ? exp.hallazgos : ["Sin hallazgos"],
      textLen: String(text).length,
      apiKey,

      // campos nuevos
      text: String(text),
      source: "web", // listo para "csv" cuando cargues archivo
      category,
      keywords,
    });

    // Si el usuario está en estadísticas o dashboard, refresca al vuelo
    try {
      renderDashboard();
      renderStatsPage();
    } catch (e) {}

    if (btnSend) {
      btnSend.disabled = false;
      btnSend.classList.remove("loading");
    }
  }, MOCK_LATENCY_MS);
}

// =====================
// Setup Index-only (con guardas)
// =====================

function setupApiSelector() {
  const apiSelect = document.getElementById("apiSelect");
  if (!apiSelect) return;

  apiSelect.value = "DEV_BACKEND";
  ACTIVE_API = API_ENDPOINTS.DEV_BACKEND;

  apiSelect.addEventListener("change", (e) => {
    const key = e.target.value;
    if (API_ENDPOINTS[key]) {
      ACTIVE_API = API_ENDPOINTS[key];
    }
  });
}

function setupInputInteractions() {
  const textarea = document.getElementById("textInput");
  const clearBtn = document.getElementById("clearButton");
  const sendBtn = document.getElementById("sendButton");
  const langSelect = document.getElementById("langSelect");

  if (!textarea) return;

  textarea.addEventListener("input", () => {
    autoResize(textarea);
    updateInputIcons();
  });

  autoResize(textarea);
  updateInputIcons();

  textarea.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      if (event.shiftKey) return;
      event.preventDefault();
      analyze();
    }
  });

  if (clearBtn) {
    clearBtn.addEventListener("click", () => {
      textarea.value = "";
      autoResize(textarea);
      textarea.focus();
      updateInputIcons();
    });
  }

  if (sendBtn) sendBtn.addEventListener("click", () => analyze());

  if (langSelect) {
    const updateLangTitle = () => {
      const val = langSelect.value;
      langSelect.title = val === "pt" ? "português" : "español";
    };
    langSelect.addEventListener("change", updateLangTitle);
    updateLangTitle();
  }
}

// =====================
// BI Dashboard (dashboard.html)
// =====================

function isLightTheme() {
  return document.body.classList.contains("theme-light");
}

function colorForSentiment(sent) {
  if (sent === "positivo") return isLightTheme() ? "#16a34a" : "#4ade80";
  if (sent === "negativo") return isLightTheme() ? "#b91c1c" : "#f97373";
  return isLightTheme() ? "#6b7280" : "#9ca3af";
}

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

  // base ring
  ctx.beginPath();
  ctx.arc(cx, cy, radius, 0, Math.PI * 2);
  ctx.arc(cx, cy, inner, 0, Math.PI * 2, true);
  ctx.closePath();
  ctx.fillStyle = isLightTheme()
    ? "rgba(17,24,39,.06)"
    : "rgba(229,231,235,.06)";
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

  // punch hole
  ctx.globalCompositeOperation = "destination-out";
  ctx.beginPath();
  ctx.arc(cx, cy, inner, 0, Math.PI * 2);
  ctx.closePath();
  ctx.fill();

  ctx.globalCompositeOperation = "source-over";

  // center text
  ctx.fillStyle = isLightTheme() ? "#111827" : "#e5e7eb";
  ctx.font = "800 18px system-ui, -apple-system, Segoe UI, sans-serif";
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.fillText(`${total}`, cx, cy - 8);

  ctx.fillStyle = isLightTheme() ? "#4b5563" : "#9ca3af";
  ctx.font = "600 12px system-ui, -apple-system, Segoe UI, sans-serif";
  ctx.fillText("análisis", cx, cy + 12);
}

function drawLine(canvas, points, labels, yMax = null) {
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  const w = (canvas.width = canvas.clientWidth);
  const h = (canvas.height = canvas.height || 260);

  ctx.clearRect(0, 0, w, h);

  const pad = 26;
  const max = yMax != null ? yMax : Math.max(1, ...points);
  const min = 0;

  // grid
  ctx.strokeStyle = isLightTheme()
    ? "rgba(17,24,39,.10)"
    : "rgba(229,231,235,.10)";
  ctx.lineWidth = 1;
  for (let i = 0; i < 4; i++) {
    const y = pad + (i * (h - pad * 2)) / 3;
    ctx.beginPath();
    ctx.moveTo(pad, y);
    ctx.lineTo(w - pad, y);
    ctx.stroke();
  }

  const stepX = (w - pad * 2) / Math.max(1, points.length - 1);

  // line
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

  // dots
  ctx.fillStyle = isLightTheme() ? "#2563eb" : "#6366f1";
  for (let i = 0; i < points.length; i++) {
    const x = pad + i * stepX;
    const y = h - pad - ((points[i] - min) / (max - min)) * (h - pad * 2);
    ctx.beginPath();
    ctx.arc(x, y, 3.5, 0, Math.PI * 2);
    ctx.fill();
  }

  // x labels
  ctx.fillStyle = isLightTheme() ? "#4b5563" : "#9ca3af";
  ctx.font = "600 11px system-ui, -apple-system, Segoe UI, sans-serif";
  ctx.textAlign = "center";
  ctx.textBaseline = "top";
  for (let i = 0; i < labels.length; i++) {
    const x = pad + i * stepX;
    ctx.fillText(labels[i], x, h - pad + 6);
  }
}

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

  // grid
  ctx.strokeStyle = isLightTheme()
    ? "rgba(17,24,39,.10)"
    : "rgba(229,231,235,.10)";
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

    ctx.fillStyle = isLightTheme()
      ? "rgba(37,99,235,.55)"
      : "rgba(99,102,241,.55)";
    ctx.strokeStyle = isLightTheme()
      ? "rgba(37,99,235,.90)"
      : "rgba(99,102,241,.90)";
    ctx.lineWidth = 1;

    const r = 10;
    roundRect(ctx, x0, y0, barW, bh, r);
    ctx.fill();
    ctx.stroke();

    ctx.fillStyle = isLightTheme() ? "#4b5563" : "#9ca3af";
    ctx.font = "600 11px system-ui, -apple-system, Segoe UI, sans-serif";
    ctx.textAlign = "center";
    ctx.textBaseline = "top";
    ctx.fillText(items[i].label, x0 + barW / 2, h - pad + 6);
  }
}

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

function computeDashboardData() {
  const history = loadHistory();

  const totals = { positivo: 0, negativo: 0, neutro: 0 };
  let probSum = 0;
  const deptCounts = new Map();

  // last 7 days
  const now = Date.now();
  const dayMs = 24 * 60 * 60 * 1000;
  const days = [];
  for (let i = 6; i >= 0; i--) {
    const d = new Date(now - i * dayMs);
    const key = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(
      2,
      "0"
    )}-${String(d.getDate()).padStart(2, "0")}`;
    days.push({
      key,
      label: `${String(d.getDate()).padStart(2, "0")}/${String(
        d.getMonth() + 1
      ).padStart(2, "0")}`,
      value: 0,
    });
  }
  const dayIndex = new Map(days.map((d, i) => [d.key, i]));

  for (const it of history) {
    const s = it.sentiment || "neutro";
    if (s === "positivo") totals.positivo += 1;
    else if (s === "negativo") totals.negativo += 1;
    else totals.neutro += 1;

    probSum += Number(it.prob || 0);

    const depts = Array.isArray(it.departamentos) ? it.departamentos : [];
    for (const d of depts) {
      const k = String(d || "General");
      deptCounts.set(k, (deptCounts.get(k) || 0) + 1);
    }

    const d = new Date(Number(it.ts || 0));
    if (!Number.isFinite(d.getTime())) continue;
    const key = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(
      2,
      "0"
    )}-${String(d.getDate()).padStart(2, "0")}`;
    if (dayIndex.has(key)) {
      days[dayIndex.get(key)].value += 1;
    }
  }

  const totalAll = totals.positivo + totals.negativo + totals.neutro;
  const probAvg = totalAll ? probSum / totalAll : 0;
  const last7d = days.reduce((a, b) => a + b.value, 0);

  const topDepts = Array.from(deptCounts.entries())
    .sort((a, b) => b[1] - a[1])
    .slice(0, 6)
    .map(([label, value]) => ({
      label: label.length > 10 ? label.slice(0, 10) + "…" : label,
      value,
      full: label,
    }));

  return { history, totals, totalAll, probAvg, last7d, days, topDepts };
}

function setText(id, value) {
  const el = document.getElementById(id);
  if (el) el.textContent = value;
}

function renderDashboard() {
  const root = document.getElementById("biRoot");
  if (!root) return; // no estás en dashboard.html

  const data = computeDashboardData();

  setText("kpiTotal", String(data.totalAll));
  setText("kpiTotalSub", data.totalAll ? "Historial local (demo)" : "Sin datos aún");

  setText("kpiPos", String(data.totals.positivo));
  setText("kpiNeg", String(data.totals.negativo));
  setText("kpiNeu", String(data.totals.neutro));

  const pct = (n) => (data.totalAll ? `${Math.round((n / data.totalAll) * 100)}%` : "—");
  setText("kpiPosSub", `Participación: ${pct(data.totals.positivo)}`);
  setText("kpiNegSub", `Participación: ${pct(data.totals.negativo)}`);
  setText("kpiNeuSub", `Participación: ${pct(data.totals.neutro)}`);

  setText("kpiProb", data.probAvg.toFixed(2));
  setText("kpiProbSub", data.totalAll ? "Promedio global" : "—");

  setText("kpi7d", String(data.last7d));
  setText("kpi7dSub", "Conteo últimos 7 días");

  const donut = document.getElementById("chartDonut");
  drawDonut(donut, [data.totals.positivo, data.totals.negativo, data.totals.neutro], [
    "positivo",
    "negativo",
    "neutro",
  ]);

  const legend = document.getElementById("legendDonut");
  if (legend) {
    legend.innerHTML = `
      <span class="item" style="color:${colorForSentiment("positivo")}"><span class="dot"></span> Positivo</span>
      <span class="item" style="color:${colorForSentiment("negativo")}"><span class="dot"></span> Negativo</span>
      <span class="item" style="color:${colorForSentiment("neutro")}"><span class="dot"></span> Neutro</span>
    `;
  }

  const line = document.getElementById("chartLine");
  drawLine(line, data.days.map((d) => d.value), data.days.map((d) => d.label));

  const bars = document.getElementById("chartBars");
  drawBars(bars, data.topDepts.length ? data.topDepts : [{ label: "General", value: 1 }]);

  const tbody = document.getElementById("biTableBody");
  if (tbody) {
    const recent = [...data.history].sort((a, b) => (b.ts || 0) - (a.ts || 0)).slice(0, 10);

    if (!recent.length) {
      tbody.innerHTML = `<tr><td colspan="5" class="bi-empty">Aún no hay datos. Ejecuta análisis desde Inicio.</td></tr>`;
    } else {
      tbody.innerHTML = recent
        .map((it) => {
          const s = it.sentiment || "neutro";
          const prob = Number(it.prob || 0).toFixed(2);
          const depts = (it.departamentos || [])
            .slice(0, 2)
            .map((d) => `<span class="bi-pill">${escapeHtml(d)}</span>`)
            .join(" ");
          const halls = (it.hallazgos || [])
            .slice(0, 2)
            .map((h) => `<span class="bi-pill">${escapeHtml(h)}</span>`)
            .join(" ");

          const badgeColor = colorForSentiment(s);
          const badge = `<span class="bi-pill" style="color:${badgeColor}">${escapeHtml(
            s
          )}</span>`;

          return `
          <tr>
            <td>${escapeHtml(formatDateShort(it.ts))}</td>
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

function setupDashboardBI() {
  const root = document.getElementById("biRoot");
  if (!root) return;

  const refreshBtn = document.getElementById("biRefreshBtn");
  const resetBtn = document.getElementById("biResetBtn");

  if (refreshBtn) refreshBtn.addEventListener("click", () => renderDashboard());

  if (resetBtn) {
    resetBtn.addEventListener("click", () => {
      const ok = confirm("¿Deseas borrar los datos del demo (historial y totales) en este navegador?");
      if (!ok) return;
      try {
        localStorage.removeItem(HISTORY_STORAGE_KEY);
        localStorage.removeItem(STATS_STORAGE_KEY);
      } catch (e) {}
      loadTotals();
      renderDashboard();
      renderStatsPage();
    });
  }

  window.addEventListener("resize", () => renderDashboard());
  renderDashboard();
}

// =====================
// ESTADISTICAS (estadisticas.html)
// =====================

function monthKey(ts) {
  const d = new Date(ts);
  if (!Number.isFinite(d.getTime())) return null;
  const yyyy = d.getFullYear();
  const mm = String(d.getMonth() + 1).padStart(2, "0");
  return `${yyyy}-${mm}`;
}

function monthLabelFromKey(key) {
  // key: YYYY-MM
  const [y, m] = String(key).split("-");
  const mm = Number(m);
  const names = ["ene","feb","mar","abr","may","jun","jul","ago","sep","oct","nov","dic"];
  const name = names[Math.max(1, Math.min(12, mm)) - 1] || "mes";
  return `${name} ${y}`;
}

function computeStatsData() {
  const history = loadHistory().slice().sort((a, b) => (b.ts || 0) - (a.ts || 0));

  const totals = { positivo: 0, negativo: 0, neutro: 0 };
  const catCounts = new Map(); // distribución por categoría (0-100)
  const catSent = new Map(); // por categoría: {pos, neu, neg}
  const kwCounts = new Map(); // nube palabras

  // Over time: por mes: ratio positivo (0-100)
  const byMonth = new Map(); // key -> {pos, neg, neu, total}
  const now = new Date();
  const monthsWanted = 6; // últimos 6 meses

  // init últimos N meses para que se vea siempre el eje
  for (let i = monthsWanted - 1; i >= 0; i--) {
    const d = new Date(now.getFullYear(), now.getMonth() - i, 1);
    const key = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}`;
    byMonth.set(key, { pos: 0, neg: 0, neu: 0, total: 0 });
  }

  for (const it of history) {
    const s = it.sentiment || "neutro";
    if (s === "positivo") totals.positivo += 1;
    else if (s === "negativo") totals.negativo += 1;
    else totals.neutro += 1;

    const cat = (it.category || "general").toLowerCase();
    catCounts.set(cat, (catCounts.get(cat) || 0) + 1);

    if (!catSent.has(cat)) catSent.set(cat, { pos: 0, neg: 0, neu: 0, total: 0 });
    const cs = catSent.get(cat);
    cs.total += 1;
    if (s === "positivo") cs.pos += 1;
    else if (s === "negativo") cs.neg += 1;
    else cs.neu += 1;

    const mkey = monthKey(it.ts);
    if (mkey && byMonth.has(mkey)) {
      const bm = byMonth.get(mkey);
      bm.total += 1;
      if (s === "positivo") bm.pos += 1;
      else if (s === "negativo") bm.neg += 1;
      else bm.neu += 1;
    }

    const kws = Array.isArray(it.keywords) ? it.keywords : [];
    for (const k of kws) kwCounts.set(k, (kwCounts.get(k) || 0) + 1);
  }

  const totalAll = totals.positivo + totals.negativo + totals.neutro;

  // Barras categorías: porcentaje (distribución) 0-100
  const categories = CATEGORY_LABELS.slice();
  for (const c of Array.from(catCounts.keys())) if (!categories.includes(c)) categories.push(c);

  const catBars = categories.map((c) => {
    const n = catCounts.get(c) || 0;
    const pct = totalAll ? Math.round((n / totalAll) * 100) : 0;
    return { category: c, count: n, pct };
  });

  // Time series (0-100%): ratio positivo sobre total por mes
  const monthKeys = Array.from(byMonth.keys());
  const timeLabels = monthKeys.map(monthLabelFromKey);
  const timeValues = monthKeys.map((k) => {
    const m = byMonth.get(k);
    if (!m || !m.total) return 0;
    return Math.round((m.pos / m.total) * 100);
  });

  // Sentiment by category (stacked 0-100)
  const catStack = categories.map((c) => {
    const cs = catSent.get(c) || { pos: 0, neg: 0, neu: 0, total: 0 };
    const t = cs.total || 0;
    const pos = t ? Math.round((cs.pos / t) * 100) : 0;
    const neu = t ? Math.round((cs.neu / t) * 100) : 0;
    const neg = t ? Math.round((cs.neg / t) * 100) : 0;
    return { category: c, pos, neu, neg, total: t };
  });

  const keywords = Array.from(kwCounts.entries())
    .sort((a, b) => b[1] - a[1])
    .slice(0, 24)
    .map(([k, n]) => ({ k, n }));

  return { history, totals, totalAll, catBars, timeLabels, timeValues, catStack, keywords };
}

function setInnerHTML(id, html) {
  const el = document.getElementById(id);
  if (el) el.innerHTML = html;
}

function ensureActiveNav() {
  const links = document.querySelectorAll(".nav-link");
  if (!links || !links.length) return;

  const path = (window.location.pathname || "").toLowerCase();
  links.forEach((a) => a.classList.remove("active"));

  let active = null;
  if (path.includes("dashboard")) active = "dashboard";
  else if (path.includes("estadisticas")) active = "estadisticas";
  else if (path.includes("docs")) active = "docs";
  else if (path.includes("recursos")) active = "recursos";
  else active = "inicio";

  links.forEach((a) => {
    const v = (a.getAttribute("data-nav") || "").toLowerCase();
    if (v === active) a.classList.add("active");
  });
}

// Render: Historial (izquierda)
function renderStatsHistory(listId, items) {
  const el = document.getElementById(listId);
  if (!el) return;

  if (!items.length) {
    el.innerHTML = `<div class="bi-empty" style="padding:1rem;">Aún no hay historial. Ejecuta análisis desde Inicio.</div>`;
    return;
  }

  const recent = items.slice(0, 40);
  el.innerHTML = recent
    .map((it) => {
      const text = String(it.text || "").trim() || "(sin texto)";
      const date = formatDateShort(it.ts);
      const source = (it.source || "web").toLowerCase() === "csv" ? "csv" : "web";
      const category = (it.category || "general").toLowerCase();
      const sentiment = (it.sentiment || "neutro").toLowerCase();

      return `
        <div class="stats-item">
          <p class="stats-item-text">${escapeHtml(text)}</p>
          <div class="stats-meta">
            <span class="stats-badge stats-badge-date">${escapeHtml(date)}</span>
            <span class="stats-badge stats-badge-source ${source}">${source === "csv" ? "Archivo CSV" : "Web"}</span>
            <span class="stats-badge stats-badge-category">${escapeHtml(category)}</span>
            <span class="stats-badge stats-badge-sentiment ${escapeHtml(sentiment)}">${escapeHtml(sentiment)}</span>
          </div>
        </div>
      `;
    })
    .join("");
}

// Render: Barras categorías (0-100)
function renderCategoryBars(containerId, catBars) {
  const el = document.getElementById(containerId);
  if (!el) return;

  if (!catBars.length) {
    el.innerHTML = `<div class="bi-empty" style="padding:1rem;">Sin categorías aún.</div>`;
    return;
  }

  el.innerHTML = `
    <div class="stats-bars">
      ${catBars
        .sort((a, b) => b.pct - a.pct)
        .map(
          (c) => `
        <div class="stats-bar-row">
          <div class="stats-bar-label">${escapeHtml(c.category)}</div>
          <div class="stats-bar-track"><div class="stats-bar-fill" style="width:${c.pct}%;"></div></div>
          <div class="stats-bar-value">${c.pct}%</div>
        </div>
      `
        )
        .join("")}
    </div>
  `;
}

// Dibujo: barras horizontales apiladas (pos/neu/neg) 0-100 por categoría
function drawStackedHorizontal(canvas, rows) {
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  const w = (canvas.width = canvas.clientWidth);
  const rowH = 36;
  const padX = 22;
  const padY = 18;
  const h = (canvas.height = padY * 2 + rows.length * rowH);

  ctx.clearRect(0, 0, w, h);

  const labelW = Math.min(220, Math.max(140, Math.floor(w * 0.28)));
  const barX = padX + labelW;
  const barW = w - barX - padX;

  ctx.font = "700 12px system-ui, -apple-system, Segoe UI, sans-serif";
  ctx.textBaseline = "middle";

  // grid 0/50/100
  ctx.strokeStyle = isLightTheme()
    ? "rgba(17,24,39,.10)"
    : "rgba(229,231,235,.10)";
  ctx.lineWidth = 1;
  [0, 50, 100].forEach((p) => {
    const x = barX + (p / 100) * barW;
    ctx.beginPath();
    ctx.moveTo(x, padY - 4);
    ctx.lineTo(x, h - padY + 4);
    ctx.stroke();
  });

  for (let i = 0; i < rows.length; i++) {
    const y = padY + i * rowH + rowH / 2;

    // label
    ctx.fillStyle = isLightTheme() ? "#111827" : "#e5e7eb";
    const label = rows[i].label;
    ctx.fillText(label, padX, y);

    // track
    const trackY = y - 7;
    const trackH = 14;

    ctx.fillStyle = isLightTheme() ? "rgba(17,24,39,.06)" : "rgba(229,231,235,.06)";
    ctx.fillRect(barX, trackY, barW, trackH);

    // segments
    const posW = (rows[i].pos / 100) * barW;
    const neuW = (rows[i].neu / 100) * barW;
    const negW = (rows[i].neg / 100) * barW;

    let x = barX;

    ctx.fillStyle = colorForSentiment("positivo");
    ctx.fillRect(x, trackY, posW, trackH);
    x += posW;

    ctx.fillStyle = colorForSentiment("neutro");
    ctx.fillRect(x, trackY, neuW, trackH);
    x += neuW;

    ctx.fillStyle = colorForSentiment("negativo");
    ctx.fillRect(x, trackY, negW, trackH);

    // percent label end
    ctx.fillStyle = isLightTheme() ? "#4b5563" : "#9ca3af";
    ctx.font = "600 11px system-ui, -apple-system, Segoe UI, sans-serif";
    ctx.textAlign = "right";
    ctx.fillText("100%", barX + barW, y);
    ctx.textAlign = "left";
    ctx.font = "700 12px system-ui, -apple-system, Segoe UI, sans-serif";
  }
}

function renderKeywordsCloud(containerId, keywords) {
  const el = document.getElementById(containerId);
  if (!el) return;

  if (!keywords.length) {
    el.innerHTML = `<div class="bi-empty" style="padding:1rem;">Sin palabras clave aún.</div>`;
    return;
  }

  el.innerHTML = keywords
    .map(
      (x) => `
      <span class="keyword-chip">
        <span class="k">${escapeHtml(x.k)}</span>
        <span class="n">${escapeHtml(String(x.n))}</span>
      </span>
    `
    )
    .join(" ");
}

function downloadCSV(filename, rows) {
  const esc = (v) => {
    const s = String(v ?? "");
    if (/[",\n]/.test(s)) return `"${s.replaceAll('"', '""')}"`;
    return s;
  };

  const csv = rows.map((r) => r.map(esc).join(",")).join("\n");
  const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();

  setTimeout(() => URL.revokeObjectURL(url), 700);
}

async function shareText(payload) {
  const text = String(payload || "Sentimental IA");
  try {
    if (navigator.share) {
      await navigator.share({ title: "Sentimental IA", text });
      return true;
    }
  } catch (e) {}
  try {
    await navigator.clipboard.writeText(text);
    alert("Resumen copiado al portapapeles.");
    return true;
  } catch (e) {
    alert("No se pudo compartir automáticamente en este navegador.");
    return false;
  }
}

// Render principal de Estadísticas
function renderStatsPage() {
  const root = document.getElementById("statsRoot");
  if (!root) return;

  const data = computeStatsData();

  // 1) Historial izquierda
  renderStatsHistory("statsHistoryList", data.history);

  // 2) Barras por categoría (distribución)
  renderCategoryBars("statsCategoryBars", data.catBars);

  // 3) Sentimiento en el tiempo (0-100) + donut
  const line = document.getElementById("chartStatsLine");
  drawLine(line, data.timeValues, data.timeLabels, 100);

  const donut = document.getElementById("chartStatsDonut");
  drawDonut(donut, [data.totals.positivo, data.totals.negativo, data.totals.neutro], [
    "positivo",
    "negativo",
    "neutro",
  ]);

  const legend = document.getElementById("legendStatsDonut");
  if (legend) {
    legend.innerHTML = `
      <span class="item" style="color:${colorForSentiment("positivo")}"><span class="dot"></span> Positivo</span>
      <span class="item" style="color:${colorForSentiment("neutro")}"><span class="dot"></span> Neutro</span>
      <span class="item" style="color:${colorForSentiment("negativo")}"><span class="dot"></span> Negativo</span>
    `;
  }

  // 4) Sentimiento por categoría (stack 0-100)
  const stack = document.getElementById("chartStatsByCategory");
  if (stack) {
    const rows = data.catStack
      .filter((x) => x.total > 0)
      .slice(0, 10)
      .map((x) => ({
        label: x.category,
        pos: x.pos,
        neu: x.neu,
        neg: x.neg,
      }));

    if (!rows.length) {
      // si no hay canvas o no hay filas, mostramos texto en contenedor alterno si existe
      const alt = document.getElementById("statsByCategoryEmpty");
      if (alt) alt.classList.remove("hidden");
    } else {
      const alt = document.getElementById("statsByCategoryEmpty");
      if (alt) alt.classList.add("hidden");
      drawStackedHorizontal(stack, rows);
    }
  }

  // 5) Nube de palabras
  renderKeywordsCloud("statsKeywordsCloud", data.keywords);
}

function setupStatsPage() {
  const root = document.getElementById("statsRoot");
  if (!root) return;

  const clearBtn = document.getElementById("statsClearBtn");
  const exportBtn = document.getElementById("statsExportBtn");
  const shareBtn = document.getElementById("statsShareBtn");

  if (clearBtn) {
    clearBtn.addEventListener("click", () => {
      const ok = confirm("¿Deseas borrar todo el historial y totales en este navegador?");
      if (!ok) return;
      try {
        localStorage.removeItem(HISTORY_STORAGE_KEY);
        localStorage.removeItem(STATS_STORAGE_KEY);
      } catch (e) {}
      loadTotals();
      renderStatsPage();
      renderDashboard();
    });
  }

  if (exportBtn) {
    exportBtn.addEventListener("click", () => {
      const history = loadHistory();
      if (!history.length) {
        alert("No hay datos para exportar.");
        return;
      }

      const rows = [
        [
          "fecha",
          "sentimiento",
          "probabilidad",
          "categoria",
          "fuente",
          "modelo",
          "departamentos",
          "hallazgos",
          "texto",
        ],
      ];

      history
        .slice()
        .sort((a, b) => (a.ts || 0) - (b.ts || 0))
        .forEach((it) => {
          rows.push([
            formatDateShort(it.ts),
            it.sentiment || "",
            Number(it.prob || 0).toFixed(2),
            it.category || "general",
            it.source || "web",
            it.metodo || "",
            (it.departamentos || []).join("; "),
            (it.hallazgos || []).join("; "),
            (it.text || "").replace(/\s+/g, " ").trim(),
          ]);
        });

      downloadCSV("sentimental_estadisticas.csv", rows);
    });
  }

  if (shareBtn) {
    shareBtn.addEventListener("click", () => {
      const data = computeStatsData();
      const payload = `Sentimental IA – Estadísticas
Total: ${data.totalAll}
Positivo: ${data.totals.positivo}
Neutro: ${data.totals.neutro}
Negativo: ${data.totals.negativo}
Top categorías: ${data.catBars
        .slice()
        .sort((a, b) => b.pct - a.pct)
        .slice(0, 3)
        .map((x) => `${x.category} ${x.pct}%`)
        .join(" | ")}
`;
      shareText(payload);
    });
  }

  window.addEventListener("resize", () => renderStatsPage());
  renderStatsPage();
}

// =====================
// DOMContentLoaded
// =====================

document.addEventListener("DOMContentLoaded", () => {
  loadTotals();
  setupThemeFromOS();
  setupThemeToggleButton();

  ensureActiveNav();

  // Index-only setups (con guardas)
  setupInputInteractions();
  setupApiSelector();

  // Dashboard BI
  setupDashboardBI();

  // Estadísticas
  setupStatsPage();

  console.log("[SentimentalIA] MODO:", MOCK_ONLY ? "MOCK TOTAL (sin BE)" : "BE");
});



