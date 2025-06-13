from fastapi import FastAPI
from models import Evento
import pika
import threading
import json
import time

app = FastAPI()
mensajes = []

def connect_rabbitmq(retries=10, delay=3):
    for attempt in range(retries):
        try:
            print(f"[{attempt+1}] ⏳ Intentando conectar a RabbitMQ...")
            connection = pika.BlockingConnection(
                pika.ConnectionParameters("rabbitmq", 5672)
            )
            print("✅ Conectado a RabbitMQ.")
            return connection
        except pika.exceptions.AMQPConnectionError as e:
            print(f"❌ Falló intento {attempt+1}: {e}")
            time.sleep(delay)
    raise RuntimeError("🛑 No se pudo conectar a RabbitMQ.")

def consume():
    try:
        connection = connect_rabbitmq()
        channel = connection.channel()
        channel.queue_declare(queue="mensajes")

        def callback(ch, method, properties, body):
            try:
                raw = body.decode()
                evento = Evento.parse_raw(raw)
                print(f"📥 Recibido evento: {evento.tipo} con ID {evento.id}")
                mensajes.append(evento)

                # Respuesta al productor usando reply_to
                if properties.reply_to:
                    ack_msg = f"Evento {evento.id} recibido y procesado."
                    ch.basic_publish(
                        exchange='',
                        routing_key=properties.reply_to,
                        properties=pika.BasicProperties(
                            correlation_id=properties.correlation_id
                        ),
                        body=ack_msg.encode()
                    )
                    print(f"📤 ACK enviado al productor: {ack_msg}")

                ch.basic_ack(delivery_tag=method.delivery_tag)

            except Exception as err:
                print(f"⚠️ Error procesando mensaje: {err} | body: {body}")

        channel.basic_consume(queue="mensajes", on_message_callback=callback)
        print("🟢 Esperando mensajes...")
        channel.start_consuming()
    except Exception as e:
        print(f"💥 Error fatal en consume(): {e}")

# Hilo del consumidor
threading.Thread(target=consume, daemon=True).start()

@app.get("/messages")
def get_messages():
    return [e.dict() for e in mensajes]
