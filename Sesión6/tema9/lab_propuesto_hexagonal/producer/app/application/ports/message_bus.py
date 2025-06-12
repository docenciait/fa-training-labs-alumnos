from abc import ABC, abstractmethod
from app.domain.entities import Evento

class MessageBusPort(ABC):

    @abstractmethod
    async def publish(self, evento: Evento):
        pass