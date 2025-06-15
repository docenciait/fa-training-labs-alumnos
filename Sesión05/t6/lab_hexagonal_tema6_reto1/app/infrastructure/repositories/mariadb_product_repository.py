# app/infrastructure/repositories/mariadb_product_repository.py

from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.application.ports.product_repository import ProductRepositoryPort
from app.domain.entities.product import Product
from app.infrastructure.db_models.product_model import ProductModel
from typing import List, Optional

class MariaDBProductRepository(ProductRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, product: Product) -> None:
        orm = ProductModel(
            id=product.id,
            name=product.name,
            price=product.price,
            stock=product.stock
        )
        self.session.add(orm)
        await self.session.commit()  # ✅ Esto guarda en la DB

    async def list_all(self) -> List[Product]:
        result = await self.session.execute(select(ProductModel))
        orm_products = result.scalars().all()
        print(f"🔎 Se han encontrado {len(orm_products)} productos en la base de datos.")  # ✅ Log útil
        return [Product(p.name, p.price, p.stock) for p in orm_products]

    async def get_by_id(self, product_id: UUID) -> Optional[Product]:
        result = await self.session.execute(
            select(ProductModel).where(ProductModel.id == str(product_id))
        )
        row = result.scalar_one_or_none()

        if not row:
            return None

        return Product(
            name=row.name,
            price=row.price,
            stock=row.stock,
            id=row.id
        )