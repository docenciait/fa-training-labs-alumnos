from app.db import models
from sqlalchemy.orm import Session
from passlib.hash import bcrypt

def create_user(db: Session, username: str, email: str, password: str):
    hashed_password = bcrypt.hash(password)
    db_user = models.User(username=username, email=email, password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def list_users(db: Session):
    return db.query(models.User).all()
