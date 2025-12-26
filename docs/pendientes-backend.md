# Tareas pendientes Backend SentimentAPI

## - Integracion ML Client

### Objetivo:

Se debe crear el componente que llame al servicio HTTP a Python y devuelva
JSON con etiquetas "prevision", "probabilidad".

### Entregable para considerar terminada la tarea:

-[ ] clase que haga POST a ```ml.base-url + ml.predict-path``` 

-[ ] Recibir informacion y mandarla a servicio ```SentimentService```

-[ ] Configurar TimeOut para recibir respuesta de servicio

-[ ] Si ML no responde, lanzar excepcion controlada con mensaje claro

-[ ] PR hacia ```dev```

Asignado:
Lorena Raygoza

## - Error ML no disponible, Health

### Objetivo:

Que Backend sea "demo-proof"

- Si ML se cae -> el usuario recibe error 503 limpio
- health endopints para debug rapido

### Entregable para considerar terminada la tarea:

-[ ] ```GET /health``` que responda con ```{"status": "ok"}```

-[ ] (Opcional) ```GET /health/ml``` que intente llamar al ML ```health```

-[ ] Excepcion custom para ML caido

-[ ] Handler en ```GlbalExceptionHandler``` que devuelva 503 con ```ErrorResponse```

-[ ] PR hacia ```dev```

Asignado: Edwing Herrera