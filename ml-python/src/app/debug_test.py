import json
import sys
import os

# Ajuste de ruta para importar desde la misma carpeta
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from motor_hibrido import enriquecer_respuesta

# PRUEBA UNIVERSAL: No menciona nada del hotel, pero es una queja de servicio
mensaje_universal = "El servicio fue pésimo y el proceso es muy lento, una decepción total."

# Simulamos que la IA detecta Negativo con 0.70
resultado = enriquecer_respuesta(mensaje_universal, "Negativo", 0.70)

print("\n" + "="*50)
print("🎯 TEST UNIVERSAL G68 (SIN SESGO HOTELERO)")
print("="*50)
print(f"TEXTO: {mensaje_universal}")
print("-" * 50)
print(json.dumps(resultado, indent=4, ensure_ascii=False))
print("="*50 + "\n")