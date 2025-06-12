from fastapi import FastAPI
from app.infrastructure.rabbit.consumer import consume, mensajes

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(consume())

@app.get("/messages")
async def get_messages():
    return [m.dict() for m in mensajes]
