"""
Script de Diagnóstico - Casos Simples de Sentimiento
Objetivo: Identificar palabras faltantes en el diccionario y validar lógica híbrida
"""
import requests
import json

# URL del API (asegúrate de que esté corriendo)
API_URL = "http://localhost:8080/sentiment"

# 30 casos de prueba con expectativa clara
CASOS_PRUEBA = [
    # === POSITIVOS CLAROS ===
    {"text": "hotel hermoso, volveré", "esperado": "Positivo", "categoria": "Positivo Simple"},
    {"text": "excelente servicio", "esperado": "Positivo", "categoria": "Positivo Simple"},
    {"text": "todo perfecto", "esperado": "Positivo", "categoria": "Positivo Simple"},
    {"text": "muy buena atención", "esperado": "Positivo", "categoria": "Positivo Simple"},
    {"text": "habitación limpia y cómoda", "esperado": "Positivo", "categoria": "Positivo Simple"},
    {"text": "desayuno delicioso", "esperado": "Positivo", "categoria": "Positivo Simple"},
    {"text": "personal amable", "esperado": "Positivo", "categoria": "Positivo Simple"},
    {"text": "lugar maravilloso", "esperado": "Positivo", "categoria": "Positivo Simple"},
    {"text": "vale la pena", "esperado": "Positivo", "categoria": "Positivo Simple"},
    {"text": "lo recomiendo totalmente", "esperado": "Positivo", "categoria": "Positivo Simple"},
    
    # === NEGATIVOS CLAROS ===
    {"text": "hotel horrible", "esperado": "Negativo", "categoria": "Negativo Simple"},
    {"text": "pésimo servicio", "esperado": "Negativo", "categoria": "Negativo Simple"},
    {"text": "muy sucio", "esperado": "Negativo", "categoria": "Negativo Simple"},
    {"text": "no vuelvo nunca", "esperado": "Negativo", "categoria": "Negativo Simple"},
    {"text": "mala experiencia", "esperado": "Negativo", "categoria": "Negativo Simple"},
    {"text": "habitación sucia", "esperado": "Negativo", "categoria": "Negativo Simple"},
    {"text": "comida terrible", "esperado": "Negativo", "categoria": "Negativo Simple"},
    {"text": "personal grosero", "esperado": "Negativo", "categoria": "Negativo Simple"},
    {"text": "decepcionante", "esperado": "Negativo", "categoria": "Negativo Simple"},
    {"text": "no lo recomiendo", "esperado": "Negativo", "categoria": "Negativo Simple"},
    
    # === NEUTROS CLAROS ===
    {"text": "normal", "esperado": "Neutro", "categoria": "Neutro Simple"},
    {"text": "ni bien ni mal", "esperado": "Neutro", "categoria": "Neutro Simple"},
    {"text": "está bien", "esperado": "Neutro", "categoria": "Neutro Simple"},
    {"text": "aceptable", "esperado": "Neutro", "categoria": "Neutro Simple"},
    
    # === CASOS COMPLEJOS (Sarcasmo/Contraste) ===
    {"text": "excelente hotel, pero sucio", "esperado": "Negativo", "categoria": "Contraste"},
    {"text": "buena ubicación pero caro", "esperado": "Neutro", "categoria": "Contraste"},
    {"text": "limpio pero ruidoso", "esperado": "Neutro", "categoria": "Contraste"},
    
    # === CASOS CRÍTICOS ===
    {"text": "encontré cucarachas", "esperado": "Negativo", "categoria": "Crítico"},
    {"text": "me robaron", "esperado": "Negativo", "categoria": "Crítico"},
    {"text": "peligroso", "esperado": "Negativo", "categoria": "Crítico"},
]

def probar_caso(caso, index):
    """Prueba un caso individual y retorna resultado"""
    try:
        response = requests.post(API_URL, json={"text": caso["text"]}, timeout=5)
        if response.status_code == 200:
            resultado = response.json()
            prevision = resultado.get("prevision", "").replace("[+] ", "").replace("[-] ", "")
            probabilidad = resultado.get("probabilidad", 0.0)
            
            # Validar si cumple expectativa
            cumple = prevision == caso["esperado"]
            emoji = "✅" if cumple else "❌"
            
            return {
                "index": index + 1,
                "texto": caso["text"],
                "esperado": caso["esperado"],
                "obtenido": prevision,
                "probabilidad": probabilidad,
                "cumple": cumple,
                "categoria": caso["categoria"],
                "emoji": emoji
            }
        else:
            return {
                "index": index + 1,
                "texto": caso["text"],
                "error": f"HTTP {response.status_code}",
                "cumple": False,
                "emoji": "⚠️"
            }
    except Exception as e:
        return {
            "index": index + 1,
            "texto": caso["text"],
            "error": str(e),
            "cumple": False,
            "emoji": "🔴"
        }

