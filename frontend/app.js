function analyze() {
  const text = document.getElementById("textInput").value;
  const result = document.getElementById("result");

  if (!text || text.length < 1) {
    alert("El texto debe tener al menos 1 caracter");
    return;
  }

  // MOCK dinámico: cambiar resultado según contenido
  let response = { prevision: "Neutro", probabilidad: 0.5 };

  const lowerText = text.toLowerCase();
  if (lowerText.includes("amor") || lowerText.includes("cariño") || lowerText.includes("excelente")) {
    response = { prevision: "Positivo", probabilidad: 0.87 };
  } else if (lowerText.includes("odio") || lowerText.includes("terrible") || lowerText.includes("mal")) {
    response = { prevision: "Negativo", probabilidad: 0.92 };
  }

  // Mostrar resultado
  result.className = "";
  result.classList.remove("hidden");

  // Limpiar clases previas
  result.classList.remove("positive", "negative", "neutral");

  // Asignar clase según sentimiento
  if (response.prevision === "Positivo") {
    result.classList.add("positive");
  } else if (response.prevision === "Negativo") {
    result.classList.add("negative");
  } else {
    result.classList.add("neutral");
  }

  result.innerHTML = `
    <strong>Sentimiento:</strong> ${response.prevision}<br>
    <strong>Probabilidad:</strong> ${response.probabilidad}
  `;
}