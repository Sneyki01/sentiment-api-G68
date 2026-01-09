import os
import sys
import joblib
import math

# Configurar rutas para importar el motor
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, "src"))

from engine.sentiment_engine import analizar_sentimiento_hibrido

# --- DATASET TEMÁTICO (100 FRASES) ---
themed_phrases = [
    # Bloque 1: Ubicación
    {"text": "El hotel está muy bien ubicado, cerca del metro.", "expected": "Positivo"},
    {"text": "Es difícil encontrar aparcamiento por la zona.", "expected": "Negativo"},
    {"text": "Hay muchos restaurantes y tiendas a pocos pasos.", "expected": "Positivo"},
    {"text": "La zona es un poco ruidosa por la noche, pero soportable.", "expected": "Neutro"}, # Mixta
    {"text": "Está en pleno centro, puedes ir andando a todos lados.", "expected": "Positivo"},
    {"text": "La parada del autobús turístico está justo en la puerta.", "expected": "Positivo"},
    {"text": "Un poco alejado del centro, pero bien comunicado.", "expected": "Neutro"},
    {"text": "La calle es muy tranquila, sin nada de ruido de tráfico.", "expected": "Positivo"},
    {"text": "Cuesta un poco encontrar la entrada del hotel.", "expected": "Negativo"},
    {"text": "Ubicación excelente para visitar los museos principales.", "expected": "Positivo"},
    {"text": "El barrio se siente un poco inseguro de noche.", "expected": "Negativo"},
    {"text": "Tuvimos que caminar unos 15 minutos para llegar al centro.", "expected": "Neutro"},
    {"text": "Ideal para los que buscan estar cerca de la estación de tren.", "expected": "Positivo"},
    {"text": "Hay un supermercado justo en la esquina, muy útil.", "expected": "Positivo"},
    {"text": "Está en una cuesta muy pronunciada, difícil para personas mayores.", "expected": "Negativo"},
    {"text": "La ubicación es lo mejor que tiene el hotel.", "expected": "Positivo"},
    {"text": "No es céntrico, pero el taxi es barato hasta allí.", "expected": "Neutro"},
    {"text": "Muy conveniente si tienes un vuelo temprano por la mañana.", "expected": "Positivo"},
    {"text": "Situado en una zona peatonal muy bonita.", "expected": "Positivo"},
    {"text": "El hotel no tiene parking propio, hay que ir a uno público.", "expected": "Negativo"},
    {"text": "Rodeado de parques para salir a caminar.", "expected": "Positivo"},
    {"text": "Un poco difícil llegar con el GPS la primera vez.", "expected": "Neutro"},
    {"text": "Cerca de la playa pero lejos de la zona comercial.", "expected": "Neutro"}, # Mixta
    {"text": "Está en una zona residencial muy silenciosa.", "expected": "Positivo"},
    {"text": "El acceso desde la autopista es muy rápido y directo.", "expected": "Positivo"},

    # Bloque 2: Habitaciones
    {"text": "La habitación era amplia y estaba muy limpia.", "expected": "Positivo"},
    {"text": "El colchón era demasiado blando para mi gusto.", "expected": "Negativo"},
    {"text": "Las almohadas eran cómodas, dormimos muy bien.", "expected": "Positivo"},
    {"text": "No había suficientes enchufes cerca de la cama.", "expected": "Negativo"},
    {"text": "El baño era moderno y tenía una ducha estupenda.", "expected": "Positivo"},
    {"text": "Se escuchaba todo lo que pasaba en la habitación de al lado.", "expected": "Negativo"},
    {"text": "La calefacción funcionaba perfectamente.", "expected": "Positivo"},
    {"text": "La televisión era un poco pequeña y antigua.", "expected": "Negativo"},
    {"text": "Nos dieron una habitación con vistas al patio interior.", "expected": "Neutro"},
    {"text": "El aire acondicionado hacía un poco de ruido al encenderse.", "expected": "Negativo"},
    {"text": "Habitación luminosa con grandes ventanales.", "expected": "Positivo"},
    {"text": "El armario era un poco pequeño para dos personas.", "expected": "Negativo"},
    {"text": "Las toallas las cambiaban todos los días.", "expected": "Positivo"},
    {"text": "La presión del agua en the baño era excelente.", "expected": "Positivo"},
    {"text": "Había un olor a tubería en el baño al entrar.", "expected": "Negativo"},
    {"text": "Cortinas opacas que quitaban bien la luz.", "expected": "Positivo"},
    {"text": "La decoración es sencilla pero funcional.", "expected": "Neutro"},
    {"text": "La nevera de la habitación no enfriaba mucho.", "expected": "Negativo"},
    {"text": "La cama de matrimonio eran dos camas juntas.", "expected": "Negativo"},
    {"text": "Todo estaba ordenado y en su sitio.", "expected": "Positivo"},
    {"text": "Faltaba algún espejo de cuerpo entero en el cuarto.", "expected": "Negativo"},
    {"text": "Habitación muy bien insonorizada.", "expected": "Positivo"},
    {"text": "El secador de pelo era de poca potencia.", "expected": "Negativo"},
    {"text": "Espacio suficiente para dejar las maletas abiertas.", "expected": "Positivo"},
    {"text": "Mobiliario un poco desgastado por el uso.", "expected": "Negativo"},

    # Bloque 3: Servicio
    {"text": "El personal de recepción fue muy amable en todo momento.", "expected": "Positivo"},
    {"text": "El check-in fue un poco lento porque solo había una persona.", "expected": "Negativo"},
    {"text": "Nos ayudaron a reservar un taxi para el aeropuerto.", "expected": "Positivo"},
    {"text": "La camarera de pisos fue muy atenta con nuestras peticiones.", "expected": "Positivo"},
    {"text": "No nos explicaron bien el horario del desayuno al llegar.", "expected": "Negativo"},
    {"text": "Hablan varios idiomas, lo cual facilita mucho las cosas.", "expected": "Positivo"},
    {"text": "El trato fue profesional, aunque un poco distante.", "expected": "Neutro"},
    {"text": "Cualquier duda que teníamos nos la resolvían enseguida.", "expected": "Positivo"},
    {"text": "Se olvidaron de traernos la cuna que pedimos por teléfono.", "expected": "Negativo"},
    {"text": "Te reciben siempre con una sonrisa.", "expected": "Positivo"},
    {"text": "El personal de mantenimiento solucionó rápido el problema de la luz.", "expected": "Positivo"},
    {"text": "Pedimos una habitación alta y nos la dieron sin problemas.", "expected": "Positivo"},
    {"text": "No fueron muy flexibles con la hora de salida.", "expected": "Negativo"},
    {"text": "Nos guardaron las maletas después del check-out de forma gratuita.", "expected": "Positivo"},
    {"text": "El servicio de habitaciones es rápido y eficaz.", "expected": "Positivo"},
    {"text": "Un poco de falta de coordinación entre los turnos.", "expected": "Negativo"},
    {"text": "Fueron muy detallistas con el pack de bienvenida.", "expected": "Positivo"},
    {"text": "El gerente salió a saludarnos, un gesto muy educado.", "expected": "Positivo"},
    {"text": "Tardaron mucho en darnos las llaves de la habitación.", "expected": "Negativo"},
    {"text": "Personal muy joven y con ganas de ayudar.", "expected": "Positivo"},
    {"text": "La limpieza pasó por alto algunas zonas del baño.", "expected": "Negativo"},
    {"text": "El servicio de desayuno es un poco caótico cuando se llena.", "expected": "Negativo"},
    {"text": "Nos dieron un mapa y muchas recomendaciones locales.", "expected": "Positivo"},
    {"text": "A veces es difícil encontrar a alguien en recepción.", "expected": "Negativo"},
    {"text": "El trato fue inmejorable de principio a fin.", "expected": "Positivo"},

    # Bloque 4: Instalaciones
    {"text": "El desayuno buffet tenía mucha variedad de fruta y bollería.", "expected": "Positivo"},
    {"text": "La piscina estaba un poco fría, pero muy limpia.", "expected": "Neutro"}, # Mixta
    {"text": "El gimnasio es pequeño pero tiene lo necesario para entrenar.", "expected": "Neutro"},
    {"text": "El Wi-Fi funcionaba bien en las zonas comunes y habitaciones.", "expected": "Positivo"},
    {"text": "El ascensor es bastante pequeño, solo caben dos personas.", "expected": "Negativo"},
    {"text": "El bar del hotel tiene unos precios muy razonables.", "expected": "Positivo"},
    {"text": "No hay opciones para celíacos en el desayuno.", "expected": "Negativo"},
    {"text": "El lobby es muy acogedor para sentarse a leer un rato.", "expected": "Positivo"},
    {"text": "La terraza tiene unas vistas espectaculares de la ciudad.", "expected": "Positivo"},
    {"text": "Faltaba iluminación en los pasillos del hotel.", "expected": "Negativo"},
    {"text": "El café del desayuno era de máquina y no sabía muy bien.", "expected": "Negativo"},
    {"text": "Zonas comunes muy bien cuidadas y decoradas.", "expected": "Positivo"},
    {"text": "La sala de reuniones es espaciosa y moderna.", "expected": "Positivo"},
    {"text": "El restaurante del hotel estaba cerrado los domingos.", "expected": "Negativo"},
    {"text": "Había zumo de naranja natural, todo un detalle.", "expected": "Positivo"},
    {"text": "El spa es de pago, aunque seas cliente del hotel.", "expected": "Negativo"},
    {"text": "Máquinas expendedoras con precios elevados.", "expected": "Negativo"},
    {"text": "El jardín está muy bien iluminado por la noche.", "expected": "Positivo"},
    {"text": "Se nota que han reformado las instalaciones recientemente.", "expected": "Positivo"},
    {"text": "El suelo de la piscina resbala un poco cuando está mojado.", "expected": "Negativo"},
    {"text": "Los huevos revueltos del buffet estaban un poco secos.", "expected": "Negativo"},
    {"text": "Ofrecen agua y manzanas de cortesía en the lobby.", "expected": "Positivo"},
    {"text": "El mobiliario del salón de desayunos es muy incómodo.", "expected": "Negativo"},
    {"text": "Acceso gratuito a prensa diaria en la recepción.", "expected": "Positivo"},
    {"text": "En general, las instalaciones están a la altura de su categoría.", "expected": "Positivo"}
]

# Cargar Modelos
model = joblib.load(os.path.join(BASE_DIR, "data", "models", "sentiment_model.pkl"))
vectorizer = joblib.load(os.path.join(BASE_DIR, "data", "models", "tfidf_vectorizer.pkl"))

print(f"--- BENCHMARK TEMÁTICO 100 FRASES (G68 SUPREME) ---")
correctos = 0
for idx, item in enumerate(themed_phrases, 1):
    res, prob, meta = analizar_sentimiento_hibrido(item['text'], model, vectorizer)
    estado = "✅ OK" if res.lower() == item['expected'].lower() else "❌ FAIL"
    if estado == "✅ OK": correctos += 1
    
    # print(f"{idx:<3} | {estado:<7} | E:{item['expected']:<10} | P:{res:<10} | {item['text'][:60]}...")

accuracy = (correctos / len(themed_phrases)) * 100
print(f"\nPRECISIÓN POR BLOQUES:")
print(f"Total: {correctos}/{len(themed_phrases)} correctos ({accuracy:.2f}%)")
