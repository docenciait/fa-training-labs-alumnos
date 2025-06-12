import asyncio
import websockets
from fastapi import FastAPI

app = FastAPI()

@app.get("/send/{msg}")
async def send_message(msg: str):
    uri = "ws://receiver:8000/notificaciones/ws"
    try:
        async with websockets.connect(uri) as websocket:
            await websocket.send(msg)
            return {"status": "sent", "msg": msg}
    except Exception as e:
        return {"error": str(e)}
