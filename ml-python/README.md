# 🚀 Guía de Uso - Sentiment Analysis API

Esta sección detalla cómo poner en marcha y probar el microservicio de IA para el análisis de sentimiento.

## 1. Gestion de Dependencias

El proyecto utiliza una estructura dual de archivos `requirements` para optimizar el peso del despliegue y mantener las herramientas de análisis separadas del servidor de producción.

## 1. Instalación según el Entorno

### A. Solo para Ejecución (Producción/API)
Si solo necesitas poner en marcha la API de sentimientos, utiliza el archivo base. </br>
Este contiene lo estrictamente necesario: `fastapi`, `uvicorn`, `scikit-learn`, entre otros.

```bash
pip install -r requirements.txt
```

### B. Para Experimentación (Desarrollo/Data Science)
Si vas a trabajar en los Notebooks, realizar análisis visual o re-entrenar el modelo, debes instalar las herramientas adicionales (como pandas, matplotlib, seaborn y nltk) que se encuentran en el archivo de desarrollo.

```bash
pip install -r requirements-dev.txt
```

*Nota: **requirements-dev.txt** incluye automáticamente todas las dependencias del archivo de producción.*

## 2. Ejecución del Servidor

Existen dos formas de arrancar la API dependiendo de tu ubicación en la terminal.</br>
**Es indispensable tener el entorno virtual activo.**

### Opción A: Desde la carpeta del código

Si te encuentras en `ml-python/src/app`:

```bash
uvicorn main:app --reload --port 8080

```

### Opción B: Desde la raíz del componente (Recomendado)

Si te encuentras en la carpeta `ml-python`:

```bash
uvicorn main:app --app-dir src/app --reload --port 8080

```

***Nota:** Usamos `--app-dir` para que el servidor localice correctamente el módulo interno (`utils.py`) y el modelo entrenado.*

---

## 3. Puntos de Acceso (Endpoints)

Una vez encendido el servidor, puedes acceder a:

* **Estado de la API:** [http://127.0.0.1:8080/](http://127.0.0.1:8080/)
* **Documentación Interactiva (Swagger):** [http://127.0.0.1:8080/docs](http://127.0.0.1:8080/docs)
* **Esquema OpenAPI (JSON):** [http://127.0.0.1:8080/openapi.json](http://127.0.0.1:8080/openapi.json)

---

## 4. Pruebas de Inferencia

Puedes probar el modelo de dos maneras:

### Vía Swagger (Interfaz Visual)

1. Ve a `/docs`.
2. Despliega el método **POST** `/predict/sentiment`.
3. Presiona **"Try it out"**.
4. Edita el JSON de ejemplo y presiona **"Execute"**.

### Vía Terminal (cURL)

Abre una nueva terminal (en la 1ra ya esta activo el servidor) y ejecuta el siguiente comando para probar una predicción rápida:

```bash
curl -X 'POST' \
  'http://127.0.0.1:8080/predict/sentiment' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "La comida estuvo excelente y el servicio fue muy rápido."
}'
```


## 5. Restricciones de Entrada

La API cuenta con validaciones de seguridad. Se rechazará cualquier petición que:

* Contenga texto vacío o solo espacios.
* Sea estrictamente numérica (ej. `"12345"`).
* No sea de tipo string.

## 6. Detener el Servicio

Para apagar el servidor, simplemente presiona `Ctrl + C` en la terminal donde se está ejecutando Uvicorn.
