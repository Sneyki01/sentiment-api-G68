import os
import sys
import joblib

# Configurar rutas para importar el motor
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, "src"))

from engine.sentiment_engine import analizar_sentimiento_hibrido

# --- DATASET DE SARCASMO Y ESTRÉS (50 FRASES) ---
sarcasm_stress_phrases = [
    # Sarcasmo e Ironía
    {"text": "Gracias por la sauna gratuita en la habitación, el aire acondicionado no funcionó en toda la noche.", "expected": "Negativo"},
    {"text": "Si te gusta el estilo 'vintage' de los años 70 sin reformar, este es tu sitio.", "expected": "Negativo"},
    {"text": "La limpieza era tan 'minimalista' que las pelusas debajo de la cama ya tenían nombre propio.", "expected": "Negativo"},
    {"text": "Un detalle encantador el hilo musical de la discoteca de al lado a las 4 de la mañana.", "expected": "Negativo"},
    {"text": "Me encantó la experiencia de 'ducha de aventura': agua hirviendo o hielo, sin avisar.", "expected": "Negativo"},
    {"text": "El buffet era tan exclusivo que si llegabas 15 minutos tarde ya no había comida.", "expected": "Negativo"},
    {"text": "Las paredes son tan delgadas que ahora sé toda la vida privada de mis vecinos de la 302.", "expected": "Negativo"},
    {"text": "El Wi-Fi es perfecto para practicar la paciencia y la meditación, porque no carga nada.", "expected": "Negativo"},
    {"text": "Me dieron una habitación con 'vistas al mar', si por mar entiendes un charco en el callejón.", "expected": "Negativo"},
    {"text": "El personal es tan relajado que parecen estar en coma profundo cuando les pides algo.", "expected": "Negativo"},
    {"text": "Excelente idea la de no poner cortinas, me encanta que toda la ciudad me vea ducharme.", "expected": "Negativo"},
    {"text": "La cama era ortopédica, si por ortopédica te refieres a dormir sobre una tabla de planchar.", "expected": "Negativo"},
    {"text": "Un aplauso al arquitecto que puso el enchufe a tres metros de la cama.", "expected": "Negativo"},
    {"text": "El 'gimnasio' es una oda a la antigüedad; las máquinas están listas para un museo.", "expected": "Negativo"},
    {"text": "Gracias por el jabón de cortesía, me alcanzó justo para lavarme el dedo pulgar.", "expected": "Negativo"},
    {"text": "El servicio de habitaciones llegó tan rápido que para cuando trajeron la cena ya era el desayuno.", "expected": "Negativo"},
    {"text": "Las sábanas tenían tantas manchas que parecían un mapa del tesoro.", "expected": "Negativo"},
    {"text": "Si quieres sentirte como en una celda de alta seguridad, este hotel es ideal.", "expected": "Negativo"},
    {"text": "La piscina estaba tan limpia que tenía su propio ecosistema de ranas y algas.", "expected": "Negativo"},
    {"text": "El ascensor es tan rápido que me dio tiempo a leer una novela mientras subía al tercer piso.", "expected": "Negativo"},
    {"text": "Me encantó el detalle de la alfombra pegajosa, así no me resbalo.", "expected": "Negativo"},
    {"text": "El check-in fue tan ágil que solo tardamos 45 minutos en encontrar mi reserva.", "expected": "Negativo"},
    {"text": "La 'terraza privada' era un balcón de 10 centímetros donde apenas cabía mi pie.", "expected": "Negativo"},
    {"text": "El desayuno buffet era una dieta forzada: solo quedaba pan duro y agua.", "expected": "Negativo"},
    {"text": "Una experiencia inolvidable... por mucho que intente olvidarla, no puedo.", "expected": "Negativo"},
    
    # Estrés y Frustración
    {"text": "¡Es inaceptable que nadie conteste al teléfono de recepción después de diez llamadas!", "expected": "Negativo"},
    {"text": "Estoy atrapado en una habitación que huele a humedad y no me quieren cambiar.", "expected": "Negativo"},
    {"text": "¡Un desastre total! No entiendo cómo este sitio tiene 4 estrellas.", "expected": "Negativo"},
    {"text": "He tenido que bajar yo mismo a por toallas porque nadie subía, ¡estoy harto!", "expected": "Negativo"},
    {"text": "Es indignante pagar este precio por una habitación llena de cucarachas.", "expected": "Negativo"},
    {"text": "¡Me siento estafado! Las fotos de la web son un engaño absoluto.", "expected": "Negativo"},
    {"text": "Viajamos con un bebé y nos dejaron sin calefacción toda la noche, ¡una vergüenza!", "expected": "Negativo"},
    {"text": "El recepcionista me gritó delante de otros huéspedes, nunca me habían tratado así.", "expected": "Negativo"},
    {"text": "¡Peligro! El parking es una ratonera y rayé el coche por las malas indicaciones.", "expected": "Negativo"},
    {"text": "Llevo dos horas esperando mi habitación y sigo aquí sentado, ¡mi tiempo vale dinero!", "expected": "Negativo"},
    {"text": "La peor experiencia de mi vida, no se lo recomendaría ni a mi peor enemigo.", "expected": "Negativo"},
    {"text": "Llegamos y el hotel estaba sobrevendido, ¡nos dejaron en la calle a medianoche!", "expected": "Negativo"},
    {"text": "¡Suciedad por todos lados! Me da asco incluso tocar el mando de la tele.", "expected": "Negativo"},
    {"text": "Tuvimos que irnos a otro hotel a mitad de la noche porque el ruido era insoportable.", "expected": "Negativo"},
    {"text": "Nadie se hace responsable del robo en mi habitación, ¡es una pesadilla!", "expected": "Negativo"},
    {"text": "Me cobraron dos veces la reserva y nadie me da una solución, ¡estoy desesperado!", "expected": "Negativo"},
    {"text": "El baño se inundó y tardaron tres horas en mandar a alguien, ¡un caos!", "expected": "Negativo"},
    {"text": "¡Basta de excusas! El servicio es nefasto y el personal es un incompetente.", "expected": "Negativo"},
    {"text": "Me siento humillado por el trato recibido en este establecimiento.", "expected": "Negativo"},
    {"text": "Es un insulto que llamen a esto 'desayuno continental'.", "expected": "Negativo"},
    {"text": "¡Cuidado! Cobran suplementos por todo sin avisar al hacer el check-in.", "expected": "Negativo"},
    {"text": "La seguridad es nula, cualquiera puede entrar a los pasillos del hotel.", "expected": "Negativo"},
    {"text": "¡Horrible! El colchón tiene un hundimiento y me voy con un dolor de espalda terrible.", "expected": "Negativo"},
    {"text": "No hay derecho a que nos traten así después de pagar una fortuna.", "expected": "Negativo"},
    {"text": "Si quieres arruinar tus vacaciones, reserva en este hotel.", "expected": "Negativo"}
]

# Cargar Modelos
model = joblib.load(os.path.join(BASE_DIR, "data", "models", "sentiment_model.pkl"))
vectorizer = joblib.load(os.path.join(BASE_DIR, "data", "models", "tfidf_vectorizer.pkl"))

print(f"--- BENCHMARK: SARCASMO Y ESTRÉS (50 FRASES) ---")
correctos = 0
for idx, item in enumerate(sarcasm_stress_phrases, 1):
    res, prob, meta = analizar_sentimiento_hibrido(item['text'], model, vectorizer)
    estado = "✅ OK" if res.lower() == item['expected'].lower() else "❌ FAIL"
    if estado == "✅ OK": correctos += 1
    
    print(f"{idx:<3} | {estado:<7} | E:{item['expected']:<10} | P:{res:<10} | Score:{meta.get('score'):>6} | {item['text'][:60]}...")

accuracy = (correctos / len(sarcasm_stress_phrases)) * 100
print(f"\nRESULTADO FINAL SARCASMO/ESTRÉS: {correctos}/{len(sarcasm_stress_phrases)} correctos ({accuracy:.2f}%)")