def main():
    print("=" * 80)
    print("🧪 DIAGNÓSTICO DE CASOS SIMPLES - G68 Sentiment API")
    print("=" * 80)
    print(f"\n📊 Total de casos a probar: {len(CASOS_PRUEBA)}\n")
    
    resultados = []
    
    # Ejecutar pruebas
    for i, caso in enumerate(CASOS_PRUEBA):
        resultado = probar_caso(caso, i)
        resultados.append(resultado)
        
        # Mostrar resultado en tiempo real
        if "error" in resultado:
            print(f"{resultado['emoji']} [{resultado['index']:02d}] ERROR: {resultado.get('error')}")
        else:
            print(f"{resultado['emoji']} [{resultado['index']:02d}] '{resultado['texto'][:40]:40s}' | "
                  f"Esperado: {resultado['esperado']:8s} | "
                  f"Obtenido: {resultado['obtenido']:8s} ({resultado['probabilidad']:.2f})")
    
    # === RESUMEN ESTADÍSTICO ===
    print("\n" + "=" * 80)
    print("📈 RESUMEN DE RESULTADOS")
    print("=" * 80)
    
    total = len(resultados)
    exitosos = sum(1 for r in resultados if r.get("cumple", False))
    fallidos = total - exitosos
    tasa_exito = (exitosos / total * 100) if total > 0 else 0
    
    print(f"\n✅ Casos Exitosos: {exitosos}/{total} ({tasa_exito:.1f}%)")
    print(f"❌ Casos Fallidos:  {fallidos}/{total} ({100-tasa_exito:.1f}%)")
    
    # Desglose por categoría
    print("\n📊 Desglose por Categoría:")
    categorias = {}
    for r in resultados:
        cat = r.get("categoria", "Desconocido")
        if cat not in categorias:
            categorias[cat] = {"total": 0, "exitosos": 0}
        categorias[cat]["total"] += 1
        if r.get("cumple", False):
            categorias[cat]["exitosos"] += 1
    
    for cat, stats in sorted(categorias.items()):
        tasa = (stats["exitosos"] / stats["total"] * 100) if stats["total"] > 0 else 0
        print(f"  • {cat:20s}: {stats['exitosos']}/{stats['total']} ({tasa:.0f}%)")
    
    # === ANÁLISIS DE FALLOS ===
    print("\n" + "=" * 80)
    print("🔍 ANÁLISIS DE CASOS FALLIDOS")
    print("=" * 80)
    
    fallos = [r for r in resultados if not r.get("cumple", False)]
    
    if not fallos:
        print("\n🎉 ¡No hay fallos! Todos los casos pasaron correctamente.")
    else:
        print(f"\nTotal de fallos: {len(fallos)}\n")
        for fallo in fallos:
            if "error" in fallo:
                print(f"❌ [{fallo['index']:02d}] ERROR TÉCNICO: {fallo.get('error')}")
                print(f"    Texto: '{fallo['texto']}'")
            else:
                print(f"❌ [{fallo['index']:02d}] '{fallo['texto']}'")
                print(f"    Esperado: {fallo['esperado']} | Obtenido: {fallo['obtenido']} ({fallo['probabilidad']:.2f})")
                print(f"    Categoría: {fallo['categoria']}")
            print()
    
    # === PALABRAS POTENCIALMENTE FALTANTES ===
    print("=" * 80)
    print("💡 PALABRAS CLAVE DETECTADAS EN CASOS FALLIDOS")
    print("=" * 80)
    
    palabras_en_fallos = set()
    for fallo in fallos:
        if "error" not in fallo:
            # Extraer palabras significativas (más de 3 letras)
            palabras = [p.strip().lower() for p in fallo['texto'].split() if len(p.strip()) > 3]
            palabras_en_fallos.update(palabras)
    
    if palabras_en_fallos:
        print("\nPalabras que podrían necesitar agregarse al diccionario:")
        print(", ".join(sorted(palabras_en_fallos)))
    else:
        print("\nNo se detectaron palabras faltantes obvias.")
    
    print("\n" + "=" * 80)
    print("✨ Diagnóstico completado")
    print("=" * 80)

if __name__ == "__main__":
    main()
