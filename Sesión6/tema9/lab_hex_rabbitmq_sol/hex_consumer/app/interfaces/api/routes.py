from fastapi import APIRouter
from app.infrastructure.rabbit.consumer import mensajes

router = APIRouter()

@router.get("/messages")
async def get_messages():
    return [m.dict() for m in mensajes]
