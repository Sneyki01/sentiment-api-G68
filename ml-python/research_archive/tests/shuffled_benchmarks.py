import os
import sys
import joblib
import random
import math
import re

# 1. Configurar rutas para importar el motor
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, "src"))

from engine.sentiment_engine import analizar_sentimiento_hibrido

# --- DATASET CONSOLIDADO (150 FRASES) ---
dataset = [
    # Bloque 1: Bienestar y Hospitalidad (50)
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

    # Bloque 2: Ambigüedad y Neutralidad (50)
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
    {"text": "El resultado del tratamiento se verá con los días.", "expected": "Neutro"},

    # Bloque 3: Sarcasmo, Estrés y Neutralidad V3 (50)
    {"text": "¡Espectacular! Jamás me habían tratado con tanto cariño y profesionalismo.", "expected": "Positivo"},
    {"text": "Una experiencia para olvidar; salí con más nudos en la espalda de los que traía.", "expected": "Negativo"},
    {"text": "El hotel cumplió con las especificaciones técnicas de la reserva.", "expected": "Neutro"},
    {"text": "¡Qué maravilla! La 'piscina climatizada' estaba perfecta para entrenar pingüinos.", "expected": "Negativo"},
    {"text": "¡Urgente! Llevo una hora encerrado en el ascensor y nadie responde al timbre.", "expected": "Negativo"},
    {"text": "El aroma del spa es... difícil de definir, algo así como incienso con vinagre.", "expected": "Neutro"},
    {"text": "Gracias por hacerme sentir como una reina en mi propio cumpleaños.", "expected": "Positivo"},
    {"text": "¿A esto le llaman buffet? Había más moscas que opciones de comida.", "expected": "Negativo"},
    {"text": "El check-in se realiza a las 15:00 y el check-out a las 11:00.", "expected": "Neutro"},
    {"text": "Me encanta pagar una fortuna para que la recepcionista me ignore totalmente.", "expected": "Negativo"},
    {"text": "Siento una paz inmensa, este retiro ha cambiado mi perspectiva de vida.", "expected": "Positivo"},
    {"text": "¡Es un caos! Perdieron mi maleta y tengo una boda en dos horas.", "expected": "Negativo"},
    {"text": "El diseño del lobby es minimalista, quizás demasiado vacío para mi gusto.", "expected": "Neutro"},
    {"text": "Bravo, lograron que un masaje de relajación me dejara moretones.", "expected": "Negativo"},
    {"text": "El personal es tan amable que casi da vergüenza pedirles nada.", "expected": "Positivo"},
    {"text": "No hay Wi-Fi, no hay señal, no hay esperanza de comunicarse aquí.", "expected": "Negativo"},
    {"text": "La temperatura de la habitación se mantiene constante a 22 grados.", "expected": "Neutro"},
    {"text": "Qué gran detalle: me cobraron el gimnasio que estuvo cerrado por obras.", "expected": "Negativo"},
    {"text": "Llevo 30 minutos esperando mi café, mi paciencia está al límite.", "expected": "Negativo"},
    {"text": "El tratamiento facial fue 'interesante', aunque no noto ningún cambio.", "expected": "Neutro"},
    {"text": "¡Sublime! El mejor regalo que me he hecho en años.", "expected": "Positivo"},
    {"text": "Sucio, ruidoso y caro. No vuelvo ni aunque me paguen ellos a mí.", "expected": "Negativo"},
    {"text": "Hay un cuadro de un payaso en la habitación que da un poco de miedo.", "expected": "Neutro"},
    {"text": "¡Genial! El aire acondicionado suena como un avión despegando.", "expected": "Negativo"},
    {"text": "Necesito hablar con el gerente de inmediato, esto es una estafa.", "expected": "Negativo"},
    {"text": "La clase de yoga fue dirigida por un instructor certificado.", "expected": "Neutro"},
    {"text": "Mi piel brilla como nunca, el equipo de estética es de otro planeta.", "expected": "Positivo"},
    {"text": "El agua del jacuzzi estaba tibia, ni fría ni caliente.", "expected": "Neutro"},
    {"text": "¿La vista al mar? Sí, si te asomas por la ventana y usas un telescopio.", "expected": "Negativo"},
    {"text": "Tengo el corazón en la garganta, me han cobrado tres veces la estancia.", "expected": "Negativo"},
    {"text": "Es un lugar correcto si lo que buscas es simplemente dormir.", "expected": "Neutro"},
    {"text": "Increíble que en pleno siglo XXI no acepten pagos con tarjeta.", "expected": "Negativo"},
    {"text": "La música de ambiente es una selección de éxitos de los años 80.", "expected": "Neutro"},
    {"text": "¡Qué lujo! La sábana tenía un agujero para que el pie respire.", "expected": "Negativo"},
    {"text": "Por fin he dormido 8 horas seguidas, la cama es una nube.", "expected": "Positivo"},
    {"text": "El recepcionista me miró como si le debiera dinero.", "expected": "Negativo"},
    {"text": "Por favor, ¡que alguien baje la música! No puedo más con este dolor de cabeza.", "expected": "Negativo"},
    {"text": "Las toallas son blancas y de algodón egipcio según la etiqueta.", "expected": "Neutro"},
    {"text": "Maravilloso el concepto de 'baño compartido' que no mencionaron al reservar.", "expected": "Negativo"},
    {"text": "El zumo de naranja tenía un sabor metálico muy extraño.", "expected": "Negativo"},
    {"text": "Salí renovada, el circuito hídrico es de lo mejor de la ciudad.", "expected": "Positivo"},
    {"text": "El hotel es rústico, si por rústico entiendes que se cae a pedazos.", "expected": "Negativo"},
    {"text": "Hay una gran diferencia entre lo que prometen y lo que dan.", "expected": "Negativo"},
    {"text": "Me siento muy ansioso, la habitación no tiene ventanas al exterior.", "expected": "Negativo"},
    {"text": "El desayuno incluye fruta de temporada y pan artesanal.", "expected": "Neutro"},
    {"text": "¡Un sueño! No quería despertarme nunca de esa camilla.", "expected": "Positivo"},
    {"text": "La atención es tan lenta que parece que trabajan a cámara lenta.", "expected": "Negativo"},
    {"text": "El edificio tiene una arquitectura ecléctica y colores vibrantes.", "expected": "Neutro"},
    {"text": "Qué buena suerte la mía, el único día que vengo y el sauna explota.", "expected": "Negativo"},
    {"text": "Me voy con una sonrisa y la energía renovada, ¡gracias equipo!", "expected": "Positivo"}
]

