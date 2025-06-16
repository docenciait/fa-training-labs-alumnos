from app.domain.ports.pedido_repository import PedidoRepositoryPort
from app.schemas import PedidoDTO

class GetPedidoHandler:
    def __init__(self, repo: PedidoRepositoryPort):
        self.repo = repo

    def execute(self, pedido_id: int):
        pedido = self.repo.get_by_id(pedido_id)
        return PedidoDTO.from_orm(pedido)