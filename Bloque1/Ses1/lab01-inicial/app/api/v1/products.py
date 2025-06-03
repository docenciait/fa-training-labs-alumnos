from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.product import ProductCreate, Product
from app.services import product_service

router = APIRouter()

@router.post("/", response_model=Product)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return product_service.create_product(db, product.name, product.description, product.price)

@router.get("/", response_model=list[Product])
def list_products(db: Session = Depends(get_db)):
    return product_service.list_products(db)

