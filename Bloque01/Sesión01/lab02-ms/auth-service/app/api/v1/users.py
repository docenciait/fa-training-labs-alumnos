from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.user import UserCreate, UserOut
from app.services.user_service import (
    create_user, get_user_by_id, get_user_by_email, get_all_users
)

router = APIRouter()

@router.post("/users/", response_model=UserOut)
def register_user(user: UserCreate):
    db_user = get_user_by_email(user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(user)

@router.get("/users/{user_id}", response_model=UserOut)
def read_user(user_id: int):
    db_user = get_user_by_id(user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/users/", response_model=List[UserOut])
def list_users():
    return get_all_users()