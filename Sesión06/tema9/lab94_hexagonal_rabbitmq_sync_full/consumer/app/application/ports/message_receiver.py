from abc import ABC, abstractmethod
from app.domain.models import Evento

class MessageReceiverPort(ABC):
    @abstractmethod
    def procesar_evento(self, evento: Evento) -> None: ...