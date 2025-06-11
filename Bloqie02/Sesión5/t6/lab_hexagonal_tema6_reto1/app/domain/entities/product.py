# app/domain/entities/product.py
from uuid import uuid4
from app.domain.events.product_events import ProductCreatedEvent

class Product:
    def __init__(self, name: str, price: float, stock: int):
        if price <= 0:
            raise ValueError("El precio debe ser positivo")
        if stock < 0:
            raise ValueError("El stock no puede ser negativo")

        self.id = uuid4()
        self.name = name
        self.price = price
        self.stock = stock
        self._events = [ProductCreatedEvent(product_id=self.id, name=self.name)]

    def pull_events(self):
        events = self._events
        self._events = []
        return events
    
    def update_stock(self, new_stock: int):
        if new_stock < 0:
            raise ValueError("El stock no puede ser negativo")
        self.stock = new_stock