# app/interfaces/api/product_routes.py
from fastapi import APIRouter, Depends
from app.application.dtos.product_dto import ProductCreateDTO, ProductDTO
from app.application.ports.product_service import ProductServicePort
from app.interfaces.api.dependencies import get_product_service

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=ProductDTO)
async def create_product(data: ProductCreateDTO, service: ProductServicePort = Depends(get_product_service)):
    return await service.create_product(data)

@router.get("/", response_model=list[ProductDTO])
async def list_products(service: ProductServicePort = Depends(get_product_service)):
    return await service.list_products()