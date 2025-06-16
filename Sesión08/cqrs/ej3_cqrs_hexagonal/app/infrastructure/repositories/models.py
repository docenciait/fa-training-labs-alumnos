from sqlalchemy import Column, Integer, String, Float
from app.db import Base

class PedidoSQL(Base):
    __tablename__ = "pedidos"
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer)
    producto = Column(String)
    cantidad = Column(Integer)
    total = Column(Float)
    estado = Column(String)