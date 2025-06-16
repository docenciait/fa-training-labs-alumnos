from sqlalchemy import Column, Integer, String, Float
from db import Base


class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, nullable=False)
    producto = Column(String, nullable=False)
    cantidad = Column(Integer, nullable=False)
    total = Column(Float, nullable=False)
