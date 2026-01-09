import requests
url = "http://localhost:8080/predict/sentiment"

test_cases = [
    "el wifi no funciona y la habitacion no esta limpia",
    "no hay comida en el restaurante",
    "el personal no es atento"
]

for text in test_cases:
    print(f"Testing: {text}")
    response = requests.post(url, json={"text": text})
    print(f"Triggers: {response.json()['explicabilidad']['triggers']}")
    print("-" * 30)
