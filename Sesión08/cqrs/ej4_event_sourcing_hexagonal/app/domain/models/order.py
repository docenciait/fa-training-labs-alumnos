from typing import List, Optional
from app.domain.events import Event

class Order:
    def __init__(self, order_id: Optional[str] = None, customer_id: Optional[str] = None, items: Optional[List[str]] = None, shipped: bool = False, paid: bool = False):
        self.order_id = order_id
        self.customer_id = customer_id
        self.items = items or []
        self.shipped = shipped
        self.paid = paid

    @classmethod
    def create(cls, order_id: str, customer_id: str, items: List[str]) -> "Order":
        return cls(order_id=order_id, customer_id=customer_id, items=items)

    def apply(self, event: Event):
        if event.event_type == "OrderCreated":
            self.order_id = event.data['order_id']
            self.customer_id = event.data['customer_id']
            self.items = event.data['items']
        elif event.event_type == "OrderShipped":
            self.shipped = True
        elif event.event_type == "PaymentReceived":
            self.paid = True

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "customer_id": self.customer_id,
            "items": self.items,
            "shipped": self.shipped,
            "paid": self.paid,
        }