from fastapi import APIRouter, HTTPException
from app.application.commands.crear_pedido import CrearPedidoCommandHandler
from app.application.queries.obtener_pedido import ObtenerPedidoQueryHandler
from app.application.dtos.pedido_dto import CrearPedidoDTO, PedidoResponseDTO
from app.infrastructure.repositories.pedido_sqlalchemy import PedidoSQLAlchemyRepository

router = APIRouter()
repo = PedidoSQLAlchemyRepository()

@router.post("/", response_model=PedidoResponseDTO)
def crear_pedido(data: CrearPedidoDTO):
    handler = CrearPedidoCommandHandler(repo)
    pedido = handler.handle(data)
    return PedidoResponseDTO(**pedido.__dict__)

@router.get("/{pedido_id}", response_model=PedidoResponseDTO)
def obtener_pedido(pedido_id: int):
    handler = ObtenerPedidoQueryHandler(repo)
    pedido = handler.handle(pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return PedidoResponseDTO(**pedido.__dict__)
