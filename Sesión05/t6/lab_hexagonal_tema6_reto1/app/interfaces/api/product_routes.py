# app/interfaces/api/product_routes.py
from uuid import UUID
from fastapi import APIRouter, Depends
from app.application.dtos.product_dto import ProductCreateDTO, ProductDTO, ProductStockDTO
from app.application.ports.product_service import ProductServicePort
from app.interfaces.api.dependencies import get_product_service
# Importamos nuevo dto



router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=ProductDTO)
async def create_product(data: ProductCreateDTO, service: ProductServicePort = Depends(get_product_service)):
    return await service.create_product(data)

@router.get("/", response_model=list[ProductDTO])
async def list_products(service: ProductServicePort = Depends(get_product_service)):
    return await service.list_products()

@router.patch("/{product_id}/stock", response_model=ProductDTO)
async def update_stock(
    product_id: UUID,
    payload: ProductStockDTO,
    service: ProductServicePort = Depends(get_product_service)
):
    return await service.update_stock(product_id, payload.new_stock)