from fastapi import FastAPI
from models import Evento
import aio_pika
import asyncio
import json

app = FastAPI()
mensajes: list[Evento] = []

RABBITMQ_URI = "amqp://guest:guest@rabbitmq/"

async def retry_connect(uri: str, retries=10, delay=3):
    for i in range(retries):
        try:
            print(f"[{i+1}] ⏳ Intentando conectar a RabbitMQ...")
            connection = await aio_pika.connect_robust(uri)
            print("✅ Conectado a RabbitMQ.")
            return connection
        except Exception as e:
            print(f"❌ Fallo en intento {i+1}: {e}")
            await asyncio.sleep(delay)
    raise RuntimeError("🛑 No se pudo conectar a RabbitMQ.")

async def consume():
    connection = await retry_connect(RABBITMQ_URI)
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)

    queue = await channel.declare_queue("mensajes", durable=True)

    async def callback(message: aio_pika.IncomingMessage):
        async with message.process():
            try:
                await asyncio.sleep(10)  # Simula procesamiento lento
                data = json.loads(message.body.decode())
                evento = Evento(**data)
                print(f"📥 Recibido evento: {evento.tipo} con ID {evento.id}")
                mensajes.append(evento)
            except Exception as err:
                print(f"⚠️ Error procesando mensaje: {err}")

    print("🟢 Esperando mensajes...")
    await queue.consume(callback)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(consume())

@app.get("/messages")
async def get_messages():
    return [m.dict() for m in mensajes]
