import requests

# Probar el caso original reportado
response = requests.post(
    "http://localhost:8080/sentiment",
    json={"text": "           hotel hermoso, volvere          "}
)

print("=" * 60)
print("CASO ORIGINAL REPORTADO:")
print("=" * 60)
print(f"Input: 'hotel hermoso, volvere'")
print(f"Response: {response.json()}")
print()

# Resultado esperado: Positivo (no Neutro)
resultado = response.json()
if resultado['prevision'] == 'Positivo':
    print("✅ ¡RESUELTO! Ahora clasifica correctamente como Positivo")
else:
    print(f"❌ AÚN FALLA: Clasificó como {resultado['prevision']}")
