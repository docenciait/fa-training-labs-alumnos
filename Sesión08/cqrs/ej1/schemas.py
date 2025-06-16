from pydantic import BaseModel

# Para el Command CREAR
class CreatePedidoCommand(BaseModel):
    usuario_id: int
    producto: str
    cantidad: int

# Para la Query Obtener
class PedidoDTO(BaseModel):
    id: int
    usuario_id: int
    producto: str
    cantidad: int
    total: float

    model_config = {
        "from_attributes": True
    }
