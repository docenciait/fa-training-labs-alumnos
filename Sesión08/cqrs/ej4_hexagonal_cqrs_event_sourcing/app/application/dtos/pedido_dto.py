from pydantic import BaseModel

class CrearPedidoDTO(BaseModel):
    usuario_id: int
    producto: str
    cantidad: int

class PedidoResponseDTO(BaseModel):
    id: int
    usuario_id: int
    producto: str
    cantidad: int
    total: float
    estado: str

    class Config:
        orm_mode = True
