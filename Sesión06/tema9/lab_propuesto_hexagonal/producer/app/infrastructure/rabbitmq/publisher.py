from aio_pika import connect_robust, Message, DeliveryMode
from app.application.ports.message_bus import MessageBusPort
from app.domain.entities import Evento
import os

class RabbitMQPublisher(MessageBusPort):
    def __init__(self, url: str = None):
        self.url = url or os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq/")

    async def publish(self, evento: Evento):
        connection = await connect_robust(self.url)
        async with connection:
            channel = await connection.channel()
            queue = await channel.declare_queue("eventos", durable=True)
            message = Message(
                body=evento.json().encode(),
                delivery_mode=DeliveryMode.PERSISTENT
            )
            await channel.default_exchange.publish(message, routing_key="eventos")