from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.payment import PaymentCreate, PaymentOut
from app.services.payment_service import (
    create_payment, get_payment_by_id, get_all_payments
)

router = APIRouter()

@router.post("/payments/", response_model=PaymentOut)
async def register_payment(payment: PaymentCreate):
    return await create_payment(payment)

@router.get("/payments/{payment_id}", response_model=PaymentOut)
def read_payment(payment_id: int):
    db_payment = get_payment_by_id(payment_id)
    if not db_payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return db_payment

@router.get("/payments/", response_model=List[PaymentOut])
def list_payments():
    return get_all_payments()