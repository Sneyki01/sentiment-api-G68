import json
import os

path = r'c:\ALURA - ONE\1. CIENCIA DE DATOS\HACKATHON\sentiment-api-G68\ml-python\data\raw\lexicon_final_optimizado.json'
temp_path = path + '.tmp'

print(f"Leyendo lexicón desde {path}...")
with open(path, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

print(f"Procesando {len(data)} palabras...")
with open(temp_path, 'w', encoding='utf-8') as f:
    f.write("{\n")
    items = list(data.items())
    for i, (k, v) in enumerate(items):
        original_score = float(v[0])
        # Ajustar el "super" de 2.0 a 1.0 y clipping general
        adjusted_score = max(-1.0, min(1.0, original_score))
        val_str = f"{adjusted_score:.3f}"
        
        comma = "," if i < len(items) - 1 else ""
        f.write(f'    "{k}": [\n        {val_str},\n')
        for j, elem in enumerate(v[1:]):
            sub_comma = "," if j < len(v[1:]) - 1 else ""
            f.write(f'        {json.dumps(elem, ensure_ascii=False)}{sub_comma}\n')
        f.write(f'    ]{comma}\n')
    f.write("}\n")

print("Lexicón procesado. Reemplazando archivo original...")
os.remove(path)
os.rename(temp_path, path)
print("¡Éxito!")
