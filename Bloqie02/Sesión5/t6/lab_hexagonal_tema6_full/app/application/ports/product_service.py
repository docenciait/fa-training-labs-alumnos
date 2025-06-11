# app/application/ports/product_service.py
from abc import ABC, abstractmethod
from typing import List
from app.application.dtos.product_dto import ProductCreateDTO, ProductDTO

class ProductServicePort(ABC):
    @abstractmethod
    async def create_product(self, data: ProductCreateDTO) -> ProductDTO: 
        pass

    @abstractmethod
    async def list_products(self) -> List[ProductDTO]: 
        pass