# app/application/ports/product_service.py
from abc import ABC, abstractmethod
from typing import List
from uuid import UUID
from app.application.dtos.product_dto import ProductCreateDTO, ProductDTO

class ProductServicePort(ABC):
    @abstractmethod
    async def create_product(self, data: ProductCreateDTO) -> ProductDTO: 
        pass

    @abstractmethod
    async def list_products(self) -> List[ProductDTO]: 
        pass
    
    @abstractmethod
    async def update_stock(self, product_id: UUID, new_stock: int) -> ProductDTO:
        pass