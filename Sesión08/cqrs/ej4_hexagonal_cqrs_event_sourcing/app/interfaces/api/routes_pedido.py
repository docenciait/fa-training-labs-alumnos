from fastapi import APIRouter, HTTPException
from app.application.commands.crear_pedido import CrearPedidoCommandHandler
from app.application.queries.obtener_pedido import ObtenerPedidoQueryHandler
from app.application.dtos.pedido_dto import CrearPedidoDTO, PedidoResponseDTO
from app.application.commands.models.crear_pedido_command import CrearPedidoCommand
from app.infrastructure.repositories.pedido_sqlalchemy import PedidoSQLAlchemyRepository
from app.application.event_store.adapters.sqlite_event_store import SQLiteEventStore

router = APIRouter()
repo = PedidoSQLAlchemyRepository()
event_store = SQLiteEventStore()

@router.post("/", response_model=PedidoResponseDTO)
def crear_pedido(data: CrearPedidoDTO):
    command = CrearPedidoCommand(**data.dict())
    handler = CrearPedidoCommandHandler(repo, event_store)
    pedido = handler.handle(command)
    return PedidoResponseDTO(**pedido.__dict__)

@router.get("/{pedido_id}", response_model=PedidoResponseDTO)
def obtener_pedido(pedido_id: int):
    handler = ObtenerPedidoQueryHandler(repo)
    pedido = handler.handle(pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return PedidoResponseDTO(**pedido.__dict__)

# uvicorn app.interfaces.main:app --reload
