FROM python:3.11-slim

WORKDIR /app

# Dependencias del sistema mínimas
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Exponemos el puerto acordado
EXPOSE 8080

# Comando de ejecución usando el módulo como paquete
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8080"]