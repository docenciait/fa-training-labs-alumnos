from app.db import crud_user
from app.schemas.user import UserCreate

def create_user(user: UserCreate):
    return crud_user.create_user(user)

def get_user_by_email(email: str):
    return crud_user.get_user_by_email(email)

def get_user_by_id(user_id: int):
    return crud_user.get_user_by_id(user_id)

def get_all_users():
    return crud_user.get_all_users()
