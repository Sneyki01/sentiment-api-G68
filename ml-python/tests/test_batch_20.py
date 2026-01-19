import requests
import json
import time

API_URL = "http://localhost:8080/sentiment"

casos = [
    {"id": 1, "tipo": "Fácil Positiva", "text": "La estancia fue maravillosa y el personal nos trató como si fuéramos de la familia."},
    {"id": 2, "tipo": "Fácil Negativa", "text": "El producto llegó roto y la caja estaba completamente aplastada, una pérdida de dinero."},
    {"id": 3, "tipo": "Sarcasmo", "text": "¡Qué buen servicio! Me prometieron entrega en 24 horas y ya vamos por la segunda semana."},
    {"id": 4, "tipo": "Doble Negación", "text": "No puedo decir que no esté satisfecho con la resolución que me dieron finalmente."},
    {"id": 5, "tipo": "Sentimiento Mixto", "text": "La habitación del hotel era preciosa, pero el ruido de la discoteca de abajo hacía imposible dormir."},
    {"id": 6, "tipo": "Operativo", "text": "La aplicación se cierra sola cada vez que intento subir la foto del comprobante."},
    {"id": 7, "tipo": "Marketing", "text": "El anuncio mostraba un resort de lujo, pero la realidad es un edificio viejo sin mantenimiento."},
    {"id": 8, "tipo": "Atención al Cliente", "text": "El agente fue muy educado, pero no tenía ni idea de cómo solucionar mi problema técnico."},
    {"id": 9, "tipo": "Administrativo", "text": "Me han cobrado la suscripción dos veces y nadie me da una respuesta clara sobre el reembolso."},
    {"id": 10, "tipo": "Neutra", "text": "El hotel dispone de tres ascensores y una zona de cafetería abierta hasta las 11."},
    {"id": 11, "tipo": "Grocera", "text": "Es una puta vergüenza que traten así a los clientes que llevamos años con ustedes."},
    {"id": 12, "tipo": "Dificil (Ironía)", "text": "Gracias por enviarme el manual de instrucciones en un idioma que solo hablan en tres islas del Pacífico."},
    {"id": 13, "tipo": "Urgencia", "text": "Necesito una respuesta inmediata; mi evento es mañana y el equipo sigue sin encender."},
    {"id": 14, "tipo": "Falsa Cortesía", "text": "Agradezco mucho que me hayan hecho perder toda la mañana para decirme que el sistema está caído."},
    {"id": 15, "tipo": "Positiva con Salvedad", "text": "El servicio es excelente, aunque el precio me parece un poco fuera de mercado."},
    {"id": 16, "tipo": "Ambigüedad", "text": "Ya me lo decía mi hermano, con esta empresa siempre es una aventura saber qué va a pasar."},
    {"id": 17, "tipo": "Operativo", "text": "El wifi del hotel solo funciona si sacas el brazo por la ventana, increíble en 2026."},
    {"id": 18, "tipo": "Marketing", "text": "Me encanta que usen materiales reciclados en el envío, eso me hace confiar más en la marca."},
    {"id": 19, "tipo": "Doble Negación", "text": "No es que no me guste la nueva interfaz, pero me cuesta mucho encontrar el botón de salida."},
    {"id": 20, "tipo": "Final Abierto", "text": "Después de lo visto hoy, dudo mucho que volvamos a contratar nada con este grupo."}
]

print("=" * 100)
print(f"🚀 INICIANDO BATCH DE PRUEBAS G68 ({len(casos)} casos)")
print("=" * 100)
print(f"{'ID':<4} | {'TIPO':<22} | {'PREVISIÓN':<10} | {'PROB':<6} | {'TOP FEATURES':<30}")
print("-" * 100)

for caso in casos:
    try:
        response = requests.post(API_URL, json={"text": caso["text"]})
        if response.status_code == 200:
            res = response.json()
            features = res['top_features']
            if len(features) > 30:
                features = features[:27] + "..."
            
            print(f"{caso['id']:<4} | {caso['tipo']:<22} | {res['prevision']:<10} | {res['probabilidad']:<6} | {features:<30}")
        else:
            print(f"{caso['id']:<4} | ERROR HTTP {response.status_code}")
    except Exception as e:
        print(f"{caso['id']:<4} | ERROR CONN: {e}")
    # time.sleep(0.1) # Pequeña pausa para no saturar logs visualmente

print("=" * 100)
