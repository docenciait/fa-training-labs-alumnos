from fastapi import APIRouter, Depends, HTTPException
from app.application.commands.crear_pedido import CrearPedidoHandler
from app.application.queries.get_pedido import GetPedidoHandler
from app.infrastructure.repositories.pedido_sqlalchemy import PedidoRepositorySQLAlchemy
from app.schemas import CrearPedidoCommand, PedidoDTO
from app.db import get_db

router = APIRouter()

@router.post("/pedidos", response_model=PedidoDTO)
def crear_pedido(cmd: CrearPedidoCommand, db=Depends(get_db)):
    handler = CrearPedidoHandler(PedidoRepositorySQLAlchemy(db))
    return handler.execute(cmd)

@router.get("/pedidos/{pedido_id}", response_model=PedidoDTO)
def obtener_pedido(pedido_id: int, db=Depends(get_db)):
    handler = GetPedidoHandler(PedidoRepositorySQLAlchemy(db))
    dto = handler.execute(pedido_id)
    if not dto:
        raise HTTPException(404, "Pedido no encontrado")
    return dto