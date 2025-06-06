from pydantic import BaseModel
from datetime import datetime

class PaymentCreate(BaseModel):
    order_id: int
    amount: float

class PaymentOut(BaseModel):
    id: int
    order_id: int
    amount: float
    payment_date: datetime

    class Config:
        orm_mode = True