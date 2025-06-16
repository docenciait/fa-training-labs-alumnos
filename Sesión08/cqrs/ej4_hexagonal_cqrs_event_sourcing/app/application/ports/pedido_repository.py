from abc import ABC, abstractmethod
from app.domain.entities.pedido import Pedido

class PedidoRepositoryPort(ABC):
    @abstractmethod
    def save(self, pedido: Pedido) -> Pedido:
        pass

    @abstractmethod
    def get_by_id(self, pedido_id: int) -> Pedido | None:
        pass
