# 🔐 FastAPI WebSocket + Redis Pub/Sub + JWT

Este proyecto muestra cómo proteger canales WebSocket en FastAPI usando JWT y Redis Pub/Sub.

## 🚀 Iniciar

```bash
docker-compose up --build
```

## 🔑 Obtener un token

```bash
curl -X POST "http://localhost:8000/login?username=alice"
```

## 📡 Conectar vía WebSocket

```bash
websocat "ws://localhost:8000/ws/noticias?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

## 📤 Publicar un mensaje

```bash
curl -X POST "http://localhost:8000/publish/noticias?message=Hola+canal"
```

## ✅ Características

- Autenticación JWT obligatoria en WebSocket
- Redis Pub/Sub para múltiples clientes y canales
- WebSocket rechazado si el token no es válido


# Explicación

Perfecto. A continuación tienes la **explicación completa del proyecto WebSocket + Redis Pub/Sub + JWT con FastAPI**, línea por línea, para cubrir el **punto 10.9: Seguridad de canales WebSocket con autenticación**.

---

## 📁 Estructura de archivos

```
fastapi_ws_pubsub_jwt/
├── app/
│   ├── main.py               # Lógica FastAPI + WebSocket + JWT
│   └── redis_pubsub.py       # Subscripción y publicación en Redis
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
```

---

## 🔑 JWT: Seguridad de canales WebSocket

---

## 📜 `main.py` explicado

### 🔁 Imports y configuración

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.redis_pubsub import subscribe_to_channel, publish_to_channel
```

* Se importa `jose.jwt` para firmar/verificar tokens.
* Se importa el sistema Pub/Sub desde `redis_pubsub.py`.

---

### 🔧 Configuración de JWT

```python
SECRET_KEY = "supersecreto123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

> Clave secreta y algoritmo de firma. En producción, esto debería ser una variable de entorno segura.

---

### 🔐 Creación de tokens

```python
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```

> Codifica el contenido del token con fecha de expiración.

---

### 🔐 Verificación de tokens

```python
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None
```

> Verifica que el token sea válido y extrae el `sub` (nombre del usuario). Si no es válido, devuelve `None`.

---

### 🧪 Endpoint `/login`

```python
@app.post("/login")
async def login(username: str):
    token = create_access_token({"sub": username})
    return {"access_token": token, "token_type": "bearer"}
```

> Para pruebas: devuelve un token JWT para el usuario indicado. No hay password ni base de datos, es solo para demo.

---

### 📡 WebSocket protegido con JWT

```python
@app.websocket("/ws/{channel}")
async def websocket_endpoint(websocket: WebSocket, channel: str, token: str = Query(...)):
```

> Este WebSocket exige que el **token JWT se pase como query param** en la URL.

Ejemplo:

```
ws://localhost:8000/ws/noticias?token=eyJhbGci...
```

---

### 🔐 Validar token al conectar

```python
    user = verify_token(token)
    if not user:
        await websocket.close(code=1008)
        return
```

* Si el token es inválido o falta, se cierra inmediatamente con código 1008 ("Policy violation").

---

### ✅ Aceptar conexión válida

```python
    await websocket.accept()
```

---

### 🧠 Registrar y suscribir a canal

```python
    if channel not in connections_by_channel:
        connections_by_channel[channel] = set()

        async def forward_message(msg: str):
            for conn in connections_by_channel[channel]:
                await conn.send_text(f"[{channel}] {msg}")

        await subscribe_to_channel(channel, forward_message)
```

* Registra el WebSocket dentro del canal.
* Si es la primera conexión al canal, se suscribe a Redis con una función `forward_message()` que hace broadcast al grupo.

---

### 🔁 Mantener conexión WebSocket viva

```python
    connections_by_channel[channel].add(websocket)
    logging.info(f"{user} conectado a canal {channel}")
```

```python
    try:
        while True:
            _ = await websocket.receive_text()
```

* Espera indefinidamente a mensajes del cliente (aunque los ignoremos).
* Necesario para mantener la conexión viva.

---

### 🔌 Al desconectar

```python
    except WebSocketDisconnect:
        connections_by_channel[channel].remove(websocket)
        logging.info(f"{user} desconectado de canal {channel}")
```

---

### 📤 Publicar mensajes

```python
@app.post("/publish/{channel}")
async def send_to_channel(channel: str, message: str):
    await publish_to_channel(channel, message)
    return {"status": "published", "channel": channel, "message": message}
```

> Cualquier usuario (sin necesidad de autenticarse) puede enviar mensajes a un canal.
> Esto podría mejorarse en el futuro con autorización basada en rol o scope.

---

## 📦 `redis_pubsub.py` explicado

```python
import redis.asyncio as redis
import asyncio

REDIS_URL = "redis://redis:6379"
pubsub_instances = {}
```

> Configura la conexión con Redis y guarda las tareas activas por canal para evitar duplicados.

---

### 🔔 Subscribirse a un canal

```python
async def subscribe_to_channel(channel: str, callback):
    if channel in pubsub_instances:
        return
```

* Evita duplicar listeners para el mismo canal.

```python
    client = redis.from_url(REDIS_URL)
    pubsub = client.pubsub()
    await pubsub.subscribe(channel)
```

* Se conecta a Redis y se suscribe al canal.

---

### 🔁 Listener asíncrono

```python
    async def reader():
        async for message in pubsub.listen():
            if message["type"] == "message":
                data = message["data"].decode()
                await callback(data)
```

> Este bucle escucha Redis y reenvía los mensajes entrantes al `callback()` que fue registrado.

---

```python
    task = asyncio.create_task(reader())
    pubsub_instances[channel] = task
```

> Se ejecuta el listener como una tarea de fondo con `asyncio.create_task`.

---

### 📤 Publicar

```python
async def publish_to_channel(channel: str, message: str):
    client = redis.from_url(REDIS_URL)
    await client.publish(channel, message)
```

> Se publica un mensaje a Redis, que se distribuye a los subscritos.

---

## ✅ Resultado: Seguridad WebSocket con JWT

| Funcionalidad                        | Estado |
| ------------------------------------ | ------ |
| Autenticación por token en WebSocket | ✅      |
| Redis Pub/Sub                        | ✅      |
| WebSocket cerrado si el token falla  | ✅      |
| Permite canales dinámicos            | ✅      |

---

