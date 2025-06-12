# app/interfaces/api/dependencies.py
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database import get_session
from app.infrastructure.repositories.mariadb_product_repository import MariaDBProductRepository
from app.application.services.product_app_service import ProductApplicationService

def get_product_service(session: AsyncSession = Depends(get_session)):
    repo = MariaDBProductRepository(session)
    return ProductApplicationService(repo)