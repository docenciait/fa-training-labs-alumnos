from schemas import PedidoDTO
from repository import PedidoRepository

class GetPedidoHandler:
    def __init__(self, repo: PedidoRepository):
        self.repo = repo

    def execute(self, pedido_id: int) -> PedidoDTO:
        pedido = self.repo.get_by_id(pedido_id)
        if not pedido:
            return None
        return PedidoDTO.model_validate(pedido)

class ListarPedidosPorUsuarioHandler:
    def __init__(self, repo: PedidoRepository):
        self.repo = repo

    def execute(self, usuario_id: int):
        pedidos = self.repo.get_all_by_usuario(usuario_id)
        return [PedidoDTO.model_validate(p) for p in pedidos]

class ContarPedidosPendientesHandler:
    def __init__(self, repo: PedidoRepository):
        self.repo = repo

    def execute(self):
        return self.repo.count_by_estado("pendiente")