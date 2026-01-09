import os
import sys
import joblib
import pandas as pd
import math

# 1. Configurar rutas para importar el motor
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, "src"))

from engine.sentiment_engine import analizar_sentimiento_hibrido

# 2. Dataset de Prueba G68 V3 (Nuevas 50 frases de Sarcasmo, Estrés y Neutralidad)
data_v3 = [
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
    {"text": "El hotel es... rústico, si por rústico entiendes que se cae a pedazos.", "expected": "Negativo"},
    {"text": "Hay una gran diferencia entre lo que prometen y lo que dan.", "expected": "Negativo"},
    {"text": "Me siento muy ansioso, la habitación no tiene ventanas al exterior.", "expected": "Negativo"},
    {"text": "El desayuno incluye fruta de temporada y pan artesanal.", "expected": "Neutro"},
    {"text": "¡Un sueño! No quería despertarme nunca de esa camilla.", "expected": "Positivo"},
    {"text": "La atención es tan lenta que parece que trabajan a cámara lenta.", "expected": "Negativo"},
    {"text": "El edificio tiene una arquitectura ecléctica y colores vibrantes.", "expected": "Neutro"},
    {"text": "Qué buena suerte la mía, el único día que vengo y el sauna explota.", "expected": "Negativo"},
    {"text": "Me voy con una sonrisa y la energía renovada, ¡gracias equipo!", "expected": "Positivo"}
]

def run_benchmark_v3():
    try:
        model = joblib.load(os.path.join(BASE_DIR, "data", "models", "sentiment_model.pkl"))
        vectorizer = joblib.load(os.path.join(BASE_DIR, "data", "models", "tfidf_vectorizer.pkl"))
    except:
        print("❌ Modelos no encontrados.")
        return

    correctos = 0
    fallos = []

    print(f"\n{'#':<3} | {'ESTADO':<10} | {'PREDICCIÓN':<10} | {'TEXTO'}")
    print("-" * 100)

    for i, d in enumerate(data_v3, 1):
        res, prob, meta = analizar_sentimiento_hibrido(d['text'], model, vectorizer)
        expected = d['expected']
        
        status = "✅ OK" if res.lower() == expected.lower() else "❌ FAIL"
        if status == "✅ OK": 
            correctos += 1
        else:
            fallos.append((i, d['text'], expected, res, meta.get('score')))
        
        print(f"{i:<3} | {status:<10} | {res:<10} | {d['text'][:60]}...")

    print("-" * 100)
    acc = (correctos / len(data_v3)) * 100
    print(f"BENCHMARK V3 G68 ELITE: {correctos}/{len(data_v3)} ({acc:.2f}%)")

    if fallos:
        print("\n🔍 ANÁLISIS DE FALLOS CRÍTICOS:")
        for f in fallos:
            print(f"[{f[0]}] {f[1]}")
            print(f"    Esperado: {f[2]} | Predicción: {f[3]} | Score: {f[4]}")

if __name__ == "__main__":
    run_benchmark_v3()
