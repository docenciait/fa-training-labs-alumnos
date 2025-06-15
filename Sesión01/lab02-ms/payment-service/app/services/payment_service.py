from app.db import crud_payment
from app.schemas.payment import PaymentCreate
import httpx
from datetime import datetime

async def verify_order(order_id: int) -> bool:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://order-service:8000/api/v1/orders/{order_id}")
        return response.status_code == 200

async def create_payment(payment: PaymentCreate):
    if not await verify_order(payment.order_id):
        raise ValueError("Order does not exist.")

    return crud_payment.create_payment(payment)


def get_payment_by_id(payment_id: int):
    return crud_payment.get_payment_by_id(payment_id)


def get_all_payments():
    return crud_payment.get_all_payments()