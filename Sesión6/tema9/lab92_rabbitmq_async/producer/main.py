from fastapi import FastAPI
from models import Evento
import aio_pika
import json

app = FastAPI()

@app.post("/send")
async def send_message(evento: Evento):
    # Conexión robusta al broker RabbitMQ
    connection = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq/")
    async with connection:
        # Abre canal
        channel = await connection.channel()
        # Declara cola durable (sobrevive reinicios del broker)
        queue = await channel.declare_queue("mensajes", durable=True)
        # Crea y publica el mensaje (marcado como persistente)
        message = aio_pika.Message(
            body=evento.json().encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT  # 💾 Persistencia
        )
        await channel.default_exchange.publish(message, routing_key="mensajes")
    return {"status": "message sent", "evento": evento}
