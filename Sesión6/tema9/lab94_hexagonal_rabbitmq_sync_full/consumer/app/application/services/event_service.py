from app.domain.models import Evento
from app.application.ports.message_receiver import MessageReceiverPort

class EventService(MessageReceiverPort):
    eventos: list[Evento] = []

    def procesar_evento(self, evento: Evento) -> None:
        self.eventos.append(evento)

    def listar(self) -> list[Evento]:
        return self.eventos