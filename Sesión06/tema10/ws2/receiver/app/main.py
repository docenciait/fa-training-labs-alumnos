from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()
active_connections = []

@app.websocket("/notificaciones/ws")
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
