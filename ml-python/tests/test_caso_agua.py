import requests
import json

API_URL = "http://localhost:8080/sentiment"

caso = {
    "text": "El agua de la ducha salía fría y tardaron tres horas en mandar al técnico"
}

print("=" * 80)
print("🧪 PRUEBA CON CASO: Agua fría + demora en servicio")
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
else:
    print(f"❌ Error: HTTP {response.status_code}")

print("=" * 80)
