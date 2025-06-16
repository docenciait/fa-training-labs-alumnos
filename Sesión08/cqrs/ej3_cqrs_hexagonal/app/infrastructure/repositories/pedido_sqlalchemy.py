from app.domain.ports.pedido_repository import PedidoRepositoryPort
from app.infrastructure.repositories.models import PedidoSQL
from app.domain.models.pedido import Pedido as PedidoDomain

class PedidoRepositorySQLAlchemy(PedidoRepositoryPort):
    def __init__(self, db_session):
        self.db = db_session

    def save(self, pedido: PedidoDomain):
        orm = PedidoSQL(**pedido.__dict__)
        self.db.add(orm)
        self.db.commit()
        self.db.refresh(orm)
        return orm

    def get_by_id(self, pedido_id: int):
        return self.db.query(PedidoSQL).filter_by(id=pedido_id).first()