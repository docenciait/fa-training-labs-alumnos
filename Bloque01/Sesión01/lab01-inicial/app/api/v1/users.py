from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user import UserCreate, User
from app.services import user_service

router = APIRouter()

# Agregar usuarios
@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, user.username, user.email, user.password)

# Listar usuarios
@router.get("/", response_model=list[User])
def list_users(db: Session = Depends(get_db)):
    return user_service.list_users(db)