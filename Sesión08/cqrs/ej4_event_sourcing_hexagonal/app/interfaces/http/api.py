from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import uuid

from app.domain.models.order import Order
from app.domain.events import OrderCreated, OrderShipped, PaymentReceived
from app.infrastructure.event_store.inmemory_event_store import InMemoryEventStore

router = APIRouter()
event_store = InMemoryEventStore()

class OrderCreateRequest(BaseModel):
    customer_id: str
    items: List[str]

@router.post("/orders/")
def create_order(order_request: OrderCreateRequest):
    order_id = str(uuid.uuid4())
    order_created_event = OrderCreated(data={
        "order_id": order_id,
        "customer_id": order_request.customer_id,
        "items": order_request.items
    })
    event_store.append(order_id, [order_created_event])
    return {"order_id": order_id, "message": "Order created successfully"}

@router.post("/orders/{order_id}/ship")
def ship_order(order_id: str):
    order = rebuild_order_from_events(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.shipped:
        return {"message": "Order already shipped"}
    event_store.append(order_id, [OrderShipped(data={})])
    return {"message": "Order shipped successfully"}

@router.post("/orders/{order_id}/pay")
def pay_order(order_id: str):
    order = rebuild_order_from_events(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.paid:
        return {"message": "Order already paid"}
    event_store.append(order_id, [PaymentReceived(data={})])
    return {"message": "Payment received successfully"}

@router.get("/orders/{order_id}")
def get_order(order_id: str):
    order = rebuild_order_from_events(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order.to_dict()

def rebuild_order_from_events(order_id: str) -> Optional[Order]:
    events = event_store.get_events(order_id)
    if not events:
        return None
    order = Order()
    for event in events:
        order.apply(event)
    return order