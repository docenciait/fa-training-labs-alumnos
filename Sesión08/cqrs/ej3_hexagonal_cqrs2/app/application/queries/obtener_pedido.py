from app.domain.entities.pedido import Pedido
from app.application.ports.pedido_repository import PedidoRepositoryPort

class ObtenerPedidoQueryHandler:
    def __init__(self, repo: PedidoRepositoryPort):
        self.repo = repo

    def handle(self, pedido_id: int) -> Pedido | None:
        return self.repo.get_by_id(pedido_id)
