from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.order import OrderCreate, OrderOut
from app.services.order_service import (
    create_order, get_order_by_id, get_all_orders
)

router = APIRouter()

# Ejercicio hacer sin async
@router.post("/orders/", response_model=OrderOut)
async def register_order(order: OrderCreate):
    return await create_order(order)

@router.get("/orders/{order_id}", response_model=OrderOut)
def read_order(order_id: int):
    db_order = get_order_by_id(order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@router.get("/orders/", response_model=List[OrderOut])
def list_orders():
    return get_all_orders()