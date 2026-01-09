import os
import sys
import joblib
import pandas as pd
import math

# 1. Configurar rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, "src"))

from engine.sentiment_engine import analizar_sentimiento_hibrido

# 2. Dataset Completo (1-100)
data = [
    # ... (Mantengo las 1-50 abreviadas internamente para el script final)
    {"text": "¡Fue una experiencia transformadora, me siento como nuevo!", "expected": "Positivo"},
    {"text": "El spa estaba tan sucio que salí con más estrés del que traía.", "expected": "Negativo"},
    {"text": "El masaje estuvo bien, ni mejor ni peor que otros.", "expected": "Neutro"},
    {"text": "¡Increíble! Gracias por hacerme sentir en las nubes.", "expected": "Positivo"},
    {"text": "¿A esto le llaman 'lujo'? Mi sofá es más cómodo que esta cama.", "expected": "Negativo"},
    {"text": "Me cobraron el agua de cortesía, un detalle de clase mundial...", "expected": "Negativo"},
    {"text": "El recepcionista fue extremadamente grosero, no vuelvo nunca.", "expected": "Negativo"},
    {"text": "Las sábanas tenían un olor extraño, pero la vista era bonita.", "expected": "Neutro"},
    {"text": "¡Llevo 40 minutos esperando mi té de hierbas! ¡Qué desastre!", "expected": "Negativo"},
    {"text": "El retiro de yoga cumplió con el itinerario básico.", "expected": "Neutro"},
    {"text": "Es el paraíso en la tierra, la atención es impecable.", "expected": "Positivo"},
    {"text": "Gracias por arruinar nuestro aniversario con su falta de organización.", "expected": "Negativo"},
    {"text": "Qué sorpresa, el sauna no funciona... otra vez. Genial.", "expected": "Negativo"},
    {"text": "El tratamiento facial me dejó la piel radiante, ¡estoy feliz!", "expected": "Positivo"},
    {"text": "No entiendo las quejas, para mí el servicio fue normal.", "expected": "Neutro"},
    {"text": "Tengo el corazón a mil, el ruido de las obras no me dejó dormir nada.", "expected": "Negativo"},
    {"text": "Un lugar decente para pasar la noche si no tienes otra opción.", "expected": "Neutro"},
    {"text": "¡Me encantaría vivir aquí para siempre! Todo es perfecto.", "expected": "Positivo"},
    {"text": "Ah, perfecto, el 'desayuno buffet' son solo tres panecillos secos.", "expected": "Negativo"},
    {"text": "Siento que por fin he recuperado mi energía vital. Gracias.", "expected": "Positivo"},
    {"text": "Mi habitación no estaba lista a las 3 PM. ¡Esto es inaceptable!", "expected": "Negativo"},
    {"text": "La música del lobby es un poco alta, pero soportable.", "expected": "Neutro"},
    {"text": "¿Cinco estrellas? Tal vez si las dibujaron ellos mismos en la pared.", "expected": "Negativo"},
    {"text": "Necesito un masaje para recuperarme del estrés de este check-in.", "expected": "Negativo"},
    {"text": "El personal es tan amable que te hacen sentir de la familia.", "expected": "Positivo"},
    {"text": "Había una hormiga en el baño, pero el resto estaba limpio.", "expected": "Neutro"},
    {"text": "¡No puedo creer que perdieran mi reserva! ¡Estoy furioso!", "expected": "Negativo"},
    {"text": "Un refugio de paz necesario en medio de tanto caos.", "expected": "Positivo"},
    {"text": "El precio es elevado, pero se ajusta a lo que ofrecen.", "expected": "Neutro"},
    {"text": "El 'aroma relajante' olía a desinfectante industrial barato.", "expected": "Negativo"},
    {"text": "No me toquen, estoy demasiado estresado con este servicio lento.", "expected": "Negativo"},
    {"text": "¡La mejor exfoliación de mi vida! Repetiré sin duda.", "expected": "Positivo"},
    {"text": "El hotel es viejo, pero lo mantienen funcionando.", "expected": "Neutro"},
    {"text": "¿El Wi-Fi? Sí, vuela... igual que mi paciencia esperando que cargue.", "expected": "Negativo"},
    {"text": "Me voy de aquí con una sonrisa de oreja a oreja.", "expected": "Positivo"},
    {"text": "El gimnasio estaba cerrado por mantenimiento sin previo aviso. Mal.", "expected": "Negativo"},
    {"text": "Se supone que venía a relajarme y salgo con migraña.", "expected": "Negativo"},
    {"text": "El servicio de limpieza pasa a las 8 AM, un poco temprano.", "expected": "Neutro"},
    {"text": "Maravilloso, simplemente maravilloso. No tengo palabras.", "expected": "Positivo"},
    {"text": "El zumo de naranja era natural, un buen detalle.", "expected": "Positivo"},
    {"text": "¡Qué maravilla esperar una hora por una toalla limpia! (Sarcasmo).", "expected": "Negativo"},
    {"text": "Odio tener que escribir esto, pero fue una experiencia nefasta.", "expected": "Negativo"},
    {"text": "Me siento renovado, el ambiente es pura calma.", "expected": "Positivo"},
    {"text": "El colchón era tan duro que parecía que dormía en el suelo.", "expected": "Negativo"},
    {"text": "Las instalaciones son modernas, pero el personal es frío.", "expected": "Neutro"},
    {"text": "Por favor, ¡que alguien me ayude con este ruido infernal!", "expected": "Negativo"},
    {"text": "Una experiencia mediocre para el precio que cobran.", "expected": "Negativo"},
    {"text": "El guía del tour de bienestar fue muy profesional y educado.", "expected": "Positivo"},
    {"text": "Wow, otra vez se olvidaron de mi cena. ¡Bravo por su memoria!", "expected": "Negativo"},
    {"text": "El mejor regalo que me he hecho este año. ¡Sublime!", "expected": "Positivo"},
    
    # NUEVAS FRASES (51-100): AMBIGÜEDAD Y NEUTRALIDAD
    {"text": "El masaje fue... diferente a lo que estoy acostumbrado.", "expected": "Neutro"},
    {"text": "El hotel es exactamente lo que esperas por ese precio.", "expected": "Neutro"},
    {"text": "El té de bienvenida tenía un sabor muy particular.", "expected": "Neutro"},
    {"text": "Terminamos el tratamiento justo a la hora prevista.", "expected": "Neutro"},
    {"text": "El estilo de la decoración es muy personal.", "expected": "Neutro"},
    {"text": "Me dieron la habitación que estaba disponible en ese momento.", "expected": "Neutro"},
    {"text": "El terapeuta se mantuvo en silencio durante toda la sesión.", "expected": "Neutro"},
    {"text": "Es un lugar para gente que no busca lujos.", "expected": "Neutro"},
    {"text": "La presión del agua en la ducha era notable.", "expected": "Neutro"},
    {"text": "El ambiente del spa es muy oscuro.", "expected": "Neutro"},
    {"text": "Hicieron lo que tenían que hacer, ni más ni menos.", "expected": "Neutro"},
    {"text": "La comida tiene especias que no reconocerías fácilmente.", "expected": "Neutro"},
    {"text": "El check-in fue un proceso que llevó su tiempo.", "expected": "Neutro"},
    {"text": "Es un concepto de bienestar difícil de explicar.", "expected": "Neutro"},
    {"text": "La temperatura de la piscina estaba según el estándar.", "expected": "Neutro"},
    {"text": "El aroma del lobby se siente desde la calle.", "expected": "Neutro"},
    {"text": "No es el tipo de sitio que ves en las fotos de las revistas.", "expected": "Neutro"},
    {"text": "El personal se limita a cumplir con el manual.", "expected": "Neutro"},
    {"text": "Salí del retiro con mucho en qué pensar.", "expected": "Neutro"},
    {"text": "La cama era bastante blanda.", "expected": "Neutro"},
    {"text": "Un establecimiento que no deja indiferente a nadie.", "expected": "Neutro"},
    {"text": "El diseño es minimalista en extremo.", "expected": "Neutro"},
    {"text": "El guía hablaba con un tono de voz muy bajo.", "expected": "Neutro"},
    {"text": "Las porciones del menú saludable son las que son.", "expected": "Neutro"},
    {"text": "La música de meditación era sonidos de la selva.", "expected": "Neutro"},
    {"text": "Se nota que el dueño tiene una visión clara del negocio.", "expected": "Neutro"},
    {"text": "La iluminación de la habitación depende de la luz natural.", "expected": "Neutro"},
    {"text": "El tratamiento facial duró los 45 minutos pactados.", "expected": "Neutro"},
    {"text": "Es una experiencia que tienes que vivir para entenderla.", "expected": "Neutro"},
    {"text": "El hotel estaba lleno de gente joven.", "expected": "Neutro"},
    {"text": "La ubicación te obliga a caminar bastante.", "expected": "Neutro"},
    {"text": "El jabón del baño no tiene aroma alguno.", "expected": "Neutro"},
    {"text": "Me encontré con varios conocidos en el área de descanso.", "expected": "Neutro"},
    {"text": "El edificio conserva toda la estructura original de 1920.", "expected": "Neutro"},
    {"text": "El zumo de frutas de la mañana era espeso.", "expected": "Neutro"},
    {"text": "Hay que seguir estrictamente las normas del lugar.", "expected": "Neutro"},
    {"text": "El color de las paredes es un verde muy intenso.", "expected": "Neutro"},
    {"text": "La recepcionista nos miró fijamente al entrar.", "expected": "Neutro"},
    {"text": "Es un lugar que requiere un esfuerzo para llegar.", "expected": "Neutro"},
    {"text": "El agua del jacuzzi burbujeaba con mucha fuerza.", "expected": "Neutro"},
    {"text": "El retiro cambió mis planes para el resto de la semana.", "expected": "Neutro"},
    {"text": "Los productos de belleza son de fabricación local.", "expected": "Neutro"},
    {"text": "El aire acondicionado hacía un ruido rítmico.", "expected": "Neutro"},
    {"text": "Pedí un cambio de toalla y me trajeron una enseguida.", "expected": "Neutro"},
    {"text": "La clase de Pilates fue muy técnica.", "expected": "Neutro"},
    {"text": "Había mucha variedad de piedras en el camino del jardín.", "expected": "Neutro"},
    {"text": "El servicio refleja la cultura de la región.", "expected": "Neutro"},
    {"text": "No se escuchaba ni un solo pájaro en el bosque del hotel.", "expected": "Neutro"},
    {"text": "La cena terminó más tarde de lo habitual.", "expected": "Neutro"},
    {"text": "El resultado del tratamiento se verá con los días.", "expected": "Neutro"}
]

