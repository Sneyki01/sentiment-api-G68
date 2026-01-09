import os
import sys
import joblib
import math

# Configurar rutas para importar el motor
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, "src"))

from engine.sentiment_engine import analizar_sentimiento_hibrido

# --- DATASET DE RESEÑAS LARGAS (25) ---
long_reviews = [
    {"text": "El hotel es una maravilla visual, el diseño es impecable y la cama es la más cómoda en la que he dormido. Sin embargo, todo eso se va al traste cuando el personal de recepción te trata como si les estuvieras haciendo un favor por alojarte allí. Una pena que la falta de educación arruine una inversión tan grande en infraestructura.", "expected": "Negativo"},
    {"text": "Llegamos con muchísima ilusión por nuestro décimo aniversario. Habíamos reservado el paquete premium con pétalos de rosa y cena privada. Al llegar, no solo no tenían la habitación lista, sino que habían perdido la reserva del restaurante. Pasamos de un estado de felicidad total a un estrés y una frustración que nos arruinaron la primera noche.", "expected": "Negativo"},
    {"text": "Quiero agradecer de corazón a Marta, la terapeuta del spa. Venía pasando por una racha personal muy complicada, con mucha ansiedad, y su trato humano y la delicadeza del masaje me hicieron llorar de alivio. No es solo un negocio de bienestar, es un refugio para el alma. Gracias, gracias y mil veces gracias.", "expected": "Positivo"},
    {"text": "¡Increíble! Si te gusta esperar 20 minutos por un café, que el agua de la ducha salga marrón y que el 'aire acondicionado' sea un agujero en la pared por el que entra el ruido de la autopista, este es tu sitio. Un auténtico paraíso... para alguien que odie su propia vida y quiera sufrir en vacaciones.", "expected": "Negativo"},
    {"text": "El establecimiento es correcto. Las habitaciones están limpias, el buffet tiene lo básico (fruta, pan, huevos) y la ubicación es céntrica. No esperes grandes lujos ni un trato personalizado, pero para un viaje de trabajo donde solo vas a dormir y ducharte, cumple perfectamente con su función.", "expected": "Neutro"},
    {"text": "¡SOCORRO! Estábamos en medio del circuito de aguas cuando las luces se apagaron por completo. Nos quedamos a oscuras, en el agua, sin que nadie viniera a decirnos nada durante diez minutos eternos. Empezamos a gritar de puro pánico. Fue una situación peligrosa y negligente por parte de la gerencia.", "expected": "Negativo"},
    {"text": "Es curioso cómo venden la 'experiencia detox'. Mi experiencia consistió en pasar hambre porque las porciones eran ridículas, pasar frío porque no encendían la calefacción 'por ecología' y terminar pagando el triple de lo que cuesta un hotel de 5 estrellas de verdad. Me siento estafado con elegancia.", "expected": "Negativo"},
    {"text": "Había leído críticas terribles sobre este sitio y venía con mucho miedo, pero la verdad es que mi experiencia ha sido totalmente distinta. El check-in fue rápido, la habitación olía a limpio y el desayuno fue más que aceptable. A veces creo que la gente exagera o tiene expectativas irreales.", "expected": "Positivo"},
    {"text": "El tratamiento de piedras calientes fue... una aventura. Primero estaban frías, luego el terapeuta se tropezó y casi se le caen encima de mi cabeza, y al final terminó la sesión diez minutos antes porque 'tenía otra cita'. No sé si reír o llorar, pero relajarme, desde luego que no.", "expected": "Negativo"},
    {"text": "La ubicación es lo mejor que tiene, estás a un paso de todo. Lo malo es que el ruido de la calle es constante, pero si traes tapones se soluciona. El desayuno es caro, pero hay una cafetería justo enfrente que es genial. En resumen: tiene sus fallos, pero la zona compensa si sabes organizarte.", "expected": "Neutro"}, # Pragmática / Balanceada
    {"text": "Llevo tres días intentando que me traigan una manta extra. Tres días. Cada vez que llamo a recepción me dicen 'en cinco minutos sube un botones'. Es fascinante ver cómo ignoran sistemáticamente una petición tan sencilla. Me pregunto si tengo que bajar yo mismo a la lavandería a buscarla.", "expected": "Negativo"},
    {"text": "Un 10 para el equipo de animación y bienestar. Mis hijos estuvieron entretenidos todo el día con actividades saludables y yo pude disfrutar del circuito termal sin preocupaciones. Es difícil encontrar un sitio que equilibre tan bien el ambiente familiar con el relax absoluto.", "expected": "Positivo"},
    {"text": "Sinceramente, no entiendo el diseño de este hotel. Tienes que subir un piso en ascensor, bajar medio tramo de escaleras y cruzar un pasillo exterior para llegar al spa. Si vas en albornoz y hace frío, te congelas. Parece que el arquitecto nunca se alojó aquí.", "expected": "Negativo"},
    {"text": "La habitación olía a tabaco rancio a pesar de ser de no fumadores. Pedimos cambio y nos dijeron que estaban llenos. Nos dieron un spray ambientador que olía peor que el tabaco. Tuvimos que dormir con la ventana abierta en pleno invierno. Una gestión nefasta de un problema evitable.", "expected": "Negativo"},
    {"text": "Es la tercera vez que vengo y noto que el nivel ha bajado drásticamente. El mobiliario está desgastado, las toallas ya no son blancas sino grises y el personal parece cansado y desmotivado. Es una pena ver cómo un sitio que era excelente se deja morir por falta de mantenimiento.", "expected": "Negativo"},
    {"text": "¡Fue un desastre desde que bajamos del taxi! Nadie nos ayudó con las maletas, el lobby estaba lleno de gente gritando y el aire acondicionado de la recepción no funcionaba. Estábamos sudando, cansados y nadie nos daba una solución. Mi nivel de estrés subió a mil en cinco minutos.", "expected": "Negativo"},
    {"text": "El menú degustación de bienestar es una obra de arte. Sabores sutiles, ingredientes frescos y una presentación que da pena comerse. Se nota que hay un chef que entiende de nutrición y de placer gastronómico a partes iguales. Caro, pero vale cada céntimo.", "expected": "Positivo"},
    {"text": "Buscábamos silencio y encontramos una boda justo debajo de nuestra ventana. El hotel no nos avisó de que habría un evento con música hasta las 4 de la mañana. Si lo hubiéramos sabido, jamás habríamos reservado. Nos sentimos engañados por falta de transparencia.", "expected": "Negativo"},
    {"text": "El tratamiento facial de oro es puro marketing. No noté ninguna diferencia en mi piel, salvo que mi cartera pesaba menos al salir. El personal es amable, sí, pero el servicio en sí me parece una pérdida de tiempo y dinero.", "expected": "Negativo"},
    {"text": "Es como entrar en otra dimensión. La decoración zen, el sonido del agua de fondo y el trato susurrado del personal te transportan. Olvidas el móvil, el trabajo y las preocupaciones. Es una inversión en salud mental más que un simple alojamiento.", "expected": "Positivo"},
    {"text": "La ducha tenía moho en las juntas y la presión del agua era nula. Cuando se lo dije a la camarera de pisos, se encogió de hombros y dijo que el edificio era viejo. No creo que la edad del edificio sea excusa para la falta de lejía y mantenimiento básico.", "expected": "Negativo"},
    {"text": "Vine por una recomendación y me voy con ganas de recomendarlo yo también. El circuito de saunas es completísimo y el detalle de la fruta fresca y las infusiones al finalizar es el broche de oro. Me sentí cuidada en cada detalle.", "expected": "Positivo"},
    {"text": "No entiendo cómo tienen 4 estrellas. El Wi-Fi no llega a las habitaciones, el televisor es del siglo pasado y el mando a distancia no tenía pilas. Son pequeños detalles que sumados hacen que la estancia sea incómoda y frustrante.", "expected": "Negativo"},
    {"text": "¡CUIDADO! Las fotos de la web están retocadas. La piscina 'olímpica' es una alberca donde apenas caben 4 personas y el 'gimnasio de última generación' son dos mancuernas oxidadas y una cinta de correr rota. Es un timo total.", "expected": "Negativo"},
    {"text": "Llegamos tarde por un retraso en el vuelo, agotados y con hambre. El recepcionista, a pesar de que la cocina estaba cerrada, nos preparó personalmente un sándwich y nos subió una botella de agua fría. Ese tipo de gestos son los que hacen que un cliente vuelva siempre.", "expected": "Positivo"}
]

# Cargar Modelos
model = joblib.load(os.path.join(BASE_DIR, "data", "models", "sentiment_model.pkl"))
vectorizer = joblib.load(os.path.join(BASE_DIR, "data", "models", "tfidf_vectorizer.pkl"))

print(f"--- BENCHMARK RESEÑAS LARGAS (G68 ULTIMATE) ---")
correctos = 0
for idx, item in enumerate(long_reviews, 1):
    res, prob, meta = analizar_sentimiento_hibrido(item['text'], model, vectorizer)
    estado = "✅ OK" if res.lower() == item['expected'].lower() else "❌ FAIL"
    if estado == "✅ OK": correctos += 1
    
    print(f"{idx:<3} | {estado:<7} | E:{item['expected']:<10} | P:{res:<10} | Score: {meta.get('score', 0):>6.2f} | {item['text'][:60]}...")

accuracy = (correctos / len(long_reviews)) * 100
print(f"\nRESULTADO FINAL: {correctos}/{len(long_reviews)} correctos ({accuracy:.2f}%)")
