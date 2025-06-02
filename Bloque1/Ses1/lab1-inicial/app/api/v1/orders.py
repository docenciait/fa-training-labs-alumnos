from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.order import OrderCreate, Order
from app.services import order_service

router = APIRouter()

@router.post("/", response_model=Order)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    return order_service.create_order(db, order.user_id, order.product_ids)

@router.get("/", response_model=list[Order])
def list_orders(db: Session = Depends(get_db)):
    return order_service.list_orders(db)