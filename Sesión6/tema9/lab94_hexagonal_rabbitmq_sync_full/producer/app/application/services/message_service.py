from app.domain.models import Evento
from app.application.ports.message_sender import MessageSenderPort

class MessageService:
    def __init__(self, sender: MessageSenderPort):
        self.sender = sender

    def enviar(self, evento: Evento) -> dict:
        success = self.sender.enviar_evento(evento)
        return {"status": "enviado" if success else "falló publicación", "evento": evento.dict()}