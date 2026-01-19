import requests
import json

API_URL = "http://localhost:8080/sentiment"

caso = {
    "text": "El hotel es normal, ni bueno ni malo."
}

print("=" * 80)
print("🧪 PRUEBA: Neutralidad explícita")
print("=" * 80)
print(f"\n📝 Texto: '{caso['text']}'")
print("\n💡 Análisis lingüístico:")
print("   'normal' = Peso 0.0")
print("   'ni bueno ni malo' = Patrón neutro forzado")
print("   Sentimiento esperado: NEUTRAL (o Neutro)")
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
    pred = resultado['prevision'].lower()
    if 'neutr' in pred: # Neutral o Neutro
        print("\n✅ CORRECTO: Clasificado como Neutral")
    else:
        print(f"\n❌ INCORRECTO: Debería ser Neutral, clasificó como {resultado['prevision']}")
else:
    print(f"❌ Error: HTTP {response.status_code}")

print("=" * 80)
