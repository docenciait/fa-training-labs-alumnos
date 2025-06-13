
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from jose import jwt, JWTError
from app.domain.models import User
from app.domain.services import ChatService
from app.infrastructure.connection_repo import InMemoryConnectionManager

SECRET_KEY = "secret"
ALGORITHM = "HS256"

router = APIRouter()
conn_mgr = InMemoryConnectionManager()
chat_service = ChatService(conn_mgr)

async def get_current_user_ws(websocket: WebSocket) -> User | None:
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=1008)
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return User(username=payload["sub"], role=payload["role"])
    except JWTError:
        await websocket.close(code=1008)
        return None

@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    user = await get_current_user_ws(websocket)
    if not user:
        return
    conn_mgr.connect(user, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await chat_service.handle_message(user, data)
    except WebSocketDisconnect:
        conn_mgr.disconnect(user)
