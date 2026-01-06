# 🧠 Entrega Final: Sentiment API G68

¡Hola! Soy **Alexis**. Aquí les dejo mi motor de sentimiento. Me enfoqué en que el sistema entienda el contexto real, especialmente el sarcasmo y las opiniones dudosas.

### 🚀 Lo que hace mi sistema:
* **Híbrido:** Combino el entrenamiento del modelo con un Motor de Reglas (Lógica humana).
* **Honesto:** Si el texto es ambiguo, el sistema marca **Neutro** en vez de forzar un resultado.
* **Detector de Sarcasmo:** Si el usuario usa palabras positivas para quejarse (ej. "Genial la suciedad"), el sistema detecta la ironía y corrige la previsión.
* **Limpio:** Procesamiento UTF-8 que respeta nuestra eñe y acentos.

### 📊 Mis Métricas (Benchmark):
* **Precisión:** 89% (Un salto importante frente al modelo base).
* **Sarcasmo:** Identificado y corregido en tiempo real.

### 🛠️ Quick Start:
```powershell
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8080