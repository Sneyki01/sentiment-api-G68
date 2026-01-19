import requests
import json

API_URL = "http://localhost:8080/sentiment"

caso = {
    "text": "No puedo dejar de recomendar este hotel después del trato que recibimos"
}

print("=" * 80)
print("🔍 VERIFICACIÓN: ¿Qué datos retorna el motor híbrido?")
print("=" * 80)
print(f"\n📝 Texto: '{caso['text']}'")
print()

# Hacer request directo
response = requests.post(API_URL, json=caso)

if response.status_code == 200:
    resultado = response.json()
    
    print("📦 RESPUESTA COMPLETA DEL API:")
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
    print()
    
    print("📊 CAMPOS DISPONIBLES:")
    for key in resultado.keys():
        print(f"   • {key}: {type(resultado[key]).__name__}")
    
    print()
    if 'explicabilidad' in resultado:
        print("✅ El campo 'explicabilidad' ESTÁ disponible")
        print(json.dumps(resultado['explicabilidad'], indent=2, ensure_ascii=False))
    else:
        print("❌ El campo 'explicabilidad' NO está en la respuesta del API")
        print("   (Pero podría estar disponible internamente en motor_hibrido)")

print("=" * 80)
