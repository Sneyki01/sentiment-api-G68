import requests
url = "http://localhost:8080/predict/sentiment"
data = {"text": "%&$/Cucarachas en la camacc¡?=)(/%"}
response = requests.post(url, json=data)
print(response.json())
