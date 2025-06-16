from models import Pedido

class PedidoRepository:
    def __init__(self, db_session):
        self.db = db_session

    def save(self, pedido: Pedido):
        self.db.add(pedido)
        self.db.commit()
        self.db.refresh(pedido)
        return pedido

    def get_by_id(self, pedido_id: int):
        return self.db.query(Pedido).filter_by(id=pedido_id).first()

    def get_all_by_usuario(self, usuario_id: int):
        return self.db.query(Pedido).filter_by(usuario_id=usuario_id).all()

    def count_by_estado(self, estado: str):
        return self.db.query(Pedido).filter_by(estado=estado).count()