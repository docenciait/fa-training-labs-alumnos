from app.db import models
from sqlalchemy.orm import Session

def create_product(db: Session, name: str, description: str, price: float):
    new_product = models.Product(name=name, description=description, price=price)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

def list_products(db: Session):
    return db.query(models.Product).all()
