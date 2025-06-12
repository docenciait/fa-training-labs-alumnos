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
            except Exception as err:
                print(f"⚠️ Error procesando mensaje: {err} | body: {body}")

        channel.basic_consume(queue="mensajes", on_message_callback=callback, auto_ack=True)
        print("🟢 Esperando mensajes...")
        channel.start_consuming()
    except Exception as e:
        print(f"💥 Error fatal en consume(): {e}")

# Inicia el consumidor en hilo
threading.Thread(target=consume, daemon=True).start()

@app.get("/messages")
def get_messages():
    return [e.dict() for e in mensajes]
