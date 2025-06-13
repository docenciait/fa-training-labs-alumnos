import pika
import json
from app.domain.models import Evento
from app.application.ports.message_sender import MessageSenderPort

class RabbitMQSender(MessageSenderPort):
    def __init__(self, host="rabbitmq", queue="eventos"):
        self.host = host
        self.queue = queue

    def enviar_evento(self, evento: Evento) -> bool:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
            channel = connection.channel()
            channel.queue_declare(queue=self.queue, durable=True)
            channel.basic_publish(
                exchange="",
                routing_key=self.queue,
                body=json.dumps(evento.dict()),
                properties=pika.BasicProperties(delivery_mode=2)
            )
            connection.close()
            return True
        except Exception as e:
            print("Error enviando evento:", e)
            return False