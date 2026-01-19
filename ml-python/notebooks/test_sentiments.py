import requests, json
url = 'http://localhost:8080/sentiment'
phrases = [
    "El hotel fue excelente, la vista al mar era impresionante.",
    "La habitación tenía una fuga en el techo y el agua goteaba toda la noche.",
    "El personal fue amable pero la limpieza dejó mucho que desear.",
    "Me encantó el spa, pero el wifi no funcionó en todo el día.",
    "¡Maravilloso! El techo gotea justo encima de la cama, una experiencia de spa gratuito.",
    "El restaurante ofrecía platos deliciosos, aunque el servicio fue lento.",
    "El ruido de la calle impedía dormir, pero la piscina estaba perfecta.",
    "Hubo filtración en el baño que arruinó mi ropa, aunque la ubicación era buena.",
    "El precio fue razonable y la habitación cómoda, sin problemas mayores.",
    "La habitación estaba sucia y había cucarachas, una experiencia terrible."
]
for i, txt in enumerate(phrases, 1):
    resp = requests.post(url, json={'text': txt})
    try:
        data = resp.json()
    except Exception as e:
        data = {'error': str(e)}
    print(f"{i}. Text: {txt}\n   Response: {json.dumps(data, ensure_ascii=False)}\n")
