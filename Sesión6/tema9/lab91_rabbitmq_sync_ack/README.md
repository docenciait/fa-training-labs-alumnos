## 1. Levantamos los servicios

```bash
docker compose up -d --build
```


![alt text](image.png)


## 2. Vemos cómo se ha recibido el ack del consumidor

- Prueba:

```bash
curl -X 'POST' \
  'http://localhost:8000/send' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "tipo": "msg",
  "id": "Identificador 1",
  "payload": {
    "additionalProp1": {"name":"John"}
  }
}'
```

![alt text](image-4.png)

## Otro ejemplo seguido

![alt text](image-5.png)
