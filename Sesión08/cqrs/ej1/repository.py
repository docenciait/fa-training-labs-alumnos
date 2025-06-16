from models import Pedido

# Repository aquí sería un adaptador posteriormente si aplicamos hexagonal

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
