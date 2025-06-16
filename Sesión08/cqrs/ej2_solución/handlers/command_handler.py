from models import Pedido
from schemas import CreatePedidoCommand, CancelarPedidoCommand, EntregarPedidoCommand
from repository import PedidoRepository

class CrearPedidoHandler:
    def __init__(self, repo: PedidoRepository):
        self.repo = repo

    def execute(self, command: CreatePedidoCommand):
        total = command.cantidad * 10.0
        pedido = Pedido(
            usuario_id=command.usuario_id,
            producto=command.producto,
            cantidad=command.cantidad,
            total=total,
            estado="pendiente"
        )
        return self.repo.save(pedido)

class CancelarPedidoHandler:
    def __init__(self, repo: PedidoRepository):
        self.repo = repo

    def execute(self, command: CancelarPedidoCommand):
        pedido = self.repo.get_by_id(command.pedido_id)
        if pedido:
            pedido.estado = "cancelado"
            self.repo.save(pedido)
        return pedido

class EntregarPedidoHandler:
    def __init__(self, repo: PedidoRepository):
        self.repo = repo

    def execute(self, command: EntregarPedidoCommand):
        pedido = self.repo.get_by_id(command.pedido_id)
        if pedido:
            pedido.estado = "entregado"
            self.repo.save(pedido)
        return pedido