from pydantic import BaseModel
from typing import List

class OrderCreate(BaseModel):
    user_id: int
    product_ids: List[int]

class OrderOut(BaseModel):
    id: int
    user_id: int
    product_ids: List[int]

    class Config:
        orm_mode = True