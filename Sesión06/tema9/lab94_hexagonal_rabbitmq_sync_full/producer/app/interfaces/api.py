from fastapi import APIRouter
from app.domain.models import Evento
from app.infrastructure.rabbitmq_sender import RabbitMQSender
from app.application.services.message_service import MessageService

router = APIRouter()

@router.post("/send")
def enviar_evento(evento: Evento):
    servicio = MessageService(RabbitMQSender())
    return servicio.enviar(evento)