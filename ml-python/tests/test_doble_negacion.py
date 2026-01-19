import requests
import json

API_URL = "http://localhost:8080/sentiment"

caso = {
    "text": "No puedo dejar de recomendar este hotel después del trato que recibimos"
}

print("=" * 80)
print("🧪 PRUEBA: Doble negación (positivo)")
print("=" * 80)
print(f"\n📝 Texto: '{caso['text']}'")
print("\n💡 Análisis lingüístico:")
print("   'No puedo dejar de recomendar' = 'Recomiendo mucho' (doble negación)")
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
        print("✅ CORRECTO: El sistema detectó correctamente la doble negación")
        print("   La frase es positiva a pesar de tener 'no' y 'dejar'")
    elif resultado['prevision'] == 'Negativo':
        print("❌ ERROR: El sistema interpretó mal la doble negación")
        print("   'No puedo dejar de recomendar' = 'Recomiendo mucho' (POSITIVO)")
    else:
        print("⚠️ NEUTRO: El sistema no pudo determinar el sentimiento")
else:
    print(f"❌ Error: HTTP {response.status_code}")

print("=" * 80)
