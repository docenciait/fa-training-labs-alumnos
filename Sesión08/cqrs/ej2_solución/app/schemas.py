from pydantic import BaseModel

class CrearPedidoCommand(BaseModel):
    usuario_id: int
    producto: str
    cantidad: int

class CancelarPedidoCommand(BaseModel):
    pedido_id: int

class EntregarPedidoCommand(BaseModel):
    pedido_id: int

class PedidoDTO(BaseModel):
    id: int
    usuario_id: int
    producto: str
    cantidad: int
    total: float
    estado: str

    model_config = {"from_attributes": True}