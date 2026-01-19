import requests
import json
import time

API_URL = "http://localhost:8080/sentiment"

casos = [
    {"id": 1, "cat": "Operativo", "tipo": "Sarcasmo", "text": "¡Qué maravilla! El aire acondicionado hace tanto ruido que parece una pista de aterrizaje."},
    {"id": 2, "cat": "Higiene", "tipo": "Crítico", "text": "Las sábanas tenían manchas amarillas y el suelo del baño estaba pegajoso."},
    {"id": 3, "cat": "Cobros", "tipo": "Crítico", "text": "Me cargaron 50 euros por un servicio que nunca pedí y no me dan factura."},
    {"id": 4, "cat": "Atención", "tipo": "Doble Negación", "text": "No puedo decir que la comida no estuviera buena, pero el camarero fue muy rudo."},
    {"id": 5, "cat": "Operativo", "tipo": "Neutro", "text": "El hotel ofrece servicio de traslado al aeropuerto cada 30 minutos."},
    {"id": 6, "cat": "Atención", "tipo": "Negativo", "text": "El recepcionista nos ignoró por estar hablando por su teléfono personal."},
    {"id": 7, "cat": "Operativo", "tipo": "Positivo", "text": "La rapidez del check-in fue asombrosa, tardamos menos de dos minutos."},
    {"id": 8, "cat": "Operativo", "tipo": "Ironía", "text": "Gracias por el 'upgrade' a una habitación con vistas a un muro de ladrillos."},
    {"id": 9, "cat": "Atención", "tipo": "Grocero", "text": "Es una puta vergüenza que traten así a los clientes antiguos."},
    {"id": 10, "cat": "Operativo", "tipo": "Negativo", "text": "El wifi es tan lento que no pude ni abrir el correo del trabajo."},
    {"id": 11, "cat": "Administrativo", "tipo": "Negativo", "text": "El proceso de cancelación es un laberinto diseñado para que no te vayas."},
    {"id": 12, "cat": "Higiene", "tipo": "Crítico", "text": "Había una cucaracha en el buffet de ensaladas, salimos corriendo."},
    {"id": 13, "cat": "Atención", "tipo": "Mixto", "text": "Me pidieron disculpas, pero el problema técnico sigue sin resolverse."},
    {"id": 14, "cat": "Cobros", "tipo": "Crítico", "text": "Me duplicaron el cobro en la tarjeta y dicen que tardan 15 días en devolverlo."},
    {"id": 15, "cat": "Marketing", "tipo": "Engañoso", "text": "La foto de la web muestra una playa privada que en realidad es pública y sucia."},
    {"id": 16, "cat": "Operativo", "tipo": "Positivo", "text": "El colchón era tan cómodo que por fin pude descansar del viaje."},
    {"id": 17, "cat": "Atención", "tipo": "Doble Negación", "text": "No es que no me guste el hotel, pero le falta mucho mantenimiento."},
    {"id": 18, "cat": "Administrativo", "tipo": "Urgencia", "text": "¡Ayuda! Mi reserva desapareció del sistema y estoy en la puerta del hotel."},
    {"id": 19, "cat": "Operativo", "tipo": "Neutro", "text": "La habitación cuenta con minibar, caja fuerte y secador de pelo."},
    {"id": 20, "cat": "Marketing", "tipo": "Sarcasmo", "text": "Bravo, han logrado que unas vacaciones de relax sean un estrés constante."},
    {"id": 21, "cat": "Higiene", "tipo": "Negativo", "text": "El olor a tabaco en la habitación de no fumadores era insoportable."},
    {"id": 22, "cat": "Atención", "tipo": "Positivo", "text": "El botones nos ayudó con las maletas y fue extremadamente educado."},
    {"id": 23, "cat": "Cobros", "tipo": "Dificil", "text": "Me dicen que el desayuno está incluido pero luego me cobran el café aparte."},
    {"id": 24, "cat": "Marketing", "tipo": "Positivo", "text": "La campaña de redes sociales me convenció y el hotel cumplió todo."},
    {"id": 25, "cat": "Administrativo", "tipo": "Neutro", "text": "Para solicitar la factura es necesario enviar el RUT por correo electrónico."},
    {"id": 26, "cat": "Operativo", "tipo": "Negativo", "text": "El agua de la ducha sale templada, nunca llega a calentar del todo."},
    {"id": 27, "cat": "Atención", "tipo": "Sarcasmo", "text": "Gracias por hacerme esperar una hora en el lobby, me encanta perder el tiempo."},
    {"id": 28, "cat": "Higiene", "tipo": "Crítico", "text": "Encontramos moho en la junta de la ducha, falta mucha limpieza profunda."},
    {"id": 29, "cat": "Cobros", "tipo": "Negativo", "text": "Intentaron cobrarme un extra por limpieza que no estaba en el contrato."},
    {"id": 30, "cat": "Operativo", "tipo": "Positivo", "text": "La insonorización es excelente, no se oye nada de la calle."},
    {"id": 31, "cat": "Marketing", "tipo": "Neutro", "text": "Vi el anuncio en Instagram y decidí reservar por la ubicación."},
    {"id": 32, "cat": "Atención", "tipo": "Grocero", "text": "El guardia de seguridad es un imbécil que no sabe tratar a la gente."},
    {"id": 33, "cat": "Administrativo", "tipo": "Doble Negación", "text": "No es imposible conseguir el reembolso, pero te lo ponen muy difícil."},
    {"id": 34, "cat": "Operativo", "tipo": "Negativo", "text": "El ascensor se quedó trabado entre pisos, pasamos mucho miedo."},
    {"id": 35, "cat": "Higiene", "tipo": "Positivo", "text": "Todo el hotel huele a limpio, se nota que cuidan los detalles."},
    {"id": 36, "cat": "Atención", "tipo": "Neutro", "text": "Pregunté por la clave del wifi y me la dieron en un papelito."},
    {"id": 37, "cat": "Cobros", "tipo": "Crítico", "text": "Me hicieron un cargo de 200 dólares que no sé de qué es."},
    {"id": 38, "cat": "Marketing", "tipo": "Sarcasmo", "text": "Vender este hostal como 'Luxury Resort' es tener mucha imaginación."},
    {"id": 39, "cat": "Operativo", "tipo": "Negativo", "text": "La luz de la habitación parpadea y el técnico nunca vino a verla."},
    {"id": 40, "cat": "Atención", "tipo": "Positivo", "text": "La chica de recepción, Marta, es lo mejor que tiene este hotel."},
    {"id": 41, "cat": "Higiene", "tipo": "Negativo", "text": "Había pelos en el desagüe cuando entramos a la habitación."},
    {"id": 42, "cat": "Administrativo", "tipo": "Positivo", "text": "Me enviaron la factura al minuto de pedírsela, muy eficientes."},
    {"id": 43, "cat": "Operativo", "tipo": "Neutro", "text": "El parking está en el sótano y es gratuito para clientes."},
    {"id": 44, "cat": "Atención", "tipo": "Urgencia", "text": "Llamo y llamo a recepción y nadie contesta, necesito una manta."},
    {"id": 45, "cat": "Cobros", "tipo": "Mixto", "text": "El precio es bueno, pero las comisiones por pago con tarjeta son altas."},
    {"id": 46, "cat": "Marketing", "tipo": "Negativo", "text": "El 'kit de bienvenida' eran dos caramelos y una botella de agua pequeña."},
    {"id": 47, "cat": "Operativo", "tipo": "Positivo", "text": "La Smart TV funciona genial y tiene Netflix configurado."},
    {"id": 48, "cat": "Atención", "tipo": "Sarcasmo", "text": "Qué alivio que el recepcionista prefiera chatear que atenderme."},
    {"id": 49, "cat": "Higiene", "tipo": "Crítico", "text": "Había hormigas en la mesa de noche, no vuelvo jamás."},
    {"id": 50, "cat": "Administrativo", "tipo": "Doble Negación", "text": "No puedo negar que el check-out fue rápido, al menos eso."},
    {"id": 51, "cat": "Operativo", "tipo": "Positivo", "text": "El gimnasio está muy completo y las máquinas son nuevas."},
    {"id": 52, "cat": "Marketing", "tipo": "Neutro", "text": "El folleto informativo está disponible en cinco idiomas."},
    {"id": 53, "cat": "Atención", "tipo": "Negativo", "text": "Me hablaron de forma muy condescendiente por no entender el sistema."},
    {"id": 54, "cat": "Cobros", "tipo": "Crítico", "text": "Me retuvieron el depósito de garantía y ya pasaron 20 días."},
    {"id": 55, "cat": "Higiene", "tipo": "Negativo", "text": "La piscina tiene demasiada arena en el fondo, parece descuidada."},
    {"id": 56, "cat": "Operativo", "tipo": "Positivo", "text": "El balcón tiene unas vistas preciosas a la montaña."},
    {"id": 57, "cat": "Marketing", "tipo": "Positivo", "text": "La oferta de reserva anticipada nos ahorró mucho dinero."},
    {"id": 58, "cat": "Atención", "tipo": "Neutro", "text": "El personal lleva uniforme y es fácil de identificar."},
    {"id": 59, "cat": "Administrativo", "tipo": "Negativo", "text": "Me piden un código de confirmación que nunca me llegó al móvil."},
    {"id": 60, "cat": "Operativo", "tipo": "Sarcasmo", "text": "Increíble que en 2026 el wifi solo funcione cerca del lobby."},
    {"id": 61, "cat": "Higiene", "tipo": "Crítico", "text": "El vaso del cepillo de dientes tenía restos de pasta dental vieja."},
    {"id": 62, "cat": "Cobros", "tipo": "Positivo", "text": "Se dieron cuenta del error en el cobro y me llamaron para devolverlo."},
    {"id": 63, "cat": "Atención", "tipo": "Negativo", "text": "El servicio de habitaciones se olvidó de mi cena dos veces."},
    {"id": 64, "cat": "Marketing", "tipo": "Sarcasmo", "text": "Si esto es un hotel de 4 estrellas, yo soy el Rey de España."},
    {"id": 65, "cat": "Operativo", "tipo": "Neutro", "text": "Las llaves son magnéticas y funcionan por aproximación."},
    {"id": 66, "cat": "Atención", "tipo": "Positivo", "text": "Nos recomendaron un tour privado que fue un acierto total."},
    {"id": 67, "cat": "Higiene", "tipo": "Negativo", "text": "La alfombra del pasillo tiene manchas que parecen muy antiguas."},
    {"id": 68, "cat": "Administrativo", "tipo": "Crítico", "text": "Cambiaron los términos del servicio sin avisar a los suscriptores."},
    {"id": 69, "cat": "Operativo", "tipo": "Negativo", "text": "El minibar hace un ruido eléctrico constante y no deja dormir."},
    {"id": 70, "cat": "Marketing", "tipo": "Positivo", "text": "Me encanta el nuevo logo y la estética moderna del hotel."},
    {"id": 71, "cat": "Atención", "tipo": "Doble Negación", "text": "No es que me hayan tratado mal, pero les falta calidez."},
    {"id": 72, "cat": "Cobros", "tipo": "Negativo", "text": "Me cobraron el parking cuando en la reserva decía que era gratis."},
    {"id": 73, "cat": "Higiene", "tipo": "Positivo", "text": "La desinfección de las zonas comunes es constante, da seguridad."},
    {"id": 74, "cat": "Operativo", "tipo": "Neutro", "text": "La presión del agua en el tercer piso es normal."},
    {"id": 75, "cat": "Atención", "tipo": "Grocero", "text": "El botones me pidió propina de forma muy agresiva y maleducada."},
    {"id": 76, "cat": "Marketing", "tipo": "Negativo", "text": "El hotel se ve mucho más viejo y desgastado que en las fotos."},
    {"id": 77, "cat": "Administrativo", "tipo": "Positivo", "text": "El proceso de reserva por la app fue fluido y sin errores."},
    {"id": 78, "cat": "Operativo", "tipo": "Sarcasmo", "text": "Me encanta que la ventana no cierre bien y entre todo el frío."},
    {"id": 79, "cat": "Atención", "tipo": "Negativo", "text": "Me dijeron que me llamarían para confirmar y sigo esperando."},
    {"id": 80, "cat": "Cobros", "tipo": "Crítico", "text": "Me cobraron una tarifa de cancelación por un error de su web."},
    {"id": 81, "cat": "Higiene", "tipo": "Negativo", "text": "Había una mancha extraña en el sofá de la habitación."},
    {"id": 82, "cat": "Operativo", "tipo": "Positivo", "text": "Tienen cargadores para coches eléctricos, un gran punto a favor."},
    {"id": 83, "cat": "Marketing", "tipo": "Neutro", "text": "Recibí el boletín de ofertas en mi correo este lunes."},
    {"id": 84, "cat": "Atención", "tipo": "Positivo", "text": "El personal de limpieza es súper discreto y eficiente."},
    {"id": 85, "cat": "Administrativo", "tipo": "Doble Negación", "text": "No es poco frecuente que el sistema de facturación falle."},
    {"id": 86, "cat": "Operativo", "tipo": "Negativo", "text": "El sensor de luz del pasillo tarda mucho en encenderse, está oscuro."},
    {"id": 87, "cat": "Cobros", "tipo": "Sarcasmo", "text": "Gracias por cobrarme el agua del grifo a precio de champán."},
    {"id": 88, "cat": "Higiene", "tipo": "Crítico", "text": "El inodoro no estaba bien anclado y perdía agua, un asco."},
    {"id": 89, "cat": "Atención", "tipo": "Positivo", "text": "Gestionaron mi cambio de habitación sin ninguna objeción."},
    {"id": 90, "cat": "Marketing", "tipo": "Negativo", "text": "Prometen 'desayuno continental' y solo hay tostadas y café malo."},
    {"id": 91, "cat": "Operativo", "tipo": "Neutro", "text": "El hotel tiene dos plantas y no dispone de jardín."},
    {"id": 92, "cat": "Administrativo", "tipo": "Negativo", "text": "Es frustrante que no contesten a los correos administrativos."},
    {"id": 93, "cat": "Cobros", "tipo": "Positivo", "text": "El desglose de la factura es clarísimo, nada de cargos ocultos."},
    {"id": 94, "cat": "Atención", "tipo": "Sarcasmo", "text": "Bravo por el camarero que me trajo la cuenta antes de pedir el postre."},
    {"id": 95, "cat": "Higiene", "tipo": "Negativo", "text": "Había polvo acumulado en las aspas del ventilador del techo."},
    {"id": 96, "cat": "Operativo", "tipo": "Positivo", "text": "El sistema de domótica de la habitación es muy intuitivo."},
    {"id": 97, "cat": "Atención", "tipo": "Dificil", "text": "El personal es amable pero se nota que están desbordados de trabajo."},
    {"id": 98, "cat": "Administrativo", "tipo": "Urgencia", "text": "¡Cancelen mi reserva ya! Mi vuelo se canceló y no quiero cargos."},
    {"id": 99, "cat": "Marketing", "tipo": "Positivo", "text": "La decoración navideña del hotel es preciosa y muy elegante."},
    {"id": 100, "cat": "Operativo", "tipo": "Mixto", "text": "Llegó el pedido de room service rápido, pero la comida estaba fría."}
]

