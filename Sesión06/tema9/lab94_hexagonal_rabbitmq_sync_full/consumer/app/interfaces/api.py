from fastapi import APIRouter
from app.application.services.event_service import EventService

router = APIRouter()
servicio = EventService()

@router.get("/messages")
def listar_eventos():
    return [e.dict() for e in servicio.listar()]