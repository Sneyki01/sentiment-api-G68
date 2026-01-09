import os
import sys
import joblib

# Configurar rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, "src"))

from engine.sentiment_engine import analizar_sentimiento_hibrido

def run_final_duel():
    # Dataset de 20 reseñas de prueba final
    final_20 = [
        ("Todo impecable. El personal fue súper amable y la ubicación es perfecta para caminar a todos lados. Repetiremos sin duda.", "Positivo"),
        ("Me encantó la 'limpieza' de la habitación; las manchas de la alfombra eran tan grandes que parecían un mapa de la ciudad.", "Negativo"),
        ("¡UNA PESADILLA! Llevo 2 horas esperando en el lobby con mis hijos y me dicen que mi reserva NO EXISTE. Nadie me da solución.", "Negativo"),
        ("La cama es cómoda y el hotel está bien situado, pero el desayuno me pareció algo pobre para el precio que tiene.", "Neutro"),
        ("No se lo recomiendo a nadie. El olor a tabaco en la habitación era insoportable y el baño estaba lleno de moho.", "Negativo"),
        ("Muy buen trato del personal, solo fallaron un poco con el Wi-Fi que iba lento, pero el resto de la estancia fue genial.", "Neutro"),
        ("El hotel está muy viejo y descuidado. Lo único bueno es que el chico de recepción fue muy simpático al recibirnos.", "Neutro"),
        ("El edificio tiene un encanto rústico increíble y la comida del restaurante es casera, pero la falta de insonorización hace que escuches hasta los pasos del vecino de arriba y el agua de la ducha sale casi fría.", "Neutro"),
        ("Excelente idea la de no poner persianas; me encanta que el sol me despierte a las 5:30 AM para aprovechar bien el día.", "Negativo"),
        ("Buscábamos desconectar y el hotel superó las expectativas. El spa es un lujo, el personal se anticipa a tus necesidades y el detalle de la fruta en la habitación nos ganó por completo.", "Positivo"),
        ("Encontré pelos en la almohada al llegar. Pedí cambio de sábanas y tardaron tres horas. Jamás volvería a este sitio.", "Negativo"),
        ("¡CUIDADO! Me han cobrado dos veces la estancia en la tarjeta y en recepción me dicen que espere a que el gerente llegue mañana. ¡Es un robo!", "Negativo"),
        ("Correcto para negocios. El escritorio es amplio y hay muchos enchufes, aunque la luz de la habitación es demasiado tenue para trabajar.", "Neutro"),
        ("Gracias por la sauna gratuita: el aire acondicionado no funcionaba y me pasé toda la noche sudando como un pollo.", "Negativo"),
        ("Relación calidad-precio de diez. Limpio, céntrico y personal servicial.", "Positivo"),
        ("Publicitan un gimnasio que es un cuarto sin aire con una cinta rota, el parking está a 3 manzanas y la habitación olía a lejía pura. No entiendo de dónde sacan las 4 estrellas.", "Negativo"),
        ("Un hotel más. No está mal pero tampoco tiene nada especial que te haga querer volver. Cumple su función.", "Neutro"),
        ("Sentí mucho miedo. La puerta de la habitación no cerraba bien y el barrio de noche se ve muy peligroso. Me fui un día antes.", "Negativo"),
        ("El lobby es de 5 estrellas pero la habitación de la planta baja parecía un sótano. El café del desayuno buenísimo, el pan duro.", "Neutro"),
        ("Un aplauso al personal del bar; tienen la habilidad única de ignorarte durante 20 minutos mientras miran el móvil.", "Negativo")
    ]

    # Cargar Modelos
    model_path = os.path.join(BASE_DIR, "data", "models", "sentiment_model.pkl")
    vectorizer_path = os.path.join(BASE_DIR, "data", "models", "tfidf_vectorizer.pkl")
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)

    print(f"--- 🦾 DUELO FINAL G68: 20 CASOS DE PRUEBA MAESTRA ---")
    correct = 0
    
    for i, (text, expected) in enumerate(final_20):
        pred, prob, meta = analizar_sentimiento_hibrido(text, model, vectorizer)
        status = "✅" if pred.lower() == expected.lower() else "❌"
        if status == "✅": correct += 1
        
        print(f"[{status}] Id: {i+1:<2} | E: {expected[:3]} | P: {pred[:3]} | Prob: {prob:.2f} | {text[:60]}...")
        if status == "❌":
            print(f"      -> Explicabilidad: {meta['explicabilidad']}")

    print(f"\nACCURACY FINAL: {correct/len(final_20):.2%}")

if __name__ == "__main__":
    run_final_duel()
