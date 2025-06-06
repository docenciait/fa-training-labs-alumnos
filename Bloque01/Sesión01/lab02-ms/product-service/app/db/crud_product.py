from app.db.database import SessionLocal
from app.db.models import Product
from app.schemas.product import ProductCreate


def create_product(product: ProductCreate):
    db = SessionLocal()
    db_product = Product(name=product.name, description=product.description, price=product.price)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    db.close()
    return db_product


def get_product_by_id(product_id: int):
    db = SessionLocal()
    product = db.query(Product).filter(Product.id == product_id).first()
    db.close()
    return product


def get_all_products():
    db = SessionLocal()
    products = db.query(Product).all()
    db.close()
    return products