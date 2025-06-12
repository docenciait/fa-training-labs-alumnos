from fastapi import APIRouter
from app.application.service import send_event
from app.domain.models import Evento

router = APIRouter()

@router.post("/send")
async def send(evento: Evento):
    await send_event(evento)
    return {"status": "ok", "evento": evento}
