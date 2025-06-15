from fastapi import FastAPI
from app.interfaces.api import router
from app.infrastructure.rabbitmq_listener import start_listener

app = FastAPI(title="Consumidor")
app.include_router(router)

@app.on_event("startup")
def iniciar():
    start_listener()