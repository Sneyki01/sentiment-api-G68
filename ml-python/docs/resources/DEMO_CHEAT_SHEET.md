# 🚀 Modelo Integral para el Análisis de Sentimientos - G68 Cheat Sheet

## 1. Preparar Entorno (Terminal)
Siempre ejecuta esto primero para ubicarte en la carpeta correcta:

```powershell
cd "ml-python\src\app"
```

## 2. Arrancar el Servidor
Copia y pega este bloque completo:

```powershell
python -u -m uvicorn main:app --host 0.0.0.0 --port 8080
```
*(Recuerda: `Ctrl + C` para detenerlo)*

## 3. Probar en Navegador
*   **Swagger UI:** [http://localhost:8080/docs](http://localhost:8080/docs)

---

## 💾 Guardar Cambios Críticos (Git)
Si necesitas guardar los arreglos de última hora:

```powershell
git add .
git commit -m "Entrega final: Modelo Integral para el Análisis de Sentimientos"
git push origin feature/entrega-modelo-integral
```
