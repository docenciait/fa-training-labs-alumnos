from fastapi import FastAPI
from pydantic import BaseModel
import pika
import json

class Evento(BaseModel):
    tipo: str
    id: str
    payload: dict

app = FastAPI()

@app.post("/send")
def send_message(evento: Evento):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
        channel = connection.channel()

        # Cola debe existir, debe coincidir exactamente
        channel.queue_declare(queue="mensajes", durable=True)

        channel.confirm_delivery()

        success = channel.basic_publish(
            exchange="",  # default
            routing_key="mensajes",  # debe coincidir exactamente con el nombre de la cola
            body=evento.json().encode(),
            properties=pika.BasicProperties(delivery_mode=2)  # persistente
        )

        connection.close()

        return {
            "status": "enviado y confirmado" if success else "falló publicación",
            "evento": evento
        }

    except Exception as e:
        return {
            "status": f"falló publicación ({type(e).__name__}: {e})",
            "evento": evento
        }
   