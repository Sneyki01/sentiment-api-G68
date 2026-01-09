import requests
import json

url = 'http://localhost:8080/predict/sentiment'
# Texto "Diluido": Muchas palabras genéricas positivas (absolutamente, totalmente, increiblemente, realmente)
# vs Palabras clave del hotel (cama, ruido)
data = {
    "text": "Fue una experiencia absolutamente increiblemente realmente totalmente buena, aunque la cama dura y mucho ruido."
}

try:
    response = requests.post(url, json=data)
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
except Exception as e:
    print(f"Error: {e}")
