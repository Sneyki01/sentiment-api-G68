import requests
import json

url = 'http://localhost:8080/predict/sentiment'
data = {
    "text": "Una experiencia absolutamente impecable; desde la calidez del personal en recepción hasta la calidad de las sábanas, se nota que cuidan cada pequeño detalle. Es de esos lugares de los que te vas planeando cuándo vas a volver antes siquiera de haber hecho el check-out."
}

try:
    response = requests.post(url, json=data)
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
except Exception as e:
    print(f"Error: {e}")
