from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Path
from connection_manager import ConnectionManager
import logging

logging.basicConfig(level=logging.INFO)
app = FastAPI()
manager = ConnectionManager()

@app.websocket("/ws/global_feed")
async def websocket_global_feed(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast_to_all(f"📣 {manager._client_id(websocket)}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.websocket("/ws/chat/{room_id}/{client_name}")
async def websocket_chat_room(websocket: WebSocket, room_id: str = Path(...), client_name: str = Path(...)):
    await manager.connect(websocket)
    await manager.join_room(room_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_to_room(room_id, f"[{room_id}] {client_name}: {data}", exclude_sender=websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)


""" 
Los clientes acceden a /ws/chat/salaX/Alice o /ws/chat/salaX/Bob

Se unen a la misma sala salaX

Envían mensajes que sólo verán los que están en esa sala
"""