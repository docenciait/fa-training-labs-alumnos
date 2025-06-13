from fastapi import FastAPI
from models import Evento
import pika
import json
import uuid

app = FastAPI()

@app.post("/send")
def send_message(evento: Evento):
    connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
    channel = connection.channel()

    # Cola de mensajes y cola de respuesta
    channel.queue_declare(queue="mensajes")
    result = channel.queue_declare(queue='', exclusive=True)  # Cola temporal de respuesta
    callback_queue = result.method.queue

    correlation_id = str(uuid.uuid4())

    response = None

    def on_response(ch, method, props, body):
        nonlocal response
        if props.correlation_id == correlation_id:
            response = body.decode()
            print(f"✅ ACK recibido del consumidor: {response}")

    # Consumidor de respuesta
    channel.basic_consume(
        queue=callback_queue,
        on_message_callback=on_response,
        auto_ack=True
    )

    channel.basic_publish(
        exchange="",
        routing_key="mensajes",
        properties=pika.BasicProperties(
            reply_to=callback_queue,
            correlation_id=correlation_id,
        ),
        body=evento.json().encode("utf-8")
    )

    print("📤 Evento enviado, esperando ACK...")

    # Espera activa (bloqueante) hasta recibir respuesta
    while response is None:
        connection.process_data_events(time_limit=1)

    connection.close()
    return {"status": "ACK recibido", "respuesta": response}
