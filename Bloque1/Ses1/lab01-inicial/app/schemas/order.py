from pydantic import BaseModel
from typing import List, Optional

class OrderCreate(BaseModel):
    user_id: int
    product_ids: List[int]

class Order(BaseModel):
    id: int
    user_id: int
    total_price: float
    status: str
    product_ids: List[int]

    class Config:
        from_attributes = True

class OrderUpdate(BaseModel):
    status: Optional[str] = None