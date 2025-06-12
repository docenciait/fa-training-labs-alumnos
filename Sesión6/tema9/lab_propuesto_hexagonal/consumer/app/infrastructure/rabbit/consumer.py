import aio_pika
import asyncio
import json
from app.domain.entities import Evento
from aio_pika.abc import AbstractIncomingMessage

mensajes: list[Evento] = []

async def connect_with_retry(uri: str, retries: int = 10, delay: int = 3):
    for attempt in range(1, retries + 1):
        try:
            print(f"[{attempt}] ⏳ Intentando conectar a RabbitMQ...")
            connection = await aio_pika.connect_robust(uri)
            print("✅ Conectado a RabbitMQ.")
            return connection
        except Exception as e:
            print(f"❌ Reintento {attempt} fallido: {e}")
            await asyncio.sleep(delay)
    raise RuntimeError("🛑 No se pudo conectar a RabbitMQ después de varios intentos.")

async def consume():
    connection = await connect_with_retry("amqp://guest:guest@rabbitmq/")
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)
    queue = await channel.declare_queue("mensajes", durable=True)

    async def callback(message: AbstractIncomingMessage):
        async with message.process():
            try:
                data = json.loads(message.body.decode())
                evento = Evento(**data)
                print(f"📥 Evento recibido: {evento.tipo} con ID {evento.id}")
                mensajes.append(evento)
            except Exception as e:
                print(f"⚠️ Error procesando mensaje: {e}")
    
    print("🟢 Esperando mensajes...")
    await queue.consume(callback)
