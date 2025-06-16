from sqlalchemy import Column, Integer, String, Float
from db import Base

class Pedido(Base):
    __tablename__ = "pedidos"
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer)
    producto = Column(String)
    cantidad = Column(Integer)
    total = Column(Float)
    estado = Column(String, default="pendiente")  # Nuevo campo en modelo