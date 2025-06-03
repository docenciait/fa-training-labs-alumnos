from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float

class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float

    class Config:
        from_attributes = True
