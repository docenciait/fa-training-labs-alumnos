# producer/main.py
from fastapi import FastAPI
from models import Evento
import pika
import json

app = FastAPI()

@app.post("/send")
def send_message(evento: Evento):
    """
    url = "amqp://guest:guest@rabbitmq:5672/"
    params = pika.URLParameters(url)
    """
    
    connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
    channel = connection.channel()
    channel.queue_declare(queue="mensajes")
    channel.basic_publish(
        exchange="",
        routing_key="mensajes",
        body=evento.json().encode("utf-8")
    )
    connection.close()
    return {"status": "message sent", "evento": evento}
