import requests
import json
import os

API_URL = "http://localhost:8080/sentiment"

# Cargar casos
# Buscamos el archivo en la nueva carpeta tests relative to the root or current script dir
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
test_file = os.path.join(base_dir, "tests", "test_batch_100.py")
output_file = os.path.join(base_dir, "docs", "reports", "final_benchmark_G68.json")

with open(test_file, 'r', encoding='utf-8') as f:
    content = f.read()
    start = content.find('[', content.find('casos ='))
    end = content.find(']', start) + 1
    casos = eval(content[start:end])

results = []
correct = 0

for c in casos:
    try:
        r = requests.post(API_URL, json={"text": c["text"]})
        res = r.json()
        pred = res['prevision'].replace('[+] ', '').replace('[-] ', '')
        
        # Mapeo de esperado
        tipo = c['tipo']
        esperado = "Neutro"
        if tipo in ['Positivo']: esperado = "Positivo"
        elif tipo in ['Negativo', 'Crítico', 'Grocero', 'Urgencia', 'Engañoso', 'Sarcasmo', 'Ironía']: esperado = "Negativo"
        elif tipo in ['Neutro']: esperado = "Neutro"
        
        # Normalización para comparar
        pred_norm = "Neutro" if pred in ["Neutral", "Neutro"] else pred
        esp_norm = "Neutro" if esperado in ["Neutral", "Neutro"] else esperado
        
        is_correct = (pred_norm == esp_norm)
        if is_correct: correct += 1
        
        results.append({
            "id": c["id"],
            "text": c["text"][:50],
            "tipo": c["tipo"],
            "pred": pred,
            "esperado": esperado,
            "status": "OK" if is_correct else "ERR"
        })
    except Exception as e:
        results.append({"id": c["id"], "status": "FAIL_CONN"})

total = len(casos)
accuracy = (correct / total) * 100

summary = {
    "total": total,
    "correct": correct,
    "accuracy": f"{accuracy:.2f}%",
    "details": results
}

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(summary, f, indent=2, ensure_ascii=False)

print(f"BENCHMARK COMPLETO: {correct}/{total} ({accuracy:.2f}%)")
