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

# --- DATASET CONSOLIDADO (200 FRASES NUEVAS) ---
dataset = [
    # BLOQUE 1: Bienestar, Spa y Retiros
    {"text": "El masaje de tejido profundo me dejó como nuevo.", "expected": "Positivo"},
    {"text": "La limpieza en las duchas deja mucho que desear.", "expected": "Negativo"},
    {"text": "El terapeuta no dijo ni una palabra, lo cual agradezco.", "expected": "Positivo"},
    {"text": "No hay suficientes toallas limpias en la zona de piscina.", "expected": "Negativo"},
    {"text": "El aroma a eucalipto en el sauna es muy relajante.", "expected": "Positivo"},
    {"text": "El agua del jacuzzi estaba turbia, me dio miedo entrar.", "expected": "Negativo"},
    {"text": "Me sentí un poco incómoda con la presión que ejerció la masajista.", "expected": "Negativo"},
    {"text": "La clase de yoga al amanecer es una experiencia mística.", "expected": "Positivo"},
    {"text": "¡Genial! El vapor del sauna no funciona y nadie avisa.", "expected": "Negativo"},
    {"text": "Un lugar decente para un spa de barrio.", "expected": "Neutro"},
    {"text": "La música del spa era demasiado alta para poder dormir.", "expected": "Negativo"},
    {"text": "Salí del facial con la cara roja y llena de granitos.", "expected": "Negativo"},
    {"text": "El personal de recepción del spa es un poco frío.", "expected": "Negativo"},
    {"text": "Las instalaciones son modernas pero el ambiente es gélido.", "expected": "Neutro"},
    {"text": "¡Qué delicia de exfoliación! Mi piel es seda.", "expected": "Positivo"},
    {"text": "¿Relajación? Con los gritos de los niños en el pasillo es imposible.", "expected": "Negativo"},
    {"text": "El vestuario es muy pequeño para tanta gente.", "expected": "Negativo"},
    {"text": "El paquete de 'Día de Spa' no incluye comida, un fallo.", "expected": "Neutro"},
    {"text": "Es el mejor retiro al que he ido en diez años.", "expected": "Positivo"},
    {"text": "El lodo del tratamiento olía a alcantarilla.", "expected": "Negativo"},
    {"text": "La iluminación tenue crea un ambiente muy íntimo.", "expected": "Positivo"},
    {"text": "Me cobraron un suplemento por el aceite que no pedí.", "expected": "Negativo"},
    {"text": "El instructor de meditación tiene una voz muy calmada.", "expected": "Positivo"},
    {"text": "Demasiado cloro en la piscina, me pican los ojos.", "expected": "Negativo"},
    {"text": "Hicieron un hueco en la agenda para atenderme, muy amables.", "expected": "Positivo"},
    {"text": "El té verde estaba frío cuando me lo sirvieron.", "expected": "Negativo"},
    {"text": "No entiendo el concepto de bienestar de este sitio.", "expected": "Neutro"},
    {"text": "El área de relax estaba llena de gente hablando por teléfono.", "expected": "Negativo"},
    {"text": "Las piedras calientes estaban quemando, casi lloro.", "expected": "Negativo"},
    {"text": "El precio es justo para la calidad del servicio.", "expected": "Neutro"},
    {"text": "¡Simplemente sublime! Repetiré el mes que viene.", "expected": "Positivo"},
    {"text": "Las zapatillas de cortesía son de cartón, literalmente.", "expected": "Negativo"},
    {"text": "El personal sabe mucho sobre anatomía y puntos de presión.", "expected": "Positivo"},
    {"text": "Un poco de moho en las esquinas del baño turco.", "expected": "Negativo"},
    {"text": "El masaje duró 40 minutos en vez de los 50 pagados.", "expected": "Negativo"},
    {"text": "Me quedé dormido de lo relajado que estaba.", "expected": "Positivo"},
    {"text": "El tratamiento de vitamina C no hace absolutamente nada.", "expected": "Negativo"},
    {"text": "Hay que reservar con meses de antelación, muy difícil.", "expected": "Neutro"},
    {"text": "La zona de hamacas es muy cómoda y silenciosa.", "expected": "Positivo"},
    {"text": "Me duele más la espalda ahora que antes de entrar.", "expected": "Negativo"},
    {"text": "Qué gran idea poner incienso de sándalo, me encanta.", "expected": "Positivo"},
    {"text": "La recepcionista me hizo esperar mientras hablaba con su novio.", "expected": "Negativo"},
    {"text": "Un retiro espiritual que se siente como un campamento militar.", "expected": "Negativo"},
    {"text": "La manicura me duró apenas dos días.", "expected": "Negativo"},
    {"text": "Todo impecable, desde la entrada hasta la salida.", "expected": "Positivo"},
    {"text": "No tienen opciones de masajes para embarazadas.", "expected": "Neutro"},
    {"text": "Es un lujo que uno se debe permitir de vez en cuando.", "expected": "Positivo"},
    {"text": "El ruido de las obras de al lado arruinó la meditación.", "expected": "Negativo"},
    {"text": "No me gustó el aceite que usaron, era muy pegajoso.", "expected": "Negativo"},
    {"text": "Salí renovado por dentro y por fuera.", "expected": "Positivo"},

    # BLOQUE 2: Hospitalidad
    {"text": "La cama era tan cómoda que no quería levantarme.", "expected": "Positivo"},
    {"text": "Encontré un pelo en la almohada, qué falta de higiene.", "expected": "Negativo"},
    {"text": "El aire acondicionado gotea y hace un charco en el suelo.", "expected": "Negativo"},
    {"text": "La vista desde el balcón es lo único que vale la pena.", "expected": "Negativo"},
    {"text": "El personal de botones fue extremadamente servicial.", "expected": "Positivo"},
    {"text": "¡Qué bien! El Wi-Fi solo funciona si sales al pasillo.", "expected": "Negativo"},
    {"text": "La habitación es mucho más pequeña que en las fotos.", "expected": "Negativo"},
    {"text": "Desayuno variado y con productos locales de calidad.", "expected": "Positivo"},
    {"text": "El ascensor tarda una eternidad, acabé subiendo por la escalera.", "expected": "Negativo"},
    {"text": "Hotel funcional para un viaje de negocios rápido.", "expected": "Neutro"},
    {"text": "El check-out a las 10:00 am es demasiado temprano.", "expected": "Negativo"},
    {"text": "Nos dejaron una botella de cava por nuestro aniversario.", "expected": "Positivo"},
    {"text": "Las paredes son de papel, se oye hasta la respiración del vecino.", "expected": "Negativo"},
    {"text": "Ubicación inmejorable, cerca de todo lo importante.", "expected": "Positivo"},
    {"text": "El 'minibar' estaba vacío y hacía un ruido infernal.", "expected": "Negativo"},
    {"text": "Pedimos servicio de habitaciones y tardaron dos horas.", "expected": "Negativo"},
    {"text": "La decoración es de los años 70, necesita una reforma urgente.", "expected": "Negativo"},
    {"text": "El agua de la ducha sale con poca presión.", "expected": "Negativo"},
    {"text": "El parking es carísimo para los huéspedes del hotel.", "expected": "Negativo"},
    {"text": "Me sentí muy seguro gracias a la seguridad del recinto.", "expected": "Positivo"},
    {"text": "Qué sorpresa, la habitación no estaba lista cuando llegamos.", "expected": "Negativo"},
    {"text": "El recepcionista nocturno no habla ni una palabra de español.", "expected": "Negativo"},
    {"text": "Las sábanas estaban impecables y olían a flores.", "expected": "Positivo"},
    {"text": "El ruido de la calle no deja pegar ojo en toda la noche.", "expected": "Negativo"},
    {"text": "Es un hotel con encanto pero con un servicio mediocre.", "expected": "Neutro"},
    {"text": "No entiendo por qué cobran por el uso de la caja fuerte.", "expected": "Negativo"},
    {"text": "El café del desayuno es imbebible, parece agua sucia.", "expected": "Negativo"},
    {"text": "La piscina de la azotea es pequeña pero tiene buenas vistas.", "expected": "Positivo"},
    {"text": "El personal de limpieza es muy educado y discreto.", "expected": "Positivo"},
    {"text": "¡Pánico total! Saltó la alarma de incendios a las 3 AM por error.", "expected": "Negativo"},
    {"text": "Reservamos una suite y nos dieron una estándar por 'error'.", "expected": "Negativo"},
    {"text": "El sofá cama es un instrumento de tortura medieval.", "expected": "Negativo"},
    {"text": "El jardín está muy bien cuidado, da gusto pasear por él.", "expected": "Positivo"},
    {"text": "Me cobraron el desayuno que supuestamente estaba incluido.", "expected": "Negativo"},
    {"text": "Un sitio tranquilo, ideal para desconectar del mundo.", "expected": "Positivo"},
    {"text": "No hay rampas para sillas de ruedas, nada accesible.", "expected": "Negativo"},
    {"text": "El olor a tabaco en la habitación era muy fuerte.", "expected": "Negativo"},
    {"text": "Nos permitieron hacer el check-in antes de tiempo, un detalle.", "expected": "Positivo"},
    {"text": "El baño es tan pequeño que apenas puedes moverte.", "expected": "Negativo"},
    {"text": "La luz de emergencia de la habitación brilla como el sol.", "expected": "Negativo"},
    {"text": "Un 10 en todo, no se puede pedir más.", "expected": "Positivo"},
    {"text": "El televisor no funcionaba y nadie vino a arreglarlo.", "expected": "Negativo"},
    {"text": "Se respira un ambiente muy familiar y acogedor.", "expected": "Positivo"},
    {"text": "Mucho ruido en los pasillos durante la madrugada.", "expected": "Negativo"},
    {"text": "El servicio de lavandería perdió mi camisa favorita.", "expected": "Negativo"},
    {"text": "Las zonas comunes son amplias y luminosas.", "expected": "Positivo"},
    {"text": "Es un hotel pretencioso para lo que realmente ofrece.", "expected": "Negativo"},
    {"text": "El buffet se queda sin comida si vas tarde.", "expected": "Negativo"},
    {"text": "Me atendieron con una sonrisa a pesar de llegar tardísimo.", "expected": "Positivo"},
    {"text": "Nunca más me hospedaré en esta cadena de hoteles.", "expected": "Negativo"},

    # BLOQUE 3: Sarcasmo e Ironía
    {"text": "¡Genial! Otra noche sin dormir gracias a la fiesta del bar.", "expected": "Negativo"},
    {"text": "Me encanta que la 'suite de lujo' tenga vistas a un callejón con basura.", "expected": "Negativo"},
    {"text": "El personal es tan eficiente que tardaron 20 minutos en darme la llave.", "expected": "Negativo"},
    {"text": "¡Bravo! El 'zumo natural' venía directamente de un cartón barato.", "expected": "Negativo"},
    {"text": "Me fascinó encontrar una mancha misteriosa en la alfombra.", "expected": "Negativo"},
    {"text": "Qué detalle que el recepcionista no me saludara al entrar.", "expected": "Negativo"},
    {"text": "Un lujo total: una toalla para tres personas.", "expected": "Negativo"},
    {"text": "La calefacción funciona tan bien que tuve que dormir con abrigo.", "expected": "Negativo"},
    {"text": "¡Qué rapidez! Solo tres llamadas para que me trajeran agua.", "expected": "Negativo"},
    {"text": "Me encanta pagar por servicios que están 'fuera de servicio'.", "expected": "Negativo"},
    {"text": "Un 'oasis de paz' si por paz entiendes vivir dentro de una obra.", "expected": "Negativo"},
    {"text": "El servicio es tan personalizado que ni siquiera sabían mi nombre.", "expected": "Negativo"},
    {"text": "¡Increíble! El spa estaba tan lleno que parecía el metro en hora punta.", "expected": "Negativo"},
    {"text": "Gracias por la cena 'gourmet': un sándwich de jamón seco.", "expected": "Negativo"},
    {"text": "El diseño es tan minimalista que se olvidaron de poner sillas.", "expected": "Negativo"},
    {"text": "¡Qué suerte! El único día que llueve y el techo tiene goteras.", "expected": "Negativo"},
    {"text": "Me encanta que el Wi-Fi tenga la velocidad de una tortuga cansada.", "expected": "Negativo"},
    {"text": "Una experiencia 'inolvidable' por todas las razones equivocadas.", "expected": "Negativo"},
    {"text": "¡Qué bien entrenados! Todos los empleados fingen que no te ven.", "expected": "Negativo"},
    {"text": "El gimnasio es excelente si tu rutina consiste en mirar una pared.", "expected": "Negativo"},
    {"text": "La 'piscina infinita' es infinita en su falta de mantenimiento.", "expected": "Negativo"},
    {"text": "Gracias por dejarme el jabón usado del huésped anterior.", "expected": "Negativo"},
    {"text": "Un concepto de hotel 'ecológico' donde no hay ni papel higiénico.", "expected": "Negativo"},
    {"text": "¡Qué nivel! El camarero me tiró el café encima y ni pidió perdón.", "expected": "Negativo"},
    {"text": "La cama era tan suave que me hundí hasta el suelo.", "expected": "Negativo"},
    {"text": "Me fascinó la colección de polvo debajo de la cama.", "expected": "Negativo"},
    {"text": "El 'aire acondicionado' es en realidad un ventilador roto.", "expected": "Negativo"},
    {"text": "¡Qué oferta! Pagué por una habitación con ventana y me dieron un sótano.", "expected": "Negativo"},
    {"text": "El servicio de habitaciones es tan rápido que la comida llegó fría.", "expected": "Negativo"},
    {"text": "Un sitio ideal si odias la comodidad y el buen trato.", "expected": "Negativo"},
    {"text": "¡Felicidades! Lograron que un día de relax fuera una pesadilla.", "expected": "Negativo"},
    {"text": "Qué detalle cobrarme 5 euros por una botella de agua de 50 céntimos.", "expected": "Negativo"},
    {"text": "El 'balcón privado' se comparte con el vecino de al lado.", "expected": "Negativo"},
    {"text": "¡Bravo! El masaje de pies consistió en hacerme cosquillas.", "expected": "Negativo"},
    {"text": "Me encanta que la tele solo tenga canales en un idioma que no hablo.", "expected": "Negativo"},
    {"text": "Una limpieza impecable... si eres una araña.", "expected": "Negativo"},
    {"text": "El hotel es tan rústico que no tiene ni electricidad estable.", "expected": "Negativo"},
    {"text": "¡Qué sorpresa! El restaurante está cerrado 'por vacaciones' sin avisar.", "expected": "Negativo"},
    {"text": "La atención al cliente brilla por su ausencia, literalmente.", "expected": "Negativo"},
    {"text": "¡Qué maravilla esperar 40 minutos por un taxi pedido por el hotel!", "expected": "Negativo"},
    {"text": "Gracias por los tapones para los oídos, los necesité por vuestra culpa.", "expected": "Negativo"},
    {"text": "El 'jacuzzi' es en realidad una bañera con burbujas de juguete.", "expected": "Negativo"},
    {"text": "¡Qué elegancia! El uniforme del personal está lleno de manchas.", "expected": "Negativo"},
    {"text": "El check-in fue tan fluido que solo tardamos una hora.", "expected": "Negativo"},
    {"text": "Me encanta el estilo 'vintage' de las alfombras comidas por la polilla.", "expected": "Negativo"},
    {"text": "¡Qué gran idea poner la discoteca debajo de las habitaciones!", "expected": "Negativo"},
    {"text": "El desayuno es 'continental': un café y mucha imaginación.", "expected": "Negativo"},
    {"text": "Me fascinó que el personal se riera de mi queja.", "expected": "Negativo"},
    {"text": "Un lugar 'encantador' si te gustan las películas de terror.", "expected": "Negativo"},
    {"text": "Gracias por arruinar mi descanso de la manera más profesional posible.", "expected": "Negativo"},

    # BLOQUE 4: Ambigüedad y Críticas
    {"text": "No sé si volvería, tengo sentimientos encontrados.", "expected": "Neutro"},
    {"text": "¡Ayuda! Me han robado el bolso en el lobby del hotel.", "expected": "Negativo"},
    {"text": "El lugar es aceptable si no tienes expectativas altas.", "expected": "Neutro"},
    {"text": "¡Fuego! Vimos salir humo de la cocina y nadie evacuaba.", "expected": "Negativo"},
    {"text": "Es un hotel que cumple su función sin más pretensiones.", "expected": "Neutro"},
    {"text": "¿Dónde está mi reserva? Dicen que no existo en el sistema.", "expected": "Negativo"},
    {"text": "Ni bien ni mal, simplemente un sitio para dormir.", "expected": "Neutro"},
    {"text": "¡Es urgente! Mi hijo tiene alergia y la habitación tiene moho.", "expected": "Negativo"},
    {"text": "La experiencia depende mucho de quién te atienda ese día.", "expected": "Neutro"},
    {"text": "Se me bloqueó la puerta y llevo 20 minutos fuera en pijama.", "expected": "Negativo"},
    {"text": "El estilo es ecléctico, no es para todo el mundo.", "expected": "Neutro"},
    {"text": "¡Rápido! El calentador ha explotado y sale agua por todas partes.", "expected": "Negativo"},
    {"text": "Me pregunto si las reseñas positivas son reales.", "expected": "Negativo"},
    {"text": "No encuentro al personal por ninguna parte, el hotel parece vacío.", "expected": "Negativo"},
    {"text": "Las sábanas tienen un tacto extraño, no sé de qué material son.", "expected": "Neutro"},
    {"text": "¡Alerta! Me han cobrado 500 euros de más en la tarjeta.", "expected": "Negativo"},
    {"text": "El precio fluctuó tres veces antes de que pudiera pagar.", "expected": "Negativo"},
    {"text": "Es difícil calificar este sitio con una sola palabra.", "expected": "Neutro"},
    {"text": "¡Socorro! Hay un insecto gigante en mi cama.", "expected": "Negativo"},
    {"text": "El horario de apertura es un poco confuso para los turistas.", "expected": "Neutro"},
    {"text": "No es lo mejor que he visto, pero he estado en sitios peores.", "expected": "Neutro"},
    {"text": "¡Necesito un médico! Me he mareado en el sauna.", "expected": "Negativo"},
    {"text": "El diseño del edificio es muy confuso, es fácil perderse.", "expected": "Negativo"},
    {"text": "Las opiniones en internet me engañaron totalmente.", "expected": "Negativo"},
    {"text": "Se siente como si el tiempo se hubiera detenido en este lugar.", "expected": "Neutro"},
    {"text": "¡Llamen a la policía! Alguien ha forzado mi caja fuerte.", "expected": "Negativo"},
    {"text": "No estoy seguro de si la limpieza fue profunda o superficial.", "expected": "Neutro"},
    {"text": "Es un establecimiento que requiere paciencia por parte del cliente.", "expected": "Negativo"},
    {"text": "¡Emergencia! No hay agua en todo el hotel y estoy enjabonado.", "expected": "Negativo"},
    {"text": "El ambiente es... peculiar, no sabría cómo describirlo.", "expected": "Neutro"},
    {"text": "El recepcionista parece que está trabajando a la fuerza.", "expected": "Negativo"},
    {"text": "¡Cuidado! Las escaleras resbalan muchísimo y no hay carteles.", "expected": "Negativo"},
    {"text": "Una opción razonable para presupuestos ajustados.", "expected": "Positivo"},
    {"text": "No sé si recomendarlo o advertir a la gente que no venga.", "expected": "Neutro"},
    {"text": "¡Qué angustia! El aire acondicionado no para de hacer un pitido.", "expected": "Negativo"},
    {"text": "Es un hotel con mucha personalidad, pero poca organización.", "expected": "Neutro"},
    {"text": "¡Por favor! Que alguien traiga las llaves de mi habitación.", "expected": "Negativo"},
    {"text": "La calidad ha bajado mucho desde la última vez que vine.", "expected": "Negativo"},
    {"text": "No entiendo la política de mascotas del establecimiento.", "expected": "Neutro"},
    {"text": "Se escuchan ruidos metálicos que vienen de las tuberías.", "expected": "Negativo"},
    {"text": "La recepción está cerrada de 2 a 4 de la tarde.", "expected": "Neutro"},
    {"text": "El trato es correcto, sin grandes alardes de simpatía.", "expected": "Neutro"},
    {"text": "Me falta información sobre las excursiones que ofrecen.", "expected": "Neutro"},
    {"text": "El edificio necesita una mano de pintura urgentemente.", "expected": "Negativo"},
    {"text": "Hay que pagar un depósito en efectivo al llegar.", "expected": "Neutro"},
    {"text": "Se echa de menos un poco más de luz en los pasillos.", "expected": "Negativo"},
    {"text": "La conexión a internet es inestable por las tardes.", "expected": "Negativo"},
    {"text": "El recepcionista nos ignoró durante diez minutos.", "expected": "Negativo"},
    {"text": "No sabría decir si me ha gustado o no la experiencia.", "expected": "Neutro"},
    {"text": "El hotel se siente un poco desangelado por las noches.", "expected": "Neutro"}
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
print(f"--- NUEVO BENCHMARK 200 FRASES (G68 ULTIMATE) ---")
print(f"Total phrases: {len(dataset)} | Blocks: {len(blocks)} | Window: {block_size}\n")

for idx, block in enumerate(blocks, 1):
    correctos = 0
    fail_list = []
    for item in block:
        res, prob, meta = analizar_sentimiento_hibrido(item['text'], model, vectorizer)
        if res.lower() == item['expected'].lower():
            correctos += 1
        else:
            fail_list.append((item['text'], item['expected'], res))
    
    accuracy = (correctos / len(block)) * 100
    print(f"BLOQUE {idx}: {correctos}/{len(block)} OK ({accuracy:.2f}%)")
    
print("\n--- FIN DEL LABORATORIO ---")
