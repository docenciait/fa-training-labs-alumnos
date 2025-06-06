from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.product import ProductCreate, ProductOut
from app.services.product_service import (
    create_product, get_product_by_id, get_all_products
)

router = APIRouter()

@router.post("/products/", response_model=ProductOut)
def register_product(product: ProductCreate):
    return create_product(product)

@router.get("/products/{product_id}", response_model=ProductOut)
def read_product(product_id: int):
    db_product = get_product_by_id(product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.get("/products/", response_model=List[ProductOut])
def list_products():
    return get_all_products()