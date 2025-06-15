Perfecto. Ahora en el punto **10.2 + inicio del 10.3**, vamos a construir un **ejemplo realista con dos aplicaciones FastAPI** que se comunican entre sí **usando WebSockets**, simulando un escenario como “microservicio A notifica a B en tiempo real”.

---

## 🎯 Objetivo del Ejercicio 10.2

> Crear dos apps FastAPI (`notifier` y `receiver`) que simulan servicios distintos. El primero se conecta al segundo mediante WebSocket para enviar mensajes en tiempo real.

---

## 🧱 Estructura del proyecto

```bash
fastapi_ws_2apps/
├── docker-compose.yml
├── notifier/
│   ├── app/
│   │   └── main.py
│   └── requirements.txt
├── receiver/
│   ├── app/
│   │   └── main.py
│   └── requirements.txt
```

---

## ⚙️ `docker-compose.yml`

```yaml
version: "3.9"
services:
  receiver:
    build:
      context: ./receiver
    ports:
      - "8001:8000"

  notifier:
    build:
      context: ./notifier
    depends_on:
      - receiver
    ports:
      - "8002:8000"
```

---

## 📦 `notifier/requirements.txt` y `receiver/requirements.txt`

Ambos usan:

```txt
fastapi>=2.0.0
uvicorn[standard]
```

---

## 📡 receiver/app/main.py (WebSocket server)

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()
active_connections = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"📥 Recibido: {data}")
    except WebSocketDisconnect:
        print("🔌 Cliente desconectado")
        active_connections.remove(websocket)
```

---

## 📤 notifier/app/main.py (cliente WebSocket + API REST)

```python
import asyncio
import websockets
from fastapi import FastAPI

app = FastAPI()

@app.get("/send/{msg}")
async def send_message(msg: str):
    uri = "ws://receiver:8000/ws"
    try:
        async with websockets.connect(uri) as websocket:
            await websocket.send(msg)
            return {"status": "sent", "msg": msg}
    except Exception as e:
        return {"error": str(e)}
```

---

## 🐳 Archivos `Dockerfile` en ambos servicios (idénticos)

```Dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## ▶️ Ejecución

```bash
docker-compose up --build
```

---

## 🔁 Prueba real

En otro terminal:

```bash
 curl http://localhost:8002/send/hola_desde_notifier
```

En la terminal del servicio **receiver** verás algo como:

```
📥 Recibido: hola_desde_notifier
```

---

## ✅ Qué se ha cubierto

| Punto | Descripción                                                  |
| ----- | ------------------------------------------------------------ |
| 10.2  | Comunicación entre servidores FastAPI usando WebSocket       |
| 10.3  | Inicio de gestión de múltiples clientes con una lista básica |

---
