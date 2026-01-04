// URL base de la API (entorno local)
const API_BASE_URL = "http://localhost:8000/sentiment";

/**
 * Lógica principal: llamar al backend para analizar el sentimiento
 */
function analyze() {
  const textarea = document.getElementById("textInput");
  const text = textarea.value.trim();
  const result = document.getElementById("result");
  const btnSend = document.getElementById("sendButton");

  // Validación de longitud: 3 a 2000 caracteres (aunque el botón aparece desde 1)
  if (text.length < 3) {
    alert("El texto debe tener al menos 3 caracteres.");
    return;
  }
  if (text.length > 2000) {
    alert("El texto no puede superar los 2000 caracteres.");
    return;
  }

  // Estado de carga: skeleton
  result.className = "result loading";
  result.classList.remove("positive", "negative", "neutral", "fade-in");
  result.classList.remove("hidden");

  result.innerHTML = `
    <div class="skeleton-line skeleton-title"></div>
    <div class="skeleton-line"></div>
    <div class="skeleton-line short"></div>
  `;

  if (btnSend) {
    btnSend.disabled = true;
    btnSend.classList.add("loading");
  }

  fetch(API_BASE_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ text: text })
  })
    .then(response => {
      if (!response.ok) {
        throw new Error("Error en la API de backend");
      }
      return response.json();
    })
    .then(data => {
      result.classList.remove("loading", "positive", "negative", "neutral");

      const prevision = data.prevision || "Neutro";
      const prob = typeof data.probabilidad === "number"
        ? data.probabilidad
        : 0.5;

      let badgeClass = "badge-neutral";
      if (prevision === "Positivo") {
        result.classList.add("positive");
        badgeClass = "badge-positive";
      } else if (prevision === "Negativo") {
        result.classList.add("negative");
        badgeClass = "badge-negative";
      } else {
        result.classList.add("neutral");
      }

      result.classList.add("fade-in");

      result.innerHTML = `
        <div style="margin-bottom: 0.35rem;">
          <strong>Sentimiento:</strong>
          <span class="badge ${badgeClass}">
            ${prevision.toUpperCase()}
          </span>
        </div>
        <div>
          <strong>Probabilidad:</strong> ${prob.toFixed(2)}
        </div>
      `;
    })
    .catch(error => {
      console.error(error);
      result.classList.remove("loading", "positive", "negative", "neutral");
      result.classList.add("neutral", "fade-in");
      result.innerHTML = "Ocurrió un error al comunicarse con el backend.";
    })
    .finally(() => {
      if (btnSend) {
        btnSend.disabled = false;
        btnSend.classList.remove("loading");
      }
    });
}

/* =========================
   Tema claro / oscuro
   ========================= */

function applyTheme(theme) {
  const root = document.documentElement;
  const btnToggle = document.getElementById("themeToggle");

  root.setAttribute("data-theme", theme);
  localStorage.setItem("sentimental-theme", theme);

  if (btnToggle) {
    btnToggle.textContent = theme === "dark" ? "☀️" : "🌙";
  }
}

function setupThemeToggle() {
  const btnToggle = document.getElementById("themeToggle");
  if (!btnToggle) return;

  const stored = localStorage.getItem("sentimental-theme");
  const initialTheme = stored === "dark" ? "dark" : "light";
  applyTheme(initialTheme);

  btnToggle.addEventListener("click", () => {
    const current = document.documentElement.getAttribute("data-theme") || "light";
    const next = current === "light" ? "dark" : "light";
    applyTheme(next);
  });
}

/* =========================
   Interacciones del input:
   - mostrar/ocultar X y ↑
   - limpiar
   ========================= */

function setupInputInteractions() {
  const textarea = document.getElementById("textInput");
  const clearBtn = document.getElementById("clearButton");
  const sendBtn = document.getElementById("sendButton");
  const attachBtn = document.getElementById("attachButton");

  if (!textarea) return;

  const updateIcons = () => {
    const hasText = textarea.value.trim().length > 0;
    if (clearBtn && sendBtn) {
      if (hasText) {
        clearBtn.classList.remove("hidden");
        sendBtn.classList.remove("hidden");
      } else {
        clearBtn.classList.add("hidden");
        sendBtn.classList.add("hidden");
      }
    }
  };

  textarea.addEventListener("input", updateIcons);
  updateIcons();

  if (clearBtn) {
    clearBtn.addEventListener("click", () => {
      textarea.value = "";
      textarea.focus();
      updateIcons();
    });
  }

  // Botón + (adjuntar) por ahora solo informativo
  if (attachBtn) {
    attachBtn.addEventListener("click", () => {
      alert("Función de adjuntar archivos/imágenes (provisional para futuras versiones).");
    });
  }
}

/* =========================
   Init
   ========================= */

document.addEventListener("DOMContentLoaded", () => {
  setupThemeToggle();
  setupInputInteractions();
});
