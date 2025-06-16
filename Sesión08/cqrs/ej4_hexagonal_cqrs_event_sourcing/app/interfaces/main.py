import logging
logging.basicConfig(level=logging.INFO)
from fastapi import FastAPI
from app.interfaces.api.routes_pedido import router as pedido_router

app = FastAPI(title="Hexagonal CQRS FastAPI")

app.include_router(pedido_router, prefix="/pedidos", tags=["Pedidos"])

from app.infrastructure.db.models import init_db
init_db()
