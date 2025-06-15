from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.payment import PaymentCreate, Payment
from app.services import payment_service

router = APIRouter()

@router.post("/", response_model=Payment)
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    return payment_service.create_payment(db, payment.order_id, payment.amount)

@router.get("/", response_model=list[Payment])
def list_payments(db: Session = Depends(get_db)):
    return payment_service.list_payments(db)