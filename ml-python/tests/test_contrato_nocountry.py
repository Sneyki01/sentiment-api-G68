"""
Test de Validación del Contrato NoCountry
Verifica que el API cumpla con el esquema:
- prevision: str (Positivo, Negativo, Neutral)
- probabilidad: float (0.0 a 1.0)
- top_features: str (n-gramas separados por ' | ')
"""
import requests
import json

API_URL = "http://localhost:8080/sentiment"

# Casos de prueba representativos
CASOS_PRUEBA = [
    {
        "text": "hotel hermoso, volveré",
        "esperado": "Positivo",
        "descripcion": "Caso original reportado"
    },
    {
        "text": "excelente hotel pero muy sucio",
        "esperado": "Negativo",
        "descripcion": "Contraste con crítico"
    },
    {
        "text": "no vuelvo nunca, pésimo servicio",
        "esperado": "Negativo",
        "descripcion": "Múltiples n-gramas negativos"
    },
    {
        "text": "vale la pena, lo recomiendo totalmente",
        "esperado": "Positivo",
        "descripcion": "Múltiples n-gramas positivos"
    },
    {
        "text": "encontré cucarachas en la habitación",
        "esperado": "Negativo",
        "descripcion": "Caso crítico"
    },
    {
        "text": "ni bien ni mal",
        "esperado": "Neutral",
        "descripcion": "Expresión neutral"
    }
]

def validar_contrato(response_json):
    """Valida que la respuesta cumpla con el contrato NoCountry"""
    errores = []
    
    # Verificar campos requeridos
    campos_requeridos = ["prevision", "probabilidad", "top_features"]
    for campo in campos_requeridos:
        if campo not in response_json:
            errores.append(f"❌ Falta campo requerido: '{campo}'")
    
    # Validar tipos de datos
    if "prevision" in response_json:
        if not isinstance(response_json["prevision"], str):
            errores.append(f"❌ 'prevision' debe ser str, es {type(response_json['prevision'])}")
        elif response_json["prevision"] not in ["Positivo", "Negativo", "Neutral"]:
            errores.append(f"❌ 'prevision' debe ser Positivo/Negativo/Neutral, es '{response_json['prevision']}'")
    
    if "probabilidad" in response_json:
        if not isinstance(response_json["probabilidad"], (int, float)):
            errores.append(f"❌ 'probabilidad' debe ser float, es {type(response_json['probabilidad'])}")
        elif not (0.0 <= response_json["probabilidad"] <= 1.0):
            errores.append(f"❌ 'probabilidad' debe estar entre 0.0 y 1.0, es {response_json['probabilidad']}")
    
    if "top_features" in response_json:
        if not isinstance(response_json["top_features"], str):
            errores.append(f"❌ 'top_features' debe ser str, es {type(response_json['top_features'])}")
    
    return errores

def probar_caso(caso):
    """Prueba un caso individual"""
    try:
        response = requests.post(API_URL, json={"text": caso["text"]}, timeout=5)
        
        if response.status_code != 200:
            return {
                "exito": False,
                "error": f"HTTP {response.status_code}",
                "caso": caso
            }
        
        resultado = response.json()
        errores_contrato = validar_contrato(resultado)
        
        return {
            "exito": len(errores_contrato) == 0,
            "caso": caso,
            "respuesta": resultado,
            "errores_contrato": errores_contrato
        }
    
    except Exception as e:
        return {
            "exito": False,
            "error": str(e),
            "caso": caso
        }

def main():
    print("=" * 80)
    print("🧪 VALIDACIÓN DEL CONTRATO NOCOUNTRY")
    print("=" * 80)
    print(f"\n📊 Casos a probar: {len(CASOS_PRUEBA)}\n")
    
    resultados = []
    
    for i, caso in enumerate(CASOS_PRUEBA, 1):
        print(f"\n[{i}/{len(CASOS_PRUEBA)}] {caso['descripcion']}")
        print(f"   Texto: '{caso['text']}'")
        
        resultado = probar_caso(caso)
        resultados.append(resultado)
        
        if "error" in resultado:
            print(f"   ❌ ERROR: {resultado['error']}")
        elif not resultado["exito"]:
            print(f"   ❌ CONTRATO INVÁLIDO:")
            for error in resultado["errores_contrato"]:
                print(f"      {error}")
        else:
            resp = resultado["respuesta"]
            print(f"   ✅ VÁLIDO")
            print(f"      • prevision: {resp['prevision']}")
            print(f"      • probabilidad: {resp['probabilidad']}")
            print(f"      • top_features: {resp['top_features']}")
    
    # Resumen
    print("\n" + "=" * 80)
    print("📈 RESUMEN DE VALIDACIÓN")
    print("=" * 80)
    
    exitosos = sum(1 for r in resultados if r["exito"])
    fallidos = len(resultados) - exitosos
    
    print(f"\n✅ Casos válidos: {exitosos}/{len(resultados)}")
    print(f"❌ Casos inválidos: {fallidos}/{len(resultados)}")
    
    if fallidos == 0:
        print("\n🎉 ¡TODOS LOS CASOS CUMPLEN CON EL CONTRATO NOCOUNTRY!")
    else:
        print("\n⚠️ Hay casos que no cumplen con el contrato")
    
    # Mostrar ejemplos de top_features
    print("\n" + "=" * 80)
    print("💡 EJEMPLOS DE TOP_FEATURES")
    print("=" * 80)
    
    for r in resultados:
        if r["exito"]:
            caso = r["caso"]
            resp = r["respuesta"]
            print(f"\n'{caso['text'][:50]}...'")
            print(f"  → {resp['top_features']}")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()
