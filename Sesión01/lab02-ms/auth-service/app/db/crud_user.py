from app.db.database import SessionLocal
from app.db.models import User
from app.schemas.user import UserCreate

def get_user_by_email(email: str):
    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    db.close()
    return user

def get_user_by_id(user_id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    db.close()
    return user

def create_user(user: UserCreate):
    db = SessionLocal()
    db_user = User(username=user.username, email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.close()
    return db_user

def get_all_users():
    db = SessionLocal()
    users = db.query(User).all()
    db.close()
    return users
