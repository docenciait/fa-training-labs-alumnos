from app.db import models
from sqlalchemy.orm import Session

def create_order(db: Session, user_id: int, product_ids: list):
    products = db.query(models.Product).filter(models.Product.id.in_(product_ids)).all()
    total_price = sum(product.price for product in products)
    db_order = models.Order(user_id=user_id, total_price=total_price, status="CREATED")
    db_order.products = products
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    # 👉 Aquí creamos un dict manualmente
    return {
        "id": db_order.id,
        "user_id": db_order.user_id,
        "total_price": float(db_order.total_price),
        "status": db_order.status,
        "product_ids": [p.id for p in db_order.products]
    }

def list_orders(db: Session):
    orders = db.query(models.Order).all()
    result = []
    for order in orders:
        product_ids = [p.id for p in order.products]
        result.append({
            "id": order.id,
            "user_id": order.user_id,
            "total_price": float(order.total_price),
            "status": order.status,
            "product_ids": product_ids
        })
    return result
