from fastapi import APIRouter
from app.application.services.message_store import MessageStore

router = APIRouter()

@router.get("/messages")
def get_messages():
    return MessageStore.list()