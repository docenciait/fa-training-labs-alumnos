import asyncio
import json
from aio_pika import connect_robust, IncomingMessage
from app.domain.entities import Evento
from app.application.services.message_store import MessageStore

async def consume():
    connection = await connect_robust("amqp://guest:guest@rabbitmq/")
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)
    queue = await channel.declare_queue("eventos", durable=True)

    async def callback(message: IncomingMessage):
        async with message.process():
            data = json.loads(message.body.decode())
            evento = Evento(**data)
            print(f"📥 Recibido evento: {evento.tipo} con ID {evento.id}")
            MessageStore.store(evento)

    await queue.consume(callback)