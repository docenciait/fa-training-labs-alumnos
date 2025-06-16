from schemas import PedidoDTO
from repository import PedidoRepository


class GetPedidoHandler:
    def __init__(self, repo: PedidoRepository):
        self.repo = repo

    def execute(self, pedido_id: int) -> PedidoDTO:
        pedido = self.repo.get_by_id(pedido_id)
        if not pedido:
            return None
        return PedidoDTO.from_orm(pedido)
