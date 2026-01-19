import requests
import json

API_URL = "http://localhost:8080/sentiment"

casos = [
    # --- POSITIVOS (RESOLUCIÓN) ---
    {"id": 1, "cat": "Higiene (Pos)", "text": "Al notar una mancha en la alfombra, el equipo de limpieza desinfectó toda la habitación de inmediato."},
    {"id": 2, "cat": "Cobros (Pos)", "text": "Hubo un error en mi factura, pero el departamento de cuentas lo corrigió y me devolvió el dinero hoy."},
    {"id": 3, "cat": "Atención (Pos)", "text": "A pesar del caos en la entrada, la recepcionista mantuvo la calma y nos atendió con mucha profesionalidad."},
    {"id": 4, "cat": "Higiene (Pos)", "text": "Me impresionó lo limpio que estaba el spa; se nota que siguen protocolos sanitarios muy estrictos."},
    {"id": 5, "cat": "Cobros (Pos)", "text": "Tuve un cargo duplicado y, tras una sola llamada, el banco y el hotel lo solucionaron en 24 horas."},
    {"id": 6, "cat": "Atención (Pos)", "text": "El gerente de guardia gestionó mi queja con una empatía y rapidez que no esperaba."},
    {"id": 7, "cat": "Higiene (Pos)", "text": "El personal de cocina fue muy cuidadoso con mi alergia severa y limpiaron toda el área para mi pedido."},
    {"id": 8, "cat": "Cobros (Pos)", "text": "Me aplicaron el descuento de fidelidad sin tener que solicitarlo, un gesto muy transparente."},
    {"id": 9, "cat": "Atención (Pos)", "text": "El equipo de seguridad actuó rápido cuando perdí mi cartera y la recuperaron en minutos."},
    {"id": 10, "cat": "Higiene (Pos)", "text": "El baño común brillaba y olía a desinfectante fresco cada vez que entraba, excelente trabajo."},
    
    # --- NEUTROS (INFORMATIVOS) ---
    {"id": 11, "cat": "Higiene (Neu)", "text": "El hotel informa que las habitaciones se limpian diariamente entre las 10:00 y las 14:00 horas."},
    {"id": 12, "cat": "Cobros (Neu)", "text": "El depósito de seguridad se bloquea al hacer el check-in y se libera al finalizar la estancia."},
    {"id": 13, "cat": "Atención (Neu)", "text": "El horario de atención telefónica para reclamaciones administrativas es de lunes a viernes."},
    {"id": 14, "cat": "Higiene (Neu)", "text": "Se han instalado dispensadores de gel hidroalcohólico en todas las entradas del edificio."},
    {"id": 15, "cat": "Cobros (Neu)", "text": "El sistema acepta tarjetas de crédito internacionales y pagos mediante transferencia bancaria."},
    {"id": 16, "cat": "Atención (Neu)", "text": "El personal de recepción está disponible las 24 horas para cualquier consulta informativa."},
    {"id": 17, "cat": "Higiene (Neu)", "text": "La normativa de higiene prohíbe el acceso de mascotas a la zona de manipulación de alimentos."},
    {"id": 18, "cat": "Cobros (Neu)", "text": "Recibí el desglose de conceptos por correo electrónico cinco minutos después del pago."},
    {"id": 19, "cat": "Atención (Neu)", "text": "Para hablar con un supervisor, es necesario rellenar primero el formulario de contacto inicial."},
    {"id": 20, "cat": "Higiene (Neu)", "text": "El agua de la piscina se analiza químicamente tres veces al día según la ley vigente."}
]

print("=" * 105)
print(f"🚀 INICIANDO BATCH RESOLUCIÓN/NEUTRALIDAD G68 ({len(casos)} casos)")
print("=" * 105)
print(f"{'ID':<4} | {'CATEGORÍA':<15} | {'PREVISIÓN':<10} | {'PROB':<6} | {'TOP FEATURES':<35}")
print("-" * 105)

positivos_ok = 0
neutros_ok = 0

for caso in casos:
    try:
        response = requests.post(API_URL, json={"text": caso["text"]})
        if response.status_code == 200:
            res = response.json()
            features = res['top_features']
            if len(features) > 32:
                features = features[:29] + "..."
            
            print(f"{caso['id']:<4} | {caso['cat']:<15} | {res['prevision']:<10} | {res['probabilidad']:<6} | {features:<35}")
            
            # Conteo de aciertos simulado (basado en etiquetas del ID)
            if caso['id'] <= 10 and res['prevision'] == 'Positivo':
                positivos_ok += 1
            elif (caso['id'] > 10 and 
                  (res['prevision'] == 'Neutral' or 
                   res['prevision'] == 'Neutro' or 
                   (res['prevision'] == 'Negativo' and res['probabilidad'] < 0.6))): # Tolerancia a negativo débil
                # Nota: Neutro puro es difícil sin palabras clave forzadas, veremos qué sale
                if res['prevision'] in ['Neutral', 'Neutro']:
                    neutros_ok += 1
        else:
            print(f"{caso['id']:<4} | ERROR HTTP {response.status_code}")
    except Exception as e:
        print(f"{caso['id']:<4} | ERROR CONN: {e}")

print("=" * 105)
print(f"📊 ACIERTOS POSITIVOS (Resolución): {positivos_ok}/10")
print(f"📊 ACIERTOS NEUTROS (Informativo): {neutros_ok}/10")
print("=" * 105)
