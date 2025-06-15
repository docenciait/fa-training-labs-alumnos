import pika, json, threading, time
from pika.exceptions import AMQPConnectionError
from app.domain.models import Evento
from app.application.services.event_service import EventService

servicio = EventService()

def callback(ch, method, properties, body):
    data = json.loads(body.decode())
    evento = Evento(**data)
    servicio.procesar_evento(evento)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_listener():
    def run():
        connection = None
        retries = 10
        for i in range(retries):
            try:
                connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
                break
            except AMQPConnectionError:
                print(f"[!] RabbitMQ not ready. Retrying ({i+1}/{retries})...")
                time.sleep(5)
        if not connection:
            raise Exception("Could not connect to RabbitMQ after multiple attempts.")

        channel = connection.channel()
        channel.queue_declare(queue="eventos", durable=True)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue="eventos", on_message_callback=callback)
        print("[*] Listening for messages...")
        channel.start_consuming()

    thread = threading.Thread(target=run)
    thread.start()
