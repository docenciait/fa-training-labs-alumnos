from pydantic import BaseModel

class Evento(BaseModel):
    tipo: str
    id: str
    payload: dict
