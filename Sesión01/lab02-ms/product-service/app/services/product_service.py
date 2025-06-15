from app.db import crud_product
from app.schemas.product import ProductCreate


def create_product(product: ProductCreate):
    return crud_product.create_product(product)


def get_product_by_id(product_id: int):
    return crud_product.get_product_by_id(product_id)


def get_all_products():
    return crud_product.get_all_products()