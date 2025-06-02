from datetime import datetime
from app.db import models
from sqlalchemy.orm import Session

def create_payment(db: Session, order_id: int, amount: float):
    db_payment = models.Payment(order_id=order_id, amount=amount, payment_date=datetime.utcnow())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

def list_payments(db: Session):
    return db.query(models.Payment).all()
