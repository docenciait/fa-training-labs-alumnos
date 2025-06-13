from fastapi import FastAPI
from models import Evento
import pika
import threading
import json
import logging
import time

logging.basicConfig(level=logging.INFO)
app = FastAPI()
mensajes = []

def connect_rabbitmq(retries=10, delay=3):
    for attempt in range(retries):
        try:
            logging.info(f"[{attempt+1}] ⏳ Intentando conectar a RabbitMQ...")
            connection = pika.BlockingConnection(
                pika.ConnectionParameters("rabbitmq")
            )
            logging.info("✅ Conectado a RabbitMQ.")
            return connection
        except pika.exceptions.AMQPConnectionError as e:
            logging.warning(f"❌ Falló intento {attempt+1}: {e}")
            time.sleep(delay)
    raise RuntimeError("🛑 No se pudo conectar a RabbitMQ.")

def callback(ch, method, properties, body):
    try:
        evento = Evento.parse_raw(body)
        logging.info(f"📥 Recibido evento: {evento.tipo} con ID {evento.id}")
        mensajes.append(evento)

        # Aquí simularíamos procesamiento si hiciera falta
        time.sleep(1)
        logging.info("✅ Procesamiento completado. Enviando ACK.")

        # Enviamos ACK manual
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        logging.error(f"❌ Error procesando mensaje: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

def consume():
    try:
        connection = connect_rabbitmq()
        channel = connection.channel()
        channel.queue_declare(queue="mensajes", durable=True)

        # Solo uno a la vez (básico para fiabilidad)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue="mensajes", on_message_callback=callback)

        logging.info("🟢 Esperando mensajes...")
        channel.start_consuming()
    except Exception as e:
        logging.critical(f"💥 Error fatal en consume(): {e}")

@app.on_event("startup")
def startup_event():
    threading.Thread(target=consume, daemon=True).start()

@app.get("/messages")
def get_all():
    return [e.dict() for e in mensajes]
