import requests
import json

url = 'http://localhost:8080/sentiment'
cases = [
    "La comida estaba riquísima, volveremos seguro.",
    "El hotel cuenta con wifi gratuito en todas las áreas.",
    "Un desastre, nunca me devolvieron el dinero del depósito.",
    "No está mal, pero podría mejorar la limpieza."
]

for text in cases:
    print(f"\nProbando: {text}")
    response = requests.post(url, json={"text": text})
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
