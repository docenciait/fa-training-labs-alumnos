from app.domain.models import Evento
from app.infrastructure.rabbit.publisher import publish_event

async def send_event(evento: Evento):
    await publish_event(evento)