# 3. Función de prueba
def run_benchmark():
    try:
        model = joblib.load(os.path.join(BASE_DIR, "data", "models", "sentiment_model.pkl"))
        vectorizer = joblib.load(os.path.join(BASE_DIR, "data", "models", "tfidf_vectorizer.pkl"))
    except:
        print("Modelos no encontrados.")
        return

    correctos = 0
    fallos = []
    
    # Solo imprimimos un resumen para no saturar
    for i, d in enumerate(data, 1):
        res, prob, meta = analizar_sentimiento_hibrido(d['text'], model, vectorizer)
        expected = d['expected'].split('/')[0].strip().replace('Positiva', 'Positivo').replace('Negativa', 'Negativo').replace('Neutra', 'Neutro')
        
        ok = res.lower() == expected.lower()
        if ok:
            correctos += 1
        else:
            fallos.append((i, d['text'], expected, res, meta.get('explicabilidad')))

    acc = (correctos / len(data)) * 100
    print(f"\n--- BENCHMARK G68 (100 FRASES) ---")
    print(f"Precisión Total: {correctos}/{len(data)} ({acc:.2f}%)")
    
    if fallos:
        print(f"\nÚltimos 10 fallos detectados:")
        for f in fallos[-10:]:
            print(f"[{f[0]}] {f[1]} | E: {f[2]} | P: {f[3]}")

if __name__ == "__main__":
    run_benchmark()
