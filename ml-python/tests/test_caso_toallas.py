import requests
import json

API_URL = "http://localhost:8080/sentiment"

caso = {
    "text": "Las toallas estaban limpias y las cambiaban todos los días"
}

print("=" * 80)
print("🧪 PRUEBA: Higiene Positiva")
print("=" * 80)
print(f"\n📝 Texto: '{caso['text']}'")
print("\n💡 Análisis lingüístico:")
print("   'limpias' = Positivo (diccionario)")
print("   Contexto de servicio regular = Positivo")
print("   Sentimiento esperado: POSITIVO")
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
    
    if resultado['prevision'] == 'Positivo':
        print("\n✅ CORRECTO: Clasificado como Positivo")
    else:
        print(f"\n❌ INCORRECTO: Debería ser Positivo, clasificó como {resultado['prevision']}")
else:
    print(f"❌ Error: HTTP {response.status_code}")

print("=" * 80)
