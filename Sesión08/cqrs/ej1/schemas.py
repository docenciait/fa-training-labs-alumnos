from pydantic import BaseModel


class CreatePedidoCommand(BaseModel):
    usuario_id: int
    producto: str
    cantidad: int


class PedidoDTO(BaseModel):
    id: int
    usuario_id: int
    producto: str
    cantidad: int
    total: float

    model_config = {
        "from_attributes": True
    }
