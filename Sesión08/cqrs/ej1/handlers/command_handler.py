from models import Pedido
from schemas import CreatePedidoCommand
from repository import PedidoRepository


class CrearPedidoHandler:
    def __init__(self, repo: PedidoRepository):
        self.repo = repo

    def execute(self, command: CreatePedidoCommand) -> Pedido:
        total = command.cantidad * 10.0  # lógica de negocio simulada
        pedido = Pedido(
            usuario_id=command.usuario_id,
            producto=command.producto,
            cantidad=command.cantidad,
            total=total
        )
        return self.repo.save(pedido)
