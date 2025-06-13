
# from typing import Protocol
# from .models import User, Message
# from fastapi import WebSocket

# class ConnectionManagerPort(Protocol):
#     def connect(self, user: User, websocket: WebSocket): ...
#     def disconnect(self, user: User): ...
#     async def broadcast(self, message: Message): ...

from abc import ABC, abstractmethod
from .models import User, Message
from fastapi import WebSocket

class ConnectionManagerPort(ABC):
    @abstractmethod
    def connect(self, user: User, websocket: WebSocket):
        pass

    @abstractmethod
    def disconnect(self, user: User):
        pass

    @abstractmethod
    async def broadcast(self, message: Message):
        pass
