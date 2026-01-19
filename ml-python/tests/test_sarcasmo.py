import requests
import json

API_URL = "http://localhost:8080/sentiment"

caso = {
    "text": "La habitación es muy 'acogedora', si por acogedora entiendes que no cabe ni mi maleta"
}

print("=" * 80)
print("🧪 PRUEBA: Sarcasmo / Ironía")
print("=" * 80)
print(f"\n📝 Texto: '{caso['text']}'")
print("\n💡 Análisis lingüístico:")
print("   'acogedora' = Positivo (en diccionario)")
print("   'no cabe ni mi maleta' = Negativo (contexto)")
print("   Sentimiento esperado: NEGATIVO (Sarcasmo)")
print()

response = requests.post(API_URL, json=caso)

if response.status_code == 200:
    resultado = response.json()
    print("✅ Respuesta:")
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
    print()
    print("📊 Análisis:")
    print(f"   • Prevision: {resultado['prevision']}")
    print(f"   • Probabilidad: {resultado['probabilidad']}")
    print(f"   • Top Features: {resultado['top_features']}")
    
    # Validar resultado
    if resultado['prevision'] == 'Negativo':
        print("\n🎉 INCREÍBLE: El sistema detectó el sarcasmo!")
    else:
        print(f"\n⚠️ RETO: El sistema clasificó como {resultado['prevision']} (probablemente por la palabra 'acogedora')")
else:
    print(f"❌ Error: HTTP {response.status_code}")

print("=" * 80)
