# app/application/services/product_app_service.py
from uuid import UUID
from app.application.ports.product_service import ProductServicePort
from app.application.ports.product_repository import ProductRepositoryPort
from app.application.dtos.product_dto import ProductCreateDTO, ProductDTO
from app.domain.entities.product import Product

class ProductApplicationService(ProductServicePort):
    def __init__(self, repo: ProductRepositoryPort):
        self.repo = repo

    async def create_product(self, data: ProductCreateDTO) -> ProductDTO:
        product = Product(data.name, data.price, data.stock)
        await self.repo.save(product)
        return ProductDTO(
            id=product.id,
            name=product.name,
            price=product.price,
            stock=product.stock
        )

    async def list_products(self) -> list[ProductDTO]:
        products = await self.repo.list_all()
        return [ProductDTO(
            id=p.id,
            name=p.name,
            price=p.price,
            stock=p.stock
        ) for p in products]
        
    # Nueva operación
    
    async def update_stock(self, product_id: UUID, new_stock: int) -> ProductDTO:
        all_products = await self.repo.list_all()
        product = next((p for p in all_products if str(p.id) == str(product_id)), None)
        if not product:
            raise ValueError("Producto no encontrado")

        product.update_stock(new_stock)
        await self.repo.save(product)

        return ProductDTO(
            id=product.id,
            name=product.name,
            price=product.price,
            stock=product.stock
        )