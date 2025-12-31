# Backend - Sentiment API (Spring boot)

## Estado actual

- Endopint '\sentiment' funcional (con mock)
- Validacion de input
- manejo de errores (400)
- Preparado para integracion con servicio ML (Python)

## Endopints
```yaml
POST: /sentiment
```
Recibe:
```json
{
  "text" : "..."
}
```

Devuelve:
```json
{
  "prevision" : "Neutro",
  "probabilidad" : "0.5"
}
```
**Pendiente**

- integracion con servicio ML (POST /predict/sentiment)
- Manejo de error 503 cuando ML no este disponible

**Puertos**

- Backend: 8000
- ML: 8080

