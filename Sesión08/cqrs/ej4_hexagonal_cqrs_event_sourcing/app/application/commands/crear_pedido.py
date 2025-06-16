import logging
from app.domain.entities.pedido import Pedido
from app.application.commands.models.crear_pedido_command import CrearPedidoCommand
from app.application.ports.pedido_repository import PedidoRepositoryPort
from app.domain.events.pedido_creado import PedidoCreado
from app.application.event_store.ports.event_store_port import EventStorePort

logger = logging.getLogger(__name__)

class CrearPedidoCommandHandler:
    def __init__(self, repo: PedidoRepositoryPort, event_store: EventStorePort):
        self.repo = repo
        self.event_store = event_store

    def handle(self, command: CrearPedidoCommand) -> Pedido:
        total = command.cantidad * 10.0
        pedido = Pedido(
            id=None,
            usuario_id=command.usuario_id,
            producto=command.producto,
            cantidad=command.cantidad,
            total=total,
            estado="pendiente"
        )
        saved = self.repo.save(pedido)

        evento = PedidoCreado(
            id=saved.id,
            usuario_id=saved.usuario_id,
            producto=saved.producto,
            cantidad=saved.cantidad,
            total=saved.total,
            estado=saved.estado,
        )
        self.event_store.save_event(str(saved.id), "PedidoCreado", evento.__dict__)
        logger.info(f"Evento emitido: {evento}")
        return saved
