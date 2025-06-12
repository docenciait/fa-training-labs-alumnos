from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Path
from .redis_pub_sub import subscribe_to_channel, publish_to_channel
import logging

app = FastAPI()
logging.basicConfig(level=logging.INFO)

connections_by_channel = {}

@app.websocket("/ws/{channel}")
async def websocket_endpoint(websocket: WebSocket, channel: str):
    await websocket.accept()
    if channel not in connections_by_channel:
        connections_by_channel[channel] = set()

        async def forward_message(msg: str):
            for conn in connections_by_channel[channel]:
                await conn.send_text(f"[{channel}] {msg}")

        await subscribe_to_channel(channel, forward_message)

    connections_by_channel[channel].add(websocket)

    try:
        while True:
            _ = await websocket.receive_text()
    except WebSocketDisconnect:
        connections_by_channel[channel].remove(websocket)


@app.post("/publish/{channel}")
async def send_to_channel(channel: str, message: str):
    await publish_to_channel(channel, message)
    return {"status": "published", "channel": channel, "message": message}
