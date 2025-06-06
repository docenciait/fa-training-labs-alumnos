from app.db.database import SessionLocal
from app.db.models import Payment
from app.schemas.payment import PaymentCreate


def create_payment(payment: PaymentCreate):
    db = SessionLocal()
    db_payment = Payment(order_id=payment.order_id, amount=payment.amount)
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    db.close()
    return db_payment


def get_payment_by_id(payment_id: int):
    db = SessionLocal()
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    db.close()
    return payment


def get_all_payments():
    db = SessionLocal()
    payments = db.query(Payment).all()
    db.close()
    return payments