print("=" * 140)
print(f"--- INICIANDO MEGA BATCH FINAL G68 (100 casos) ---")
print("=" * 140)
print(f"{'ID':<4} | {'CAT.':<10} | {'TIPO':<10} | {'PREVISIÓN':<10} | {'PROB':<6} | {'TOP FEATURES':<40}")
print("-" * 140)

aciertos = 0
for caso in casos:
    try:
        response = requests.post(API_URL, json={"text": caso["text"]})
        if response.status_code == 200:
            res = response.json()
            features = res['top_features']
            if len(features) > 37: features = features[:34] + "..."
            
            label_esperada = "UNK"
            if caso['tipo'] in ['Positivo']: label_esperada = "Positivo"
            elif caso['tipo'] in ['Negativo', 'Crítico', 'Grocero', 'Urgencia', 'Engañoso']: label_esperada = "Negativo"
            elif caso['tipo'] in ['Neutro']: label_esperada = "Neutral"
            # Sarcasmo e Ironía se esperan Negativos
            elif caso['tipo'] in ['Sarcasmo', 'Ironía']: label_esperada = "Negativo"
            
            # Simple check de aciertos
            correct = False
            if label_esperada != "UNK":
                if (label_esperada == "Neutral" and res['prevision'] in ["Neutral", "Neutro"]): correct = True
                elif res['prevision'] == label_esperada: correct = True
            
            if correct: aciertos += 1
            
            mark = "CORRECTO" if correct else "ERROR" if label_esperada != "UNK" else "?"
            
            print(f"{caso['id']:<4} | {caso['cat']:<10} | {caso['tipo']:<10} | {res['prevision']:<10} | {res['probabilidad']:<6} | {features:<40} | {mark}")

        else:
            print(f"{caso['id']:<4} | ERROR HTTP {response.status_code}")
    except Exception as e:
        print(f"{caso['id']:<4} | ERROR CONN: {e}")

print("=" * 140)
print(f"REPORT - ACCURACY ESTIMADO (En casos no ambiguos): {aciertos}/??? (Se calculará en base a tipos válidos)")
print("=" * 140)
