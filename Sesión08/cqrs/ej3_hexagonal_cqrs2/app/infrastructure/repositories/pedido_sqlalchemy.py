from app.application.ports.pedido_repository import PedidoRepositoryPort
from app.domain.entities.pedido import Pedido
from app.infrastructure.db.models import PedidoModel, SessionLocal
from sqlalchemy.orm import Session

class PedidoSQLAlchemyRepository(PedidoRepositoryPort):
    def __init__(self):
        self.db: Session = SessionLocal()

    def save(self, pedido: Pedido) -> Pedido:
        db_pedido = PedidoModel(
            usuario_id=pedido.usuario_id,
            producto=pedido.producto,
            cantidad=pedido.cantidad,
            total=pedido.total,
            estado=pedido.estado,
        )
        self.db.add(db_pedido)
        self.db.commit()
        self.db.refresh(db_pedido)

        return Pedido(
            id=db_pedido.id,
            usuario_id=db_pedido.usuario_id,
            producto=db_pedido.producto,
            cantidad=db_pedido.cantidad,
            total=db_pedido.total,
            estado=db_pedido.estado,
        )

    def get_by_id(self, pedido_id: int) -> Pedido | None:
        db_pedido = self.db.query(PedidoModel).filter(PedidoModel.id == pedido_id).first()
        if db_pedido is None:
            return None
        return Pedido(
            id=db_pedido.id,
            usuario_id=db_pedido.usuario_id,
            producto=db_pedido.producto,
            cantidad=db_pedido.cantidad,
            total=db_pedido.total,
            estado=db_pedido.estado,
        )
