from app.domain.entities import Evento
from app.application.ports.message_bus import MessageBusPort

class EventSenderService:
    def __init__(self, publisher: MessageBusPort):
        self.publisher = publisher

    async def enviar_evento(self, evento: Evento):
        await self.publisher.publish(evento)