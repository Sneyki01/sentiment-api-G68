import os
import sys
import joblib

# Configurar rutas para importar el motor
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, "src"))

from engine.sentiment_engine import analizar_sentimiento_hibrido

# --- RESEÑAS REALES (ADAPTADAS) ---
real_reviews = [
    {
        "id": "1. Lujo (Cancún)",
        "text": "El lugar es una locura de bonito, las albercas impecables y la comida del restaurante italiano fue lo mejor del viaje. Pero, sinceramente, el servicio de concierge deja mucho que desear. Pedimos una reserva para cenar con tres días de antelación y nos dijeron que no había lugar, pero cuando pasamos por el restaurante estaba a la mitad. Sientes que si no das propina por adelantado no te mueven ni un dedo. Por el precio que pagas, el trato debería ser más parejo.",
        "expected": "Negativo / Mixto"
    },
    {
        "id": "2. Negocios (Madrid)",
        "text": "Habitación funcional y cama muy cómoda, típica de la cadena. Lo mejor es que está pegado a la estación y llegas a cualquier lado. Lo malo: el Wi-Fi en la planta 5 es inexistente. Tuve que bajarme al lobby a las 11 de la noche para poder enviar unos correos de trabajo porque en el cuarto no cargaba ni el Google. El buffet del desayuno está bien, pero el café es de máquina de polvos, bastante malo para ser un hotel en España.",
        "expected": "Neutro / Mixto"
    },
    {
        "id": "3. Económico (Medellín)",
        "text": "El ambiente es genial, conoces gente de todo el mundo en la terraza y las clases de salsa gratis son un detallazo. La ubicación en El Poblado es perfecta para salir de fiesta. Puntos negativos: La limpieza de los baños compartidos es muy regular, a veces faltaba papel y olía mal por la tarde. Además, mi cama crujía muchísimo cada vez que me movía y las cortinas de la litera estaban medio caídas. Si buscas lujo no es aquí, pero para parchar con amigos está 10/10.",
        "expected": "Positivo / Mixto"
    }
]

# Cargar Modelos
model = joblib.load(os.path.join(BASE_DIR, "data", "models", "sentiment_model.pkl"))
vectorizer = joblib.load(os.path.join(BASE_DIR, "data", "models", "tfidf_vectorizer.pkl"))

print(f"--- PRUEBA DE FUEGO: RESEÑAS REALES (MUNDO REAL) ---")
for item in real_reviews:
    res, prob, meta = analizar_sentimiento_hibrido(item['text'], model, vectorizer)
    print(f"\nID: {item['id']}")
    print(f"Predicción: {res} | Prob: {prob} | Score: {meta.get('score')}")
    print(f"Reseña: {item['text'][:120]}...")
print("\n--- FIN DEL TEST ---")
