# app/application/ports/product_repository.py
from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.product import Product

class ProductRepositoryPort(ABC):
    @abstractmethod
    async def save(self, product: Product) -> None: 
        pass

    @abstractmethod
    async def list_all(self) -> List[Product]: 
        pass
    
