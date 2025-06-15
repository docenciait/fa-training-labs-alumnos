
from typing import Dict
from fastapi import WebSocket
from app.domain.models import User, Message
from app.domain.ports import ConnectionManagerPort

class InMemoryConnectionManager(ConnectionManagerPort):
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    def connect(self, user: User, websocket: WebSocket):
        self.active_connections[user.username] = websocket

    def disconnect(self, user: User):
        self.active_connections.pop(user.username, None)

    async def broadcast(self, message: Message):
        for ws in self.active_connections.values():
            await ws.send_text(f"[{message.sender}] {message.content}")
