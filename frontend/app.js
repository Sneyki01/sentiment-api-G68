function analyze() {
  const text = document.getElementById("textInput").value;
  const result = document.getElementById("result");

  if (!text || text.length < 5) {
    alert("El texto debe tener al menos 5 caracteres");
    return;
  }

  // MOCK de respuesta (se reemplaza por fetch mañana)
  const response = {
    prevision: "Positivo",
    probabilidad: 0.87
  };

  result.className = "";
  result.classList.remove("hidden");

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
