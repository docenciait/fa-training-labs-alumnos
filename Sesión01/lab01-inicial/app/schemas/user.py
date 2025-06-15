from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class User(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    # Todos los campos opcionales, porque con PUT actualizas todo
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
