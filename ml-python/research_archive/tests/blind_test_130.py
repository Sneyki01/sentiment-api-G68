import os
import sys
import joblib
import pandas as pd

# Configurar rutas para importar el motor
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, "src"))

from engine.sentiment_engine import analizar_sentimiento_hibrido

def run_blind_test_130():
    # Dataset de 130 reseñas proporcionado por el usuario
    dataset_130 = [
        # 🟢 15 Positivas
        ("Un hotel de ensueño, el servicio fue impecable de principio a fin.", "Positivo"),
        ("La cama más cómoda en la que he dormido nunca, ¡un 10!", "Positivo"),
        ("Ubicación perfecta y personal encantador, volveremos seguro.", "Positivo"),
        ("Todo brillante: limpieza, comida y trato. Totalmente recomendable.", "Positivo"),
        ("Un oasis de paz, las instalaciones son modernas y de lujo.", "Positivo"),
        ("Desayuno buffet exquisito, muchísima variedad y todo fresco.", "Positivo"),
        ("El equipo de recepción es súper eficiente, check-in en 2 minutos.", "Positivo"),
        ("Vistas espectaculares que valen cada céntimo que pagas.", "Positivo"),
        ("Habitación amplia, luminosa y con un diseño precioso.", "Positivo"),
        ("Excelente relación calidad-precio en pleno centro histórico.", "Positivo"),
        ("La piscina infinita es una maravilla, muy bien cuidada.", "Positivo"),
        ("El personal se desvive por ayudarte, trato muy humano.", "Positivo"),
        ("Todo impecable, la limpieza es de otro planeta.", "Positivo"),
        ("Wifi rápido y estable, ideal para nómadas digitales.", "Positivo"),
        ("Regalo de bienvenida y nota escrita a mano, detalles que enamoran.", "Positivo"),

        # 🔴 15 Negativas
        ("Una decepción absoluta, suciedad por todas partes.", "Negativo"),
        ("El personal fue grosero y maleducado desde que llegamos.", "Negativo"),
        ("Habitación minúscula y oscura, parecía una celda.", "Negativo"),
        ("Ruido insoportable toda la noche, no pudimos pegar ojo.", "Negativo"),
        ("Huele a tabaco rancio y humedad, una experiencia asquerosa.", "Negativo"),
        ("El buffet es una estafa: comida fría y de mala calidad.", "Negativo"),
        ("Instalaciones viejas y descuidadas, nada que ver con las fotos.", "Negativo"),
        ("Pagué por una suite y me dieron una habitación estándar.", "Negativo"),
        ("El baño perdía agua y el suelo estaba siempre empapado.", "Negativo"),
        ("Pésima gestión, perdieron mi reserva y no me dieron solución.", "Negativo"),
        ("Aire acondicionado roto en plena ola de calor, un infierno.", "Negativo"),
        ("Seguridad nula, cualquiera entra y sale como si nada.", "Negativo"),
        ("Caro para lo que ofrece, es un hostal con precio de 4 estrellas.", "Negativo"),
        ("Cucarachas en el pasillo, falta de higiene alarmante.", "Negativo"),
        ("No volvería ni aunque me pagaran por quedarme aquí.", "Negativo"),

        # 😫 20 de Stress
        ("¡Es una vergüenza! Llevo una hora esperando en recepción y nadie aparece.", "Negativo"),
        ("¡Auxilio! Se ha inundado el baño y el agua está llegando a la cama.", "Negativo"),
        ("¡Me siento estafado! Me han cobrado el doble y nadie me da una explicación.", "Negativo"),
        ("¡Inaceptable! Hay chinches en la cama, ¡exijo que me cambien de hotel ya!", "Negativo"),
        ("¡Basta ya de mentiras! Me dijeron que había parking y me han dejado en la calle.", "Negativo"),
        ("¡Peligro! El ascensor se ha quedado bloqueado y no contestan al timbre.", "Negativo"),
        ("¡Indignante! Han entrado en mi cuarto mientras estaba fuera y falta dinero.", "Negativo"),
        ("¡Es una pesadilla! El ruido de las obras es atronador desde las 6 AM.", "Negativo"),
        ("¡No aguantamos más! El olor a cloaca en la habitación es insoportable.", "Negativo"),
        ("¡Vergonzoso! Trato humillante por parte del gerente del hotel.", "Negativo"),
        ("¡Tengo un ataque de nervios! Mi reserva no aparece y todo está lleno en la ciudad.", "Negativo"),
        ("¡Desastre total! El techo gotea justo encima de mi maleta abierta.", "Negativo"),
        ("¡Es un timo! El spa está cerrado y no avisaron al hacer la reserva.", "Negativo"),
        ("¡Horrible! El colchón está hundido y me duele la espalda de forma terrible.", "Negativo"),
        ("¡Nadie me ayuda! El teléfono de recepción no funciona y estoy aislado.", "Negativo"),
        ("¡Cuidado! Cobran suplementos fantasmas al salir, son unos ladrones.", "Negativo"),
        ("¡Qué asco! Sábanas con manchas de sangre, ¡exijo una hoja de reclamaciones!", "Negativo"),
        ("¡Odisea! Tres horas para hacer el check-in, organización desastrosa.", "Negativo"),
        ("¡Incompetentes! Han perdido mi equipaje que dejaron en consigna.", "Negativo"),
        ("¡Basta! No hay agua caliente y hace un frío polar fuera.", "Negativo"),

        # ⚖️ 20 Neutras con Mezcla
        ("El hotel es precioso pero el personal del bar es bastante lento.", "Neutro"),
        ("Habitación muy limpia aunque el wifi solo funciona cerca de la puerta.", "Neutro"),
        ("Desayuno muy rico pero el espacio del buffet es demasiado pequeño.", "Neutro"),
        ("Cama cómoda, lástima que el aire acondicionado haga tanto ruido.", "Neutro"),
        ("Excelente ubicación, pero el precio es elevado para los servicios que da.", "Neutro"),
        ("Personal amable pero las instalaciones necesitan una reforma urgente.", "Neutro"),
        ("Vistas increíble, sin embargo el baño es antiguo y algo incómodo.", "Neutro"),
        ("Hotel tranquilo pero está muy lejos de cualquier restaurante o tienda.", "Neutro"),
        ("Check-in rápido aunque la habitación no era la que pedimos originalmente.", "Neutro"),
        ("Piscina bonita pero el agua está siempre llena de hojas y bichos.", "Neutro"),
        ("Diseño moderno pero poco funcional, no hay donde colgar las toallas.", "Neutro"),
        ("El buffet tiene calidad pero poca variedad si te quedas muchos días.", "Neutro"),
        ("Buena insonorización de la calle, pero se oye todo lo del pasillo.", "Neutro"),
        ("Te dan agua gratis el primer día, pero el resto te la cobran cara.", "Neutro"),
        ("Gimnasio bien equipado aunque le falta mantenimiento a las máquinas.", "Neutro"),
        ("El barrio es seguro pero de noche está demasiado oscuro para caminar.", "Neutro"),
        ("Servicio de limpieza impecable pero pasan a horas muy tempranas.", "Neutro"),
        ("Televisión de gran formato pero solo se ven canales locales.", "Neutro"),
        ("Parking propio pero la plaza es tan estrecha que apenas puedes salir.", "Neutro"),
        ("Estancia correcta, tiene cosas muy buenas y otras que deben mejorar.", "Neutro"),

        # 🌤️ 15 Neutras (Mayoría Positivas)
        ("Muy buena experiencia en general, quitando que el café podría ser mejor.", "Neutro"),
        ("Casi perfecto, solo le faltaría un poco más de presión a la ducha.", "Neutro"),
        ("Todo genial, el único pero es que el parking es de pago y algo caro.", "Neutro"),
        ("Nos encantó el trato, aunque la habitación era un pelín calurosa.", "Neutro"),
        ("Hotel fantástico, lástima que el spa cierre tan temprano los domingos.", "Neutro"),
        ("Volvería sin dudarlo, a pesar de que el ascensor es un poco lento.", "Neutro"),
        ("Limpieza de 10, solo fallaron un día al reponer las cápsulas de café.", "Neutro"),
        ("Personal encantador, si tuvieran más enchufes en el cuarto sería ideal.", "Neutro"),
        ("Ubicación imbatible, el ruido de la calle es mínimo para estar tan céntrico.", "Neutro"),
        ("Desayuno espectacular, solo eché de menos más fruta de temporada.", "Neutro"),
        ("Cama muy confortable, aunque las almohadas me parecieron algo blandas.", "Neutro"),
        ("Instalaciones modernas, el único detalle es que el lobby es algo frío.", "Neutro"),
        ("Gran atención al cliente, excepto por un pequeño malentendido al llegar.", "Neutro"),
        ("Wifi muy estable, suficiente para trabajar, aunque no para gaming.", "Neutro"),
        ("Ambiente acogedor, solo mejorarla la iluminación del espejo del baño.", "Neutro"),

        # 🌧️ 15 Neutras (Mayoría Negativas)
        ("Bastante flojo, lo único que se salva es que la ubicación es céntrica.", "Neutro"),
        ("Instalaciones descuidadas, al menos el personal de noche fue amable.", "Neutro"),
        ("Mucha humedad en el cuarto, aunque nos cambiaron las sábanas diario.", "Neutro"),
        ("Desayuno pobre y repetitivo, aunque el zumo de naranja era natural.", "Neutro"),
        ("Baño muy viejo y con grifos que bailan, pero estaba limpio al llegar.", "Neutro"),
        ("Mobiliario roto y antiguo, al menos el wifi funcionaba decentemente.", "Neutro"),
        ("Ruido constante de tuberías, aunque la cama era sorprendentemente pasable.", "Neutro"),
        ("Poca luz en la habitación, lo único bueno es que era bastante grande.", "Neutro"),
        ("Servicio muy lento en el restaurante, aunque la comida no estaba mala.", "Neutro"),
        ("El aire no enfriaba casi nada, suerte que pudimos abrir la ventana.", "Neutro"),
        ("Check-in caótico, por lo menos tuvieron el detalle de guardarnos las maletas.", "Neutro"),
        ("Habitación interior sin vistas, aunque por el precio no se puede pedir mucho.", "Neutro"),
        ("Toallas viejas y desgastadas, pero el personal de limpieza era educado.", "Neutro"),
        ("El gimnasio da pena, pero al menos la sauna funcionaba bien.", "Neutro"),
        ("Zona algo ruidosa, lo compensa que está pegado a la parada del bus.", "Neutro"),

        # 📝 20 Largas
        ("El edificio es una joya histórica y el lobby impresiona, pero al entrar en la habitación te das cuenta de que la alfombra tiene años y el aire acondicionado hace un estruendo que impide dormir; el desayuno es variado pero el servicio de mesas es un desastre total.", "Neutro"),
        ("Viajamos en pareja y el trato fue exquisito al recibirnos, incluso nos dieron un upgrade, pero la experiencia se torció cuando descubrimos que la ducha no tenía agua caliente y tardaron cuatro horas en mandar a un técnico que no arregló nada.", "Neutro"),
        ("La ubicación frente a la playa es un sueño y las piscinas están muy limpias, pero es inaceptable que te cobren 15 euros por una hamaca siendo cliente del hotel y que el bar de la piscina cierre justo cuando empieza el atardecer.", "Neutro"),
        ("Un hotel de contrastes: por un lado tienes un personal de recepción maravilloso y un buffet de cena increíble, pero por otro las habitaciones huelen a cañería y el ruido de la discoteca de abajo hace imposible descansar hasta las 5 de la mañana.", "Neutro"),
        ("Me gustó mucho la decoración moderna y el concepto de bar abierto, sin embargo, la limpieza de las zonas comunes deja mucho que desear y las escaleras de emergencia estaban llenas de cajas y basura, lo cual me parece un peligro.", "Neutro"),
        ("Ideal para negocios por su rapidez y buena conexión, pero si vas a relajarte busca otro sitio porque el spa es ruidoso y el personal de masajes parece tener mucha prisa por terminar contigo; la comida del restaurante es cara pero deliciosa.", "Neutro"),
        ("El hotel ofrece muchas actividades para niños y eso se agradece, pero el descontrol en los pasillos es total y nadie hace nada por mantener el silencio; el desayuno es correcto pero faltan mesas para tanta gente.", "Neutro"),
        ("Lo mejor es el rooftop con vistas 360, pero el precio de las copas es abusivo y la atención es bastante prepotente; la habitación estaba bien pero encontramos restos de comida de los anteriores huéspedes en un cajón.", "Neutro"),
        ("Un sitio con mucho encanto rústico y comida casera espectacular, pero la falta de cobertura y el wifi inexistente lo hacen difícil si necesitas estar conectado; además, el camino de acceso es una tortura para el coche.", "Neutro"),
        ("Estuvimos tres noches y la primera fue genial, pero la segunda se estropeó la calefacción y nos morimos de frío; nos dieron una manta extra pero no una solución real ni un descuento por las molestias causadas.", "Neutro"),
        ("Las fotos de la web prometen un paraíso y la realidad es un hotel que tuvo su gloria hace 20 años pero que hoy tiene grietas y humedades; lo único que lo mantiene a flote es su personal, que es de diez.", "Neutro"),
        ("El servicio de limpieza es impecable y la habitación olía siempre a flores, pero el colchón era tan blando que nos levantamos con dolor de cuello; el desayuno es espectacular pero el café es de máquina automática mala.", "Neutro"),
        ("Nos permitieron entrar antes de tiempo y nos guardaron el equipaje, pero al entrar al baño vimos que no habían cambiado las toallas y la papelera estaba llena; el personal se disculpó pero el error es básico.", "Neutro"),
        ("La zona es inmejorable para visitar museos y caminar, pero el ruido de los camiones de basura cada noche a las 3 AM es desesperante; el hotel es bonito pero los cristales de las ventanas no aíslan nada.", "Neutro"),
        ("Tienen un sistema de check-in automático que falla más que una escopeta de feria y acabas necesitando ayuda humana igual; la habitación es tecnológica y moderna pero le falta calidez y alma.", "Neutro"),
        ("El buffet de desayuno tiene de todo, pero es imposible disfrutarlo con el volumen de la música tan alto y los camareros corriendo de un lado a otro; las habitaciones son cómodas pero el armario es de risa.", "Neutro"),
        ("Una experiencia agridulce: nos encantó el spa y el detalle del cava, pero nos decepcionó encontrar polvo en las estanterías y que el televisor no sintonizara ningún canal correctamente.", "Neutro"),
        ("El personal de recepción es muy atento, pero el de seguridad es bastante desagradable y te vigila como si fueras a robar algo; la habitación es amplia y el baño está bien, aunque la luz parpadeaba.", "Neutro"),
        ("Un hotel boutique con mucho estilo pero con una gestión de reservas nefasta; nos dijeron que teníamos cama doble y nos dieron dos camas unidas que se separaban, aunque la decoración era preciosa.", "Neutro"),
        ("Lo recomiendo por su ubicación y limpieza, pero aviso de que el parking es una pesadilla y el desayuno se queda corto si llegas después de las 9:30 porque ya no reponen casi nada.", "Neutro"),

        # 😏 10 con Sarcasmo
        ("Me encantó la experiencia de 'ducha de aventura': nunca sabes si el agua saldrá hirviendo o congelada.", "Negativo"),
        ("Gracias por el buffet 'exclusivo'; si llegas tarde, el privilegio de no comer es todo tuyo.", "Negativo"),
        ("La limpieza era tan 'minimalista' que las pelusas de debajo de la cama ya tenían su propio ecosistema.", "Negativo"),
        ("Un aplauso al arquitecto que puso el único enchufe del cuarto detrás del cabecero de la cama.", "Negativo"),
        ("El Wi-Fi es perfecto para practicar la meditación, porque te da tiempo a reflexionar mientras carga un email.", "Negativo"),
        ("La vista al mar era increíble, si te asomabas por la ventana y usabas un periscopio para ver sobre el edificio de enfrente.", "Negativo"),
        ("Me encantó que las paredes fueran de papel; ahora sé que mi vecino tiene una tos muy fea y que le gusta el reggaetón.", "Negativo"),
        ("El 'gimnasio' es una oda a la historia antigua; esas máquinas deben de ser del siglo pasado por lo menos.", "Negativo"),
        ("Excelente idea la de no poner cortinas opacas, me encanta despertarme con el sol dándome directamente en la cara a las 6 AM.", "Negativo"),
        ("El servicio de habitaciones fue tan rápido que cuando trajeron la cena ya se me había pasado el hambre del día anterior.", "Negativo")
    ]

    # Cargar Modelos (G68 PRO ACTUAL)
    model_path = os.path.join(BASE_DIR, "data", "models", "sentiment_model.pkl")
    vectorizer_path = os.path.join(BASE_DIR, "data", "models", "tfidf_vectorizer.pkl")
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)

    print(f"--- 🕵️ TEST CIEGO LABORAL G68: 130 RESEÑAS CRÍTICAS ---")
    correct = 0
    failures = []
    
    # Por categoria para analisis detallado
    cat_stats = {}

    for i, (text, expected) in enumerate(dataset_130):
        pred, prob, meta = analizar_sentimiento_hibrido(text, model, vectorizer)
        
        # Determinar categoria (aproximada por el orden)
        cat = "OTRO"
        if i < 15: cat = "Positivas"
        elif i < 30: cat = "Negativas"
        elif i < 50: cat = "Stress"
        elif i < 70: cat = "Neutras Mezcla"
        elif i < 85: cat = "Neutras Mayoría Pos"
        elif i < 100: cat = "Neutras Mayoría Neg"
        elif i < 120: cat = "Largas"
        else: cat = "Sarcasmo"
            
        if cat not in cat_stats: cat_stats[cat] = {"correct": 0, "total": 0}
        cat_stats[cat]["total"] += 1

        if pred.lower() == expected.lower():
            correct += 1
            cat_stats[cat]["correct"] += 1
        else:
            failures.append((i+1, cat, text, expected, pred, prob))

    print(f"\nACCURACY GLOBAL CIEGA: {correct/len(dataset_130):.2%}")
    
    print("\n--- DESGLOSE POR CATEGORÍA ---")
    for cat, stats in cat_stats.items():
        acc = stats["correct"] / stats["total"]
        print(f"{cat:<20}: {acc:.2%} ({stats['correct']}/{stats['total']})")

    print(f"\n--- ANÁLISIS DE FALLOS ---")
    for id, cat, text, exp, pred, prob in failures:
        print(f"Id: {id:<2} | Cat: {cat:<10} | E: {exp[:3]} | P: {pred[:3]} | Prob: {prob:.2f} | {text[:70]}...")

if __name__ == "__main__":
    run_blind_test_130()
