from fastapi import FastAPI
from app.db import Base, engine
from app.infrastructure.repositories.models import PedidoSQL
from app.interfaces.http.pedido_controller import router as pedido_router

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(pedido_router)