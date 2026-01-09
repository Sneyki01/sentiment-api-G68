import os
import sys
import joblib
import pandas as pd

# Configurar rutas para importar el motor
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, "src"))

from engine.sentiment_engine import analizar_sentimiento_hibrido

def run_blind_test():
    # Dataset generado por Gemini (100 frases virgenes)
    dataset_gemini = [
        # 30 Positivas
        ("La domótica de la habitación es de otro planeta; luces, persianas y clima se ajustan con un susurro.", "Positivo"),
        ("El purificador de aire con filtro HEPA en el cuarto es un detalle de salud que se agradece muchísimo.", "Positivo"),
        ("Desayuno de autor con huevos benedictinos sobre cama de aguacate orgánico, simplemente exquisito.", "Positivo"),
        ("Insonorización técnica impecable: a milímetros de la Gran Vía y el silencio es absoluto.", "Positivo"),
        ("El kit de bienvenida para mi perro incluía una cama de viscoelástica y snacks premium, un puntazo.", "Positivo"),
        ("Mobiliario diseñado por arquitectos de renombre, se respira un lujo contemporáneo soberbio.", "Positivo"),
        ("Ducha de cromoterapia y presión regulable que te deja como nuevo después de un vuelo largo.", "Positivo"),
        ("La sostenibilidad no es solo un cartel; sistema de aguas grises y cero plásticos de un solo uso.", "Positivo"),
        ("Smart mirror en el baño con noticias y tiempo mientras te afeitas, ¡qué nivel de detalle!", "Positivo"),
        ("El rooftop tiene una carta de coctelería molecular que es una auténtica locura sensorial.", "Positivo"),
        ("Trato personalizado de guante blanco; sabían mi nombre y mis preferencias desde el minuto uno.", "Positivo"),
        ("Camas con sábanas de 1000 hilos de algodón egipcio, dormir aquí es como flotar en una nube.", "Positivo"),
        ("Carga inalámbrica en todas las mesitas de noche y enchufes USB-C por doquier, muy funcional.", "Positivo"),
        ("El jardín vertical del lobby crea un microclima de paz en medio del caos urbano.", "Positivo"),
        ("Gimnasio con máquinas Peloton y zona de yoga con vistas a la catedral, de primera.", "Positivo"),
        ("Servicio de mayordomía digital vía WhatsApp rápido y extremadamente eficiente.", "Positivo"),
        ("Cafetera de cápsulas artesanales y minibar con productos de km cero, una delicia.", "Positivo"),
        ("Toallas de alto gramaje que te abrazan después de un baño en la piscina climatizada.", "Positivo"),
        ("La biblioteca del hotel es un refugio cultural con ediciones raras y un olor a papel antiguo mágico.", "Positivo"),
        ("Wifi 6 con velocidades de vértigo, ideal para nómadas digitales que no podemos permitirnos cortes.", "Positivo"),
        ("Piscina de sal con hilo musical subacuático, una experiencia de relax sobresaliente.", "Positivo"),
        ("Menú de almohadas con 6 opciones distintas para garantizar un descanso a medida.", "Positivo"),
        ("Iluminación circadiana que ayuda a mitigar el jet lag de forma natural, pura ciencia aplicada.", "Positivo"),
        ("Check-in facial súper ágil, en menos de un minuto estaba ya camino a mi suite.", "Positivo"),
        ("El parking incluye cargadores Tesla de carga rápida sin coste adicional, un lujo necesario.", "Positivo"),
        ("Personal políglota con una cultura exquisita que te recomienda joyas ocultas de la ciudad.", "Positivo"),
        ("Amenities de marca nicho con fragancias de aceites esenciales que son adictivas.", "Positivo"),
        ("El concepto de 'open bar' de meriendas saludables es un detalle de categoría superior.", "Positivo"),
        ("Suite con techos de 4 metros y ventanales motorizados, amplitud y luz que enamorar.", "Positivo"),
        ("Un oasis moderno que redefine el concepto de hospitalidad de lujo en el siglo XXI.", "Positivo"),

        # 30 Neutras/Mixtas
        ("La estética del hotel es rompedora, pero la funcionalidad del baño deja algo que desear.", "Neutro"),
        ("Desayuno variado y de calidad, aunque el servicio de café fue un poco atropellado por la afluencia.", "Neutro"),
        ("Ubicación inmejorable en pleno centro, pero el ruido nocturno del barrio es una maza constante.", "Neutro"),
        ("Habitación amplia y moderna, si bien el colchón me pareció un pelín más duro de lo habitual.", "Neutro"),
        ("Personal de recepción encantador, pero el proceso de facturación final fue algo lento.", "Neutro"),
        ("El spa es una maravilla arquitectónica, aunque el aforo limitado hace que sea difícil disfrutarlo.", "Neutro"),
        ("Precios competitivos para la zona, a pesar de que las dimensiones del gimnasio son reducidas.", "Neutro"),
        ("Vistas espectaculares desde el balcón, pero la limpieza de los cristales podría mejorar.", "Neutro"),
        ("Cena en el restaurante deliciosa, aunque las raciones me parecieron de poca monta para el precio.", "Neutro"),
        ("Edificio con mucha historia y encanto, sin embargo los ascensores son algo pequeños y lentos.", "Neutro"),
        ("Wifi gratuito de buena velocidad, pero la cobertura en la planta 4 era bastante errática.", "Neutro"),
        ("Amenities de lujo en el baño, pero el dispensador de la ducha estaba encasquillado.", "Neutro"),
        ("Ambiente tranquilo y sofisticado, aunque la iluminación de los pasillos es algo lúgubre.", "Neutro"),
        ("Late check-out concedido, pero nos llamaron dos veces de limpieza antes de la hora acordada.", "Neutro"),
        ("La piscina tiene un diseño increíble, pero el agua estaba tirando a fría para ser climatizada.", "Neutro"),
        ("Cerca de los principales museos, pero la zona es algo impersonal y falta de comercios locales.", "Neutro"),
        ("El diseño de la suite es minimalista y elegante, aunque faltan huecos para dejar la maleta.", "Neutro"),
        ("Cafetera en la habitación de gran marca, pero solo te dejan dos cápsulas de cortesía.", "Neutro"),
        ("Mucho personal disponible, pero a veces se siente que el trato es un poco guionizado.", "Neutro"),
        ("Toallas suaves y esponjosas, aunque el tamaño me resultó algo pequeño para un 5 estrellas.", "Neutro"),
        ("Ideal para viajes de negocios, pero falto de calidez para una escapada romántica en pareja.", "Neutro"),
        ("Buena presión de agua, pero el ajuste de la temperatura era una lucha de extremos.", "Neutro"),
        ("El parking es seguro y amplio, pero el acceso desde la calle es un laberinto confuso.", "Neutro"),
        ("Televisión de gran formato, pero el sistema de canales internacionales era muy limitado.", "Neutro"),
        ("Decoración vanguardista en zonas comunes, si bien las habitaciones tiran a clásicas y sobrias.", "Neutro"),
        ("Servicio de habitaciones rápido, pero el menú es algo corto y sin opciones saludables.", "Neutro"),
        ("Lado positivo: el trato del personal; lado negativo: el mantenimiento de las ventanas.", "Neutro"),
        ("Correcto para una noche de escala, pero no le pidas mucho más en cuanto a servicios.", "Neutro"),
        ("Se nota el esfuerzo por ser sostenibles, aunque todavía usan botellas de plástico en el bar.", "Neutro"),
        ("Buen aislamiento térmico en invierno, pero el panel del aire acondicionado hace un ruido seco.", "Neutro"),

        # 25 Negativas Sarcasmo
        ("Increíble 'piscina climatizada', ideal si quieres entrenar para una expedición al Ártico.", "Negativo"),
        ("Gracias por la 'sinfonía urbana' de martillazos a las 8 de la mañana en el pasillo, muy zen.", "Negativo"),
        ("La 'vista panorámica' incluía un primer plano inolvidable de la caldera de la comunidad vecina.", "Negativo"),
        ("Excelente concepto de 'minibar minimalista': una botella de agua tibia y mucho aire acondicionado.", "Negativo"),
        ("Me encantó el detalle de la 'alfombra con historia', parece que guarda manchas de la Expo del 92.", "Negativo"),
        ("Un 10 al servicio de habitaciones por su paciencia; esperé dos horas para una manta y nunca llegó.", "Negativo"),
        ("La 'conexión wifi de alta velocidad' me permitió viajar al pasado y recordar los tiempos del módem.", "Negativo"),
        ("Elegante búnker sin ventanas donde puedes perder la noción del tiempo y de la salud mental.", "Negativo"),
        ("Maravillosa habitación 'vintage' donde el moho de las esquinas es ya un elemento decorativo.", "Negativo"),
        ("Gracias por cobrarme 20 euros por el parking; por ese precio esperaba que me lavaran el coche.", "Negativo"),
        ("El personal es tan discreto que el botones estuvo pegado a su móvil ignorándome por completo.", "Negativo"),
        ("La cerradura electrónica es tan segura que ni con mi propia tarjeta pude entrar en tres intentos.", "Negativo"),
        ("Ducha con efecto 'sorpresa': hoy te quemas y mañana te hielas en cuestión de segundos.", "Negativo"),
        ("El buffet es un ejercicio de supervivencia: o llegas el primero o te alimentas de pan duro.", "Negativo"),
        ("Qué lujo de 'toallas exfoliantes', raspan tanto que me he ahorrado ir al dermatólogo.", "Negativo"),
        ("Si te gusta el riesgo, las escaleras del hotel tienen peldaños que bailan un tango al pisarlas.", "Negativo"),
        ("La insonorización es tan buena que escuché perfectamente el estornudo del huésped de al lado.", "Negativo"),
        ("Gracias por el 'aire acondicionado ecológico' (o eso dicen porque no encendía ni a tiros).", "Negativo"),
        ("El 'servicio de té' consistía en un hervidor con cal y dos sobres de azúcar de hace una década.", "Negativo"),
        ("El jardín es un cementerio de plantas secas que inspira una melancolía literaria profunda.", "Negativo"),
        ("Qué innovador no poner jabón en el baño; debe ser por la nueva tendencia de 'lavado con agua sola'.", "Negativo"),
        ("La cama era tan 'firme' que creo que dormí encima de un bloque de hormigón con sábanas.", "Negativo"),
        ("Un hotel de 4 estrellas con categoría de pensión de carretera, pero con precios de palacio real.", "Negativo"),
        ("Gracias por la 'experiencia detox' de no tener wifi ni cobertura en toda la maldita estancia.", "Negativo"),
        ("El recepcionista de noche es un maestro del suspense; te mira, calla y sigue durmiendo.", "Negativo"),

        # 15 Estrés/Crisis
        ("Me robaron el portátil de la habitación y la respuesta del hotel fue que 'el seguro no cubre descuidos'.", "Negativo"),
        ("Inundación total por una tubería rota a las 3 AM y nos dejaron en el lobby sin ropa de abrigo.", "Negativo"),
        ("Encontré una cucaracha en la almohada y me dijeron que era normal por ser una zona costera. Indignante.", "Negativo"),
        ("El recepcionista me gritó delante de otros clientes por pedir un cambio de habitación. Una humillación.", "Negativo"),
        ("Nos vendieron una habitación que ya estaba ocupada; entramos y había gente durmiendo. Un fallo de seguridad crítico.", "Negativo"),
        ("Fuerte olor a gas en el pasillo y nadie de mantenimiento aparecía. Tuvimos que llamar a los bomberos nosotros.", "Negativo"),
        ("Higiene nula: sábanas con manchas de sangre seca y paredes con moho negro. Me fui a los diez minutos.", "Negativo"),
        ("Se fue la luz y el sistema de emergencia no funcionó; atrapado en el ascensor 40 minutos en la oscuridad.", "Negativo"),
        ("Trato grosero, prepotente y hasta racista por parte del personal de seguridad. Una experiencia nefasta.", "Negativo"),
        ("Sobreventa total; nos mandaron a un hostal mugriento a 10 km después de tener una reserva pagada hace meses.", "Negativo"),
        ("El techo del baño se desplomó mientras mi hijo se duchaba. De milagro no hubo una desgracia.", "Negativo"),
        ("Intoxicación alimentaria tras el buffet del desayuno; tres de nosotros terminamos en urgencias.", "Negativo"),
        ("La puerta de la habitación no cerraba bien y el hotel se negó a arreglarla 'porque era domingo'.", "Negativo"),
        ("Si valoras tu seguridad y tu dinero, aléjate de esta estafa de hotel. Gestión peligrosa y delictiva.", "Negativo"),
        ("Me cargaron tres veces el importe de la estancia y me dicen que 'el jefe no está' para devolverlo.", "Negativo")
    ]

    # Cargar Modelos (G68 V8 ACTUAL)
    model_path = os.path.join(BASE_DIR, "data", "models", "sentiment_model.pkl")
    vectorizer_path = os.path.join(BASE_DIR, "data", "models", "tfidf_vectorizer.pkl")
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)

    print(f"--- 🕵️ TEST CIEGO DE HONESTIDAD G68 (100 frases nuevas) ---")
    correct = 0
    failures = []

    for i, (text, expected) in enumerate(dataset_gemini):
        pred, prob, meta = analizar_sentimiento_hibrido(text, model, vectorizer)
        if pred.lower() == expected.lower():
            correct += 1
        else:
            failures.append((i+1, text, expected, pred, prob))

    print(f"\nACCURACY CIEGA: {correct/len(dataset_gemini):.2%}")
    print(f"\n--- ANÁLISIS DE FALLOS (CRÍTICO) ---")
    for id, text, exp, pred, prob in failures:
        print(f"Id: {id:<2} | E: {exp[:3]} | P: {pred[:3]} | Prob: {prob:.2f} | {text[:70]}...")

if __name__ == "__main__":
    run_blind_test()
