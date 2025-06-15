from app.db.database import SessionLocal
from app.db.models import Order
from app.schemas.order import OrderCreate


def create_order(order: OrderCreate):
    db = SessionLocal()
    db_order = Order(user_id=order.user_id, product_ids=order.product_ids)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    db.close()
    return db_order


def get_order_by_id(order_id: int):
    db = SessionLocal()
    order = db.query(Order).filter(Order.id == order_id).first()
    db.close()
    return order


def get_all_orders():
    db = SessionLocal()
    orders = db.query(Order).all()
    db.close()
    return orders