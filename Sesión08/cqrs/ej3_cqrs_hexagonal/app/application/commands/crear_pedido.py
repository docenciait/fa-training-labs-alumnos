from app.domain.models.pedido import Pedido
from app.domain.ports.pedido_repository import PedidoRepositoryPort
from app.schemas import CrearPedidoCommand

class CrearPedidoHandler:
    def __init__(self, repo: PedidoRepositoryPort):
        self.repo = repo

    def execute(self, command: CrearPedidoCommand):
        pedido = Pedido(command.usuario_id, command.producto, command.cantidad)
        return self.repo.save(pedido)