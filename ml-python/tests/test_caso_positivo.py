import requests
import json

API_URL = "http://localhost:8080/sentiment"

caso = {
    "text": "La cama es una nube, volvería mañana mismo"
}

print("=" * 80)
print("🧪 PRUEBA: Frase positiva con metáfora")
print("=" * 80)
print(f"\n📝 Texto: '{caso['text']}'")
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
    print()
    
    # Analizar n-gramas
    features = resultado['top_features'].split(' | ')
    print("🔍 N-gramas detectados:")
    for i, feat in enumerate(features, 1):
        num_palabras = len(feat.split())
        tipo = "frase" if num_palabras >= 2 else "palabra"
        print(f"   {i}. '{feat}' ({tipo})")
    
    print()
    # Validar resultado
    if resultado['prevision'] == 'Positivo':
        print("✅ CORRECTO: Clasificado como Positivo")
    else:
        print(f"❌ INCORRECTO: Debería ser Positivo, clasificó como {resultado['prevision']}")
else:
    print(f"❌ Error: HTTP {response.status_code}")

print("=" * 80)
