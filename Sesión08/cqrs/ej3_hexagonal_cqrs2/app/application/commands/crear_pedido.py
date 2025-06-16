from app.domain.entities.pedido import Pedido
from app.application.dtos.pedido_dto import CrearPedidoDTO
from app.application.ports.pedido_repository import PedidoRepositoryPort

class CrearPedidoCommandHandler:
    def __init__(self, repo: PedidoRepositoryPort):
        self.repo = repo

    def handle(self, data: CrearPedidoDTO) -> Pedido:
        total = data.cantidad * 10.0  # Lógica de dominio simplificada
        pedido = Pedido(
            id=None,
            usuario_id=data.usuario_id,
            producto=data.producto,
            cantidad=data.cantidad,
            total=total,
            estado="pendiente"
        )
        return self.repo.save(pedido)
