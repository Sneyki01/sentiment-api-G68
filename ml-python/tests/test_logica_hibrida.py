import requests
import json

API_URL = "http://localhost:8080/sentiment"

# Caso problemático original
caso_problematico = {
    "text": "Me cobraron el mini bar que nunca toqué y ahora dicen que no pueden devolverme el dinero"
}

print("=" * 80)
print("🧪 PRUEBA DE LÓGICA HÍBRIDA (Diccionario + Modelo ML)")
print("=" * 80)
print(f"\n📝 Texto: '{caso_problematico['text']}'")
print()

response = requests.post(API_URL, json=caso_problematico)

if response.status_code == 200:
    resultado = response.json()
    print("✅ Respuesta exitosa:")
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
    print()
    print("📊 Análisis:")
    print(f"   • Prevision: {resultado['prevision']}")
    print(f"   • Probabilidad: {resultado['probabilidad']}")
    print(f"   • Top Features: {resultado['top_features']}")
    print()
    
    # Verificar mejora
    features = resultado['top_features'].split(' | ')
    print("🔍 N-gramas detectados:")
    for i, feat in enumerate(features, 1):
        num_palabras = len(feat.split())
        tipo = "frase" if num_palabras >= 2 else "palabra"
        print(f"   {i}. '{feat}' ({tipo}, {num_palabras} palabra{'s' if num_palabras > 1 else ''})")
    
    print()
    if any(len(f.split()) >= 2 for f in features):
        print("✅ MEJORA CONFIRMADA: Se detectaron frases contextuales (2+ palabras)")
    else:
        print("⚠️ Solo se detectaron palabras sueltas")
else:
    print(f"❌ Error: HTTP {response.status_code}")
    print(response.text)

print("=" * 80)
