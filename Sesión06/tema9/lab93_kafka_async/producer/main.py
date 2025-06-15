from fastapi import FastAPI
from models import Evento
from aiokafka import AIOKafkaProducer
import asyncio
import json
import logging

app = FastAPI()
producer: AIOKafkaProducer = None
BOOTSTRAP_SERVERS = "kafka:9092"
TOPIC = "eventos"

async def get_kafka_producer():
    global producer
    retries = 10
    for i in range(retries):
        try:
            producer = AIOKafkaProducer(
                bootstrap_servers=BOOTSTRAP_SERVERS
            )
            await producer.start()
            print("✅ Productor Kafka iniciado correctamente.")
            return
        except Exception as e:
            print(f"❌ Reintentando conexión a Kafka ({i+1}/{retries}): {e}")
            await asyncio.sleep(3)
    raise RuntimeError("🛑 No se pudo conectar a Kafka.")

@app.on_event("startup")
async def startup_event():
    await get_kafka_producer()

@app.on_event("shutdown")
async def shutdown_event():
    if producer:
        await producer.stop()

@app.post("/send")
async def send_message(evento: Evento):
    value = json.dumps(evento.dict()).encode("utf-8")
    await producer.send_and_wait(TOPIC, value=value)
    return {"status": "message sent", "evento": evento}
