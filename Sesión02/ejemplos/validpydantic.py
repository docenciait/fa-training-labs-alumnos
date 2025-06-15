from pydantic import BaseModel

from typing import Optional

class UserBase(BaseModel):
    username: str  # Campo requerido de tipo string
    email: str     # Campo requerido de tipo string
    full_name: str | None # Campo opcional, por defecto None
    age: int       # Campo requerido de tipo entero

ub : UserBase = UserBase(username="admin1", email="myemail@gmail.com", full_name=None, age= 32)


invalid_data = { "username": "john.doe", "age": "treinta" }

# print(f"json: {ub.model_dump_json() } \n dict: {ub.model_dump()}")

json_validation = ub.model_dump()
print(ub.model_validate_json(json_validation))