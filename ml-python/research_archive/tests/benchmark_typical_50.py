import os
import sys
import joblib

# Configurar rutas para importar el motor
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, "src"))

from engine.sentiment_engine import analizar_sentimiento_hibrido

# --- DATASET DE 50 RESEÑAS TÍPICAS ---
typical_reviews = [
    # 🟢 Excelentes (20)
    {"text": "Una estancia inolvidable. El personal nos trató como a la realeza desde el primer minuto.", "expected": "Positivo"},
    {"text": "La limpieza es impecable. Podrías comer en el suelo de la habitación.", "expected": "Positivo"},
    {"text": "Las mejores vistas de la ciudad. El rooftop es simplemente espectacular.", "expected": "Positivo"},
    {"text": "Desayuno buffet muy variado y con productos locales de alta calidad.", "expected": "Positivo"},
    {"text": "Ubicación inmejorable, cerca de todos los puntos de interés pero sin ruido.", "expected": "Positivo"},
    {"text": "La cama era tan cómoda que no quería levantarme. Dormí como un bebé.", "expected": "Positivo"},
    {"text": "Detalles que marcan la diferencia: nos dejaron una nota de bienvenida y bombones.", "expected": "Positivo"},
    {"text": "El diseño del hotel es moderno y acogedor. Muy instagrameable.", "expected": "Positivo"},
    {"text": "Relación calidad-precio excelente. Superó todas mis expectativas.", "expected": "Positivo"},
    {"text": "Ideal para viajes de negocios. El wifi es ultra rápido y estable.", "expected": "Positivo"},
    {"text": "El spa es un oasis de paz en medio del caos de la ciudad.", "expected": "Positivo"},
    {"text": "Check-in y check-out rapidísimos. Muy eficiente todo el equipo.", "expected": "Positivo"},
    {"text": "Nos hicieron un upgrade de habitación sin pedirlo. ¡Gracias!", "expected": "Positivo"},
    {"text": "Piscina climatizada fantástica, perfecta para relajarse después de caminar.", "expected": "Positivo"},
    {"text": "El restaurante del hotel merece una estrella Michelin. Cena exquisita.", "expected": "Positivo"},
    {"text": "Todo el personal habla varios idiomas, lo cual facilitó mucho la comunicación.", "expected": "Positivo"},
    {"text": "Un hotel con alma. Se nota que cuidan cada pequeño detalle decorativo.", "expected": "Positivo"},
    {"text": "Silencioso, elegante y cómodo. Volveré sin duda en mi próximo viaje.", "expected": "Positivo"},
    {"text": "Perfecto para familias. Tienen actividades geniales para los niños.", "expected": "Positivo"},
    {"text": "Baño amplio con ducha de efecto lluvia. Un lujo total.", "expected": "Positivo"},

    # 🟡 Regulares (15)
    {"text": "Buen hotel, pero el desayuno es algo caro para lo que ofrece.", "expected": "Neutro"},
    {"text": "La habitación estaba limpia, aunque los muebles se ven un poco anticuados.", "expected": "Neutro"},
    {"text": "Bien ubicado, pero el ruido de la calle se filtraba un poco por las ventanas.", "expected": "Neutro"},
    {"text": "El personal es amable, pero el servicio en el bar fue un poco lento.", "expected": "Neutro"},
    {"text": "Habitación pequeña para dos personas, pero funcional para una noche.", "expected": "Neutro"},
    {"text": "Bonito hotel, pero el gimnasio es minúsculo y le faltan máquinas.", "expected": "Neutro"},
    {"text": "Todo bien, excepto que el aire acondicionado hacía un ruido extraño.", "expected": "Neutro"},
    {"text": "La ubicación es excelente, pero el parking del hotel es muy difícil de maniobrar.", "expected": "Neutro"},
    {"text": "Cama cómoda, pero las almohadas eran demasiado blandas para mi gusto.", "expected": "Neutro"},
    {"text": "Cumple con lo que promete, aunque no esperes lujos extra.", "expected": "Neutro"},
    {"text": "El wifi funcionaba bien en el lobby, pero la señal llegaba débil a la habitación.", "expected": "Neutro"},
    {"text": "Buen trato, aunque tardaron mucho en traernos las toallas que pedimos.", "expected": "Neutro"},
    {"text": "Moderno y limpio, pero el barrio de noche se siente un poco solitario.", "expected": "Neutro"},
    {"text": "El desayuno buffet es rico, pero reponen la comida muy lentamente.", "expected": "Neutro"},
    {"text": "Estancia correcta. Ni frío ni calor, un hotel estándar de cadena.", "expected": "Neutro"},

    # 🔴 Negativas (15)
    {"text": "Una decepción total. Las fotos de la web no tienen nada que ver con la realidad.", "expected": "Negativo"},
    {"text": "Había moho en las juntas de la ducha. Falta mucha higiene.", "expected": "Negativo"},
    {"text": "Imposible dormir. Paredes de papel y se oía todo lo de la habitación de al lado.", "expected": "Negativo"},
    {"text": "El recepcionista fue extremadamente grosero cuando pedimos ayuda con las maletas.", "expected": "Negativo"},
    {"text": "Nos cobraron suplementos que no estaban informados en la reserva.", "expected": "Negativo"},
    {"text": "Olor a tabaco rancio en una habitación que se suponía de no fumadores.", "expected": "Negativo"},
    {"text": "El aire acondicionado no funcionaba y hacía 30 grados. No nos dieron solución.", "expected": "Negativo"},
    {"text": "Encontré pelos en las sábanas al llegar. Tuvieron que cambiarnos de cuarto.", "expected": "Negativo"},
    {"text": "Desayuno pobre: pan duro y café de máquina quemado.", "expected": "Negativo"},
    {"text": "Ascensores estropeados. Tuvimos que subir cuatro pisos con maletas por la escalera.", "expected": "Negativo"},
    {"text": "Publicitan parking gratuito y al llegar nos dijeron que estaba lleno.", "expected": "Negativo"},
    {"text": "La zona es peligrosa. No me sentí seguro volviendo al hotel de noche.", "expected": "Negativo"},
    {"text": "Hicimos la reserva con meses de antelación y al llegar no la encontraban.", "expected": "Negativo"},
    {"text": "El agua de la ducha salía tibia tirando a fría. Una tortura en invierno.", "expected": "Negativo"},
    {"text": "No volvería ni aunque me regalaran la estancia. Pésima gestión.", "expected": "Negativo"}
]

# Cargar Modelos
try:
    model = joblib.load(os.path.join(BASE_DIR, "data", "models", "sentiment_model.pkl"))
    vectorizer = joblib.load(os.path.join(BASE_DIR, "data", "models", "tfidf_vectorizer.pkl"))
except Exception as e:
    print(f"Error cargando modelos: {e}")
    sys.exit(1)

print(f"--- BENCHMARK 50 RESEÑAS TÍPICAS (G68 SUPREME) ---")
correctos = 0
for idx, item in enumerate(typical_reviews, 1):
    res, prob, meta = analizar_sentimiento_hibrido(item['text'], model, vectorizer)
    estado = "✅ OK" if res.lower() == item['expected'].lower() else "❌ FAIL"
    if estado == "✅ OK": correctos += 1
    
    # Solo imprimimos fallos para no saturar
    if estado == "❌ FAIL":
        print(f"FAIL {idx}: E:{item['expected']} | P:{res} | {item['text'][:50]}...")

accuracy = (correctos / len(typical_reviews)) * 100
print(f"\nRESULTADO FINAL: {correctos}/{len(typical_reviews)} correctos ({accuracy:.2f}%)")
