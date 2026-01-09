import os
import sys
import joblib
import pandas as pd

# Configurar rutas para importar el motor
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, "src"))

from engine.sentiment_engine import analizar_sentimiento_hibrido

def run_benchmark_elite():
    # 1. Datos del Nuevo Lote (95 frases)
    elite_phrases = [
        # Positivas (35)
        ("El concepto de 'open bar' por la tarde es un detalle de categoría.", "Positivo"),
        ("La insonorización es increíble; estás en plena calle principal y no oyes ni un claxon.", "Positivo"),
        ("Nos dieron un kit para el perro con camita y cuenco, ¡qué detalle!", "Positivo"),
        ("El suelo radiante del baño es lo mejor que he probado en invierno.", "Positivo"),
        ("Un 10 para el servicio de aparcacoches, fueron súper rápidos.", "Positivo"),
        ("La estética industrial del hotel me fascinó, muy neoyorquina.", "Positivo"),
        ("El desayuno tiene zumo de naranja natural exprimido al momento, se agradece.", "Positivo"),
        ("Camas balinesas en la piscina gratuitas para los huéspedes, un lujo.", "Positivo"),
        ("Me olvidé el cargador y en recepción me prestaron uno sin problemas.", "Positivo"),
        ("La presión del agua en la ducha es casi un masaje, salí renovado.", "Positivo"),
        ("Habitaciones con domótica muy fácil de usar, todo desde una tablet.", "Positivo"),
        ("El personal de seguridad es muy amable y te ayuda con las direcciones.", "Positivo"),
        ("Desayuno en la habitación sin cargo extra, un placer de domingo.", "Positivo"),
        ("La ubicación para ir de compras es imbatible, sales y tienes todas las tiendas.", "Positivo"),
        ("Hotel boutique con encanto, se respira paz en cada rincón.", "Positivo"),
        ("El olor del gel de baño es adictivo, ¿saben dónde se puede comprar?", "Positivo"),
        ("Techo altísimo y ventanales enormes, mucha luz natural.", "Positivo"),
        ("El check-out a las 12:00 es genial para no ir corriendo por la mañana.", "Positivo"),
        ("Todo el hotel es accesible para silla de ruedas, muy bien pensado.", "Positivo"),
        ("El pianista del bar crea una atmósfera mágica por las noches.", "Positivo"),
        ("Cafetera Nespresso en el cuarto con reposición diaria de cápsulas.", "Positivo"),
        ("La terraza tiene una de las mejores puestas de sol que he visto nunca.", "Positivo"),
        ("Limpieza de diez, pasaron incluso por la tarde a repasar las toallas.", "Positivo"),
        ("El personal de animación es muy divertido sin llegar a ser pesado.", "Positivo"),
        ("Ideal si buscas algo moderno y funcional a buen precio.", "Positivo"),
        ("Me encantó la biblioteca del hall, un sitio precioso para leer.", "Positivo"),
        ("Muy cerca del aeropuerto, el transfer gratuito pasó cada 15 minutos.", "Positivo"),
        ("El minibar es gratuito y lo reponen cada día con refrescos y snacks.", "Positivo"),
        ("Dormí 9 horas del tirón, el colchón es pura nube.", "Positivo"),
        ("Un trato exquisito, nos sentimos como en casa desde que cruzamos la puerta.", "Positivo"),
        ("La comida del buffet cambia cada día, nunca te aburres.", "Positivo"),
        ("Baño con bañera hidromasaje, un sueño para terminar el día.", "Positivo"),
        ("El equipo de eventos organizó nuestra boda de forma impecable.", "Positivo"),
        ("Todo nuevo, se nota que acaban de inaugurar o reformar.", "Positivo"),
        ("Las sábanas de algodón egipcio son de otro mundo, suavidad máxima.", "Positivo"),

        # Neutras (25)
        ("El hotel es precioso, pero la cuesta para llegar a pie es criminal.", "Neutro"),
        ("Buen servicio, aunque tardaron una eternidad en darnos la factura.", "Neutro"),
        ("La piscina es más pequeña de lo que parece en el gran angular de la web.", "Neutro"),
        ("Habitación muy limpia pero el armario era diminuto para dos personas.", "Neutro"),
        ("El personal es joven y con ganas, pero les falta un poco de experiencia.", "Neutro"),
        ("Cerca de todo, pero es imposible aparcar si no pagas el parking del hotel.", "Neutro"),
        ("Desayuno aceptable, pero los huevos revueltos estaban muy secos.", "Neutro"),
        ("El diseño es minimalista, tanto que no había ni un cajón para la ropa.", "Neutro"),
        ("Buena televisión pero el mando no funcionaba y tuve que bajar a recepción.", "Neutro"),
        ("El spa está bien, aunque te obligan a comprar su gorro por 5 euros.", "Neutro"),
        ("Wifi decente en el escritorio, pero en la cama la señal se pierde.", "Neutro"),
        ("Habitación bien insonorizada de la calle, pero se oye el pasillo.", "Neutro"),
        ("El café del desayuno es excelente, pero la bollería es industrial.", "Neutro"),
        ("Me dieron una habitación cerca del ascensor y el 'ding' es constante.", "Neutro"),
        ("Hotel de paso correcto, pero no para un viaje romántico.", "Neutro"),
        ("La luz de emergencia sobre la puerta brilla demasiado de noche.", "Neutro"),
        ("El personal de recepción fue amable, el del restaurante muy tosco.", "Neutro"),
        ("Mucho estilo pero poca practicidad: el lavabo era plano y salpicaba todo.", "Neutro"),
        ("Está en una zona tranquila, pero necesitas coche para todo.", "Neutro"),
        ("El gimnasio solo abre de 9 a 20, horario muy corto para ejecutivos.", "Neutro"),
        ("Te dan una sola llave por habitación, un poco incómodo si sois dos.", "Neutro"),
        ("Buena temperatura en el cuarto, pero el termostato es confuso.", "Neutro"),
        ("La decoración es un poco fría, parece más un hospital que un hotel.", "Neutro"),
        ("Ofrecen tour gratuito pero luego te presionan para dejar propina alta.", "Neutro"),
        ("El jabón es 3 en 1 de pared, esperaba botes individuales por este precio.", "Neutro"),

        # Negativas / Sarcasmo (30)
        ("La 'experiencia zen' fue escuchar los gritos de los niños en el pasillo a las 7 AM.", "Negativo"),
        ("Había una mancha sospechosa en el cubrecolchón. No quise ni saber qué era.", "Negativo"),
        ("Gracias por la lección de geología: la cama era literalmente una piedra.", "Negativo"),
        ("¡Inaudito! Entraron en mi habitación mientras estaba en la ducha.", "Negativo"),
        ("El aire acondicionado goteaba y me dijeron que pusiera una papelera debajo.", "Negativo"),
        ("Un olor a tabaco rancio que se te queda impregnado en el pelo.", "Negativo"),
        ("El desayuno buffet era una competición por el último trozo de pan.", "Negativo"),
        ("Publicitan parking y es un callejón sin vigilancia a dos manzanas.", "Negativo"),
        ("La cortina de la ducha tenía moho negro en la parte inferior. Asco.", "Negativo"),
        ("El recepcionista estaba más pendiente de su móvil que de mi check-in.", "Negativo"),
        ("No hay agua caliente por las mañanas, dicen que es por la 'alta demanda'.", "Negativo"),
        ("¡Un timo! El spa es de pago y no lo avisan en ninguna parte al reservar.", "Negativo"),
        ("La tele es del siglo pasado y solo se ven tres canales con nieve.", "Negativo"),
        ("Me cobraron el minibar que ni siquiera abrí. Una lucha para que devuelvan el dinero.", "Negativo"),
        ("La 'terraza privada' es un trozo de hormigón compartido con la habitación de al lado.", "Negativo"),
        ("Paredes tan finas que mi vecino estornudó y yo le dije 'salud'.", "Negativo"),
        ("Cucarachas en el pasillo. La respuesta del hotel: 'es normal por el calor'.", "Negativo"),
        ("Reservé cama de matrimonio y me dieron dos camas con un hueco en medio.", "Negativo"),
        ("El secador de pelo se quemó a los dos minutos de encenderlo. Peligroso.", "Negativo"),
        ("El hotel está en obras y no avisaron. Ruido de taladros desde temprano.", "Negativo"),
        ("Si te gusta dormir en un horno, ven aquí, la calefacción no se puede apagar.", "Negativo"),
        ("Hice el check-in online para ahorrar tiempo y tardé más que los que no lo hicieron.", "Negativo"),
        ("El zumo de naranja es agua con polvos color naranja. Un insulto.", "Negativo"),
        ("Sábanas rotas y con agujeros. ¿En serio esto es un 4 estrellas?", "Negativo"),
        ("El 'vistas a la ciudad' era una vista directa a un muro de ladrillos.", "Negativo"),
        ("Pedí una habitación tranquila y me pusieron encima de la cocina.", "Negativo"),
        ("Me ignoraron en el bar durante 20 minutos mientras los camareros charlaban.", "Negativo"),
        ("Tuvimos que pagar por las toallas de la piscina. Detalle muy cutre.", "Negativo"),
        ("El ascensor se quedó bloqueado conmigo dentro y tardaron media hora en sacarme.", "Negativo"),
        ("No volvería ni aunque me pagaran. Gestión desastrosa y falta de higiene.", "Negativo"),

        # Estrés Máximo (10)
        ("Es inadmisible que después de confirmar por teléfono que el parking estaba incluido, al llegar me digan que tengo que buscarme la vida porque no hay plazas libres, y encima el recepcionista me conteste de malas formas.", "Negativo"),
        ("La situación fue surrealista: el inodoro se desbordó a las dos de la mañana, inundando media habitación, y nos dijeron que no nos podían cambiar de cuarto porque estaban llenos, ¡tuvimos que limpiar nosotros!", "Negativo"),
        ("Me siento totalmente estafado porque las fotos de la página web deben de tener 20 años o están hechas con Photoshop; el hotel está que se cae a pedazos y huele a humedad en cada esquina.", "Negativo"),
        ("Viajaba por una emergencia familiar y necesitaba descansar, pero entre el camión de la basura que pasa a las 4 AM y la gente dando portazos, ha sido la peor noche de mi vida, me voy más cansado de lo que vine.", "Negativo"),
        ("Es increíble que un hotel de esta categoría no tenga un generador; se fue la luz en todo el barrio y nos dejaron a oscuras, sin agua y sin ninguna explicación durante seis horas.", "Negativo"),
        ("Lo que empezó como un fin de semana romántico terminó con nosotros pidiendo una hoja de reclamaciones porque el personal de limpieza tiró a la basura una bolsa con compras personales pensando que era desperdicio.", "Negativo"),
        ("El buffet del desayuno es un peligro sanitario: moscas sobre la fruta, leche tibia y el personal manipulando la comida sin guantes ni cuidado. Se me quitaron las ganas de comer nada más entrar.", "Negativo"),
        ("No entiendo cómo pueden dormir tranquilos cobrando 200 euros la noche por una habitación donde no funciona ni el wifi, ni el teléfono para llamar a recepción, ni la cerradura electrónica de la puerta.", "Negativo"),
        ("Tuvimos que irnos a otro hotel a las once de la noche porque el aire acondicionado empezó a soltar un humo negro y un olor a quemado que hacía imposible respirar, y nadie nos pidió ni perdón.", "Negativo"),
        ("Una auténtica falta de respeto al cliente: reservamos con meses de antelación y al llegar nos dijeron que nuestra habitación se la habían dado a otro grupo y que nos mandaban a un hostal cercano de mucha menor categoría.", "Negativo")
    ]

    # 2. Cargar Modelos
    model_path = os.path.join(BASE_DIR, "data", "models", "sentiment_model.pkl")
    vectorizer_path = os.path.join(BASE_DIR, "data", "models", "tfidf_vectorizer.pkl")
    
    if not os.path.exists(model_path):
        print("Error: No hay modelo para testear.")
        return

    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)

    # 3. Ejecutar Test
    print(f"--- DIAGNÓSTICO PRE-ENTRENAMIENTO (LOTE ÉLITE 95) ---")
    correct = 0
    total = len(elite_phrases)

    for i, (texto, esperado) in enumerate(elite_phrases):
        pred, prob, meta = analizar_sentimiento_hibrido(texto, model, vectorizer)
        is_ok = "✅" if pred.lower() == esperado.lower() else "❌"
        if is_ok == "✅": correct += 1
        
        # Mostrar solo los fallos para analizar
        if is_ok == "❌":
            print(f"{i+1:<2} | {is_ok} | E:{esperado[:3]} | P:{pred[:3]} | p:{prob:.2f} | {texto[:60]}...")

    print(f"\nRESULTADO DIAGNÓSTICO: {correct}/{total} ({ (correct/total)*100:.2f}%)")

if __name__ == "__main__":
    run_benchmark_elite()