# 2. Mezclar y Dividir
random.shuffle(dataset)
block_size = 50
blocks = [dataset[i:i + block_size] for i in range(0, len(dataset), block_size)]

# 3. Cargar Modelos
try:
    model = joblib.load(os.path.join(BASE_DIR, "data", "models", "sentiment_model.pkl"))
    vectorizer = joblib.load(os.path.join(BASE_DIR, "data", "models", "tfidf_vectorizer.pkl"))
except Exception as e:
    print(f"Error cargando modelos: {e}")
    sys.exit(1)

# 4. Ejecutar Pruebas por Bloque
print(f"--- PRUEBA DE BENCHMARKS ALEATORIOS (G68 ULTIMATE) ---")
print(f"Total de frases: {len(dataset)} | Bloques: {len(blocks)} | Tamaño: {block_size}\n")

for idx, block in enumerate(blocks, 1):
    correctos = 0
    print(f"BLOQUE {idx}: Evaluando...")
    for item in block:
        res, prob, meta = analizar_sentimiento_hibrido(item['text'], model, vectorizer)
        if res.lower() == item['expected'].lower():
            correctos += 1
    
    accuracy = (correctos / len(block)) * 100
    print(f"   > Resultado: {correctos}/{len(block)} correctos ({accuracy:.2f}%)\n")

print("--- FIN DE LAS PRUEBAS ---")
