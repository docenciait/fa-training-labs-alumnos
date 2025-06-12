import aio_pika
import asyncio
import json
from app.domain.models import Evento

mensajes: list[Evento] = []

async def consume():
    connection = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq/")
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)
    queue = await channel.declare_queue("mensajes", durable=True)

    async def callback(message: aio_pika.IncomingMessage):
        async with message.process():
            data = json.loads(message.body.decode())
            evento = Evento(**data)
            mensajes.append(evento)

    await queue.consume(callback)

def setup_consumer():
    loop = asyncio.get_event_loop()
    loop.create_task(consume())
