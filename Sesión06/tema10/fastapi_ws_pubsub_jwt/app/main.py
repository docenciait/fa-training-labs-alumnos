from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query, HTTPException
from fastapi.responses import JSONResponse
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.redis_pubsub import subscribe_to_channel, publish_to_channel
import logging

app = FastAPI()
logging.basicConfig(level=logging.INFO)

SECRET_KEY = "supersecreto123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

connections_by_channel = {}

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None

@app.post("/login")
async def login(username: str):
    token = create_access_token({"sub": username})
    return {"access_token": token, "token_type": "bearer"}

@app.websocket("/ws/{channel}")
async def websocket_endpoint(websocket: WebSocket, channel: str, token: str = Query(...)):
    user = verify_token(token)
    if not user:
        await websocket.close(code=1008)
        return

    await websocket.accept()
    if channel not in connections_by_channel:
        connections_by_channel[channel] = set()

        async def forward_message(msg: str):
            for conn in connections_by_channel[channel]:
                await conn.send_text(f"[{channel}] {msg}")

        await subscribe_to_channel(channel, forward_message)

    connections_by_channel[channel].add(websocket)
    logging.info(f"{user} conectado a canal {channel}")

    try:
        while True:
            _ = await websocket.receive_text()
    except WebSocketDisconnect:
        connections_by_channel[channel].remove(websocket)
        logging.info(f"{user} desconectado de canal {channel}")

@app.post("/publish/{channel}")
async def send_to_channel(channel: str, message: str):
    await publish_to_channel(channel, message)
    return {"status": "published", "channel": channel, "message": message}
