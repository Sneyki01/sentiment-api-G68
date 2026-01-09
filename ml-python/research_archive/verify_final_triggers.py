import requests
url = "http://localhost:8080/predict/sentiment"

test_cases = [
    "muy buena habitacion",
    "la habitacion es muy limpia",
    "personal super atento",
    "comida extremadamente mala",
    "sin wifi",
    "habitacion no muy limpia"
]

for text in test_cases:
    print(f"Testing: {text}")
    response = requests.post(url, json={"text": text})
    print(f"Triggers: {response.json()['explicabilidad']['triggers']}")
    print("-" * 30)
