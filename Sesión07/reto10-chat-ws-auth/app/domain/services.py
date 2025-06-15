
from .models import Message, User
from .ports import ConnectionManagerPort

class ChatService:
    def __init__(self, connection_manager: ConnectionManagerPort):
        self.connection_manager = connection_manager

    async def handle_message(self, user: User, text: str):
        if user.role != "admin":
            return  # No permisos para enviar
        msg = Message(sender=user.username, content=text)
        await self.connection_manager.broadcast(msg)
