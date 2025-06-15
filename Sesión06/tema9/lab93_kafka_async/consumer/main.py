# consumer/main.py
from fastapi import FastAPI
from aiokafka import AIOKafkaConsumer
from models import Evento
import json
import asyncio

app = FastAPI()
mensajes: list[Evento] = []

KAFKA_BOOTSTRAP = "kafka:9092"
TOPIC = "eventos"

async def consume():
    consumer = AIOKafkaConsumer(
        TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP,
        group_id="grupo-consumidor-2",
        auto_offset_reset="earliest"
    )
    await consumer.start()
    try:
        async for msg in consumer:
            print(f"Msg: {msg }")
            data = json.loads(msg.value.decode())
            evento = Evento(**data)
            print(f"📥 Recibido evento: {evento.tipo} con ID {evento.id}")
            mensajes.append(data)
    finally:
        await consumer.stop()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(consume())

@app.get("/messages")
async def get_messages():
    print(f"Mensaje recibido: {mensajes}")
    return mensajes
