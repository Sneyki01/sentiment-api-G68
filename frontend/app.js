function analyze() {
  const text = document.getElementById("textInput").value.trim();
  const result = document.getElementById("result");

  // Validación de longitud: 3 a 2000 caracteres
  if (text.length < 3) {
    alert("El texto debe tener al menos 3 caracteres.");
    return;
  }
  if (text.length > 2000) {
    alert("El texto no puede superar los 2000 caracteres.");
    return;
  }


  // Mostrar mensaje mientras espera la respuesta
  result.className = "";
  result.classList.remove("hidden");
  result.classList.remove("positive", "negative", "neutral");
  result.innerHTML = "Analizando sentimiento...";

  fetch("http://localhost:8000/sentiment", {
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
      // Limpiar clases previas
      result.classList.remove("positive", "negative", "neutral");

      if (data.prevision === "Positivo") {
        result.classList.add("positive");
      } else if (data.prevision === "Negativo") {
        result.classList.add("negative");
      } else {
        result.classList.add("neutral");
      }

      result.innerHTML = `
        <strong>Sentimiento:</strong> ${data.prevision}<br>
        <strong>Probabilidad:</strong> ${data.probabilidad.toFixed(2)}
      `;
    })
    .catch(error => {
      console.error(error);
      result.classList.remove("positive", "negative", "neutral");
      result.classList.add("neutral");
      result.innerHTML = "Ocurrió un error al comunicarse con el backend.";
    });
} //function analyze
