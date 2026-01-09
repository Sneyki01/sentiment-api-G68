import os
import sys
import joblib

# Configurar rutas para importar el motor
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, "src"))

from engine.sentiment_engine import analizar_sentimiento_hibrido

# --- DATASET DE 20 RESEÑAS LARGAS Y COMPLEJAS ---
complex_long_reviews = [
    # 🎭 Sarcasmo e Ironía
    {"text": "Me fascinó la propuesta de 'ayuno intermitente' forzado que ofrece el hotel, ya que el buffet cerraba media hora antes de lo anunciado y el personal te miraba como si les estuvieras robando el alma si pedías un café.", "expected": "Negativo"},
    {"text": "Si lo que buscas es una experiencia de inmersión total en la vida de los demás, este es tu sitio: gracias a las paredes de papel pude enterarme de la crisis matrimonial de la 204 y de los gustos musicales, bastante cuestionables por cierto, del huésped de la 206.", "expected": "Negativo"},
    {"text": "Excelente gestión del espacio en el baño; es tan pequeño que puedes lavarte los dientes, usar el inodoro y ducharte, todo al mismo tiempo y sin moverte un centímetro. Eficiencia pura para gente con prisa.", "expected": "Negativo"},
    {"text": "Le doy cinco estrellas al equipo de limpieza por su increíble habilidad para ignorar sistemáticamente la montaña de polvo bajo la cama, creo que están intentando crear una reserva natural de ácaros protegida.", "expected": "Negativo"},
    {"text": "Un aplauso al decorador por elegir esas cortinas tan finas que permiten que la luz de la farola de la calle ilumine mi habitación como si fuera un interrogatorio policial durante toda la madrugada.", "expected": "Negativo"},
    {"text": "La conexión Wi-Fi es una joya vintage; te transporta directamente a 1995, permitiéndote reflexionar sobre la vida mientras esperas diez minutos a que cargue la página principal de un periódico.", "expected": "Negativo"},
    {"text": "Qué detalle tan rústico que el agua de la ducha salga de un color amarillento durante los primeros cinco minutos, realmente te hace sentir que estás en una cabaña abandonada en el bosque y no en un hotel de ciudad.", "expected": "Negativo"},

    # 😫 Estrés y Frustración
    {"text": "Es absolutamente indignante que, tras pagar una tarifa de lujo, nos informen al llegar que la piscina y el spa están cerrados por mantenimiento, algo que casualmente olvidaron mencionar en su página web al hacer la reserva.", "expected": "Negativo"},
    {"text": "Llevo tres horas esperando en recepción con dos niños pequeños después de un vuelo de diez horas, y lo único que recibo son encogimientos de hombros y excusas baratas sobre que el sistema informático se ha caído.", "expected": "Negativo"},
    {"text": "La situación fue límite cuando, tras avisar tres veces de que el aire acondicionado goteaba sobre la cama, la única 'solución' que nos ofrecieron fue un cubo de plástico para recoger el agua y una toalla extra.", "expected": "Negativo"},
    {"text": "No hay palabras para describir la sensación de inseguridad al ver que la puerta del balcón no cerraba bien y que cualquier persona podía acceder desde la terraza común, y la respuesta del hotel fue que 'el barrio es muy tranquilo'.", "expected": "Negativo"},
    {"text": "El olor a tubería en el pasillo de la cuarta planta era tan nauseabundo que tuvimos que poner toallas húmedas en la rendija de la puerta para poder dormir sin sentir mareos, una experiencia que no le deseo a nadie.", "expected": "Negativo"},
    {"text": "Me parece un insulto que el recepcionista me discutiera el precio de la reserva delante de otros clientes, insinuando que yo estaba mintiendo cuando tenía el comprobante impreso en mis propias manos.", "expected": "Negativo"},
    {"text": "El ruido de las obras en la habitación contigua empezó a las siete de la mañana sin previo aviso, transformando nuestro fin de semana de descanso en una tortura de martillazos y gritos de los operarios.", "expected": "Negativo"},

    # 🧐 Mixtas / Realistas
    {"text": "El hotel tiene un lobby que parece sacado de una película de Hollywood, pero en cuanto cruzas la puerta del ascensor, la realidad te golpea con alfombras manchadas, pasillos oscuros y un olor a tabaco rancio que se te pega a la ropa.", "expected": "Negativo"},
    {"text": "Aunque el personal del desayuno fue muy amable y trató de compensar el caos, es imposible disfrutar de una comida cuando hay veinte personas esperando por una mesa y la comida se acaba más rápido de lo que pueden reponerla.", "expected": "Neutro"},
    {"text": "La ubicación es inmejorable para visitar los museos, pero el precio que pagas por el silencio es demasiado alto, ya que la habitación que nos asignaron no tenía ni una ventana al exterior, pareciendo más un búnker que una suite.", "expected": "Neutro"},
    {"text": "Agradezco el esfuerzo de la chica de prácticas por intentar arreglar el problema del televisor, pero la falta de personal cualificado en este establecimiento es evidente y termina afectando directamente a la experiencia del huésped.", "expected": "Neutro"},
    {"text": "El colchón era sorprendentemente cómodo, pero es difícil descansar cuando el extractor del baño de la habitación de arriba suena como el motor de un avión cada vez que alguien enciende la luz.", "expected": "Neutro"},
    {"text": "Es una pena que un edificio con tanta historia y potencial esté tan mal gestionado, con detalles tan descuidados como bombillas fundidas, grifos que bailan y un servicio de habitaciones que nunca contesta al teléfono.", "expected": "Negativo"}
]

# Cargar Modelos
model = joblib.load(os.path.join(BASE_DIR, "data", "models", "sentiment_model.pkl"))
vectorizer = joblib.load(os.path.join(BASE_DIR, "data", "models", "tfidf_vectorizer.pkl"))

print(f"--- BENCHMARK: 20 RESEÑAS LARGAS Y COMPLEJAS (G68 SUPREME) ---")
correctos = 0
for idx, item in enumerate(complex_long_reviews, 1):
    res, prob, meta = analizar_sentimiento_hibrido(item['text'], model, vectorizer)
    estado = "✅ OK" if res.lower() == item['expected'].lower() else "❌ FAIL"
    if estado == "✅ OK": correctos += 1
    
    print(f"{idx:<2} | {estado:<6} | E:{item['expected']:<10} | P:{res:<10} | Score:{meta.get('score'):>6} | {item['text'][:70]}...")

accuracy = (correctos / len(complex_long_reviews)) * 100
print(f"\nRESULTADO FINAL COMPLEJAS/LARGAS: {correctos}/{len(complex_long_reviews)} correctos ({accuracy:.2f}%)")
