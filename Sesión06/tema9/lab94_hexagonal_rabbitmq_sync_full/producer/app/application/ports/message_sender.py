from abc import ABC, abstractmethod
from app.domain.models import Evento

class MessageSenderPort(ABC):
    @abstractmethod
    def enviar_evento(self, evento: Evento) -> bool: ...