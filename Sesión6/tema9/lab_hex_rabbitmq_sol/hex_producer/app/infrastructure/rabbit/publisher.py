import aio_pika
from app.domain.models import Evento
import json

async def publish_event(evento: Evento):
    connection = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq/")
    async with connection:
        channel = await connection.channel()
        await channel.declare_queue("mensajes", durable=True)
        await channel.default_exchange.publish(
            aio_pika.Message(
                body=evento.json().encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT
            ),
            routing_key="mensajes"
        )
