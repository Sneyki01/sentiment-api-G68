import requests
import json

API_URL = "http://localhost:8080/sentiment"

casos = [
    {"id": 1, "cat": "Higiene", "text": "Había moho en las paredes del baño y un olor a humedad que hacía difícil respirar."},
    {"id": 2, "cat": "Cobros", "text": "Me han cobrado la reserva dos veces y el banco dice que es culpa de su pasarela de pagos."},
    {"id": 3, "cat": "Atención", "text": "El gerente me gritó delante de otros clientes cuando pedí la hoja de reclamaciones."},
    {"id": 4, "cat": "Higiene", "text": "Encontré restos de comida y una cucaracha debajo de la mesa del restaurante."},
    {"id": 5, "cat": "Cobros", "text": "Publicitan un precio final, pero al llegar te cargan tasas 'obligatorias' que no figuran en la web."},
    {"id": 6, "cat": "Atención", "text": "Llamé por una emergencia médica en la habitación y nadie contestó en recepción durante 15 minutos."},
    {"id": 7, "cat": "Higiene", "text": "Las sábanas tenían manchas de sangre y la habitación claramente no había sido desinfectada."},
    {"id": 8, "cat": "Cobros", "text": "He cancelado mi suscripción hace meses y me siguen llegando cargos a mi tarjeta de crédito."},
    {"id": 9, "cat": "Atención", "text": "El agente de soporte se burló de mi acento y me colgó sin darme ninguna solución."},
    {"id": 10, "cat": "Higiene", "text": "El personal de cocina no usaba guantes ni mascarilla mientras manipulaba alimentos frescos."},
    {"id": 11, "cat": "Cobros", "text": "Siento que me han estafado; el cargo en mi cuenta es el triple de lo que firmé en el contrato."},
    {"id": 12, "cat": "Atención", "text": "Me ignoraron por completo en el mostrador mientras el personal hablaba de sus cosas personales."},
    {"id": 13, "cat": "Higiene", "text": "El agua de la piscina estaba turbia y varios niños salieron con erupciones en la piel."},
    {"id": 14, "cat": "Cobros", "text": "Intenté pagar en efectivo y me obligaron a usar una app que me cobró una comisión abusiva."},
    {"id": 15, "cat": "Atención", "text": "Es vergonzoso que una empresa de este tamaño no tenga un protocolo para personas con discapacidad."},
    {"id": 16, "cat": "Higiene", "text": "Había jeringuillas usadas en la zona de papeleras del parking del hotel, es un peligro."},
    {"id": 17, "cat": "Cobros", "text": "Me bloquearon un depósito de seguridad de 500 euros y llevan un mes sin liberarlo."},
    {"id": 18, "cat": "Atención", "text": "Me prometieron una compensación por los fallos y ahora dicen que no tienen registro de esa promesa."},
    {"id": 19, "cat": "Higiene", "text": "El aire acondicionado expulsaba un polvo negro que me causó un ataque de alergia severo."},
    {"id": 20, "cat": "Cobros", "text": "Me han incluido en una lista de morosos por una factura que ellos mismos admitieron que era un error."}
]

print("=" * 105)
print(f"🚀 INICIANDO BATCH CRÍTICO G68 ({len(casos)} casos)")
print("=" * 105)
print(f"{'ID':<4} | {'CATEGORÍA':<10} | {'PREVISIÓN':<10} | {'PROB':<6} | {'TOP FEATURES':<35}")
print("-" * 105)

aciertos = 0
for caso in casos:
    try:
        response = requests.post(API_URL, json={"text": caso["text"]})
        if response.status_code == 200:
            res = response.json()
            features = res['top_features']
            if len(features) > 32:
                features = features[:29] + "..."
            
            print(f"{caso['id']:<4} | {caso['cat']:<10} | {res['prevision']:<10} | {res['probabilidad']:<6} | {features:<35}")
            
            if res['prevision'] == 'Negativo':
                aciertos += 1
        else:
            print(f"{caso['id']:<4} | ERROR HTTP {response.status_code}")
    except Exception as e:
        print(f"{caso['id']:<4} | ERROR CONN: {e}")

print("=" * 105)
print(f"📊 RESULTADO FINAL: {aciertos}/{len(casos)} detectados como NEGATIVO")
print("=" * 105)
