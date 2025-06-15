## Pruebas

- Puedes usar noticias como cualquier otro canal pero siempre debe llevar el parámetro message si no no lo entiende el websocket

```bash
curl -X POST "http://localhost:8000/publish/noticias?message=Hola+desde+el+backend"
```

Abrir un par de clientes para suscribirse:

```bash
 ws://localhost:8000/ws/noticias
```

## REDIS

[Redis Pub/Sub](https://redis.io/es/soluciones/casos-de-uso/mensajeria/#:~:text=Redis%20Pub%2FSub%20es%20un,el%20gran%20rendimiento%20son%20fundamentales.)

Tu ejemplo implementa un sistema **WebSocket + Redis Pub/Sub** en FastAPI para comunicación **en tiempo real** usando canales. Lo analizamos en detalle, porque está muy bien estructurado y combina varios conceptos:

---

## 🎯 ¿Qué hace este sistema?

* Los **clientes WebSocket** se suscriben a canales (por ejemplo, `/ws/noticias`).
* Cuando haces un `POST /publish/noticias`, se publica un mensaje en Redis.
* Redis **difunde el mensaje** a todos los **clientes WebSocket** conectados a ese canal.

Es una **arquitectura de Pub/Sub real**, donde:

* Redis actúa como **bus de mensajes**,
* FastAPI escucha Redis y reenvía a websockets activos.

---

## 🧱 Estructura general

```
┌────────────┐        ┌───────────────┐       ┌──────────────┐
│ Cliente WS │◄──────▶ FastAPI WS    │       │ Cliente WS   │
│ /ws/{canal}│        │ Suscriptor WS │◄────▶│ /ws/{canal}  │
└────────────┘        └──────┬────────┘       └──────────────┘
                             │
                             ▼
                     ┌──────────────┐
                     │ Redis PubSub │
                     └────┬─────────┘
                          ▼
                   POST /publish/{canal}
```

---

## 🧩 `main.py` explicado

### 🔌 WebSocket handler

```python
@app.websocket("/ws/{channel}")
async def websocket_endpoint(websocket: WebSocket, channel: str):
```

* Permite al cliente conectarse a un canal (ej: `/ws/chat`).
* Se guarda la conexión WebSocket en `connections_by_channel[channel]`.

### 🔁 Forwarding de mensajes

```python
        async def forward_message(msg: str):
            for conn in connections_by_channel[channel]:
                await conn.send_text(f"[{channel}] {msg}")
```

* Función que será llamada cada vez que Redis publique un mensaje en el canal.
* Reenvía el mensaje a todos los clientes WebSocket conectados.

### 📡 Suscripción única por canal

```python
await subscribe_to_channel(channel, forward_message)
```

* Solo crea un suscriptor Redis si no existe aún (usa `pubsub_instances`).

### 🔄 WebSocket listener (pero ignora entrada)

```python
while True:
    _ = await websocket.receive_text()
```

* Mantiene viva la conexión, pero **no usa los mensajes entrantes**.

### 🔚 Desconexión

```python
except WebSocketDisconnect:
    connections_by_channel[channel].remove(websocket)
```

* Cuando un cliente se desconecta, se elimina de la lista de conexiones activas.

---

### 📤 Publicación desde endpoint REST

```python
@app.post("/publish/{channel}")
async def send_to_channel(channel: str, message: str):
    await publish_to_channel(channel, message)
```

* Este endpoint simula un evento externo.
* Llama a Redis `PUBLISH` para notificar a los suscriptores del canal.

---

## 🧠 `redis_pub_sub.py` explicado

### 🧭 Estado global

```python
pubsub_instances = {}
```

* Guarda las tareas que están escuchando en cada canal para **evitar múltiples listeners** sobre el mismo canal.

---

### 📥 Suscripción a canal

```python
await pubsub.subscribe(channel)
```

* Abre una suscripción Redis al canal especificado.
* `pubsub.listen()` espera nuevos mensajes en ese canal.

```python
async def reader():
    async for message in pubsub.listen():
        if message["type"] == "message":
            data = message["data"].decode()
            await callback(data)
```

* Crea una tarea `asyncio.create_task(...)` que permanece escuchando.
* Cuando Redis recibe un nuevo mensaje, llama al `callback` proporcionado por FastAPI.

---

### 📤 Publicar a un canal

```python
await client.publish(channel, message)
```

* Envía un mensaje al canal.
* Todos los `pubsub.listen()` que estén suscritos a ese canal lo recibirán.

---

## 🧪 Ejemplo práctico

1. Abres 2 websockets en tu navegador:

```bash
ws://localhost:8000/ws/chat
ws://localhost:8000/ws/chat
```

2. Lanzas desde otro cliente (curl o Postman):

```bash
curl -X POST "http://localhost:8000/publish/chat" \
     -H "Content-Type: application/json" \
     -d '"¡Hola mundo!"'
```

3. Resultado:
   Los dos clientes WebSocket reciben:

```
[chat] ¡Hola mundo!
```

---

## 🧠 Ventajas de este diseño

| Característica             | Ventaja                                             |
| -------------------------- | --------------------------------------------------- |
| Redis Pub/Sub              | Escalable, desacopla publicación y suscripción      |
| FastAPI + WebSocket        | Comunicación en tiempo real                         |
| Suscripción dinámica       | Cada canal se activa solo si hay interés            |
| Evita listeners duplicados | Solo un listener Redis por canal                    |
| Forwarding por canal       | Controlado y modular, puedes filtrar, loguear, etc. |

---
