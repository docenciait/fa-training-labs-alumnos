from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.order import OrderCreate, Order, OrderUpdate
from app.services import order_service

router = APIRouter()

@router.post("/", response_model=Order)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    return order_service.create_order(db, order.user_id, order.product_ids)

@router.get("/", response_model=list[Order])
def list_orders(db: Session = Depends(get_db)):
    return order_service.list_orders(db)

@router.put("/orders/{order_id}", response_model=Order)
def update_order(order_id: int, order_update: OrderUpdate, db: Session = Depends(get_db)):
    updated_order = order_service.update_order(db, order_id, order_update)
    if updated_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated_order
