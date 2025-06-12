Perfecto. Vamos a explicar el código **línea por línea** de los dos archivos clave del proyecto **WebSocket + Redis Pub/Sub** en FastAPI:

---

## 📜 `main.py`

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Path
from app.redis_pubsub import subscribe_to_channel, publish_to_channel
import logging

app = FastAPI()
logging.basicConfig(level=logging.INFO)

# Mapeo de canales -> set de conexiones WebSocket
connections_by_channel = {}
```

🔹 Se importa FastAPI y los métodos de pub/sub de Redis.
🔹 `connections_by_channel` almacena todas las conexiones activas por canal.

---

### Endpoint WebSocket

```python
@app.websocket("/ws/{channel}")
async def websocket_endpoint(websocket: WebSocket, channel: str):
    await websocket.accept()
```

🔸 Se acepta la conexión WebSocket al canal dinámico (ej: `/ws/noticias`).

```python
    if channel not in connections_by_channel:
        connections_by_channel[channel] = set()
```

🔸 Si es la primera vez que alguien se conecta a este canal, se inicializa su set de clientes.

---

### Redis listener (pub/sub)

```python
        async def forward_message(msg: str):
            for conn in connections_by_channel[channel]:
                await conn.send_text(f"[{channel}] {msg}")
```

🔸 Esta función será llamada cada vez que Redis publique un mensaje en ese canal.
🔸 Reenvía el mensaje a todos los clientes WebSocket conectados a ese canal.

```python
        await subscribe_to_channel(channel, forward_message)
```

🔸 Se suscribe al canal Redis (una sola vez por canal) y asocia el callback `forward_message`.

---

### Registro del cliente

```python
    connections_by_channel[channel].add(websocket)
    logging.info(f"Cliente conectado a canal {channel}. Total: {len(connections_by_channel[channel])}")
```

---

### Escucha de mensajes (el cliente no publica nada, pero mantiene viva la conexión)

```python
    try:
        while True:
            _ = await websocket.receive_text()
```

🔹 Se mantiene la conexión viva esperando mensajes que nunca se usarán.
🔹 Si no pones esto, FastAPI cierra el WebSocket al instante.

---

### Manejo de desconexión

```python
    except WebSocketDisconnect:
        connections_by_channel[channel].remove(websocket)
        logging.info(f"Cliente desconectado de canal {channel}")
```

---

### Endpoint REST para publicar

```python
@app.post("/publish/{channel}")
async def send_to_channel(channel: str, message: str):
    await publish_to_channel(channel, message)
    return {"status": "published", "channel": channel, "message": message}
```

🔸 Cualquier petición POST a `/publish/{canal}?message=...` publica en Redis.
🔸 Todos los clientes suscritos por WebSocket lo recibirán en tiempo real.

---

## 📜 `redis_pubsub.py`

Este archivo contiene la integración asincrónica con Redis para Pub/Sub.

```python
import redis.asyncio as redis
import asyncio
```

🔸 Usamos el cliente oficial `redis.asyncio`, moderno y mantenido.

---

### Configuración

```python
REDIS_URL = "redis://redis:6379"
pubsub_instances = {}  # canal -> tarea activa
```

🔸 `pubsub_instances` se usa para evitar crear múltiples listeners para el mismo canal.

---

### 📥 `subscribe_to_channel(channel, callback)`

```python
async def subscribe_to_channel(channel: str, callback):
    if channel in pubsub_instances:
        return  # ya existe un listener
```

🔹 Evita duplicar listeners si ya se está suscrito a ese canal.

```python
    client = redis.from_url(REDIS_URL)
    pubsub = client.pubsub()
    await pubsub.subscribe(channel)
```

🔸 Se conecta a Redis y se suscribe al canal.

---

### Escucha continua

```python
    async def reader():
        async for message in pubsub.listen():
            if message["type"] == "message":
                data = message["data"].decode()
                await callback(data)
```

🔸 Esta función se ejecuta en bucle y llama al callback cada vez que Redis publica un mensaje.

```python
    task = asyncio.create_task(reader())
    pubsub_instances[channel] = task
```

🔸 Crea una tarea de fondo con `asyncio.create_task` para que el listener viva de forma independiente.

---

### 📤 `publish_to_channel(channel, message)`

```python
async def publish_to_channel(channel: str, message: str):
    client = redis.from_url(REDIS_URL)
    await client.publish(channel, message)
```

🔹 Publica un mensaje en el canal Redis.
🔹 Automáticamente será recibido por todos los listeners suscritos al mismo canal.

---

## ✅ Resumen del flujo completo

```mermaid
flowchart TD
  A[Cliente WebSocket se conecta a /ws/{canal}] --> B[Acepta conexión y registra socket]
  B --> C[Se suscribe en Redis al canal]
  D[Otro cliente o API REST publica en /publish/{canal}]
  D --> E[Redis recibe mensaje]
  E --> F[Callback reenvía mensaje a todos los WebSocket de ese canal]
```

---

## Pruebas

```bash
curl -X POST "http://localhost:8000/publish/noticias?message=Hola+desde+el+backend"
```

Abrir un par de:

```bash
 ws://localhost:8000/ws/noticias
```