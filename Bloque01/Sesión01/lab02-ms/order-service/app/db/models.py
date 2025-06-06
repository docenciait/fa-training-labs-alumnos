from sqlalchemy import Column, Integer, JSON
from app.db.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    product_ids = Column(JSON, nullable=False)  # Guardamos una lista de IDs en JSON