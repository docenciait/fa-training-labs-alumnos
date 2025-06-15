from fastapi import APIRouter, Depends
from app.domain.entities import Evento
from app.infrastructure.rabbitmq.publisher import RabbitMQPublisher
from app.application.services.event_sender import EventSenderService

router = APIRouter()

@router.post("/send")
async def send(evento: Evento):
    service = EventSenderService(RabbitMQPublisher())
    await service.enviar_evento(evento)
    return {"status": "enviado", "evento": evento}