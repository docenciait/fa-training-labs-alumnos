# app/application/dtos/product_dto.py
from pydantic import BaseModel
from uuid import UUID

class ProductCreateDTO(BaseModel):
    name: str
    price: float
    stock: int

class ProductDTO(BaseModel):
    id: UUID
    name: str
    price: float
    stock: int
    
# Nuevo dto para stock
class ProductStockDTO(BaseModel):
    new_stock : int
    
